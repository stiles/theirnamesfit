#!/usr/bin/env python3
"""Check recorded birth and death years against the Wikipedia lead each row cites.

`scripts/enrich_wikipedia.py` only ever fills an empty cell, so a wrong date it wrote in an
earlier run survives every re-run. An earlier version of its date parser read any parenthesised
year pair as a lifespan, which turned career spans into deaths: the site told readers that
Cecil Fielder died in 1988 and Eric Gagne in 2004, both of whom are alive.

Rows where the lead disagrees are proposed as corrections. Rows where the lead looks like it
is about somebody else are only reported, because the fix there is the citation and not the
date — a bishop who died in 1476 sourced to the film director's article does not need his
dates replaced with the director's.

    python3 scripts/check_dates.py             # report, and write the correction file
    python3 scripts/check_dates.py --dry-run   # report only

Writes data/audit/corrections/dates.csv for `scripts/audit.py apply`, and a log beside it.
"""

from __future__ import annotations

import argparse
import csv
import re
import time
from collections import defaultdict
from pathlib import Path

from audit import merge_corrections
from enrich_wikipedia import api_extracts, dates, tokens, wiki_target

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "aptronyms.csv"
OUT = ROOT / "data" / "audit" / "corrections" / "dates.csv"
LOG = ROOT / "data" / "audit" / "corrections" / "dates.log.md"

COLUMNS = ["id", "full_name", "verdict", "new_birth_year", "new_death_year", "reason"]

# A lead that opens by listing several people cannot verify any one of them.
INDEX_PAGE = re.compile(r"\bmay refer to\b|\bis a (?:\w+ )?surname\b|\bis a given name\b", re.I)

# Two dates a century apart are not the same person, however well the names match. This is
# how a fifteenth-century bishop ended up sourced to John Carpenter the film director.
SAME_ERA = 100


def era_gap(row: dict[str, str], birth: str, death: str) -> int:
    """Largest disagreement in years between what we hold and what the lead says."""
    pairs = [(row["birth_year"], birth), (row["death_year"], death)]
    gaps = [abs(int(a) - int(b)) for a, b in pairs if a and b]
    if gaps:
        return max(gaps)
    # Nothing lines up field to field; compare whatever dates each side has.
    ours = [int(v) for v in (row["birth_year"], row["death_year"]) if v]
    theirs = [int(v) for v in (birth, death) if v]
    return min(abs(a - b) for a in ours for b in theirs) if ours and theirs else 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = list(csv.DictReader(MASTER.open(encoding="utf-8")))
    targets: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        target = wiki_target(row.get("person_source_url", ""))
        if target:
            targets[target[0]][target[1]].append(row)

    extracts: dict[tuple[str, str], str] = {}
    for host, titles in targets.items():
        keys = list(titles)
        print(f"{host}: {len(keys)} articles", flush=True)
        for i in range(0, len(keys), 20):
            try:
                for title, text in api_extracts(host, keys[i : i + 20]).items():
                    extracts[(host, title)] = text
            except Exception as exc:  # noqa: BLE001
                print(f"  batch failed: {type(exc).__name__}", flush=True)
            time.sleep(0.8)

    fixes: list[dict[str, str]] = []
    review: list[tuple[dict[str, str], str, str, str]] = []

    for host, titles in targets.items():
        for title, group in titles.items():
            lead = extracts.get((host, title), "")
            if not lead:
                continue
            birth, death = dates(lead[:900])

            for row in group:
                # BC years are negative here and the parser has no concept of them, so it
                # would read "died 503 BC" as no death at all.
                if row["birth_year"].startswith("-") or row["death_year"].startswith("-"):
                    continue

                problems = []
                if birth and row["birth_year"] and row["birth_year"] != birth:
                    problems.append(f"birth {row['birth_year']} should be {birth}")
                if death and row["death_year"] and row["death_year"] != death:
                    problems.append(f"death {row['death_year']} should be {death}")
                # A lead giving a birth would give a death as well. A death recorded against
                # a birth-only lead is the spurious-lifespan bug.
                if birth and not death and row["death_year"]:
                    problems.append(f"death {row['death_year']} recorded, lead gives birth only")
                if not problems:
                    continue

                if INDEX_PAGE.search(lead[:220]):
                    review.append((row, title, "cited page is an index, not a biography", lead))
                elif not set(tokens(row["full_name"])) <= set(tokens(title)):
                    review.append((row, title, "article title is not this person's name", lead))
                elif era_gap(row, birth, death) > SAME_ERA:
                    review.append((row, title, "cited article is about a different era", lead))
                else:
                    fixes.append({
                        "id": row["id"],
                        "full_name": row["full_name"],
                        "verdict": "fix",
                        "new_birth_year": birth or row["birth_year"],
                        "new_death_year": death or "NULL",
                        "reason": "; ".join(problems) + " per the cited article.",
                    })

    print(f"\n{len(extracts)} leads read")
    print(f"{len(fixes)} rows corrected against their own source")
    print(f"{len(review)} rows need a human, listed in the log")

    for fix in fixes:
        print(f"  {fix['id']} {fix['full_name']:26} {fix['reason']}")
    for row, title, why, _ in review:
        print(f"  REVIEW {row['id']} {row['full_name']:20} {why} ({title})")

    if args.dry_run:
        print("\ndry run; nothing written")
        return

    total = merge_corrections(OUT, COLUMNS, fixes)

    lines = [
        "# Date check",
        "",
        "Generated by `scripts/check_dates.py`, which compares the birth and death years we",
        "hold against the Wikipedia lead each row cites.",
        "",
        f"Corrected against the cited source: **{total}**.",
        f"Referred for review: **{len(review)}**.",
        "",
        "## Referred for review",
        "",
        "The date is not the problem in these rows. The citation is: it points at an index",
        "page, at somebody else with the same name, or at a person from another century.",
        "",
    ]
    for row, title, why, lead in sorted(review, key=lambda x: x[0]["id"]):
        lines += [
            f"### {row['id']} {row['full_name']} — {row['occupation']}",
            "",
            f"Cited: [{title}]({row['person_source_url']}) — {why}.",
            "",
            f"Recorded dates: {row['birth_year'] or '?'}–{row['death_year'] or '?'}.",
            "",
            f"> {lead[:280].strip()}",
            "",
        ]
    LOG.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nwrote {OUT.relative_to(ROOT)} ({total} corrections, {len(fixes)} from this run)")
    print(f"wrote {LOG.relative_to(ROOT)}")
    print("\nrun `python3 scripts/audit.py apply` to fold it into the master")


if __name__ == "__main__":
    main()
