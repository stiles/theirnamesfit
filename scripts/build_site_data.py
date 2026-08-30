#!/usr/bin/env python3
"""Emit the public site's data from the master dataset.

The website never reads the research CSV directly. This writes a filtered, slugged snapshot
into site/src/data/ which is committed, so the deploy needs Node and nothing else.

Only the fields the site is allowed to show survive the trip: no ids, no review_status, no
type tags beyond the ironic flag. The score decides the running order and is then dropped,
so it reaches the reader only as a position in the register.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "aptronyms.csv"
OUT = ROOT / "site" / "src" / "data"

MIN_SCORE = 3
KEEP_STATUS = {"verified", "probable"}

# The register runs strongest first, so the reader meets Usain Bolt before Alfred Adler.
# Within a score band the better-sourced row wins, and after that the shortest connection
# line, which is the best available proxy for "needs no explaining".
STATUS_ORDER = {"verified": 0, "probable": 1}

# Sound records that the site declines to publish, because the joke lands on a rape conviction,
# an indecency arrest or a racist's chosen targets and stops being funny. They stay in the
# research data. Keyed by id, which merge.py keeps stable.
WITHHELD = {
    "apt-0315",  # Don Black, white supremacist
    "apt-0316",  # Don Popadick, indecent exposure defendant
    "apt-0483",  # Hastie Eugene Love, convicted rapist
}

# Any of these as a bare first path segment would be shadowed by a person's page.
RESERVED = {
    "about", "names", "name", "random", "fields", "field", "inaptronyms", "og", "api",
    "search", "index", "sitemap", "sitemap-index", "robots", "404", "assets", "_astro",
    "favicon", "feed", "rss",
}

FIELD_LABELS = {
    "sports": "Sports",
    "science": "Science",
    "medicine": "Medicine",
    "law": "Law",
    "arts": "Arts",
    "politics": "Politics",
    "weather": "Weather",
    "trades": "Trades",
    "religion": "Religion",
    "food": "Food and drink",
    "education": "Education",
    "business": "Business",
    "military": "Military",
    "transport": "Transport",
    "media": "Media",
    "crime": "Crime",
    "other": "Other",
}

# Publishers worth naming. Anything else falls back to its bare domain, which reads fine.
SOURCES = {
    "wikipedia.org": "Wikipedia",
    "baseball-reference.com": "Baseball Reference",
    "pro-football-reference.com": "Pro Football Reference",
    "basketball-reference.com": "Basketball Reference",
    "hockey-reference.com": "Hockey Reference",
    "sports-reference.com": "Sports Reference",
    "olympedia.org": "Olympedia",
    "npiregistry.cms.hhs.gov": "NPI Registry",
    "fjc.gov": "Federal Judicial Center",
    "bioguide.congress.gov": "Congressional Biographical Directory",
    "history.house.gov": "U.S. House of Representatives",
    "senate.gov": "U.S. Senate",
    "doi.org": "published paper",
    "orcid.org": "ORCID",
    "espncricinfo.com": "ESPNcricinfo",
    "afltables.com": "AFL Tables",
    "transfermarkt.com": "Transfermarkt",
    "theguardian.com": "The Guardian",
    "nytimes.com": "The New York Times",
    "washingtonpost.com": "The Washington Post",
    "bbc.com": "BBC",
    "bbc.co.uk": "BBC",
    "newscientist.com": "New Scientist",
    "slate.com": "Slate",
    "neatorama.com": "Neatorama",
    "legacy.com": "obituary",
    "findagrave.com": "Find a Grave",
    "imdb.com": "IMDb",
    "linkedin.com": "LinkedIn",
    "nps.gov": "National Park Service",
    "noaa.gov": "NOAA",
    "usgs.gov": "USGS",
}

# Hidden search words. Somebody typing "death" is looking for the undertakers, and no
# undertaker's record contains the word. Each tag is added when its pattern matches the
# record's text; the tags never appear on the page, they only widen what search finds.
TAGS = {
    "death": r"funeral|mortician|mortuar|undertaker|cemeter|coroner|\bgraves?\b|burial|embalm"
             r"|medical examiner|crematori|obituar",
    "horses": r"equestrian|eventing|jockey|\bcanters?\b|gallop|dressage|horse|\bstables?\b",
    "birds": r"ornitholog|\bbird|owl|stork|dove|finch|partridge|falcon|hawk|eagle|crane",
    "fish": r"fisher|fishing|angler|marine biolog|ichthyolog|trout|salmon|whale|shark",
    "beer": r"brewer|brewing|brewery|\bale\b|distill|hops",
    "wine": r"wine|vineyard|viticultur|enolog|sommelier",
    "space": r"astronaut|astronom|cosmonaut|space|planet|orbit|telescope",
    "music": r"musician|composer|organist|bassist|drummer|conduct|orchestra|choir|violin"
             r"|pianist|singer|band\b",
    "teeth": r"dentist|dental|orthodont|endodont|periodont|tooth",
    "police": r"police|sheriff|constab|detective|prison|patrol",
    "money": r"\bbank|treasur|\btax|account|financ|invest|econom",
    "trees": r"botan|forest|arborist|horticult|garden|timber|woodland",
}

# Where a note stops being about the person and starts being about the research.
NOTE_CUTS = ("Audit:", "Flagged automatically:", "Reviewer:", "Review:", "Rescored", "Downgraded")
NOTE_REJECT = re.compile(r"\b(rescor|downgrad|reject|review|audit|rubric|borderline)", re.I)


def slugify(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    return slug


def source_label(url: str) -> str:
    host = re.sub(r"^https?://", "", url).split("/")[0].lower()
    host = re.sub(r"^www\.", "", host)
    for domain, label in SOURCES.items():
        if host == domain or host.endswith("." + domain):
            return label
    return host


def clean_note(note: str) -> str:
    """Keep the part of a note that is about the person, drop the part about the review."""
    text = note
    for cut in NOTE_CUTS:
        text = text.split(cut)[0]
    text = text.strip().strip(";").strip()
    if not text or NOTE_REJECT.search(text):
        return ""
    if not text.endswith((".", "!", "?")):
        text += "."
    return text


def typographic(text: str) -> str:
    """Straight quotes look like a data dump. Curl them for display."""
    text = re.sub(r'"([^"]*)"', "\u201c\\1\u201d", text)
    text = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", text)
    return text.replace(" - ", " \u2013 ")


def year(value: str) -> int | None:
    return int(value) if value.lstrip("-").isdigit() else None


def life(row: dict[str, str]) -> str:
    """A dates line, but only where it earns its place: the dead and the historical."""
    born, died = year(row["birth_year"]), year(row["death_year"])

    def show(y: int) -> str:
        return f"{abs(y)} BC" if y < 0 else str(y)

    if born and died:
        return f"{show(born)}\u2013{show(died)}"
    if died:
        return f"died {show(died)}"
    if born and born < 1900:
        return f"born {show(born)}"
    return ""


def related_for(entry: dict, by_field: dict[str, list[dict]], everyone: list[dict]) -> list[str]:
    """Three neighbours from the same field, rotating so no two pages suggest the same trio."""
    pool = by_field[entry["field"]]
    if len(pool) > 3:
        i = pool.index(entry)
        return [pool[(i + n) % len(pool)]["slug"] for n in range(1, 4)]
    picks = [p["slug"] for p in pool if p is not entry]
    i = everyone.index(entry)
    for n in range(len(everyone)):
        if len(picks) == 3:
            break
        candidate = everyone[(i + n + 1) % len(everyone)]
        if candidate["score"] == 5 and candidate["slug"] not in picks and candidate is not entry:
            picks.append(candidate["slug"])
    return picks[:3]


def main() -> None:
    everything = list(csv.DictReader(MASTER.open(encoding="utf-8")))
    rows = [
        r for r in everything
        if r["review_status"] in KEEP_STATUS
        and int(r["aptronym_score"]) >= MIN_SCORE
        and r["id"] not in WITHHELD
    ]

    entries = []
    for row in rows:
        types = row["aptronym_type"].split("|")
        haystack = " ".join(
            row[c] for c in ("occupation", "field", "organization", "connection", "name_origin")
        )
        entries.append({
            "slug": slugify(row["full_name"]),
            "name": typographic(row["full_name"]),
            "occupation": typographic(row["occupation"]),
            "field": row["field"],
            "country": row["country"],
            "organization": typographic(row["organization"]),
            "life": life(row),
            "connection": typographic(row["connection"]),
            "origin": typographic(row["name_origin"]),
            "context": typographic(clean_note(row["notes"])),
            "source": row["person_source_url"],
            "sourceLabel": source_label(row["person_source_url"]),
            "nameSource": row["name_source_url"],
            "tags": " ".join(t for t, p in TAGS.items() if re.search(p, haystack, re.I)),
            "score": int(row["aptronym_score"]),
            "sourcing": STATUS_ORDER[row["review_status"]],
            # Only where the irony is the point. Plenty of rows carry it as a second reading,
            # and those belong in the main collection, not on the inaptronyms page.
            "ironic": types[0] == "ironic",
            "translation": "translation" in types,
        })

    problems = []
    dupes = [s for s, n in Counter(e["slug"] for e in entries).items() if n > 1]
    if dupes:
        problems.append(f"duplicate slugs: {', '.join(sorted(dupes))}")
    collisions = sorted({e["slug"] for e in entries} & RESERVED)
    if collisions:
        problems.append(f"slugs collide with site routes: {', '.join(collisions)}")
    for e in entries:
        if not e["slug"]:
            problems.append(f"unsluggable name: {e['name']!r}")
        if not e["source"]:
            problems.append(f"no source url: {e['name']}")
        if not e["occupation"] or not e["connection"]:
            problems.append(f"missing occupation or connection: {e['name']}")
    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        sys.exit(1)

    entries.sort(key=lambda e: (-e["score"], e["sourcing"], len(e["connection"]), e["name"]))
    by_field: dict[str, list[dict]] = {}
    for e in entries:
        by_field.setdefault(e["field"], []).append(e)
    for e in entries:
        e["related"] = related_for(e, by_field, entries)
    for i, e in enumerate(entries, start=1):
        # A permanent register number, assigned once here and carried through every sort and
        # filter on the site, so a slice of the register still shows where it sits in the whole.
        e["no"] = i
        # The score and its sourcing rank are editorial inputs, not public site data.
        del e["score"], e["sourcing"]

    counts = Counter(e["field"] for e in entries)
    births = [year(r["birth_year"]) for r in rows]
    births = [b for b in births if b is not None]
    meta = {
        "total": len(entries),
        "researched": len(everything),
        "rejected": sum(1 for r in everything if r["review_status"] == "rejected"),
        "fields": [
            {"slug": f, "label": FIELD_LABELS.get(f, f.title()), "count": n}
            for f, n in counts.most_common()
        ],
        "countries": len({e["country"] for e in entries if e["country"]}),
        "ironic": sum(1 for e in entries if e["ironic"]),
        "translation": sum(1 for e in entries if e["translation"]),
        "earliestBirth": min(births),
        "latestBirth": max(births),
        "span": max(births) - min(births),
    }

    OUT.mkdir(parents=True, exist_ok=True)
    for name, payload in (("entries.json", entries), ("meta.json", meta)):
        path = OUT / name
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}  {path.stat().st_size / 1024:.0f} KB")

    print(f"{meta['total']} entries, {len(meta['fields'])} fields, {meta['countries']} countries, "
          f"{meta['ironic']} ironic, earliest birth {meta['earliestBirth']}")


if __name__ == "__main__":
    main()
