# Canonical sources research log

Agent domain: canonical literature and press collections (all fields).  
Output: `canonical.csv` — **162 rows**, 0 validation errors after `merge.py --check`.

## Search queries (by strategy)

### Concept-first: aptronym / nominative determinism press
1. `Guardian Matthew Cantor urologist Adam Weiner aptronym 2024`
2. `Guardian Gary Nunn Reckless by name aptronym 2014`
3. `Guardian Hannah Jane Parkinson names inspire choices 2018`
4. `site:slate.com Timothy Noah Aptronym Watch Sue Yoo Charol Shakeshaft`
5. `site:slate.com Wayne Schmuck used-car distributor Noah`
6. `BBC Tom Colls When the name fits the job aptronym 2011`
7. `Seven Days Vermont Ken Picard Aptronyms 2014`
8. `Chicago Tribune field day aptly named workers 1995`
9. `NYT Tim Spiers Arsenal Wenger James Trafford nominative determinism 2025`
10. `Susie Dent nominative determinism saga.co.uk`
11. `Doctor Willard Bliss NYT 1881 How Dr. Bliss Got His Name`
12. `aptronym Herb Caen namephreak San Francisco Chronicle`
13. `Bob Levey Washington Post aptronym`
14. `Het Parool Nomen est omen aptronym Dutch`
15. `Paul Dickson What's in a Name aptronym list`
16. `Richard Lederer aptronym perfect fit name`
17. `Reuters Barbara Goldberg right name right time aptronym`
18. `NYT Clyde Haberman name means what it says aptronym`
19. `WSJ Dr Chopp Congressman Weiner aptronym`
20. `New Scientist Feedback nominative determinism archive`
21. `Aptonyms wiki Canadian Aptonym Centre`
22. `Gene Weingarten inaptonym Washington Post`
23. `nominative determinism Splatt Weedon urology`
24. `Limb Limb Limb Limb nominative determinism hospital medicine`
25. `Ernest Abel names career choices medicine Names journal`
26. `99 percent invisible outerbridge crossing aptronym`
27. `nomen est omen aptronym Dutch examples`
28. `Timothy Noah Matt Gobush Democrat Slate`
29. `Zoltan Ovary gynecologist immunologist aptronym correction`

### Name-first verification (Wikipedia list audit)
30. `Gary Bowser Nintendo hacker aptronym`
31. `Doug Bowser Nintendo president aptronym`
32. `Max Schreck German fright Nosferatu`
33. `Ciro Immobile Italian footballer gentle`
34. `Claudio Gentile defender gentle`
35. `Péter Magyar Hungarian prime minister`
36. `Nicolae Militaru Romanian defense minister`
37. `Eugène Terre'Blanche white land French`

## Sources examined

| Source | URL | New candidates | Notes |
| --- | --- | ---: | --- |
| Wikipedia Aptronym | en.wikipedia.org/wiki/Aptronym | 95 | Discovery; each verified/rejected individually |
| Wikipedia Nominative determinism | en.wikipedia.org/wiki/Nominative_determinism | 22 | Limb table, New Scientist origin, Caen/Levey refs |
| Guardian Cantor 2024 | theguardian.com/.../aptronym-job-normative-determinism | 12 | **Adam Weiner**, Aerial Powers, Dustin Partridge, David Loud |
| Guardian Nunn 2014 | theguardian.com/.../mind-your-language-nominative-determinism | 6 | Mark Reckless, Colin Bass, Charles Reade, Duncan Gay |
| Guardian Parkinson 2018 | theguardian.com/.../hannah-jane-parkinson-names-inspire-choices-life | 4 | Roger Kneebone, Margaret Court, forum examples |
| Slate Shakeshaft Yellow Pages | slate.com/.../charol-shakeshaft-topped.html | 35 | Core press collection; full category list extracted |
| Slate Sue Yoo / Schmuck / Gobush | slate.com (multiple) | 8 | Confirmed Advokat, Schmuck, Gobush |
| BBC Tom Colls 2011 | news.bbc.co.uk/today/.../9664697.stm | 10 | Fromage, Koolhaas, Crook, Vickers, Avery |
| Seven Days Picard 2014 | sevendaysvt.com/.../aptronyms-2014 | 8 | **Don Popadick**, Eric Hacker, Angel Means |
| Chicago Tribune 1995 | chicagotribune.com/.../a-field-day-with-aptly-named-workers | 6 | Reader letters; borderline unless cross-verified |
| NYT Athletic Spiers 2025 | nytimes.com/athletic/6524643/... | 4 | Wenger/Arsenal, Trafford, Wolfe/Wolves |
| 99% Invisible | 99percentinvisible.org/.../outerbridge-crossing | 3 | Outerbridge, Flowerdew, Cardinal Sin |
| Susie Dent Saga Jul-24 | pocketmags.com/.../word-to-the-wise | 2 | Burns-Cox, Pullum (borderline) |
| NYT TimesMachine 1881 | timesmachine.nytimes.com/.../98564242.pdf | 1 | **Doctor Willard Bliss** given name verified |

### Sources attempted but blocked or incomplete
- NYT Haberman 2011 (403) — examples recovered via Wikipedia refs and BBC
- WSJ Chopp/Weiner 2011 (401) — Chopp from Slate Yellow Pages
- Reuters Goldberg 2008 (401) — not independently fetched
- New Scientist Feedback archives — examples taken from ND Wikipedia prose
- Aptonyms wiki — treated as discovery only; not used as verification
- Limb et al. 2015 DOI (406) — surname patterns cited from ND Wikipedia table
- Abel 2010 — cited from ND bibliography; no individual names extracted
- Het Parool Nomen est omen — referenced in ND; no individual Dutch names verified this pass

## Rejected or flagged entries (kept in CSV)

| Name | review_status | Reason |
| --- | --- | --- |
| Gary Bowser | rejected | Aptronym depends on Super Mario villain, not occupation |
| Doug Bowser | rejected | Same; Nintendo president, not occupational fit |
| Neversink | rejected | Submerged town, not a person |
| Zoltan Ovary | rejected | Madden/Slate correction: immunologist, not gynecologist |
| Ciro Immobile | verified (ironic) | Translation sourced; inaptronym — agile forward |
| Claudio Gentile | verified (ironic) | Italian "gentile" = gentle; hard-man defender |
| Gary Bowser / Doug Bowser | rejected | Fictional-character name link |
| Chicago Tribune reader names (Yawn, Looney, Burns, etc.) | borderline | Dear Abby letters; person existence not independently confirmed |
| Peter Pullum / Burns-Cox | borderline | Susie Dent column only; no employer page fetched |
| Sina Movahed | borderline | Phonetic link plausible but strained |

## Strongest independent finds (not on Wikipedia aptronym list)

1. **Adam Weiner** — urologist interviewed in Guardian 2024; self-describes name as icebreaker
2. **Don Popadick** — Seven Days 2014 Aptronym of the Year; indecent exposure arrest
3. **Dustin Partridge** — NYC Bird Alliance ornithologist; building access aided by surname (Guardian 2024)
4. **Roger Kneebone** — Imperial College surgeon; Guardian 2018
5. **Wayne Schmuck** — Schmuck v. United States; Slate + Supreme Court record
6. **James Trafford / David Møller Wolfe** — club-name determinism (NYT Athletic 2025)

## Score distribution (162 rows)

| Score | Count |
| --- | ---: |
| 5 | 34 |
| 4 | 88 |
| 3 | 34 |
| 2 | 2 |
| 1 | 4 |

(rejected rows included at scores 1–2)

## Not reached / next pass

- Full Timothy Noah Slate Yellow Pages second page (climatology edition) — partial
- Reuters Goldberg 2008 full text
- NYT Haberman 2011 and WSJ 2011 original articles
- New Scientist Feedback archive systematic scrape (pre-2000 columns)
- Aptonyms wiki full category browse with per-person verification
- Het Parool "Nomen est omen" column Dutch examples (Hoekstra 2001 book as alternate)
- Paul Dickson *What's in a Name?* full chapter (book not fetched)
- Richard Lederer collections
- Herb Caen / Bob Levey original column dates beyond ND summary
- Abel 2010 physician initial-letter analysis — individual names
- Limb et al. 2015 — verify individual Dr Pain, Dr Gore, etc. from primary paper
- Ken Picard Seven Days 2012–2016 annual lists (partially searched, not fully harvested)

Most promising leads: Limb/Abel medical surname lists, Dickson/Lederer book indices, Aptonyms wiki with strict verification, and NYT/Reuters paywalled originals via archive access.
