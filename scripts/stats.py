#!/usr/bin/env python3
"""Print a summary of the master dataset. Used to keep the README numbers honest."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "aptronyms.csv"
CHECK = ROOT / "data" / "url_check.csv"


def table(title: str, counter: Counter, total: int, order: list[str] | None = None) -> None:
    print(f"\n{title}")
    keys = order or [k for k, _ in counter.most_common()]
    for key in keys:
        n = counter.get(key, 0)
        if n:
            print(f"  {key or '(blank)':22} {n:5}  {n / total:5.1%}")


def main() -> None:
    rows = list(csv.DictReader(MASTER.open(encoding="utf-8")))
    total = len(rows)
    kept = [r for r in rows if r["review_status"] != "rejected"]

    print(f"records                {total}")
    print(f"not rejected           {len(kept)}")
    print(f"score 3+ and reviewed  "
          f"{sum(1 for r in kept if int(r['aptronym_score']) >= 3 and r['review_status'] in {'verified', 'probable'})}")

    table("review_status", Counter(r["review_status"] for r in rows), total,
          ["verified", "probable", "borderline", "rejected"])
    table("aptronym_score (all records)", Counter(r["aptronym_score"] for r in rows), total,
          ["5", "4", "3", "2", "1"])
    table("aptronym_score (excluding rejected)", Counter(r["aptronym_score"] for r in kept),
          len(kept), ["5", "4", "3", "2", "1"])

    types = Counter()
    for r in rows:
        for t in r["aptronym_type"].split("|"):
            if t:
                types[t] += 1
    table("aptronym_type (multi-valued)", types, total)
    table("field", Counter(r["field"] for r in rows), total)
    table("name_status", Counter(r["name_status"] for r in rows), total,
          ["birth_name", "legal_name", "professional_name", "pseudonym", "unknown"])

    countries = Counter(r["country"] for r in rows if r["country"])
    print(f"\ncountries              {len(countries)}")
    for country, n in countries.most_common(12):
        print(f"  {country:22} {n:5}")

    def years(subset: list[dict[str, str]]) -> list[int]:
        return [int(r["birth_year"]) for r in subset if r["birth_year"].lstrip("-").isdigit()]

    dated = years(rows)
    print(f"\nbirth year known       {len(dated)} of {total}")
    if dated:
        print(f"  earliest             {min(dated)}")
        print(f"  latest               {max(dated)}")
    # Reported separately because every one of the earliest-born records is a rejected Roman
    # cognomen, so the overall minimum overstates the range of the usable data.
    kept = years([r for r in rows if r["review_status"] != "rejected"])
    if kept:
        print(f"  earliest not rejected {min(kept)}")
    print(f"death year known       {sum(1 for r in rows if r['death_year'])}")
    print(f"name_origin recorded   {sum(1 for r in rows if r['name_origin'])}")
    print(f"name_source_url        {sum(1 for r in rows if r['name_source_url'])}")
    print(f"discovery_source_url   {sum(1 for r in rows if r['discovery_source_url'])}")

    if CHECK.exists():
        checks = list(csv.DictReader(CHECK.open(encoding="utf-8")))
        person = [c for c in checks if c["column"] == "person_source_url"]
        live = sum(1 for c in person if c["status"] == "200")
        print(f"\nperson source urls     {len(person)} checked, {live} returned 200")
        bad = Counter(c["status"] for c in person if c["status"] != "200")
        for status, n in bad.most_common(8):
            print(f"  {status:22} {n:5}")


if __name__ == "__main__":
    main()
