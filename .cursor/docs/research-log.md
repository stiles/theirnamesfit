# Research log

How the aptronym database was built, what was searched, what was rejected and what is still
open. Per-domain detail lives in the individual logs in `data/research/*.log.md` (17 files)
and `data/audit/corrections/*.log.md` (6 files); this file is the overview and the record of
decisions that apply across domains.

Final state: 1,325 people, 691 reviewed as real and scoring 3 or better, 294 rejected on
review and retained with reasons.

## Method

Three research waves, then an audit, then mechanical integrity sweeps.

**Wave 1 — canonical sources and the richest occupations.** Five parallel agents: the
established literature and press collections; North American team sports; individual and
Olympic sports; medicine; law and crime. Output 508 rows.

**Wave 2 — remaining occupations, languages and eras.** Eight parallel agents: world team
sports; science and academia; politics and the military; weather and the natural world; arts
and media; business, food, religion and trades; non-English translation cases; historical
figures. Output 741 rows, 1,265 unique people after deduplication.

**Audit.** The dataset was split into five slices and each given to a reviewer with authority
to rescore, retype or reject, but not to add. They rejected 265 rows and corrected 202 more.
This was the most valuable stage of the project and is documented in its own section below.

**Wave 3 — the gaps, with a hardened brief.** The anti-padding rules the audit produced were
written into `.cursor/docs/research-brief.md`, and four agents were sent at the gaps the first
two waves reported: sports officials and historical rosters, newspaper archives, the languages
the translation pass missed, and twelve neglected professions. They were told explicitly that
there was no row target and that padding would get their file discarded. Output 58 rows — far
fewer, and much better. See "What the hardened brief did" below.

Every agent was told to work in two directions:

- **Concept-first:** search `aptronym`, `aptonym`, `nominative determinism`, `nomen est omen`,
  `namephreak`, `perfect name for the job` and local-language equivalents, plus the domain.
- **Name-first:** invent a surname that would be pointed for a role, then search a roster,
  register, court listing, faculty page or journal index to find out whether such a person
  actually exists. This produced most of the material that is not already on published lists.

## Yield by research file

A person is credited to the first file that contributed them, in merge order, so the rows column
measures new people rather than raw output — several agents independently found the same well
known names. `rej` is how many were later rejected on audit and `avg` is the mean aptronym score
of the survivors.

| file | rows | kept | rej | rej% | avg |
| --- | ---: | ---: | ---: | ---: | ---: |
| canonical.csv | 162 | 137 | 25 | 15% | 3.90 |
| arts-media.csv | 121 | 45 | 76 | 63% | 3.31 |
| science.csv | 104 | 90 | 14 | 13% | 3.78 |
| weather-nature.csv | 104 | 94 | 10 | 10% | 3.19 |
| business-food-faith-trades.csv | 102 | 65 | 37 | 36% | 4.11 |
| politics-military.csv | 94 | 38 | 56 | 60% | 3.79 |
| sports-world.csv | 92 | 78 | 14 | 15% | 3.31 |
| sports-northamerica.csv | 90 | 86 | 4 | 4% | 3.12 |
| medicine.csv | 89 | 86 | 3 | 3% | 3.09 |
| law-crime.csv | 83 | 78 | 5 | 6% | 3.29 |
| sports-individual.csv | 82 | 75 | 7 | 9% | 3.35 |
| historical.csv | 77 | 60 | 17 | 22% | 3.08 |
| translation.csv | 65 | 54 | 11 | 17% | 4.09 |
| sports-gaps.csv | 26 | 26 | 0 | 0% | 4.23 |
| professions-gaps.csv | 15 | 15 | 0 | 0% | 4.73 |
| translation-gaps.csv | 14 | 14 | 0 | 0% | 3.71 |
| archives.csv | 3 | 3 | 0 | 0% | 4.00 |
| restored.csv | 1 | 1 | 0 | 0% | 3.00 |

The translation agent shows the largest gap between output and credit: it delivered 138 rows but
only 65 people no earlier file had, because the canonical and science sweeps had already found
the famous non-English cases.

The pattern is stark. Sports, medicine and law rejected at 3 to 9 per cent, because their
sources are exhaustive public databases — Baseball Reference, the Federal Judicial Center,
Olympedia — where a claim is either in the register or it is not. Arts and politics rejected at
63 and 60 per cent, because they have no equivalent register and an agent under quota pressure
falls back on famous names plus invented reasoning.

## Sources that produced the most

Counted from `person_source_url` and `discovery_source_url` in the finished file.

| source | rows | what it gave |
| --- | ---: | --- |
| Wikipedia | 632 | the aptronym and nominative determinism articles seeded the canonical set, and their reference lists led to most of the press coverage |
| Olympedia | 52 | historical Olympians are deep, well documented and almost entirely unmined by existing lists, and its editors sometimes remark on apt names themselves |
| Baseball Reference and the other Sports Reference sites | 92 | across baseball, football, basketball and hockey; the best name-first search surface in existence |
| Federal Judicial Center biographical directory | 38 | every US federal judge ever, searchable and authoritative |
| Slate, mostly Timothy Noah's "Aptronym Watch" | 37 | the most productive single press collection |
| catholic-hierarchy.org | 15 | a complete searchable database of bishops |
| Limb, Limb, Limb & Limb (2015), *Bulletin of the RCS* | 15 | the surname-by-specialty study that anchors the medical domain, though see the caveat below |
| NPI registry lookups | 52 | proves a licence exists, not a specialty; all now capped at `probable` |
| New Scientist "Feedback" | — | the origin literature; partially accessible, and the single biggest remaining gap |
| Old Bailey Online | — | 197,000 trials, searchable; barely scratched |

## The audit

Five reviewers, one per slice, each told that padding was expected and that they were the
quality gate rather than a contributor. Verdicts: 265 reject, 136 rescore, 66 fix.

Rejections fell into recurring patterns, and these are worth naming because they are what an
enthusiastic collector gets wrong:

1. **Invented etymology, 90-odd rows.** A foreign or obscure word attached to a person by
   vibe. The clearest examples: "Zimmer is German for room, and he scores the rooms of cinema"
   (Hans Zimmer); "Fellini suggests feline grace"; "Groening resembles groningen or mourning in
   Dutch"; "Mahler derives from Maler, the German word for painter, though he composed
   symphonies" — a row whose own sentence concedes the name does not fit the work.
2. **Reasoning backwards from fame.** Agents ran celebrity aptronym listicles and wrote a
   rationalisation for each name. Mozart, Dalí, Monet, Manet, Rembrandt, Morricone, Miyazaki,
   Strauss, Sting, Bono and Ringo Starr were all rejected on this ground. Sting was the
   sharpest case: the row claimed the name described his "sharp vocal attack", when his
   nickname came from a black-and-yellow striped sweater.
3. **Backwards eponyms.** If a unit, law, disease or process is named *after* the person, the
   name did not fit the work — the work took the name. An entire cluster was rejected: Newton,
   Joule, Watt, Ohm, Hertz, Ampère, Kelvin, Faraday, Boyle, Hooke, Bessemer, Davy, Seaborg,
   Parkinson, Hodgkin, Volta. The same logic killed 13 Roman cognomina and epithets awarded
   for a deed — Pompey *Magnus* earned that name by conquest — while Agricola and Decimus
   Brutus survived because those were family names predating the achievement.
4. **Biography substituted for etymology.** Eight sports rows pasted a player's statistics onto
   a surname with no lexical link: a striker named Carroll who scored headers is not an
   aptronym.
5. **Padding by admission.** The politics agent stated it had included score-2 rows "as
   borderline padding for press-secretary and common-surname coverage". Those were rejected
   rather than rescored: a politician with an unremarkable common surname is not an aptronym at
   any score.
6. **Common surname plus generic word.** Field, Bell, Ball, Stone, Price, Marshall, Warren,
   Wright and Ward are among the commonest surnames in English and were repeatedly inflated to
   4 or 5.

The audits also found things worth keeping that were scored too low, most notably Charles
Coward, who escaped captivity repeatedly and smuggled prisoners out of Auschwitz — a textbook
5 for an ironic entry.

### Sourcing problems the audit surfaced

- **51 medical rows rest on an NPI registry lookup**, which proves a licence number exists but
  not that the named person practises that specialty. Most had been marked `verified`. They are
  now capped at `probable`, as are rows sourced from consumer physician directories such as
  US News Health, Healthgrades and Vitals, where the specialty is self-reported. 68 rows in
  total sit on a source the sweep classes as weak, and none of them is `verified`.
- **15 rows cite Limb et al. (2015).** That paper counted surnames on the GMC register by
  specialty and listed surnames — Waterfall, Pump, Horn, Hickey — *without naming individuals*.
  No row was found to have fabricated a person outright, but five paired a Limb aggregate
  surname with a separate name-first registry hit. Rows that rest on the aggregate alone are
  `borderline` with a note saying only the surname is attested.
- **All 38 Federal Judicial Center URLs were checked individually** after one agent warned that
  probing FJC URL slugs produced false-positive landing pages. All 38 resolved to the right
  judge.

## Mechanical integrity sweeps

Three defects were reported independently by four of the five reviewers, which made them
pattern-detectable and worth handling in one reproducible pass (`scripts/integrity.py`) rather
than row by row:

- **1,087 rows had `name_status` = `birth_name` set by default, unchecked.** All except those a
  reviewer had explicitly verified were reset to `unknown`. A later Wikipedia pass re-established
  552 of them from article leads; the 707 still `unknown` are genuinely unchecked.
- **166 rows had hedging language in `connection`** — evokes, suggests, resembles, faintly,
  loosely, echoes — and are now capped at `borderline` with a note. The word choice is a
  reliable tell: if the sentence needs "faintly" to work, the aptronym does not.
- **Weak person sources are capped at `probable`**: licence registries, LinkedIn, surname-meaning
  sites, listicles, social posts, search-results pages, and Wiktionary used to verify a person
  rather than a word.

Two housekeeping sweeps run in the same pass. Country names were normalised (`US`, `USA`, `GB`,
`Great Britain` and so on), which cut the country count from 82 to 76 without losing any real
distinction; England, Scotland, Wales and Northern Ireland were deliberately kept separate from
the United Kingdom, because they compete separately in most sports and much of this data is
sporting. Mobile Wikipedia hosts (`en.m.wikipedia.org`) were rewritten to the canonical host,
since they defeat both deduplication and the enrichment pass's grouping by host.

## Automated verification

**Every source URL was fetched** (`scripts/check_urls.py`, results in `data/url_check.csv`).
Wikipedia links are resolved through the API rather than fetched, so an article that does not
exist is reported as missing instead of as a live page — a soft-404 that ordinary link checking
passes without comment.

Final state of 2,184 references across 1,556 unique URLs:

| | |
| --- | ---: |
| live | 1,930 |
| bot-walled or rate-limited | 244 |
| timed out | 8 |
| **dead** | **2** |

Both dead links are on rejected rows and are kept as evidence. Nothing that survived review
cites a page that returns 404.

The bot-walled group is not a data problem but is worth naming, because it constrains what can
be re-verified later: Olympedia and Baseball Reference return 403 or 429 to any automated
client, and LinkedIn returns its custom 999. Those rows were confirmed by hand when written and
cannot be rechecked by machine.

Getting to that state took two rounds of repair.

**Round one** found seven Wikipedia links to non-existent articles and nine dead institutional
pages. All sixteen were researched by hand: fifteen were replaced with working URLs and one
person (a claimed Bristol chemist named Frost) could not be verified at all and was rejected.
The Wikipedia failures were instructive — mostly a plausible-looking disambiguation suffix that
does not exist, such as `Joshua_Bell_(violinist)` for a man whose article is simply
`Joshua Bell`, or `Michael_Lord_(politician)` for a man whose article is under his peerage
title. This is what an agent does when it knows a person exists and guesses the URL.

**Round two** came after the checker itself was fixed. Its Wikipedia batches had been recording
a rate-limited request as fifty missing articles, which buried the real failures under 524 false
ones; batches now retry with backoff and fall back to one title at a time. It also could not
send non-ASCII URLs at all, which turned out to be hiding two live and genuinely useful
citations, the Hungarian *cápa* (shark, for Robert Capa) and the Persian آمین. With those fixed,
twelve real problems surfaced and each was resolved:

- **Steve Slater**, supposedly a Great Britain rugby league winger born in 1954, was fabricated.
  None of the twenty Slaters in the Rugby League Project's complete player database is a Steve,
  the cited article does not exist, and Bradford Bulls did not carry that name until 1996.
  Rejected.
- **Philander Rodman** is real and better documented than the row claimed. He is Philander
  Rodman Jr., a US Air Force serviceman and later a restaurateur in Angeles City, father of
  Dennis Rodman, who acknowledged fathering 29 children by 16 mothers and died in 2020. Now
  cited to ESPN's obituary. Being a junior, the forename was inherited, which is what makes it
  an aptronym rather than a choice.
- **Storm Dunlop** (1942–2025) had no Wikipedia article but a stronger source than one: the
  Royal Meteorological Society's obituary, which also establishes that he was a fellow of both
  the Royal Meteorological and Royal Astronomical Societies and president of the British
  Astronomical Association.
- **Zoltan Ovary**, kept as a rejected row because the widely repeated claim that he was a
  gynaecologist is false, now cites the NYU medical archives, which give his dates and confirm
  he was an immunologist who discovered the passive cutaneous anaphylaxis reaction.
- **Raymond Baker**, the Surrey bowler behind the butcher-and-baker quip, was filed under the
  wrong birth year and the wrong article title; the correct article also shows he was a
  medium-pacer rather than a fast bowler.
- **Four Wiktionary etymology links pointed at entries that do not exist**, because an agent
  had assumed the surname would have its own page. Each was repointed at the word that actually
  carries the meaning: `oiseau` rather than `loiseau`, capitalised `Publicola` rather than
  lowercase. Two of these repairs changed the finding rather than just the link:
  - **Beekman** has no Wiktionary entry, and the Dutch root is *beek*, a brook. So Matt Beekman
    the commercial beekeeper is a purely English homophone — bee-man — and the row now says so
    instead of implying a Dutch etymology that does not exist.
  - **Cherrier** does have a French Wiktionary entry, and it gives an Occitan origin unrelated
    to cherries, which independently confirms a rejection that had rested only on an agent's
    assertion.
- **Six live people had sources that had rotted**, and all six turned out to have better ones:
  Bobby George, Erik Fish, Olympia Aldersey and Gregory Price all have Wikipedia articles;
  Kevin Farmer is named as division director on a standing NRCS engineering page rather than the
  staff directory that rotates; Seulgi Moon is in the UCLA department directory.
- **Edgar Kaal**, a Dutch hairdresser whose surname means bald, was downgraded from `verified`
  to `borderline`. His salon's website has gone, and what remains documents the business rather
  than the man.

One of those repairs corrected an auditor rather than a researcher. The audit had downgraded
Seulgi Moon on the grounds that she studies hillslopes and not the Moon; her publication list
includes work on ice stability in the lunar south polar region, so the score went back up to 3
while staying `borderline`, because Moon is a common Korean surname and the coincidence is
partial.

### The defect the URL check uncovered

Three Baseball Reference links turned out to be guessed player ids that returned 404 — visible
only once the checker stopped being throttled, because a bot wall answering 403 looks the same
whether the page exists or not. Cool Papa Bell, Oil Can Boyd and Jim Bottomley were repointed at
Wikipedia, which also corrected Boyd's birth year.

Reading those three rows properly exposed a whole class of error the five-slice audit had missed,
because it is invisible unless you read the `connection` sentence as a causal claim: **a nickname
awarded for the very trait the row treats as a coincidence.** Twenty-eight non-rejected rows
mentioned a nickname, and seventeen of them were wrong in this way.

Frank "Home Run" Baker was the starkest, sitting at a score of 5: he was called Home Run Baker
because of the home runs he hit in the 1911 World Series. Cy Young's nickname is short for
Cyclone, awarded after a tryout in which his fastball wrecked a fence. "Mule" Suttles was named
for his hitting power, "Swish" for shooting — twice, in two different sports. Catfish Hunter's
nickname was invented for him wholesale by Charlie Finley, publicity backstory included. Satchel
Paige carried satchels as a railway porter as a boy, which describes an earlier job and says
nothing about pitching. Two MMA fighters had simply chosen "Pain" as a ring name.

Twelve rows were rejected on that basis, and five more downgraded where the aptness had been
manufactured rather than merely misread: two Denver weather presenters, "Stormy" Rottman and
"Sunny" Roseman, were branded by the same station specifically to pair with each other, which is
the Faith Popcorn problem in broadcast form.

The same read caught one unrelated case of famous-name rationalising that had survived the audit.
Louis Armstrong's row read his surname as "strong arm" and called it apt for a trumpeter, an
instrument played with breath and lips.

The general rule, now in the brief: **if the name was given because of the thing, it is not an
aptronym.** It is the same error as the eponym cluster the audit rejected — Newton, Watt, Ohm —
but harder to see, because a nickname sounds like a name in a way that a unit of measurement
does not.

One more row failed a rule nobody had thought to check mechanically. An entry reading simply
**Plate**, an MLB umpire, sat at `verified` with a score of 5. Retrosheet's umpire register does
contain it — `platu901  Plate  Plate`, one game worked on 17 July 1946 — but with no first name
and no dates, which means the surname is attested and the person is not identifiable. It is now
`borderline` at 3, the same treatment given to the Limb surname-only cases, rather than rejected,
because the register entry is real. The four other single-token names in the file are mononyms of
genuinely identifiable people — Galen, Avicenna, Paracelsus, Bono — and all four were already
scored 2 or 3 with their adopted names flagged.

Fixing that exposed a structural flaw in the pipeline: `audit.py apply` ran before the third-wave
merge, so no correction could ever target a third-wave row, and one keyed to `apt-1310` was
silently skipped as an unknown id. The rebuild now applies corrections twice, before and after
that merge. The first pass still defines the id space the auditors reviewed; the second reaches
the newer rows. The step is idempotent, and a full rebuild run twice produces byte-identical
output.

**Wikipedia lead paragraphs were parsed** for every one of the 615 cited articles across eight
language editions (`scripts/enrich_wikipedia.py`), filling 42 birth years and 30 death years,
establishing 552 `name_status` values, and detecting ten cases where the article gives a birth
name different from the one recorded. Two of those undercut well-known examples and are the
single most useful thing the automated passes found:

- **Faith Popcorn**, the food-industry trend forecaster, was born Faith Plotkin. She chose the
  surname, so the aptronym is manufactured rather than coincidental. Rescored from 4 to 2.
- **Frank Field**, one of American television's first weather presenters, was born Franklyn
  Feld. "Field" is an anglicisation of the German for field, which makes this a translation
  case, not a coincidence — and it also reaches his children Storm and Allison Field, whose apt
  surname descends from their father's name change.

Also flagged: Marilyn vos Savant (born Marilyn Mach; vos Savant is her mother's family name),
Vijay Merchant, Stan Lee, Woody Allen, Fred Astaire, Robert Capa, Dorothea Lange and Arianna
Huffington.

## Candidates rejected before they became rows

Recorded here because they are the kind of thing a future pass should not spend time on again.
Fuller lists are in the per-domain logs.

- **Nameless anecdotes.** "A butcher named Bacon in Leeds", the Kentish Note Book's 1888
  tradesmen ("an auctioneer named Sales", "a draper named Cuff"), Herb Caen's reader
  submissions. The trades are cited but no individual is identifiable, which fails R. M.
  Rennick's ground rules for odd-name collectors — the paper that exists precisely because
  Victorian newspapers printed invented curious-name filler.
- **Cardinal Rapsong**, the Vatican's supposed spokesman on rock music: a New Scientist
  anecdote with no verifiable person behind it.
- **Zoltan Ovary**, widely listed as a gynaecologist. Slate corrected this: he was an
  immunologist. Kept as a `rejected` row so the correction is on the record.
- **Gary and Doug Bowser**, whose names echo a Super Mario villain rather than an occupation.
- **Neversink, New York**, a town that flooded: a place, not a person.
- **Surname-only entries** where a productive-looking name could not be tied to an individual:
  Kicker, Guard, Tackle, Catcher, Puck and Ice returned no real players in any roster searched.
- **Fabricated people.** One candidate ("Furman Grip") could not be verified as existing at all.
- **Non-people.** Businesses and shop signs, including the butcher's shop "C. van der Ham"
  that illustrates the Wikipedia article.

## What the hardened brief did

The clearest experimental result in the project. Waves 1 and 2 were given row targets and
rejected at 22 per cent overall. Wave 3 was given the anti-padding rules, no row target, and an
explicit statement that a documented dead end was a valid result. It returned 58 rows, none of
which were rejected, with the two highest mean scores of any file (4.73 and 4.23).

Agents also began reporting negative results honestly, which is worth as much as the rows. The
archives agent established that Chronicling America's legacy JSON API is retired and that
Trove, Papers Past, Welsh Newspapers Online and HathiTrust page views all sit behind bot walls
— then delivered three solid rows and a map of what does work. The professions agent reported
intelligence, long-haul transport and the search for a plumber named Flood as barren.

The lesson for any future pass: a row target causes padding, and padding costs more to remove
than the rows are worth.

## Not yet searched thoroughly

Ordered by expected yield.

1. **New Scientist "Feedback", 1994 to date.** The origin literature for the whole concept and
   still only partially read. Twelve specific issues are identified in the brief. Most are
   paywalled; the Internet Archive has some. Every named researcher in those columns is a
   candidate and the column has run for thirty years.
2. **Digitised newspapers at scale.** The phrase searches are known to work — "aptly named",
   "true to his name", "curious coincidence of name" — but the archives need a browser session
   rather than an API. Chronicling America, Trove, Papers Past and the British Newspaper Archive
   between them cover four countries and two centuries.
3. **Old Bailey Online**, systematically. 197,000 trials searchable by name and offence, with a
   working API. Only a single defendant was extracted.
4. **Sports officials and college rosters.** Umpire and referee registers, NCAA rosters, minor
   leagues. Huge, documented, searchable, and the third-pass agent only sampled them.
5. **The books.** Paul Dickson's *What's in a Name?* (1996) collects a large private aptronym
   archive; Richard Lederer's word books add more. Both are borrow-only on the Internet Archive.
   Ernest Weekley's *The Romance of Names* (1914) is free and was only skimmed.
6. **Languages barely touched:** Chinese, Korean, Vietnamese, most South Asian and most African
   languages, Indonesian, Thai, Filipino, Persian, Basque, Catalan, Georgian, Armenian and the
   Baltic languages. Italian, Portuguese, Turkish and Greek were opened in wave 3 but not worked
   through.
7. **Nurses and midwives**, which returned only one solid row and remain the most neglected
   profession in the file relative to its size.
8. **Non-US and non-UK law.** Canada, Australia, New Zealand, Ireland, India and South Africa
   all have public judicial directories that were not searched.
9. **Intelligence, actuarial work, air traffic control and long-haul transport**, reported as
   barren on a first pass but not exhausted.
10. **Women in every domain.** Every published aptronym list skews heavily male and so does this
    one. Women's leagues, and women in medicine, law and science, need a dedicated pass rather
    than being folded into each domain.

## Reproducing this

```
make rebuild   # replay research -> apply audit corrections -> merge -> integrity sweeps
make enrich    # Wikipedia pass                                        (network)
make urls      # re-check every source URL                             (network)
make db stats
```

`make rebuild` is deterministic. It replays the wave 1 and 2 research files in a fixed order so
record ids stay stable, because every audit correction file is keyed by id. This matters: an
early run re-sorted the ids after adding new rows and silently retargeted 480 corrections onto
the wrong records. The merge now uses sticky ids, ranks a reviewed rejection above an
unreviewed claim so that replaying research cannot undo an audit, and refuses to pull in
research files unless asked.

Twelve correction files in `data/audit/corrections/` are replayed on every rebuild, carrying 529
verdicts: 284 rejections, 146 rescores and 99 fixes. Five are the audit slices, one holds manual
decisions on chosen names, and six are the verification rounds. They are applied twice, before
and after the third-wave merge, so that a correction can target either id generation.

A blank cell in a correction file means "leave this alone", so removing a bad citation rather
than replacing it needs the literal value `NULL` — which is what makes a wrong etymology link
deletable instead of permanent.

The same run also exposed a dedupe bug worth recording: collapsing rows on normalised name
alone fused a 1948-born horror director with a fifteenth-century Bishop of Worcester, both
called John Carpenter, and a police chief with a film director, both called Alfred Hitchcock.
Both pairs were separated and the lost people restored — Alf Hitchcock, the Association of
Chief Police Officers' national lead on knife crime, is a genuine entry and was nearly lost
entirely. The key now includes `field`, and cross-field name collisions are printed on every
merge for a human to check.
