#!/usr/bin/env python3
"""Repoint NPI-sourced rows at the individual record that backs them.

Fifty-one medical rows cite the NPI registry's front door rather than a provider record.
That citation names nobody, and because the homepage returns 200 forever the link check can
never surface it. The registry has a JSON API, so the record can be recovered: search on the
name, keep the result whose licensed taxonomy matches the occupation we recorded, and write
the provider URL back.

A row is only resolved when exactly one provider matches on both name and taxonomy. Common
names return dozens of clinicians and no amount of string comparison can pick the right one,
so those are left for a human with the candidates listed.

Writes a correction file for `scripts/audit.py apply`, which is where the master gets touched.

    python3 scripts/resolve_npi.py            # query and write the correction file
    python3 scripts/resolve_npi.py --dry-run  # query and report, write nothing
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from audit import merge_corrections

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "aptronyms.csv"
OUT = ROOT / "data" / "audit" / "corrections" / "npi.csv"
LOG = ROOT / "data" / "audit" / "corrections" / "npi.log.md"

API = "https://npiregistry.cms.hhs.gov/api/"
RECORD = "https://npiregistry.cms.hhs.gov/provider-view/{}"
UA = "aptronym-research/1.0 (data journalism project; contact via repo)"

HOST = re.compile(r"^https?://(?:www\.)?npiregistry\.cms\.hhs\.gov", re.IGNORECASE)
ROOTLESS = re.compile(r"^https?://[^/?#]+/?$", re.IGNORECASE)

# The registry is a US licensing system, so a non-US row cannot be in it at all.
DOMESTIC = "United States"

# Occupation as we recorded it -> substrings that must appear in the provider's taxonomy.
# Any one of them is enough. Taxonomy strings are the registry's own wording, e.g.
# "Obstetrics & Gynecology, Urogynecology and Reconstructive Pelvic Surgery".
TAXONOMY = {
    "anesthesiologist": ("anesthesiology",),
    "cardiologist": ("cardiovascular", "cardiology"),
    "dentist": ("dentist",),
    "dermatologist": ("dermatology",),
    "obstetrician-gynecologist": ("obstetrics", "gynecology"),
    "pediatrician": ("pediatrics",),
    "plastic surgeon": ("plastic surgery",),
    "prosthodontist": ("prosthodontics",),
    "psychiatrist": ("psychiatry",),
    "registered nurse": ("registered nurse",),
    "surgeon": ("surgery",),
    "surgical critical care surgeon": ("critical care", "surgery"),
    "urologist": ("urology",),
}

CORRECTION_COLUMNS = [
    "id", "full_name", "verdict", "new_aptronym_score", "new_review_status",
    "new_aptronym_type", "new_connection", "new_name_origin", "new_name_status",
    "new_person_source_url", "new_notes", "reason",
]


def norm(value: str) -> str:
    """Casefold and strip punctuation, so O'BRIEN and O'Brien compare equal."""
    return re.sub(r"[^a-z]", "", (value or "").lower())


def search(first: str, last: str) -> list[dict]:
    query = urllib.parse.urlencode(
        {"version": "2.1", "first_name": first, "last_name": last, "limit": 200}
    )
    req = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp).get("results", [])


def taxonomies(provider: dict) -> list[str]:
    """Primary taxonomies, or all of them when the registry marks none as primary. Some
    entries carry a null description, which is not evidence of anything."""
    listed = provider.get("taxonomies", [])
    primary = [t["desc"] for t in listed if t.get("primary") and t.get("desc")]
    return primary or [t["desc"] for t in listed if t.get("desc")]


def licensed_as(provider: dict, wanted: tuple[str, ...]) -> bool:
    """Whether any taxonomy names one of the specialties we are looking for. The match has
    to respect word boundaries: "Psychiatry & Neurology" contains the letters of urology."""
    listed = " | ".join(taxonomies(provider)).lower()
    return any(re.search(rf"\b{re.escape(word)}", listed) for word in wanted)


def state_of(provider: dict) -> str:
    for address in provider.get("addresses", []):
        if address.get("state"):
            return address["state"]
    return ""


def describe(provider: dict) -> str:
    basic = provider.get("basic", {})
    name = f"{basic.get('first_name', '')} {basic.get('last_name', '')}".strip().title()
    return f"{provider['number']} {name}, {'; '.join(taxonomies(provider))} ({state_of(provider)})"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = list(csv.DictReader(MASTER.open(encoding="utf-8")))
    targets = [
        r for r in rows
        if HOST.match(r["person_source_url"]) and ROOTLESS.match(r["person_source_url"])
    ]
    print(f"{len(targets)} rows cite the NPI registry homepage\n")
    if not targets:
        # Everything has been repointed already. Rewriting the correction file and the log
        # from an empty run would throw away the work that made the run empty.
        print("nothing to resolve; leaving the correction file and log as they are")
        return

    corrections: list[dict[str, str]] = []
    unresolved: list[tuple[dict[str, str], str, list[dict]]] = []

    for row in targets:
        label = f"{row['id']} {row['full_name']:22}"

        if row["country"] != DOMESTIC:
            unresolved.append((row, f"recorded as {row['country']}; NPI is a US register", []))
            print(f"{label} SKIP  not a US row ({row['country']})")
            continue

        wanted = TAXONOMY.get(row["occupation"])
        if not wanted:
            unresolved.append((row, f"no taxonomy mapping for {row['occupation']!r}", []))
            print(f"{label} SKIP  unmapped occupation {row['occupation']!r}")
            continue

        try:
            results = search(row["first_name"], row["last_name"])
        except Exception as exc:  # noqa: BLE001
            unresolved.append((row, f"lookup failed: {type(exc).__name__}", []))
            print(f"{label} ERROR {type(exc).__name__}")
            continue
        finally:
            time.sleep(0.3)

        # The API matches loosely: a search for Abby returns Abbie. Only an exact name is
        # evidence about the person we recorded.
        named = [
            p for p in results
            if norm(p.get("basic", {}).get("first_name")) == norm(row["first_name"])
            and norm(p.get("basic", {}).get("last_name")) == norm(row["last_name"])
        ]
        matched = [p for p in named if licensed_as(p, wanted)]

        if len(matched) == 1:
            provider = matched[0]
            npi = provider["number"]
            state = state_of(provider)
            corrections.append({
                "id": row["id"],
                "full_name": row["full_name"],
                "verdict": "fix",
                "new_person_source_url": RECORD.format(npi),
                "new_notes": (
                    f"NPI {npi}, licensed in {state} as "
                    f"{'; '.join(taxonomies(provider))}." if state else
                    f"NPI {npi}, licensed as {'; '.join(taxonomies(provider))}."
                ),
                "reason": "Repointed from the registry homepage to the provider record.",
            })
            print(f"{label} OK    {describe(provider)}")
        elif not named:
            unresolved.append((row, f"no exact name match in {len(results)} results", []))
            print(f"{label} NONE  no exact name match ({len(results)} loose results)")
        elif not matched:
            unresolved.append((row, f"{len(named)} name matches, none in {row['occupation']}", named))
            print(f"{label} MISS  {len(named)} name matches, none licensed as {row['occupation']}")
        else:
            unresolved.append((row, f"{len(matched)} providers match name and specialty", matched))
            print(f"{label} MANY  {len(matched)} match name and specialty")

    print(f"\nresolved   {len(corrections)}")
    print(f"unresolved {len(unresolved)}")

    if args.dry_run:
        print("\ndry run; nothing written")
        return

    total = merge_corrections(OUT, CORRECTION_COLUMNS, corrections)

    lines = [
        "# NPI resolution",
        "",
        "Generated by `scripts/resolve_npi.py`. Every row here cited",
        "`https://npiregistry.cms.hhs.gov/` — the registry front door, which identifies nobody.",
        "The script searched the registry API by name and kept the provider whose licensed",
        "taxonomy matches the recorded occupation.",
        "",
        f"Resolved to a single provider record: **{total}**.",
        f"Left for review: **{len(unresolved)}**.",
        "",
        "## Left for review",
        "",
        "These keep the homepage citation, which `scripts/integrity.py` caps at `borderline`,",
        "so they drop out of the published register until someone sources them properly.",
        "",
    ]
    for row, why, candidates in unresolved:
        lines.append(f"### {row['id']} {row['full_name']} — {row['occupation']}")
        lines.append("")
        lines.append(f"{why}.")
        if candidates:
            lines.append("")
            lines.append("Candidates:")
            lines.append("")
            for provider in candidates[:12]:
                lines.append(f"- {describe(provider)}")
            if len(candidates) > 12:
                lines.append(f"- ...and {len(candidates) - 12} more")
        lines.append("")
    LOG.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nwrote {OUT.relative_to(ROOT)} ({total} corrections, {len(corrections)} from this run)")
    print(f"wrote {LOG.relative_to(ROOT)}")
    print("\nrun `python3 scripts/audit.py apply` to fold it into the master")


if __name__ == "__main__":
    main()
