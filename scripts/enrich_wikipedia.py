#!/usr/bin/env python3
"""Enrich Wikipedia-sourced rows from the article lead paragraph.

Two jobs, both of which the research agents did unevenly:

1. **Dates.** Pull `birth_year` and `death_year` out of the lead, which is where Wikipedia
   puts them in a predictable shape.
2. **Name status.** Detect leads that give a birth name differing from the name we recorded.
   That is the signal for a stage name, pen name or pseudonym, which the brief requires us
   to flag rather than treat as a birth name. Where the lead gives no alternate name and the
   recorded surname appears in the bolded title, we can also promote `unknown` to
   `birth_name` with reasonable confidence.

Writes data/wikipedia_enrichment.csv as an audit trail. Pass --apply to update the master.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import ssl
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "aptronyms.csv"
OUT = ROOT / "data" / "wikipedia_enrichment.csv"

UA = "aptronym-research/1.0 (data journalism project; contact via repo)"
CTX = ssl.create_default_context()

# "(born 12 March 1970)", "(1802-1885)", "(born Reginald Kenneth Dwight; 25 March 1947)"
YEAR = r"(1[0-9]{3}|20[0-9]{2}|[89][0-9]{2})"
BORN_YEAR = re.compile(rf"\bborn[^);.]{{0,40}}?\b{YEAR}\b")
RANGE_YEARS = re.compile(rf"\(\s*(?:c\.\s*)?{YEAR}\s*[–—-]\s*(?:c\.\s*)?{YEAR}\s*\)")
LEAD_RANGE = re.compile(rf"[;(]\s*(?:c\.\s*)?[^;()]{{0,30}}?{YEAR}\s*[–—-]\s*[^;()]{{0,30}}?{YEAR}")

# "(born Marshall Bruce Mathers III;" / "born Norma Jeane Mortenson," / "né Smith"
ALT_NAME = re.compile(
    r"\b(?:born|n[ée]e?)\s+((?:[A-Z][\w'’\-]+\.?\s+){1,4}[A-Z][\w'’\-]+)(?=\s*[;,)]|\s+on\b|\s+in\b)"
)
PARTICLES = {
    "de", "van", "von", "der", "den", "del", "della", "di", "da", "dos", "du", "la", "le",
    "el", "al", "bin", "ibn", "ben", "mac", "mc", "o", "st", "san", "santa", "ter", "te",
}
SUFFIXES = {"jr", "sr", "i", "ii", "iii", "iv", "v", "phd", "md"}


def api_extracts(host: str, titles: list[str], attempts: int = 5) -> dict[str, str]:
    """Fetch lead extracts, retrying with backoff: the API rate-limits bursts."""
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            return _api_extracts_once(host, titles)
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(2 ** attempt)
    raise last if last else RuntimeError("unreachable")


def _api_extracts_once(host: str, titles: list[str]) -> dict[str, str]:
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": "1",
        "explaintext": "1",
        "redirects": "1",
        "titles": "|".join(titles),
    }
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60, context=CTX) as resp:
        data = json.load(resp)

    query = data.get("query", {})
    alias = {t: t for t in titles}
    for norm in query.get("normalized", []):
        alias[norm["from"]] = norm["to"]
    for redir in query.get("redirects", []):
        for src, dst in list(alias.items()):
            if dst == redir["from"]:
                alias[src] = redir["to"]

    by_title = {
        p.get("title", ""): html.unescape(p.get("extract", "") or "")
        for p in query.get("pages", {}).values()
    }
    return {t: by_title.get(alias[t], "") for t in titles}


def tokens(name: str) -> list[str]:
    cleaned = re.sub(r"[^\w\s'’\-]", " ", name.lower())
    out = []
    for tok in cleaned.split():
        tok = tok.strip("'’-").rstrip(".")
        if tok and tok not in PARTICLES and tok not in SUFFIXES and len(tok) > 1:
            out.append(tok)
    return out


def names_differ(recorded: str, candidate: str) -> bool:
    """True when the Wikipedia lead's birth name is materially different."""
    a, b = tokens(recorded), tokens(candidate)
    if not a or not b:
        return False
    # A surname carried over means it is the same family name, not a pseudonym.
    return a[-1] != b[-1]


def wiki_target(url: str) -> tuple[str, str] | None:
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc.endswith("wikipedia.org") or "/wiki/" not in parsed.path:
        return None
    title = urllib.parse.unquote(parsed.path.split("/wiki/", 1)[1]).replace("_", " ")
    return parsed.netloc, title.split("#", 1)[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    with MASTER.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        cols = list(reader.fieldnames or [])
        rows = list(reader)

    targets: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        target = wiki_target(row.get("person_source_url", ""))
        if target:
            host, title = target
            targets[host][title].append(row)

    extracts: dict[tuple[str, str], str] = {}
    for host, titles in targets.items():
        keys = list(titles)
        print(f"{host}: {len(keys)} articles")
        for i in range(0, len(keys), 20):
            chunk = keys[i : i + 20]
            try:
                got = api_extracts(host, chunk)
            except Exception:  # noqa: BLE001
                # One title at a time, so a throttled or malformed batch costs us one
                # article rather than twenty.
                got = {}
                for title in chunk:
                    try:
                        got.update(api_extracts(host, [title], attempts=3))
                    except Exception:  # noqa: BLE001
                        pass
                    time.sleep(0.5)
            for title, text in got.items():
                extracts[(host, title)] = text
            time.sleep(1.0)

        # Anything still missing was almost certainly throttled rather than absent. Sweep it
        # again with longer waits: without this the pass is not reproducible, and the whole
        # pipeline claims to be.
        for attempt in range(4):
            missing = [t for t in keys if (host, t) not in extracts]
            if not missing:
                break
            print(f"  retry {attempt + 1}: {len(missing)} titles")
            time.sleep(10 * (attempt + 1))
            for i in range(0, len(missing), 10):
                try:
                    for title, text in api_extracts(host, missing[i : i + 10]).items():
                        extracts[(host, title)] = text
                except Exception:  # noqa: BLE001
                    pass
                time.sleep(2.0)

        still = [t for t in keys if (host, t) not in extracts]
        for title in still:
            print(f"  unreachable after retries: {title!r}")

    report: list[dict[str, str]] = []
    filled_birth = filled_death = flagged = promoted = 0

    for host, titles in targets.items():
        for title, group in titles.items():
            text = extracts.get((host, title), "")
            if not text:
                continue
            lead = text[:900]

            birth = death = ""
            span = RANGE_YEARS.search(lead) or LEAD_RANGE.search(lead)
            if span:
                birth, death = span.group(1), span.group(2)
            else:
                got = BORN_YEAR.search(lead)
                if got:
                    birth = got.group(1)

            match = ALT_NAME.search(lead)
            title_tokens = set(tokens(title))
            for row in group:
                # Only read a birth name off an article that is actually about this person.
                # Several rows share one article — Frank Field's page also sources his
                # children — and his birth name is not theirs.
                about_this_person = set(tokens(row["full_name"])) <= title_tokens
                alt = ""
                if match and about_this_person and names_differ(row["full_name"], match.group(1)):
                    alt = match.group(1)

                actions = []
                if birth and not row["birth_year"]:
                    row["birth_year"] = birth
                    filled_birth += 1
                    actions.append(f"birth_year={birth}")
                if death and not row["death_year"]:
                    row["death_year"] = death
                    filled_death += 1
                    actions.append(f"death_year={death}")

                if alt:
                    if row["name_status"] in {"unknown", "birth_name"}:
                        row["name_status"] = "professional_name"
                        actions.append("name_status=professional_name")
                    note = f"Wikipedia gives the birth name as {alt}."
                    if note not in row["notes"]:
                        row["notes"] = f"{row['notes']} {note}".strip()
                    flagged += 1
                    actions.append(f"alt_name={alt}")
                elif row["name_status"] == "unknown" and not match:
                    surname = tokens(row["full_name"])[-1:] or [""]
                    if surname[0] and surname[0] in tokens(title):
                        row["name_status"] = "birth_name"
                        promoted += 1
                        actions.append("name_status=birth_name")

                if actions:
                    report.append({
                        "id": row["id"],
                        "full_name": row["full_name"],
                        "article": f"{host}/wiki/{title}",
                        "actions": "; ".join(actions),
                    })

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["id", "full_name", "article", "actions"])
        writer.writeheader()
        writer.writerows(report)

    print(f"\narticles fetched      {len(extracts)}")
    print(f"birth_year filled     {filled_birth}")
    print(f"death_year filled     {filled_death}")
    print(f"alternate names found {flagged}")
    print(f"name_status promoted  {promoted}")
    print(f"report                {OUT.relative_to(ROOT)}")

    if not args.apply:
        print("\ndry run; pass --apply to write the master")
        return

    with MASTER.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {MASTER.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
