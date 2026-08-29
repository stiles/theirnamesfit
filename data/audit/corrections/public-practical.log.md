# Audit log: public-practical slice

**Auditor:** quality-gate subagent  
**Date:** 2026-08-29  
**Slice:** `data/audit/public-practical.csv` (230 rows)  
**Output:** `data/audit/corrections/public-practical.csv` (122 corrections)

## Coverage

| Metric | Count |
| --- | --- |
| Rows triaged (full slice read) | 230 |
| Rows with source URL fetched (HTTP HEAD/curl or WebFetch) | 78 |
| Corrections written | 122 |
| Reject | 117 |
| Rescore | 4 |
| Fix | 1 |

Fetched URLs spanned: Roman cognomina, bioguide.congress.gov search links (15), LinkedIn (1), Slate listicle sources, NASA/BBC/USDA PDFs, Dutch tradespeople (538/DBNL), and strong controls (Coward, Souster, Will Power, Major rank matches).

## Rejection reasons by pattern

### 1. Common-surname politics padding (48 rejections)
Score-2 rows kept “for coverage” per agent admission (Warren, Scott, Perino). Extended to all common English surnames at any score where the connection is generic: King, Marshall, Brooks, Warren (given + surname), Cloud, Sharp, Slaughter, etc. **Angus King**, **Elizabeth Warren**, **Rick/Tim Scott**, **Dana Perino**, **Peter/Steve King**, **Jim/Roger Marshall** exemplify the pattern.

### 2. Famous-person padding without name fit (16 rejections)
Rows whose notes admit “weak surname link; included as [hero pilot/astronaut].” **Sullenberger**, **Al Haynes**, **Eric Moody**, **Jeremy Hansen**, four **Walker** astronauts, **Marianne Merchez**. Train “captain” rows used job title as `name_element`, not surname.

### 3. Roman awarded cognomina / descriptive epithets (13 rejections)
Rejected where cognomen followed deed or described appearance:
- **Magnus** (after eastern victories), **Africanus** (Africa campaign), **Pius** (recall campaign), **Publicola** ×2 (popular support; etymology disputed), **Spinther** (actor resemblance), **Strabo** (cross-eyed), **Catus** (legal cleverness), **Cicero** (ancestor’s nose), **Sulla Felix** (fortune claim)
- **Caesar**, **Cincinnatus** — no pointed occupational fit
- **Æthelred the Unready** — folk-etymology epithet, not coincidental name

**Kept (no correction):** **Decimus Brutus** (ironic family name predates assassination; rescore 4→3), **Agricola** (inherited family cognomen; ironic farmer/general).

### 4. Invented / hedging connections (34 rejections)
Substring wordplay (**Baldwin**→wind), phonetic stretches (**McClellan**→clear, **Perino**→persona), “evokes/suggests/loosely/faintly/resembles” rows. USDA Forest Service oak-silviculture PDF author mining produced a cluster of **Dey**, **Brose**, **Stoleson**, **Clark**, **Stout**, **Baldwin** padding.

### 5. Sourcing failures (6 rejections)
- **Edward Major** — LinkedIn-only
- **Kevin Admiral** — person URL is generic aptronym Wikipedia page
- **Cuff**, **Hosegood** — anonymous Kentish Note Book entries, notes say individual not identified
- **Robert Odell Owens** — duplicate of Major Owens (apt-0775)

### 6. Rescores (4)
- **Am Rong** 4→3 (with URL/country fix): valid Slate/Wikipedia phonetic irony but needs journalistic context
- **Mike Hookem** 4→3: “suggests hooking” hedging
- **Roy Blunt** 3→2: post-hoc plain-speaking inference
- **Margaret Spellings** 4→3: legitimate but common surname

## Five worst entries

1. **apt-0497 Henry I. Baldwin** — “Baldwin contains *win*, faintly echoing *wind*” in forestry; pure invented substring analysis.
2. **apt-1182 Trina Brake** — self-described “near-miss”; Field Operations job title vs Brake surname; ironic wordplay admitted failure kept at 3.
3. **apt-0451 Pompey Magnus** — scored 5 while notes say cognomen “added after eastern victories”; aptronym logic inverted.
4. **apt-0342 Edward Major** — rank-match aptronym sourced only to LinkedIn; agent knew LinkedIn was unacceptable elsewhere.
5. **apt-0038 Am Rong** — wrong `person_source_url` (Slate Shakeshaft article), wrong country (United States vs Cambodia); irony is real but record was careless.

## Strong entries verified (unchanged)

Charles Coward (5 ironic), Will Power, Geoff/Wes Souster, Edwin Kist, Hennie de Haan, Herman Dijk, John Sergeant, Josh Major, Larry Speakes, Gordon Ramsay (oven cleaner), Paul Bearer/Moody, Simon Head, P. Head, Barney Frank, George Francis Train, George C. Marshall (Marshal Marshall joke documented).

## Systemic problems for other slices

1. **Score-2 as padding policy** — politics agent admitted borderline rows for press secretaries and common surnames; reject, don’t rescore.
2. **Bioguide search URLs** — 15 rows use `bioguide.congress.gov/search/bio/…` (often 403 to bots); replace with direct member URLs or Wikipedia.
3. **`birth_name` mass default** — dozens unchecked; wrestling (**Paul Bearer** correctly flagged `professional_name`) shows at least one ring-name row handled right while politicians lack verification.
4. **USDA PDF author mining** — weak homophone forestry padding; expect similar clusters in science/trades slices.
5. **Roman cognomina treated as birth-name coincidences** — awarded agnomina inflate scores; require deed-before-name check dataset-wide.
6. **Slate 2005 Shakeshaft listicle** — used as both `person_source_url` and discovery for many rows; acceptable for discovery only, not sole verification.
7. **Duplicate people** — Major Owens / Robert Odell Owens; check merged master for variant spellings.
