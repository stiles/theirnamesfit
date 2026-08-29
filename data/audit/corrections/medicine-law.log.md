# Medicine-law audit log

**Auditor slice:** `data/audit/medicine-law.csv` (245 rows)  
**Date:** 2026-08-29  
**Output:** `data/audit/corrections/medicine-law.csv` (122 corrections)

## Coverage

| Metric | Count |
| --- | --- |
| Rows read (full slice) | 245 |
| Rows checked in depth | 245 |
| Source URLs fetched | 142 |
| FJC judge URLs verified | 38/38 correct person |
| Corrections written | 122 |

### Fetch strategy

1. **Priority pass (140 URLs):** all hedging-language connections, all NPI-only `person_source_url` values, all score 4–5 rows on common surnames (Stone, Hart, Payne, Skinner, Wright, etc.), all fatrazie.com sources, plus a 25-row random sample.
2. **Targeted pass (62 URLs):** canonical entries (Igor Judge, Kneebone, Chopp, Counsell, Limb family), Limb-discovery rows, judge profiles, and rows flagged in triage.

Many fetches returned 403/503 (BMJ, Green Bay Press Gazette, LinkedIn, health.usnews.com) or generic NPI search pages with no person name in HTML — treated as sourcing failures, not person non-existence.

## Verdict summary

| Verdict | Count |
| --- | --- |
| reject | 6 |
| rescore | 61 |
| fix | 55 |
| keep | 0 |

## Rejection reasons by pattern

### Fabricated or circular connections (6 rejects)

| ID | Name | Reason |
| --- | --- | --- |
| apt-0141 | Brett Welch | Admits "faintly echoes wretch/Welsh" — invented phonetic chain |
| apt-0300 | Derrick Tooth | Tooth/truth/testicle wordplay with no defensible link |
| apt-0341 | Edward Keelan | "Echoes Keaney" — names co-author, not etymology |
| apt-0546 | Jacques Boucher | Fatrazie lists butcher (boucher-charcutier), not dentist |
| apt-0664 | Joseph Galvin | BMJ paper co-author with zero name-to-work fit |
| apt-0977 | Richard Chopp | Duplicate of apt-0986; Slate is discovery not verification |

### Score inflation (61 rescored)

Dominant pattern: **common English surnames scored 4–5 on glancing semantic overlap.**

- **Hart × 5** (cardiologists): 4 → 2 (heart homophone, extremely common surname)
- **Stone × 4** (urologists): 4 → 3 (kidney stones link is real but surname is common)
- **Skinner × 5** (dermatologists): 4 → 2 (skin suggestion, common occupational surname)
- **Payne × 10**: 3 → 2 (pain link, very common surname)
- **Wright × 2** (judges): 3 → 2
- **Chase × 3**, **Marshall × 3**, **Lawson × 3**, **Burns × 4**, **Armstrong × 3**: virtue/occupational echoes demoted 1–2 points
- **Charles Bell**: 4 → 2 — Bell's palsy is an eponym *from* him, not an apt name fit

### Sourcing fixes (55 fix)

- **38 NPI-only rows** marked `verified` → `probable` (NPI homepage confirms licence lookup exists, not specialty)
- **5 fatrazie.com rows** → `borderline` (discovery registry only)
- **4 Wisconsin officer rows** → `probable`/`borderline` (single 2019 press survey, first names missing)
- **URL replacements:** Corona Rintawan (→ Wikipedia bio), James Counsell (→ Outer Temple), Richard Thomas Chopp (→ Healthline), Rob Banks (→ Nominative determinism pending force profile)

## Limb et al. (2015) aggregate handling

**21 rows** cite `doi.org/10.1308/147363515X14134529299420` in `discovery_source_url`.

| Treatment | Rows | Examples |
| --- | --- | --- |
| **Identified doctor + independent profile** | 12 | Christopher Limb (NHS), David Leslie Limb (Leeds NHS), Andrew Ballaro (GMC + website), Christopher K. Payne (clinic page) |
| **Identified + weak/ephemeral source** | 4 | Katrina Butcher (NHS jobs beta URL), Richard Limb (CV PDF), Margaret Boyle (NPI only) |
| **NPI name-first + Limb surname only** | 5 | David Gore, Brian Cox, Douglas Hart, Kristi Kinder, Sheila Boyle — demoted to `probable`/`borderline`; Limb attests surname frequency, not this individual's specialty |

**No row was found presenting a Limb-table surname (Waterfall, Pump, Horn) as a fabricated named individual** — the aggregate problem here manifests as NPI name-first searches paired with Limb discovery notes, not outright surname-only fabrication.

## NPI-only sourcing

| Metric | Count |
| --- | --- |
| Rows with `person_source_url` = NPI registry homepage | 51 |
| Of those marked `verified` before audit | 38 → all changed to `probable` |
| Already `probable` | 13 → score demotions where inflated |

NPI registry proves a licensed provider exists at lookup time; it does **not** establish occupation specialty from the URL alone. Agents treated NPI name-first search hits as full verification.

## FJC URL audit

All **38** federal judge URLs resolve to the correct named judge biography. No false-positive slug landing pages found in this slice (contrast with agent report from other slices).

## Five worst entries

1. **apt-0341 Edward Keelan** — connection literally cites another author's surname (Keaney) as the aptronym link; pure fabrication.
2. **apt-0300 Derrick Tooth** — stacks tooth/truth/testicle puns with no clean sentence; Mahler/Zimmer-tier invented reasoning.
3. **apt-0288 David Weedon** — "evokes weeds and unwanted growth" for a dermatopathologist; surname etymology invented (he is famous for a skin pathology textbook and a 1977 urology paper).
4. **apt-0546 Jacques Boucher** — listed as dentist; fatrazie source says boucher-charcutier (butcher); wrong person class entirely.
5. **apt-0141 Brett Welch** — "faintly echoes wretch and law's Welch/Welsh homophones" — hedging admission of zero real link.

**Honorable mention:** apt-0235 Cosmo Gerald Gordon (invented gavel/courtroom-authority link for Scottish surname Gordon) — rescore 2→1, not rejected because person and bench role are real.

## Systemic problems for other slices

1. **NPI/directory homepage as `person_source_url`** — generic registry URLs marked `verified`; apply `probable` minimum and require employer or clinic page.
2. **Aggregate paper surnames → named individuals** — Limb/Pelham/BMJ tables used as discovery then paired with first NPI hit; note when only aggregate surname is attested.
3. **Hedging language as connection** — 71 rows used evokes/suggests/resembles/echoes; treat as automatic score-cap at 2 and `borderline` review.
4. **Eponym reversal** — conditions named *after* doctors (Bell, Bright, Parkinson) scored as if the name caused the fit.
5. **Discovery URL as person_source_url** — fatrazie, Slate, Legal Cheek, Pocketmags, Wikipedia listicles used for verification; move to `discovery_source_url` only.
6. **`birth_name` default** — 97 rows tagged `birth_name` with `verified`; most should be `unknown` unless source states it.
7. **Score 4–5 padding on common surnames** — Hart, Stone, Payne, Skinner, Wright, Chase, Marshall, Burns need strict rubric in every slice.

## Rows deliberately not changed

Strong entries confirmed: Igor Judge, Michael T. Judge, William Wayne Justice, Roger Kneebone, Russell Brain, Hans/Werner Richter, Leopold Arzt, Sue Yoo, Anderson Nurse, Aaron Doctor, Angel Colon, Richard Thomas Chopp (after URL fix), Christopher Limb family, Smith & Wesson addiction-medicine pair, Florence Nightingale, Rob Banks (person real; source still weak).
