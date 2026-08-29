# Arts-commerce audit log

**Auditor:** quality-gate subagent  
**Slice:** `data/audit/arts-commerce.csv` (249 rows)  
**Date:** 2026-08-29

## Coverage

| Metric | Count |
| --- | --- |
| Rows read (full slice) | 249 |
| Rows with hedging language flagged | 82 |
| Source URLs fetched or HEAD-checked | 68 |
| Corrections written | 123 |

### URL verification sample (68)

Fetched content or confirmed HTTP 2xx for person sources including: Gustav Mahler, Hans Zimmer, Sting, Alfred Hitchcock, John Carpenter (disambiguation), Gabe Pressman, Anthony Brewergray (Border Mail), Chris Rock, David Copperfield, Liniker (Wikipedia + Guardian), River Phoenix, Robert Capa, Yung Lean, Emily Wines, Anthony Hazard (InsuranceProviders), Francine Prose, St. John Fisher (Catholic-Hierarchy), Ringo Starr, plus 33 additional HEAD checks across the slice. Wikipedia rate-limited bulk curls; priority famous-name and wrong-person rows verified via direct fetch.

### Performer birth-name checks (score 4–5)

Checked all 15 performers at score 4–5 marked `birth_name`. Corrections: `apt-0658` → `professional_name`; `apt-0990` → `legal_name`; `apt-0998` → `pseudonym`. Demoted or rejected the rest (Mahler, Joshua Bell, Chris Rock, Amy Winehouse, etc.).

## Verdict summary

| Verdict | Count |
| --- | --- |
| reject | 99 |
| rescore | 23 |
| fix | 1 |
| **Total** | **123** |

`name_status` corrections: **3**

## Rejection patterns

### 1. Famous-name rationalisation (largest bucket: 78 rejects)

Agents attached unsourced etymologies to celebrities. Tell: connection sentences with *evokes*, *suggests*, *resembles*, *faintly*, *loosely*, *echoing*, *though*, or *sounds like*. Examples: Mahler (painter surname / composer), Zimmer (room / cinema), Glass (transparency / minimalism), Cameron (camera), Swift (speed).

### 2. Hedging on score 2–3 borderline rows (included above)

Many rows already marked `borderline` but left at score 2–3; rubric says score 1 or reject. Rejected rather than demoted when connection was invented.

### 3. Wrong person / corrupted merge (5 rejects)

- `apt-0624` John Carpenter — film director occupation merged with 15th-c. Bishop of Worcester (`death_year` 1476).
- `apt-0031` Alfred Hitchcock — notes reference ACPO spokesman confusion; connection is fabricated in any case.
- `apt-0410` Gary Oldman and Gary Numan — composite two-person list entry.
- `apt-1038` Sales — unidentifiable 1888 anecdote.
- `apt-0903` Patience Scales — person unverified.

### 4. Manufactured / chosen names scored as coincidence (8 rejects + rescores)

- `apt-1115` Sting — nickname from striped sweater (Wikipedia), not vocal attack.
- `apt-0750` Liniker — uncle named her after Gary Lineker (Guardian).
- `apt-0066` Anna Pavlova — dessert named after dancer, inverse causation.
- Stage names demoted: Bono, Houdini, Copperfield, Capa, Ringo Starr, Yung Lean, River Phoenix.

### 5. Religious given-name clichés (9 rejects)

Catholic bishops named Angel / Miguel Angel / Fisher “fishers of men” treated as score 4 aptronyms. Standard Hispanic given names and biblical wordplay, not surname coincidence.

### 6. Listicle padding without verification (4 rejects)

Robin Mahfood, Shelby Goldgrab, Rev. Paradise, Barnaby Smith — discovery from nominative-determinism compilations without authoritative person confirmation.

## Rescores (kept, score adjusted)

Notable demotions: Joshua Bell 4→2, Amy Winehouse 4→2, Johann Strauss II 2→1.  
Notable promotions: Tom Cook 4→5, Jeff Baker 4→5 (direct occupational surnames).

## Five worst entries

1. **`apt-0624` John Carpenter** — occupation says horror-film director; record describes a medieval bishop who died in 1476.
2. **`apt-1115` Sting** — connection invented; Wikipedia documents wasp nickname from striped sweater.
3. **`apt-0474` Hans Zimmer** — “scores the rooms of cinema” is nonsense etymology.
4. **`apt-0469` Gustav Mahler** — row admits painter etymology doesn’t fit composer; scored 4 anyway.
5. **`apt-0410` Gary Oldman and Gary Numan** — two-person novelty pairing, not an aptronym.

## Systemic problems (apply dataset-wide)

1. **Fame-padding pipeline** — research agents appear to have run Wikipedia aptronym lists and backfilled connection sentences for every famous surname in the slice. Apply hedging-language grep + fame filter to all slices before merge.

2. **`name_status` defaults to `birth_name`** — performers, magicians, and photographers with adopted names were not checked. Mandatory Wikipedia birth-name pass for any arts/media row.

3. **Row corruption from multi-source merges** — contradictory `notes` fields (Hitchcock, Carpenter) suggest dedupe/merge combined different people. Run occupation vs. source sanity check (`death_year`, org vs. occupation).

4. **Score inflation on translation type** — `translation` used to justify any foreign word remotely related to work; require `name_source_url` *and* occupational fit test, not thematic vibe.

5. **Composite entries** — ban pipe-delimited multi-person rows (`Gary Oldman; Numan`).

6. **Religious Angel/Mary/Grace given names** — treat as separate failure mode; given names in Catholic cultures are not aptronyms unless virtue-name cases with documented intent (Increase Mather tier, not Miguel Angel tier).

## Rows deliberately left alone (strong examples)

Gabe Pressman (5), Anthony Brewergray (5), David W. Music (5), Ferry Kok (5), Otto Koch (5), Francine Prose (5), Max Schreck (4), Javier Cámara (4), Benjamin Millepied (4), Frank Beard ironic (4), Jaime Sin inaptronym (5).
