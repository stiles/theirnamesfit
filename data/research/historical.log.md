# Historical aptronym research log

Agent domain: historical figures (roughly pre-1920). Output: `historical.csv` (77 rows).

## Concept-first searches

| Query | Source / result | New candidates |
| --- | --- | --- |
| `aptronym historical figures nominative determinism` | Wikipedia aptronym; Ohry 2013 PDF | Physick, Leech, Nightingale, Arzt |
| `nominative determinism Kentish Note Book 1888` | Wikipedia nominative determinism | Hosegood, Sales, Cuff (borderline) |
| `Names Figure in Sports Careers 1912 Spokesman-Review` | Wikipedia aptronym cite; Newspapers.com blocked | Ten Million verified via Wikipedia |
| `Old Bailey baker surname Baker trial` | oldbaileyonline.org | William Baker (1750), William Wilkinson victim (1831) |
| `Philip Syng Physick father American surgery` | Wikipedia, Ohry PDF | Physick (score 5) |
| `Joseph Locke railway engineer lock` | Wikipedia | Joseph Locke (not judge James Locke in master) |
| `Christopher Wren architect bird name` | Excluded — in arts-media.csv | 0 |
| `Puritan virtue names Mayflower ironic` | Wikipedia, ANB refs | Cotton/Increase Mather, Mercy Otis Warren, Patience Wright |
| `Roman cognomina Cicero chickpea Plutarch` | Plutarch Life of Cicero (Loeb/Thayer) | Cicero; Scipio, Brutus, Magnus, Cincinnatus (Romans deduped to translation.csv) |
| `Æthelred Unready unræd etymology` | Wikipedia, Wiktionary | Æthelred the Unready |
| `George Berkeley bishop immaterialism` | Wikipedia | George Berkeley |
| `William Blackstone Commentaries cornerstone` | Wikipedia, Etymonline | William Blackstone |
| `George Jeffreys Hanging Judge Bloody Assizes` | Wikipedia | Jeffreys (epithet not surname pun) |
| `Chronicling America aptly named appropriate name` | loc.gov (search UI) | No verified individuals extracted this pass |
| `Trove Australia appropriate name occupation` | trove.nla.gov.au | Not pursued to individuals this pass |
| `Ernest Weekley Romance of Names occupational persistence` | Archive.org snippet | Informed Cooper, Baker dating logic |
| `Rennick Hogg Sisters odd names ground rules` | Names journal abstract | Applied to Kentish Note Book rows → borderline |
| `Royal Society fellows Bell Hunter Bright` | Wikipedia biographies | Bell, Hunter, Bright, Hodgkin, Parkinson |
| `Fielder Jones center fielder aptronym` | Wikipedia aptronym list | Fielder Jones |
| `Hooke's law Robert Hooke` | Wikipedia | Robert Hooke |
| `SI unit eponym Joule Faraday Gilbert` | Wikipedia | Joule, Faraday, Gilbert (Watt/Volta/Ohm in science.csv — skipped) |
| `William Painter crown cork inventor` | Wikipedia | William Painter |
| `Percival Pott disease fracture surgeon` | Wikipedia | Percival Pott |
| `Henry Bessemer steel process` | Wikipedia | Henry Bessemer |
| `Publius Valerius Publicola friend of the people` | Wikipedia | Publicola (distinct from Quintus Pedius in politics-military) |
| `Alexander Burns Wallace Rule of Nines` | Wikipedia nominative determinism | Wallace |
| `William Makepeace Thackeray virtue name` | Wikipedia | Thackeray |
| `Benjamin Rush physician rush hurry` | Wikipedia, Etymonline | Rush (probable) |

## Name-first / roster searches

| Surname probe | Directory / source | Result |
| --- | --- | --- |
| `Baker` + Old Bailey | oldbaileyonline.org | William Baker sugar baker 1750 |
| `Hunter` + surgery | ODNB/Wikipedia | John & William Hunter |
| `Physick` + surgeon | Wikipedia | Philip Syng Physick |
| `Train` + railroad | Wikipedia | Train — duplicate in business-food-faith-trades.csv, removed |
| `Locke` + engineer | Wikipedia | Joseph Locke kept |
| `Miller` + industrial era | Guild records (not retrieved) | No verified row this pass |
| `Gold` + goldsmith historical | DNB search (not retrieved) | Unfinished |
| `Printer` + printing trade historical | — | Unfinished |
| `Carter` + Kentish Note Book | Wikipedia cite only | Carriers not individually identified |
| `Glasscock` + baseball | Wikipedia / master | Removed — Jack Glasscock already in master |

## Sources examined

| Source | Yield |
| --- | --- |
| Wikipedia biographical articles | ~60 verified rows |
| Old Bailey Online (2 trials) | Baker, Wilkinson, Clark (borderline) |
| Ohry 2013 nominative determinism PDF | Physick, Leech, Beard, Armstrong, La Garde |
| Plutarch / Wiktionary (Roman cognomina) | Cicero, Scipio; others deduped to translation.csv |
| Kentish Note Book via Wikipedia | 3 borderline trade rows |
| Wikisource DNB 1885–1900 | Not mined this pass |
| biographi.ca / adb.anu.edu.au | Not mined this pass |
| Chronicling America / Trove / BNA | Discovery only; no rows added |
| Spokesman-Review 1912 article | Paywall/Cloudflare; Ten Million via secondary |

## Deliberate exclusions (duplicates)

Removed from `historical.csv` because already in master or other staging: Leopold Arzt, Ebenezer Emmons, Ambroise Paré, Selwyn Image, George Francis Train, Roman cognomina batch (Sulla, Caesar, Cincinnatus, Magnus, Brutus, Flaccus, Agricola, Catus, Pius, Strabo), Louis Anatole La Garde, John Glasscock (master: Jack Glasscock), plus master holds Wordsworth, Crapper, Brain, Bliss, Learned Hand, Lumière, Outerbridge, Snowman, Loving.

## Rejections / borderline kept

| Candidate | Reason |
| --- | --- |
| Kentish Note Book Hosegood/Sales/Cuff | Real trades cited but individuals unverified → borderline |
| John Clark (Old Bailey baker) | Occupation confirmed; Clark≠baker → borderline score 2 |
| Evangelista Torricelli | No name meaning link → borderline |
| Agassiz, Lyely, Huxley, Lewis & Clark, etc. | Real people; aptronym fit weak → borderline score 2 |
| Ivan the Terrible | Translated epithet — rejected per brief |
| Silence Dogood | Pseudonym/fictional persona — rejected |
| Victorian newspaper "curious names" paragraphs | Not confirmed in registers — rejected |

## Unfinished leads (next pass)

1. **Spokesman-Review 1912** — full name list from "Names Figure in Sports Careers" (microfilm or state library).
2. **Chronicling America** — `"aptly named"` / `"singular coincidence"` in pre-1920 papers; cross-check each in census/registers per Rennick.
3. **Dictionary of Canadian Biography / ADB** — concept searches for trade+surname persistence in colonial records.
4. **Guild & livery apprenticeship indexes** — Miller, Goldsmith, Brewer, Printer in 18th–19th c. London.
5. **Old Bailey bulk** — systematic `occupation:baker` + surname Baker post-1750.
6. **Puritan ironic cases** — Temperance running taverns, Silence as preacher (need primary parish record).
7. **Civil War officer rosters** — Gunner/Gunn, Battle, War, Colonel Rank.
8. **Appletons' Cyclopædia on Wikisource** — extract apt trade names with birth/death dates.

## Validation

```
python3 scripts/merge.py --check
```

No problems attributed to `historical.csv` after Kentish row fix and deduplication.
