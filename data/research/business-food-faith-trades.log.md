# Research log: business-food-faith-trades

Agent domain: business/finance, food/drink, religion, trades/services, transport, education.

## Summary

- **Output:** `business-food-faith-trades.csv` — **110 rows**
- **Score distribution:** 5=29, 4=43, 3=30, 2=8
- **Review status:** verified=99, probable=3, borderline=8
- **Field spread:** religion 26, transport 25, business 19, trades 16, food 15, education 9

---

## Concept-first searches (25+)

| Query | Source / result |
|-------|-----------------|
| `aptronym chef baker butcher plumber funeral director pilot teacher` | Wikipedia aptronym list; Slate Shakeshaft article |
| `aptronym site:en.wikipedia.org banker OR chef OR priest OR pilot` | Des Britten, M. Moran Weston, Bronislav Yermak, Mikuláš Lexmann |
| `Bishop Bishop Thetford Church of England 2023` | Ian Bishop — already in master |
| `Slate charol shakeshaft topped` | Cashdollar, Billings, Schmuck, Greathouse, Boring — many in master |
| `Chicago Tribune 1995 field day aptly named workers` | Timeout; bancodeprofissionais mirrors only |
| `aptronym oven cleaner Gordon Ramsay` | Business Insider; ramsayscleanercookers.co.uk |
| `Andrew Waterhouse professor wine UC Davis` | wineserver.ucdavis.edu — ironic wine professor |
| `Tom Lehrer teacher mathematician Lehrer German` | Wikipedia + Wiktionary |
| `Les McBurney firefighter aptronym` | radiolab.org — already in master |
| `Patience Scales piano teacher aptronym` | afm6.org — also in arts-media staging |
| `Paul Schwinghammer contractor aptronym` | hallmarkhomes.com |
| `Philander Beadle divorce lawyer aptronym` | No verified person found (Herb Caen anecdote only) |
| `Furman Grip bank president aptronym Herb Caen` | Appears fabricated; rejected |
| `Forbes Beveridge Tito's Vodka` | 404 |
| `nominative determinism education aptonyms` | Fordham Institute: Romer, Wise, Loveless |
| `BBC train driver Surekha Yadav` | bbc.com |
| `Etihad Rail first Emirati train captain` | khaleejtimes.com, gulfnews.com |
| `Wes Souster tailor Souster means sew` | sousterandhicks.com |
| `Graves funeral home staff Norfolk` | gravesfuneralhomeinc.com — five Graves family directors |
| `nasa.gov astronaut Walker biography` | Shannon Walker, David M., Joseph A., Charles D. |
| `Joseph A. Walker NASA test pilot` | Wikipedia, news.va.gov |
| `Alper Gezeravci astronaut Turkish` | Wikipedia + Wiktionary |
| `Herbert S. Goldstein rabbi` | Wikipedia |
| `Des Britten chef priest Wellington` | Wikipedia |
| `Michelin chef surname Cook OR Baker` | Jeff Baker, Tom Cook, Luke Butcher, David Fisher |
| `insurance agent Hazard OR Fairbanks` | insuranceproviders.com, carmanfairbanksinsurance.com |
| `CPA bookkeeper Ledger` | ledgerlinq.com (Sarah Frampton) |
| `CASH Financial Bankee Kwan` | cash.com.hk |
| `Gerald Priest monsignor Texarkana` | texarkanagazette.com obituary |
| `Stephen Pope theology Boston College` | bc.edu |
| `John Hardon Jesuit` | Wikipedia |
| `They've heard the jokes Sin Priest Pope Ledger` | theledger.com 2003 |
| `icon.ink nominative determinism jobs` | Brad Slaughter, Joshua Butt (weak/tabloid) |
| `Bear Woods head football coach Wetumpka` | wetumpkasports.com |
| `Silas Masih Pepper Salt chef` | pepperandsalt.com.au |
| `catholic-hierarchy bishop Baker Fisher Grace Brewer Carpenter Porter Angel` | 15+ bishops |
| `Jimmy Doolittle aptronym` | Wikipedia — already in master |
| `Eric Moody BA flight 9 volcanic ash` | bbc.co.uk |
| `Al Haynes United 232 captain` | Wikipedia |

## Name-first searches

| Surname / pattern | Method | Yield |
|-----------------|--------|-------|
| Baker, Cook, Brewer, Butcher, Fisher | Michelin, Caterer, employer pages | Jeff Baker, Tom Cook, Luke Butcher, Sean Baker, Greg Brewer, Anthony Brewergray, Cathy Brewer, David Fisher, Peter Doughty-Cook |
| Priest, Pope, Grace, Angel, Cohen, Music | Catholic-Hierarchy, Wikipedia, bc.edu | 20+ clergy |
| Graves, Barber, Watt, Gill, Souster, Schwinghammer | Funeral home staff, trade sites, obits | 12 trades rows |
| Trippe, Train, Ride, Power, Speed, Walker, Yadav | Wikipedia, NASA, BBC, Gulf News | 25 transport rows |
| Cashdollar, Billings, Bond, Hazard, Frampton, Kwan | Hill Rag, Bates, insurance dirs, SEC-adjacent | 10 business rows |
| Learn, Head, Lehrer, Scales, Woods | School pages, sched.com, Wetumpka athletics | 9 education rows |
| Carpenter (bishop) | Catholic-Hierarchy | John Carpenter of Worcester |
| Porter (bishop) | Catholic-Hierarchy | George Porter, Thomas Porter |
| Ramsay (oven cleaner) | Business Insider | Gordon Ramsay UK cleaner |
| Waterhouse (wine) | UC Davis | Andrew Waterhouse ironic |
| Masih (Pepper & Salt) | Restaurant about page | Silas Masih |

## Sources examined (candidate yield)

| Source | New candidates |
|--------|----------------|
| Slate Shakeshaft 2005 | 0 new (most in master) |
| Wikipedia Aptronym | 15+ cross-checked |
| Catholic-Hierarchy.org | 18 bishops |
| NASA astronaut bios (PDF) | Gibson, Hathaway |
| gravesfuneralhomeinc.com | 5 Graves family |
| vanmag.com, berkeleyside.org, donaldrussell.com | 4 chefs/critic |
| Brookings, hillrag.com, insuranceproviders.com | 6 business |
| radiolab Hello My Name Is | McBurney already in master |
| Herb Caen / This Is True namephreaks | Patience Scales (arts-media), Furman Grip rejected |

## Rejected candidates

| Name | Reason |
|------|--------|
| Furman Grip | Herb Caen anecdote; no verified banker located |
| Philander Beadle | Caen/listicle only; no matching divorce lawyer found |
| Cynthia Houser | Slate-only real-estate agent; no authoritative current page |
| Dave Flood (plumber) | LinkedIn-only |
| Robert Coffin (undertaker) | Listicle confusion with poet Robert P. T. Coffin |
| Wake & Paine | Business name, not a person |
| Librarian Bookendorf, Cashier Ka Ching | Likely joke entries in listicles |
| Doug Bowser | Nintendo character pun, not occupational fit |
| Ian Bishop, Jaime Sin, Mark L. Prophet, etc. | Already in master |
| Les McBurney | Already in master (field: law) |
| Amy Winehouse, David W. Music, Patience Scales | Covered in arts-media staging |
| James Doolittle | Already in master |
| Thomas Graves III/IV | Dedupe key collides with Jr. (norm strips suffix); kept Jr., Jason, Mildred |
| Richard Grip | Kept at probable (LinkedIn only) |
| Joseph Bond | Kept at probable (MarketScreener) |
| LinkedIn-only teachers (Teachey, Tailor) | No authoritative employer page |

## Cross-staging duplicates (not errors in this file)

Merge check flags overlap with `arts-media.csv`, `politics-military.csv`, `science.csv`, `historical.csv`, `translation.csv` for figures also filed elsewhere (John Carpenter, Train, Morris, Trump, Waterhouse, translation-type clergy, etc.). Rows retained here for domain coverage; merge dedupe will pick best row.

## Gaps and promising next passes

1. **Plumbers:** No verified Flood/Leak/Pipe with non-LinkedIn source despite extensive directory searching.
2. **Electricians named Watt:** Ronald Lee Watt (plumber obit) found; electrician Watt entries were directory noise only.
3. **Muslim clergy:** Imam/Temple surname searches on Catholic-Hierarchy irrelevant; need Islamic directory pass.
4. **Rabbis beyond Cohen/Goldstein:** Herbert S. Goldstein added; more Cohen rabbis likely but dedupe carefully.
5. **Truckers/drivers:** Carter/Hauler name-first on FMCSA or state CDL rosters.
6. **Accountants:** Auditor/Tally surname with state CPA board lookup.
7. **Forbes Beveridge article:** Still 404; Tito's corporate page works for Beveridge (in master).
8. **Chicago Tribune 1995 field day:** Original URL timed out; secondary mirrors lack named examples.

## Strongest finds

1. **Peter Doughty-Cook** — legal name embedded in Peter Cooks Bread Ltd (score 5, wordplay).
2. **William Moody / Paul Bearer** — licensed mortician whose ring name puns pallbearer (score 5).
3. **Gordon Ramsay** (Durham oven cleaner) — ironic mirror of celebrity chef namesake (score 5).
