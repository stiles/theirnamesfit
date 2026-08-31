#!/usr/bin/env python3
"""Mechanical integrity sweeps over the master dataset.

The five human-directed audits each independently reported the same three systemic
defects in the research agents' output. Those defects are pattern-detectable, so they are
handled here in one reproducible pass rather than row by row:

1. `name_status` was mass-defaulted to `birth_name` without anyone checking. Rows that no
   auditor explicitly set are downgraded to `unknown`, which is what we actually know.
2. Hedging language in `connection` ("evokes", "faintly", "loosely") marks a link that was
   rationalised rather than observed. Those rows are capped at `borderline`.
3. Some rows verify a person against a source that cannot establish who they are: a
   licence-registry lookup, a surname-meaning site, a listicle, a social profile, a
   search-results page, or a bare homepage. Those rows are capped and annotated.

Run with --apply to write. Without it, prints the diff it would make.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "aptronyms.csv"
CORRECTIONS = ROOT / "data" / "audit" / "corrections"
ENRICHMENT = ROOT / "data" / "wikipedia_enrichment.csv"

RANK = {"rejected": 0, "borderline": 1, "probable": 2, "verified": 3}

HEDGE = re.compile(
    r"\b(evoke[sd]?|evoking|suggest(?:s|ing)?|faint(?:ly)?|loose(?:ly)?|resembl\w+|"
    r"echo(?:e[sd]|ing)?|vaguely|arguably|somewhat|tenuous\w*|might be read|can be read|"
    r"could be read|jocular\w*|punningly)\b",
    re.IGNORECASE,
)

# Hosts that cannot, on their own, establish that a named person holds a given job.
WEAK_HOSTS = {
    "linkedin.com": "professional social profile, self-reported",
    "npidb.org": "licence registry lookup",
    "npino.com": "licence registry lookup",
    "npiprofile.com": "licence registry lookup",
    "npiregistry.cms.hhs.gov": "licence registry lookup",
    "health.usnews.com": "physician directory listing, specialty self-reported",
    "healthgrades.com": "physician directory listing, specialty self-reported",
    "vitals.com": "physician directory listing, specialty self-reported",
    "webmd.com": "physician directory listing, specialty self-reported",
    "doximity.com": "physician directory listing, specialty self-reported",
    "houseofnames.com": "commercial surname-meaning site",
    "surnamedb.com": "commercial surname-meaning site",
    "forebears.io": "surname frequency site",
    "ancestry.com": "genealogy aggregator, user-submitted",
    "geni.com": "genealogy aggregator, user-submitted",
    "findagrave.com": "genealogy aggregator, user-submitted",
    "zxc.wiki": "machine-translated wiki mirror",
    "fatrazie.com": "aptronym listicle",
    "neatorama.com": "listicle",
    "ranker.com": "listicle",
    "boredpanda.com": "listicle",
    "buzzfeed.com": "listicle",
    "thefactsite.com": "listicle",
    "reddit.com": "user forum",
    "quora.com": "user forum",
    "twitter.com": "social post",
    "x.com": "social post",
    "facebook.com": "social post",
    "tiktok.com": "social post",
    "knowyourmeme.com": "meme aggregator",
    "topendsports.com": "unsourced sports trivia site",
}

# Search-results and directory-index URLs, which do not identify an individual.
SEARCH_PATTERNS = [
    re.compile(r"bioguide\.congress\.gov/search/bio/?$", re.IGNORECASE),
    re.compile(r"[?&](q|query|search|s)=", re.IGNORECASE),
    re.compile(r"/search/?$", re.IGNORECASE),
]

# Hosts whose individual records sit behind a search form. A citation to the front door of
# one of these names nobody, and unlike a dead link it will return 200 forever, so the URL
# check can never surface it.
DATABASE_HOSTS = {
    "npiregistry.cms.hhs.gov",
    "npidb.org",
    "npino.com",
    "npiprofile.com",
    "healthgrades.com",
    "vitals.com",
    "doximity.com",
    "forebears.io",
    "ancestry.com",
    "geni.com",
    "findagrave.com",
    "boxrec.com",
    "olympedia.org",
    "baseball-reference.com",
    "pro-football-reference.com",
    "basketball-reference.com",
    "hockey-reference.com",
}

# A URL with nothing after the host is a homepage, not a record.
ROOTLESS = re.compile(r"^https?://[^/?#]+/?$", re.IGNORECASE)

# Wiktionary establishes a word's meaning, never a person's identity.
WIKTIONARY = re.compile(r"wiktionary\.org", re.IGNORECASE)

MOBILE_WIKI = re.compile(r"\.m\.wikipedia\.org", re.IGNORECASE)

# Agents wrote country names in whatever form their source used. England, Scotland, Wales and
# Northern Ireland are deliberately kept distinct from United Kingdom: they compete separately
# in most sports, which is exactly the context many of these rows come from.
COUNTRY_CANON = {
    "us": "United States",
    "usa": "United States",
    "u.s.": "United States",
    "u.s.a.": "United States",
    "united states of america": "United States",
    "america": "United States",
    "gb": "United Kingdom",
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
    "great britain": "United Kingdom",
    "britain": "United Kingdom",
    "fr": "France",
    "de": "Germany",
    "nl": "Netherlands",
    "persia": "Iran",
}


def host_of(url: str) -> str:
    match = re.match(r"https?://([^/]+)", url or "")
    if not match:
        return ""
    return match.group(1).lower().removeprefix("www.")


def audited_name_status_ids() -> set[str]:
    """Ids where a human-directed audit explicitly set name_status."""
    ids: set[str] = set()
    for path in CORRECTIONS.glob("*.csv"):
        if ".template." in path.name:
            continue
        with path.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if (row.get("new_name_status") or "").strip():
                    ids.add((row.get("id") or "").strip())
    return ids


def cap(row: dict[str, str], ceiling: str) -> bool:
    if RANK[row["review_status"]] > RANK[ceiling]:
        row["review_status"] = ceiling
        return True
    return False


def note(row: dict[str, str], text: str) -> None:
    existing = row.get("notes", "").strip()
    if text not in existing:
        row["notes"] = f"{existing} {text}".strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    with MASTER.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        cols = list(reader.fieldnames or [])
        rows = list(reader)

    protected = audited_name_status_ids()
    counts = {
        "name_status downgraded": 0,
        "hedged connection capped": 0,
        "weak person source capped": 0,
        "database homepage as person source capped": 0,
        "site homepage as person source capped": 0,
        "search-url person source capped": 0,
        "wiktionary as person source capped": 0,
        "country normalised": 0,
        "mobile url normalised": 0,
    }
    examples: dict[str, list[str]] = {k: [] for k in counts}

    def record(key: str, row: dict[str, str], detail: str = "") -> None:
        counts[key] += 1
        if len(examples[key]) < 6:
            examples[key].append(f"{row['id']} {row['full_name']}{detail}")

    for row in rows:
        country = row.get("country", "").strip()
        canon = COUNTRY_CANON.get(country.lower(), country)
        if canon != row.get("country", ""):
            row["country"] = canon
            record("country normalised", row, f" ({country!r} -> {canon!r})")

        # A .m. host is the same article, but it defeats deduplication and the enrichment
        # pass groups by host.
        for col in ("person_source_url", "name_source_url", "discovery_source_url"):
            if MOBILE_WIKI.search(row.get(col, "")):
                row[col] = MOBILE_WIKI.sub(".wikipedia.org", row[col])
                record("mobile url normalised", row, f" ({col})")

        if row["name_status"] == "birth_name" and row["id"] not in protected:
            row["name_status"] = "unknown"
            record("name_status downgraded", row)

        if row["review_status"] != "rejected" and HEDGE.search(row.get("connection", "")):
            hit = HEDGE.search(row["connection"]).group(0)
            if cap(row, "borderline"):
                note(row, "Flagged automatically: connection wording asserts a loose link.")
                record("hedged connection capped", row, f" ('{hit}')")

        url = row.get("person_source_url", "")
        host = host_of(url)
        if row["review_status"] != "rejected":
            if ROOTLESS.match(url):
                # Somebody's own site is self-published but it is at least about them. A
                # database front door is not: the record it should point at was never cited.
                if host in DATABASE_HOSTS:
                    if cap(row, "borderline"):
                        note(row, "Person source is a database homepage, not an individual record.")
                        record("database homepage as person source capped", row, f" ({host})")
                elif cap(row, "probable"):
                    note(row, "Person source is a site homepage, self-published.")
                    record("site homepage as person source capped", row, f" ({host})")

            if host in WEAK_HOSTS:
                if cap(row, "probable"):
                    note(row, f"Person source is a {WEAK_HOSTS[host]}.")
                    record("weak person source capped", row, f" ({host})")
            elif WIKTIONARY.search(url):
                if cap(row, "probable"):
                    note(row, "Person source is Wiktionary, which attests the word not the person.")
                    record("wiktionary as person source capped", row)
            elif any(p.search(url) for p in SEARCH_PATTERNS):
                if cap(row, "probable"):
                    note(row, "Person source is a search or index page, not an individual record.")
                    record("search-url person source capped", row, f" ({host})")

    for key, count in counts.items():
        print(f"{count:5}  {key}")
        for ex in examples[key]:
            print(f"         {ex}")

    # In `make rebuild` this sweep runs before the Wikipedia pass, so rule 1 only ever discards
    # the researchers' unchecked default. Run standalone afterwards, it discards the pass as
    # well, and the only way back is the network.
    if counts["name_status downgraded"] and ENRICHMENT.exists():
        established = sum(
            1 for r in csv.DictReader(ENRICHMENT.open(encoding="utf-8"))
            if "name_status=" in r.get("actions", "")
        )
        if established:
            print(
                f"\nNOTE: {established} name_status values came from the Wikipedia pass and are "
                "not protected here.\n      Re-run `make enrich` after applying, or run the whole "
                "pipeline with `make all`."
            )

    if not args.apply:
        print("\ndry run; pass --apply to write")
        return

    with MASTER.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nwrote {MASTER.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
