#!/usr/bin/env python3
"""Build data/aptronyms.db, a queryable SQLite copy of the master CSV.

The CSV is the source of truth because it diffs cleanly in git. This exists so the dataset
can be queried without loading it into pandas, and so the many-to-many between people and
aptronym types is available as a real join rather than a pipe-delimited string.
"""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "aptronyms.csv"
DB = ROOT / "data" / "aptronyms.db"

INT_COLUMNS = {"birth_year", "death_year", "aptronym_score"}

SCHEMA = """
DROP VIEW  IF EXISTS publishable;
DROP TABLE IF EXISTS aptronym_types;
DROP TABLE IF EXISTS people;

CREATE TABLE people (
    id                   TEXT PRIMARY KEY,
    full_name            TEXT NOT NULL,
    first_name           TEXT,
    last_name            TEXT,
    occupation           TEXT,
    field                TEXT,
    organization         TEXT,
    country              TEXT,
    birth_year           INTEGER,
    death_year           INTEGER,
    aptronym_type        TEXT,
    aptronym_score       INTEGER CHECK (aptronym_score BETWEEN 1 AND 5),
    name_element         TEXT,
    connection           TEXT,
    name_origin          TEXT,
    name_status          TEXT,
    person_source_url    TEXT,
    name_source_url      TEXT,
    discovery_source_url TEXT,
    notes                TEXT,
    review_status        TEXT
);

CREATE TABLE aptronym_types (
    id            TEXT NOT NULL REFERENCES people(id),
    aptronym_type TEXT NOT NULL,
    PRIMARY KEY (id, aptronym_type)
);

CREATE INDEX people_field         ON people(field);
CREATE INDEX people_score         ON people(aptronym_score);
CREATE INDEX people_review        ON people(review_status);
CREATE INDEX people_country       ON people(country);
CREATE INDEX people_last_name     ON people(last_name);
CREATE INDEX types_type           ON aptronym_types(aptronym_type);

-- Rows fit to publish: reviewed as real and scoring at least a clear fit.
CREATE VIEW publishable AS
SELECT * FROM people
WHERE review_status IN ('verified', 'probable')
  AND aptronym_score >= 3
ORDER BY aptronym_score DESC, full_name;
"""


def main() -> None:
    rows = list(csv.DictReader(MASTER.open(encoding="utf-8")))
    DB.unlink(missing_ok=True)
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)

    columns = [c for c in rows[0] if c]
    placeholders = ", ".join("?" for _ in columns)
    people: list[tuple] = []
    types: list[tuple[str, str]] = []

    for row in rows:
        values = []
        for col in columns:
            val = (row.get(col) or "").strip()
            if col in INT_COLUMNS:
                values.append(int(val) if val.lstrip("-").isdigit() else None)
            else:
                values.append(val or None)
        people.append(tuple(values))
        for t in {t for t in (row.get("aptronym_type") or "").split("|") if t}:
            types.append((row["id"], t))

    con.executemany(
        f"INSERT INTO people ({', '.join(columns)}) VALUES ({placeholders})", people
    )
    con.executemany(
        "INSERT OR IGNORE INTO aptronym_types (id, aptronym_type) VALUES (?, ?)", types
    )
    con.commit()

    counts = {
        "people": con.execute("SELECT count(*) FROM people").fetchone()[0],
        "type links": con.execute("SELECT count(*) FROM aptronym_types").fetchone()[0],
        "publishable": con.execute("SELECT count(*) FROM publishable").fetchone()[0],
    }
    con.close()
    for label, n in counts.items():
        print(f"{n:6}  {label}")
    print(f"wrote {DB.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
