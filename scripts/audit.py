#!/usr/bin/env python3
"""Split the master dataset into audit slices, and apply audit corrections back to it.

    python3 scripts/audit.py split    # write data/audit/<slice>.csv for reviewers
    python3 scripts/audit.py apply    # fold data/audit/corrections/*.csv into the master
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "aptronyms.csv"
AUDIT = ROOT / "data" / "audit"
CORRECTIONS = AUDIT / "corrections"

# Reviewer-facing slices, sized to be auditable in one pass.
SLICES: dict[str, set[str]] = {
    "sports": {"sports"},
    "science-weather": {"science", "weather"},
    "medicine-law": {"medicine", "law"},
    "arts-commerce": {"arts", "media", "business", "food", "religion"},
    "public-practical": {
        "politics", "military", "crime", "education", "trades", "transport", "other",
    },
}

CORRECTION_COLUMNS = [
    "id",
    "full_name",
    "verdict",
    "new_aptronym_score",
    "new_review_status",
    "new_aptronym_type",
    "new_connection",
    "new_name_origin",
    "new_name_status",
    "new_person_source_url",
    "new_notes",
    "reason",
]

VERDICTS = {"keep", "rescore", "reject", "fix"}


def read_master() -> tuple[list[str], list[dict[str, str]]]:
    with MASTER.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


def do_split() -> None:
    cols, rows = read_master()
    AUDIT.mkdir(parents=True, exist_ok=True)
    CORRECTIONS.mkdir(parents=True, exist_ok=True)

    assigned = 0
    for name, fields in SLICES.items():
        subset = [r for r in rows if r["field"] in fields]
        assigned += len(subset)
        path = AUDIT / f"{name}.csv"
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=cols)
            writer.writeheader()
            writer.writerows(subset)
        print(f"{path.relative_to(ROOT)}: {len(subset)} rows")

        template = CORRECTIONS / f"{name}.template.csv"
        with template.open("w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerow(CORRECTION_COLUMNS)

    if assigned != len(rows):
        print(f"WARNING: {len(rows) - assigned} rows fell outside every slice")


def do_apply() -> None:
    cols, rows = read_master()
    by_id = {r["id"]: r for r in rows}
    applied = 0
    skipped: list[str] = []
    verdicts: dict[str, int] = {}

    paths = sorted(p for p in CORRECTIONS.glob("*.csv") if ".template." not in p.name)
    if not paths:
        print("no correction files found in data/audit/corrections/")
        return

    for path in paths:
        with path.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                rid = (row.get("id") or "").strip()
                target = by_id.get(rid)
                if not target:
                    skipped.append(f"{path.name}: unknown id '{rid}'")
                    continue

                verdict = (row.get("verdict") or "").strip().lower()
                if verdict and verdict not in VERDICTS:
                    skipped.append(f"{path.name}: {rid} bad verdict '{verdict}'")
                    continue
                verdicts[verdict or "blank"] = verdicts.get(verdict or "blank", 0) + 1

                changed = False
                for key, value in row.items():
                    # DictReader yields a None key when a row has more fields than the
                    # header, which happens when a reviewer leaves an unquoted comma.
                    if key is None:
                        skipped.append(f"{path.name}: {rid} has unquoted extra fields")
                        continue
                    if not key.startswith("new_"):
                        continue
                    value = (value or "").strip()
                    if not value:
                        continue
                    column = key[4:]
                    if column not in cols:
                        skipped.append(f"{path.name}: {rid} unknown column '{column}'")
                        continue
                    # A blank cell means "leave alone", so removing a bad citation needs an
                    # explicit sentinel.
                    if value == "NULL":
                        value = ""
                    if target[column] != value:
                        target[column] = value
                        changed = True

                if verdict == "reject" and target["review_status"] != "rejected":
                    target["review_status"] = "rejected"
                    changed = True

                reason = (row.get("reason") or "").strip()
                if reason and verdict in {"reject", "rescore", "fix"}:
                    note = target.get("notes", "").strip()
                    audit_note = f"Audit: {reason}"
                    if audit_note not in note:
                        target["notes"] = f"{note} {audit_note}".strip()
                        changed = True

                applied += int(changed)

    with MASTER.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"correction files: {len(paths)}")
    print(f"verdicts: {verdicts}")
    print(f"rows changed: {applied}")
    for s in skipped:
        print(f"  skipped: {s}")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "split":
        do_split()
    elif command == "apply":
        do_apply()
    else:
        raise SystemExit(__doc__)
