# Science-weather audit log

**Auditor slice:** `data/audit/science-weather.csv` (238 rows)  
**Date:** 2026-08-29

## Coverage

| Metric | Count |
| --- | --- |
| Rows read (full slice) | 238 |
| Rows checked in detail | 238 |
| Source URLs fetched (HTTP/WebFetch) | 68 |
| Corrections written | 54 |

### Fetched URLs (sample)

Verified by fetch: Amy Freeze, Dennis Bird, Hugh Fish, Andrew Fountain, Jodie Crane, Lord Kelvin, Frank Field, Storm Field, Michael Fish, John Fish, Carla Dove, Sara Blizzard, Casey Cloud, Walker Snowden, Diana Woei, Fisker surname page, Price Fishback, William Flood, Dae-Sik Moon faculty page, New Scientist Feedback (Winter/Frost), Ben Wettervogel (partial), Robert W. Field Wikipedia, Kentucky Mesonet about page, Heather Lake FOX URL (partial), Nicole Sprinkles NWS PDF (partial), cloud's weather about, weathergroup.com Walker Snowden, Barbara/David Snow Wikipedia (prior knowledge + row review).

Dead or broken on fetch: `weather.gov/gjt/staff` (404), Lancaster climate event archive for Winter/Frost (404), Rotman Price faculty bio (redirect/generic).

## Verdict counts

| Verdict | Count |
| --- | --- |
| reject | 13 |
| rescore | 36 |
| fix | 5 |
| keep | 0 |

## Rejection / demotion patterns

### 1. SI-unit and law eponym confusion (14 rows)

Agents scored Volta, Ampère, Ohm, Hertz, Newton, Joule, Watt, Kelvin, Faraday, Bessemer, Davy, Boyle, Hooke, Seaborg at 4–5 as if the name fit the work. In every case the unit, process, or law was named **after** the person. Rejected or scored 1.

### 2. Score inflation on common surnames (12 rows)

Economists Price (×4), Cash; geologists Bird; astronomers Moon (×3); physicists Field (×2). Agents treated "happens to share a field word" as score 5. Demoted to 2–3.

### 3. Invented / hedged connections (15 rows)

Rows using *evokes*, *suggests*, *faint*, *loosely*, *resembles* (39 total in slice; 15 corrected). Examples: Dennis Bird (geologist, not ornithologist), Hugh Fish (water chemist, not fish biologist), Diana Woei (folk Dutch etymology), Michael Fish (weather not marine life), Brooke Brighton (bright in Brighton).

### 4. Unverifiable persons (4 rows)

Hugo Winter, Robin Frost — only New Scientist Feedback one-liner; event URL dead. C. J. Berry, R. A. Sparkes — WIT Substack only. Rejected or borderline rejected.

### 5. Wrong specialty or wrong source (5 rows)

Allison Field sourced via father's Wikipedia; Storm Field via Nominative determinism wiki; Art Hawkins claimed hawks not waterfowl; Braeden Winters NWS page 404; Lorentz Fisker on surname disambiguation page.

### 6. Duplicate person (1 row)

William Schwind = Billy Schwind (apt-0120 / apt-1242), same Kentucky Mesonet URL.

## Five worst entries

1. **apt-0025 Alessandro Volta** — Scored 5 as aptronym; volt is named for him. Canonical backwards-eponym error.
2. **apt-0294 Dennis Bird** — Score 5 geologist "named bird"; Stanford profile is biogeochemistry, zero bird research.
3. **apt-0304 Diana Woei** — Dutch wind etymology invented; notes admit folk etymology; still scored 3 verified.
4. **apt-0520 Hugo Winter / apt-1017 Robin Frost** — Persons exist only as a New Scientist pun; no biographical source.
5. **apt-0565 James Marshall Shepherd** — "Shepherd evokes tending flocks on open grazing lands" is pure invention on a common surname.

## Genuinely strong entries confirmed (not corrected)

Amy Freeze (4), Ben Wettervogel (5), Casey Cloud (5), Carla Dove (5), Dallas Raines (5), Ken Weathers (5), Larry Sprinkle (5), Sara Blizzard (5), Storm Huntley (5), Tasha Snow (5), Tom Finch (5), Walker Snowden (5), Claire Loiseau (5), Price Fishback (4 after demotion).

## Systemic problems for other slices

1. **Backwards eponym blind spot** — Any row where occupation/discipline took the person's name (SI units, laws, processes, elements) was scored as `direct` 5. Audit all science slices for Watt, Newton, Ohm, Boyle, etc.
2. **`birth_name` default** — 227/238 rows marked `birth_name` without evidence; should be `unknown` unless sourced.
3. **Listicle-sourced padding** — New Scientist Feedback, Neatorama Name Number, WIT Substack, TreeHugger weather-name lists used as both discovery and verification.
4. **Scientific-authorship overclaim** — Surname match treated as paper-level fit (Fish, Bird, Snow) without checking whether the person actually works on that subject.
5. **Score 5 density** — 74/238 rows at 5; implausible under rubric. Expect heavy demotion in any research-agent slice.
6. **Hedging in `connection`** — 39 rows violate the "one plain sentence, no hedging" rule; strong audit smell.
7. **Rotting station staff URLs** — Broadcast meteorology entries need Wikipedia or archived bios; NWS `weather.gov/*/staff` pages 404 frequently.

## Validation

```
python3 -c "import csv;rows=list(csv.DictReader(open('data/audit/corrections/science-weather.csv')));ids={r['id'] for r in csv.DictReader(open('data/aptronyms.csv'))};print(len(rows),'corrections');print('bad ids:',[r['id'] for r in rows if r['id'] not in ids])"
```
