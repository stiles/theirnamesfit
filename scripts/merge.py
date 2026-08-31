#!/usr/bin/env python3
"""Merge research CSVs into the master dataset: validate, dedupe, assign stable ids.

    python3 scripts/merge.py --check                 validate everything, write nothing
    python3 scripts/merge.py --only a.csv b.csv      merge just these research files
    python3 scripts/merge.py --fresh --key name      rebuild from research, ignoring the master

Ids are **sticky**. A row that already has an id keeps it, and only genuinely new people get
the next number in sequence. This matters because the audit correction files in
data/audit/corrections/ are keyed by id: if ids were re-derived from sort position, adding a
row near the top of the alphabet would silently retarget every correction below it.

Stickiness alone was not enough, because it says nothing about how a *new* id is chosen. New
numbers went out in alphabetical order within whatever batch a merge happened to cover, so
the id a person ended up with depended on how the merges had been grouped. A rebuild that
grouped them differently reshuffled the tail of the file: 47 people swapped ids, and a
reviewer's note about an umpire recorded only as "Plate" was reapplied to Paul Fair, who is
a different umpire, rescoring him on the strength of it.

So the mapping is written down instead of re-derived. data/id_ledger.csv records the id every
person has ever been given, and is committed. Merging consults it before issuing anything new,
which makes the id space independent of batching, ordering and how many passes have been run.

The dedupe key is name plus field by default. Namesakes across domains are common — an NFL
defensive end and a district attorney both called Chase Young — and collapsing on name alone
fuses two people into one corrupt row.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "data" / "research"
MASTER = ROOT / "data" / "aptronyms.csv"
LEDGER = ROOT / "data" / "id_ledger.csv"
LEDGER_COLUMNS = ["id", "key_name", "key_field", "full_name"]

COLUMNS = [
    "id", "full_name", "first_name", "last_name", "occupation", "field", "organization",
    "country", "birth_year", "death_year", "aptronym_type", "aptronym_score", "name_element",
    "connection", "name_origin", "name_status", "person_source_url", "name_source_url",
    "discovery_source_url", "notes", "review_status",
]

TYPES = {"direct", "wordplay", "semantic", "phonetic", "translation", "ironic", "other"}
NAME_STATUS = {"birth_name", "legal_name", "professional_name", "pseudonym", "unknown"}
REVIEW_STATUS = {"verified", "probable", "borderline", "rejected"}
FIELDS = {
    "sports", "medicine", "science", "law", "politics", "military", "weather", "arts",
    "media", "business", "food", "religion", "education", "trades", "crime", "transport",
    "other",
}

# Preference order when two rows describe the same person. A reviewed rejection outranks an
# unreviewed claim, so re-running a merge can never quietly undo an audit decision.
REVIEW_RANK = {"rejected": 4, "verified": 3, "probable": 2, "borderline": 1, "": 0}


def norm_name(name: str) -> str:
    """Fold a name to a dedupe key: strip accents, punctuation, case and extra space."""
    folded = unicodedata.normalize("NFKD", name)
    folded = "".join(c for c in folded if not unicodedata.combining(c))
    folded = folded.lower().replace("&", "and")
    folded = re.sub(r"\b(jr|sr|ii|iii|iv|dr|prof|sir|rev)\b", " ", folded)
    folded = re.sub(r"[^a-z0-9 ]+", " ", folded)
    return " ".join(folded.split())


def read_ledger() -> tuple[dict[tuple[str, str], str], dict[tuple[str, str], str]]:
    """The key -> id mapping, and the name each key was last seen under."""
    if not LEDGER.exists():
        return {}, {}
    with LEDGER.open(newline="", encoding="utf-8") as fh:
        entries = list(csv.DictReader(fh))
    ids = {(r["key_name"], r["key_field"]): r["id"] for r in entries}
    names = {(r["key_name"], r["key_field"]): r["full_name"] for r in entries}
    return ids, names


def write_ledger(
    rows: list[dict[str, str]],
    ledger: dict[tuple[str, str], str],
    names: dict[tuple[str, str], str],
) -> int:
    """Record the id of every person in the merge output, keeping entries for people who are
    not in this run. A ledger row is never rewritten: an id, once issued, is theirs. A person
    can hold more than one key — a rename leaves the old spelling behind as an alias — which
    is the point, since the alias is what stops the id being handed to somebody else."""
    added = 0
    for row in rows:
        key = (norm_name(row["full_name"]), row["field"])
        if key not in ledger:
            ledger[key] = row["id"]
            added += 1
        names[key] = row["full_name"]

    with LEDGER.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=LEDGER_COLUMNS)
        writer.writeheader()
        for key, rid in sorted(ledger.items(), key=lambda kv: (kv[1], kv[0])):
            writer.writerow({
                "id": rid,
                "key_name": key[0],
                "key_field": key[1],
                "full_name": names.get(key, ""),
            })
    return added


def ledger_id(row: dict[str, str], ledger: dict[tuple[str, str], str], taken: set[str]) -> str:
    """The id this person has been issued before, if any. The name-only fallback covers the
    first-pass merge, which dedupes on name alone and so may carry a different field than the
    one the person finally settles in."""
    name = norm_name(row["full_name"])
    found = ledger.get((name, row["field"]))
    if found and found not in taken:
        return found

    same_name = [rid for (n, _), rid in ledger.items() if n == name and rid not in taken]
    return same_name[0] if len(same_name) == 1 else ""


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = set(COLUMNS) - set(reader.fieldnames or [])
        extra = set(reader.fieldnames or []) - set(COLUMNS)
        if missing or extra:
            raise SystemExit(
                f"{path.name}: header mismatch (missing={sorted(missing)}, extra={sorted(extra)})"
            )
        rows = []
        for row in reader:
            if None in row:
                raise SystemExit(f"{path.name}: row for '{row.get('full_name')}' has extra fields")
            row["_source_file"] = path.name
            rows.append(row)
        return rows


def validate(row: dict[str, str], where: str, problems: list[str]) -> None:
    def flag(msg: str) -> None:
        problems.append(f"{where} [{row.get('full_name', '?')}] {msg}")

    if not row.get("full_name", "").strip():
        flag("missing full_name")
    if not row.get("person_source_url", "").strip():
        flag("missing person_source_url")

    types = [t for t in row.get("aptronym_type", "").split("|") if t]
    if not types:
        flag("missing aptronym_type")
    for t in types:
        if t not in TYPES:
            flag(f"bad aptronym_type '{t}'")

    score = row.get("aptronym_score", "").strip()
    if not score.isdigit() or not 1 <= int(score) <= 5:
        flag(f"bad aptronym_score '{score}'")

    if row.get("field", "").strip() not in FIELDS:
        flag(f"bad field '{row.get('field')}'")
    if row.get("name_status", "").strip() not in NAME_STATUS:
        flag(f"bad name_status '{row.get('name_status')}'")
    if row.get("review_status", "").strip() not in REVIEW_STATUS:
        flag(f"bad review_status '{row.get('review_status')}'")

    for col in ("birth_year", "death_year"):
        val = row.get(col, "").strip()
        if val and not re.fullmatch(r"-?\d{1,4}", val):
            flag(f"bad {col} '{val}'")

    if "translation" in types and not row.get("name_source_url", "").strip():
        flag("translation type without name_source_url")

    for col in ("person_source_url", "name_source_url", "discovery_source_url"):
        val = row.get(col, "").strip()
        if val and not val.startswith(("http://", "https://")):
            flag(f"{col} is not a url '{val[:40]}'")


def merge_pair(keep: dict[str, str], drop: dict[str, str]) -> dict[str, str]:
    """Fill blanks in `keep` from `drop` and union the type list."""
    for col in COLUMNS:
        if col == "id":
            continue
        if not keep.get(col, "").strip() and drop.get(col, "").strip():
            keep[col] = drop[col]
    keep["id"] = keep.get("id") or drop.get("id", "")
    a = [t for t in keep.get("aptronym_type", "").split("|") if t]
    b = [t for t in drop.get("aptronym_type", "").split("|") if t]
    keep["aptronym_type"] = "|".join(dict.fromkeys(a + b))
    notes = [n for n in (keep.get("notes", ""), drop.get("notes", "")) if n.strip()]
    if len(notes) == 2 and notes[0] != notes[1] and notes[1] not in notes[0]:
        keep["notes"] = f"{notes[0]} / {notes[1]}"
    return keep


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("--fresh", action="store_true", help="ignore the existing master")
    parser.add_argument("--only", nargs="*", help="research filenames to merge")
    parser.add_argument("--all-research", action="store_true", help="merge every research file")
    parser.add_argument("--key", choices=["name", "name+field"], default="name+field")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    if MASTER.exists() and not args.fresh:
        rows.extend(read_rows(MASTER))

    if args.only:
        paths = [RESEARCH / n for n in args.only]
        for p in paths:
            if not p.exists():
                raise SystemExit(f"no such research file: {p}")
    elif args.all_research:
        paths = sorted(RESEARCH.glob("*.csv"))
    else:
        # Default to the master alone. Replaying research files unasked is how an earlier
        # run silently reverted audit decisions.
        paths = []
    for path in paths:
        rows.extend(read_rows(path))

    problems: list[str] = []
    for row in rows:
        validate(row, row["_source_file"], problems)

    def key_of(row: dict[str, str]) -> tuple[str, str]:
        name = norm_name(row["full_name"])
        return (name, "") if args.key == "name" else (name, row["field"])

    by_key: dict[tuple[str, str], dict[str, str]] = {}
    dupes: list[str] = []
    collisions: dict[str, set[str]] = {}
    for row in rows:
        name = norm_name(row["full_name"])
        if not name:
            continue
        collisions.setdefault(name, set()).add(row["field"])
        key = key_of(row)
        if key in by_key:
            existing = by_key[key]
            a = REVIEW_RANK.get(existing.get("review_status", ""), 0)
            b = REVIEW_RANK.get(row.get("review_status", ""), 0)
            keep, drop = (existing, row) if a >= b else (row, existing)
            by_key[key] = merge_pair(keep, drop)
            dupes.append(f"{row['full_name']} ({existing['_source_file']} + {row['_source_file']})")
        else:
            by_key[key] = row

    out = sorted(by_key.values(), key=lambda r: (norm_name(r["full_name"]), r["field"]))

    # Sticky ids: keep what a row already has, then what the ledger says this person was
    # given before, and only then a fresh number.
    ledger, ledger_names = read_ledger()
    used = {r["id"] for r in out if r.get("id", "").strip()}

    pending = [r for r in out if not r.get("id", "").strip()]
    for row in pending:
        found = ledger_id(row, ledger, used)
        if found:
            row["id"] = found
            used.add(found)

    issued = 0
    next_num = 1
    for row in pending:
        if row.get("id", "").strip():
            continue
        while f"apt-{next_num:04d}" in used:
            next_num += 1
        row["id"] = f"apt-{next_num:04d}"
        used.add(row["id"])
        issued += 1

    cross_field = {n: f for n, f in collisions.items() if len(f) > 1}

    print(f"read     {len(rows)} rows from {0 if args.fresh else 1} master + {len(paths)} research")
    print(f"deduped  {len(dupes)} collapsed -> {len(out)} unique people")
    print(f"ids      {len(pending) - issued} recovered from the ledger, {issued} newly issued")
    if cross_field:
        print(f"\n{len(cross_field)} same-name pairs kept apart across fields (check these):")
        for name, fields in sorted(cross_field.items()):
            print(f"  {name}: {', '.join(sorted(fields))}")
    if problems:
        print(f"\n{len(problems)} validation problems:")
        for p in problems:
            print(f"  {p}")

    if args.check:
        return 1 if problems else 0

    with MASTER.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(out)
    print(f"\nwrote    {MASTER.relative_to(ROOT)}")

    added = write_ledger(out, ledger, ledger_names)
    print(f"wrote    {LEDGER.relative_to(ROOT)} ({added} new)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
