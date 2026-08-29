# Newspaper and periodical archive research log

Agent domain: digitised newspaper and periodical archives (all fields, all eras). Output: `archives.csv` (3 rows).

## Archive access summary

| Archive | Access method | Result |
| --- | --- | --- |
| Chronicling America (loc.gov) | Legacy JSON API (`chroniclingamerica.loc.gov/.../format=json`) | **404** — retired; redirects to loc.gov |
| Chronicling America (loc.gov) | `https://www.loc.gov/collections/chronicling-america/?q=…&dl=page&fo=json` | **Cloudflare 403** from automated clients |
| Chronicling America (archive.org) | `collection:chroniclingamerica AND aptly named` | **0 hits** in IA index |
| Trove (trove.nla.gov.au) | Web UI `"aptly named"` | **Anubis bot wall** — no programmatic access |
| Papers Past (paperspast.natlib.govt.nz) | Web UI | **Incapsula block** |
| Welsh Newspapers Online | Web UI + `/api/v1/search` | **Cloudflare challenge** |
| Internet Archive texts | Advanced search + OCR download | **Partial** — Weekley OCR open; Dickson/Lederer borrow-only (401) |
| HathiTrust | Catalog API + babel full-text | **Cloudflare block** on page fetch |
| Old Bailey Online | Website | **403** to bots; **DHI api-proto JSON works** |
| New Scientist Feedback | Article URLs on newscientist.com | **Works** for several columns (see below) |
| British History Online | Web pages | **Works** for medieval London records |

---

## Concept-first searches (newspaper phrase inventory)

Per brief, each string was attempted on Chronicling America (loc.gov), Trove, Papers Past, and Welsh Newspapers Online where reachable. Automated hit counts were **not obtained** for CA/Trove/Papers Past/Welsh due to bot protection; manual web search confirms these phrases appear widely in 19th-century “curious names” filler.

| # | Query string | Archive / endpoint | Hits | Candidates extracted |
| --- | --- | --- | --- | --- |
| 1 | `"aptly named"` | loc.gov CA `?q=aptly+named&dl=page&fo=json` | blocked | 0 |
| 2 | `"appropriately named"` | loc.gov CA | blocked | 0 |
| 3 | `"aptronym"` | loc.gov CA | blocked | 0 |
| 4 | `"aptonym"` | loc.gov CA | blocked | 0 |
| 5 | `"nominative determinism"` | loc.gov CA | blocked | 0 |
| 6 | `"nomen est omen"` | loc.gov CA | blocked | 0 |
| 7 | `"a singular coincidence" + name` | loc.gov CA | blocked | 0 |
| 8 | `"his name is suggestive"` | loc.gov CA | blocked | 0 |
| 9 | `"curious coincidence of name"` | loc.gov CA | blocked | 0 |
| 10 | `"name fits the man"` | loc.gov CA | blocked | 0 |
| 11 | `"true to his name"` | loc.gov CA | blocked | 0 |
| 12 | `"true to her name"` | loc.gov CA | blocked | 0 |
| 13 | `"living up to his name"` | loc.gov CA | blocked | 0 |
| 14 | `"well named" + occupation` | loc.gov CA | blocked | 0 |
| 15 | `"what's in a name" + occupation` | loc.gov CA | blocked | 0 |
| 16 | `"aptly named"` | Trove newspapers | blocked | 0 |
| 17 | `"aptly named"` | Papers Past | blocked | 0 |
| 18 | `"aptly named"` | Welsh Newspapers Online | blocked | 0 |
| 19 | `"Kentish Note Book" Carter Hosegood` | Internet Archive fulltext | 0 | 0 |
| 20 | `"Kentish Note Book"` | Internet Archive title search | 0 | 0 |
| 21 | `"What's in a name" Shooters Hill` | Web search | secondary only | 0 (individuals already rejected in master) |

---

## Reference-book extractions (Internet Archive / HathiTrust)

| # | Source | Query / method | Yield |
| --- | --- | --- | --- |
| 22 | Ernest Weekley, *The Romance of Names* (1914) | IA OCR `romanceofnames00week_0_djvu.txt` | Confirmed Roger Carpenter listed as **pepperer** beside Walter Ussher tanner (1336–52 London citizens) — surname/trade **contradiction** example, not added (Carpenter was a carpenter/grocer warden per BHO, not a pepperer trade) |
| 23 | Paul Dickson, *What's in a Name?* (1996) | IA id `whatsinnamerefle00dick` | **401 borrow-only** — OCR not retrievable |
| 24 | Richard Lederer, *Crazy English* | IA id `crazyenglishulti00lede` | **401 borrow-only** |
| 25 | Richard Lederer, *Amazing Words* | IA id `amazingwordsalph0000lede` | Not downloaded (same restriction expected) |
| 26 | Kentish Note Book vol. I (Howell 1891) | HathiTrust `ha102688999` | Catalog reachable; page OCR **Cloudflare blocked** — could not verify Shooters Hill note beyond Wikipedia/New Scientist secondary cites |

---

## New Scientist Feedback (origin literature)

Issue list from brief; articles fetched where URL resolved:

| Issue date | Issue # | URL | Named candidates | Rows added |
| --- | --- | --- | --- | --- |
| 5 Nov 1994 | 1950 | [Feedback](https://www.newscientist.com/article/1833707-feedback-243/) | Snowman, Trench, Splatt, Weedon, Hunt | 0 (all in master) |
| 17 Dec 1994 | 1956 | not fetched (URL not resolved this pass) | Cavonius coinage | 0 (Cavonius in master) |
| 18 Sep 1999 | — | cited in 2015 redux column | Hugh Seymour optometrist | 0 (in master) |
| 2015 redux | — | [Nominative determinism redux](https://www.newscientist.com/article/2017525-feedback-nominative-determinism-redux/) | Fogg, Hurtig, Pusey, Gunzinger, Lawless, Fridge, Frost/Winter | **2 added** (Gunzinger, Lawless); see rejections |

Other Feedback URLs attempted: `mg20425654-300`, `mg22390243-800`, `mg22425600-300`, `2100678` — **404 or timeout**.

---

## Old Bailey Online (DHI api-proto)

Base: `https://www.dhi.ac.uk/api-proto/view/oldbailey_record` and `_single?idkey=…`

| # | Query | Hits (1750–1913) | Extracted |
| --- | --- | --- | --- |
| 27 | `William Baker sugar baker` | (trial t17501205-75) | 0 — **William Baker already in master** |
| 28 | `James Smith Goldsmith` | 66,526 (noisy) | **1 verified** — James Smith, goldsmith witness, t17500228-1 |
| 29 | `defendantSurname:Butcher AND butcher` | 3,626 | 0 surname-match in sample |
| 30 | `defendantSurname:Baker AND baker` | 5,150 | 0 new beyond William Baker |
| 31 | `defendantSurname:Fisher AND fishmonger` | 497 | 0 |
| 32 | `defendantSurname:Mason AND mason` | 1,599 | 0 |
| 33 | `defendantSurname:Taylor AND tailor` | 2,887 | 0 |
| 34 | `defendantSurname:Miller AND miller` | 2,053 | 0 |
| 35 | `defendantSurname:Cooper AND cooper` | 4,030 | 0 |
| 36 | `Goldsmith` year 1750–1760, paginated | 30 trials | 1 unique `Smith, Goldsmith` |
| 37–46 | Batch: Slater, Potter, Carter, Cook, Barber, Smith/blacksmith, Wright, Collier, Mercer, Shepherd + matching trade | 400–4,000 each | 0 additional verified matches after full-text regex pass |

**Productivity note:** Old Bailey api-proto is the only newspaper-adjacent archive that yielded verifiable new rows this pass. Productive pattern: `{First} {Surname} , {trade}` in trial testimony with `year_gte=1750`, then `_single` fetch. Witnesses count if occupation is sworn.

---

## Candidates rejected (with reason)

| Candidate | Source | Reason |
| --- | --- | --- |
| Hosegood, Sales, Cuff, Carter carriers (Shooters Hill) | Kentish Note Book 1888 / Wikipedia | Nameless trade tallies; individuals not identified — already **rejected** in master |
| Peter Fogg, dispensing optician | New Scientist 2015 | Fogg/fog vision link is weak wordplay; best person source is LinkedIn/review directory → capped at probable; omitted |
| Kate Hurtig, Head of Pain | New Scientist / BioSpace | Surname Hurtig is German/Dutch for “quick”, not pain — **invented etymology** if read as “hurt” |
| Dr Pusey, Perth Cat Haven | New Scientist | **Unverified** — no Cat Haven affiliation found; Tony Pusey is at Terrestrial Ecosystems |
| Jeff Fridge, Inverness Crematorium | New Scientist | **Unverified** — current bereavement manager is John MacLean per Highland Council |
| Robin Frost / Hugo Winter, climate commentators | New Scientist | Already **rejected** in master (no person page) |
| Roger Carpenter, pepperer | Weekley 1914 | Weekley’s contradiction example; BHO suggests Carpenter was a **carpenter**, not pepperer — misleading |
| James Smith match mis-flag | t17500228-1 | Daniel Richley is defendant; Smith is **witness** — row kept with note |
| 19th-century “aptly named” paragraphs (generic) | CA/Trove (inaccessible) | Rennick 1982 ground rules: filler without independent identity → do not record |

---

## Rows written to `archives.csv`

| Name | Score | review_status | Person source |
| --- | --- | --- | --- |
| James Smith | 4 | verified | Old Bailey t17500228-1 |
| Mark Gunzinger | 4 | verified | Defense News op-ed |
| James Lawless | 4 | verified | Fianna Fáil TD biography |

Score distribution: 4×3. No 5s, no borderline/rejected rows in file.

---

## Gaps and next pass (highest yield)

1. **Chronicling America** — run phrase searches from a browser or LOC Jupyter notebooks (`libraryofcongress/data-exploration`) with session cookies; map hit counts per query string before extracting names.
2. **Old Bailey bulk export** — systematic `{trade}` + `defendantSurname:{Trade}` api-propo scan with `_single` fetch and regex for `, {trade} ,` indictment lines; expect more Baker/ Smith goldsmith-tier rows post-1750.
3. **Trove & Papers Past** — human-in-loop or authenticated API if available; Australian/NZ papers often print “appropriately named” notices with full names.
4. **Kentish Note Book original** — physical/HathiTrust volume at `ha102688999` once Cloudflare bypass available; may identify individual Carters/Hosegood if parish registers follow the note.
5. **New Scientist Feedback backlog** — 215 nominations mentioned in 2015 column; mine remaining issue URLs from `#1956`, `#2056`, `#2208`, `#2239`, `#2455`, `#2525`, `#2572`, `#2603`, `#2957`, `#2979`, `#3024`.
6. **Dickson/Lederer** — onsite IA borrow or library copy to extract named entries not already in master.

---

## Strongest finds this pass

1. **James Smith, goldsmith** — independent court record, direct trade/surname fit, not previously in database.
2. **Mark Gunzinger** — authoritative military publication + New Scientist discovery chain.
3. **James Lawless** — ironic barrister, verified via official party biography (distinct from John Lawless police officer in master).
