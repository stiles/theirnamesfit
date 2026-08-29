# Science / engineering / academia research log

Agent domain: science, engineering, academia (excluding medicine/veterinary). Target: 100+ verified staging rows.

## Sources mined

1. **Research brief** — `/Users/mstiles/github/aptronym/.cursor/docs/research-brief.md` (classification, CSV schema, sourcing rules)
2. **Master dedup** — `data/aptronyms.csv` (~506 rows); grep surnames before add
3. **Wikipedia** — [Nominative determinism](https://en.wikipedia.org/wiki/Nominative_determinism) bibliography and examples
4. **New Scientist Feedback** — origin issue 5 Nov 1994; follow-ups 1994–2015 including [Return of nominative determinism (2013)](https://www.newscientist.com/article/1978183-feedback-return-of-nominative-determinism/), [Feedback #239](https://www.newscientist.com/article/mg14419546-200-feedback/)
5. **Improbable Research** — [John Hoyland obituary](https://improbable.com/2014/11/18/sad-news-john-hoyland-father-of-nominative-determinism-is-gone/), [Aral Okay geologist](https://improbable.com/2011/06/19/okay-geologist/)
6. **Kevin Krajick / Neatorama** — [Name Number paper (2013)](https://www.neatorama.com/2013/03/19/The-Name-Number-for-Geology-and-for-Other-Professions/) — rich cross-field name list
7. **Jen Hunt origin** — The Psychologist 7(10), 1994, p.480 (via Wikipedia)
8. **Google Scholar / DOI** — author-subject verification (Loiseau avian malaria, Ion Ion electroanalytical, Skidmore cow-dung entomology, etc.)
9. **Faculty pages** — `.edu`, `.ac.uk` (Michigan ornithology, UCLA geomorphology, Dundee water science, Purdue CS, etc.)
10. **ORCID / university profiles** — Sean Cash, John Buschman, Scott Hatch, Gene Shearer

## Search queries run (25+)

| Query | Result |
| --- | --- |
| `nominative determinism scientist ornithologist` | Canon list; Wingfield, Hatch, Byrd |
| `Scott Hatch ornithologist USGS` | ORCID + Pacific Seabird Group award |
| `John Wingfield ornithologist UC Davis` | Faculty page; bird endocrinology |
| `Sumner Starrfield astronomer ASU` | ASU profile; stellar explosions |
| `Hugh Fish Thames water chemist` | Wikipedia; RSC water group chairman |
| `John Fish marine biologist Aberystwyth` | IBERS profile |
| `Gordon Cheeseman food chemistry RSC` | DOI dairy chapter; New Scientist cite |
| `Malcolm Bolton Cambridge reinforcement` | Cambridge geo directory |
| `Andrew Fountain glaciologist Portland State` | PDX faculty expert page |
| `Brian Atwater geologist Cascadia USGS` | Wikipedia; Science 1987 |
| `Wayne Gall entomologist Buffalo Museum` | NY Entomological Society bio |
| `Gene Shearer NIH immunologist` | Wikipedia; New Scientist Feedback |
| `Ken Drinkwater Bedford Institute Oceanography` | ESSAS profile |
| `Simon Grove rainforest James Cook entomologist` | Tasmanian Literary Awards bio |
| `Jerry Forest Franklin forest ecologist` | Wikipedia (middle name Forest) |
| `Vernon Byrd ornithologist Fish Wildlife` | DOI Condor/Condor papers |
| `Claire Loiseau PLOS ONE bird` | DOI 10.1371/journal.pone.0044729 |
| `Stephen Sparks volcanologist Bristol` | Wikipedia FRS |
| `Seulgi Moon UCLA geomorphologist` | ESS faculty page |
| `Price economist labor market` | Multiple verified Price economists |
| `Thomas Hacker Purdue computer security` | Polytechnic profile |
| `SI unit scientists Ampère Volta Ohm Watt` | Wikipedia namesakes |
| `Carl Jung Adler nominative determinism` | Wikipedia + Wiktionary translation |
| `Lawrence Casler nominative determinism 1975` | DOI Psych Reports |
| `Frances Fry NRPB radiation` | DOI radiological protection |
| `Iain Begg economist LSE` | LSE profile (New Scientist said Ian Begg Cambridge) |
| `Eddy Carmack oceanographer Arctic` | Scholar/DOI ocean circulation |
| `nominative determinism geology Stone Rock` | Byron/John/Mike Stone USGS/UW/Waterloo |

## Top finds (score 5)

1. **Claire Loiseau** — French *loiseau* = bird; PLOS ONE avian malaria paper is the citation
2. **Ion Ion** — surname literally *ion*; electroanalytical chemistry DOI
3. **Jerry Forest Franklin** — forename + surname both forest-related; father of new forestry
4. **Brian Atwater** — water in surname; Cascadia tsunami geologist
5. **Hugh Fish / John Fish** — fish surnames; water chemist + marine biologist pair from same New Scientist Feedback item

## Rows delivered

- **File:** `data/staging/science.csv`
- **Count:** 104 unique people (not in master)
- **Score distribution:** 46×5, 41×4, 15×3, 2×2
- **Review status:** 83 verified, 15 probable, 6 borderline
- **Validation:** `python3 scripts/merge.py --check` — no problems attributed to science.csv

## Exclusions / rejections

| Name | Reason |
| --- | --- |
| Bob Walk | Sports (MLB pitcher); wrong domain — also in master |
| William Tranquilli, Alex Hogg | Veterinary medicine — other agent's scope |
| Hugh Seymour, Peter Fogg | Optometry — medicine-adjacent |
| Simon Waters (Bristol hydrologist) | Could not verify current faculty page |
| Philip Glass (UIUC materials) | Profile URL did not resolve cleanly |
| Wendy Fullilove | Krajick 1989 cite could not be verified; removed from staging |
| Richard Lazarus "Case Against Death" | Likely different author than UC Berkeley stress psychologist — kept as borderline with note |
| Nobel laureates with score-2 non-fits | Deliberately omitted (Darwin, Curie, etc.) — padding per brief |
| Brice Pitt, Roy Phang | Psychiatry/dentistry — medicine agent |
| Splatt & Weedon | Already in master (medicine) |
| Mark Avery, Alan Heavens, David Bird, etc. | Already in master |

## Gaps / next leads

- **New Scientist issue-by-issue mining** — issues #1956, #2056, #2208, #2239, #2455, #2525, #2572, #2603, #2957, #2979, #3024 not fully scraped
- **Casler 1975 paper examples** — Finger, Grunt, Stern/Cope, Lively/Reckless, Mumpower need individual DOI verification
- **Foreign translation cases** — German/French/Scandinavian scientists beyond Jung/Adler/Loiseau
- **Paper-title genre** — systematic Scholar search: author surname = paper noun (e.g. more Anne Dyer–type matches)
- **Geology name-number** — Rockhold, Flint, Tremblay from Krajick list need verification
- **Jen Hunt identity** — 1994 Manchester author vs later Jennifer Hunt; kept as probable
- **Marc Abrahams Guardian column** (27 Mar 2006) — not fully mined
- **Improbable Research Annals** long-running feature archives

## Notes

- Forename aptronyms included where canon supports (Gene Shearer, Eddy Carmack, Forrest Hall) with notes
- SI-unit scientists scored as `direct` 5 — name became unit (Ampère, Volta, Ohm, Watt, Newton, Hertz, Kelvin)
- Nominative contradeterminism kept where documented (Andrew Waterhouse wine/water)
- LinkedIn used only for Steven Bookman where no better employer page found — flagged probable
