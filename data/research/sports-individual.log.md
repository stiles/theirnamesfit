# Research log: sports-individual.csv

Agent domain: individual and Olympic sports (track, swimming, cycling, motorsport, tennis, golf, boxing, MMA, wrestling, weightlifting, gymnastics, rowing, sailing, surfing, skiing, mind sports, darts, snooker, etc.), plus coaches, referees, and broadcasters.

Target: 80+ verified rows. **Delivered: 82 rows.** Validation: `python3 scripts/merge.py --check` passed.

## Concept-first searches

| Query | Result |
| --- | --- |
| Olympedia athlete surname Swift runner sprinter | Eugene Swift, Greggmar Swift, Bailey Swift |
| Olympedia swimmer Waters Fish Float athlete | Erik Fish; Jeff Float excluded (already in dataset) |
| Olympedia cyclist Wheeler Rider Hill | Chris Wheeler, Charlie Hill, Harry Hill |
| BoxRec boxer Strong Hook Armstrong | Henry Hook, Henry Armstrong, Tiger Jack Payne |
| Olympedia gymnast Turner Flip athlete surname | Rowland "Flip" Wolfe |
| FIDE chess player Bishop Knight King Castle | Klaus Bischoff (German for bishop) |
| PGA golfer Green Putt Bunker Sand Links surname | Richard/Hubert/Ken Green, John Bird, Sam Byrd |
| ATP tennis player Court Serve Ace Netter | Margaret Court, Anna Smashnova |
| Olympedia skier Frost Snow Ice Winter athlete | Lis Frost, Axel Frost, Tormod Frostad |
| Olympic athlete named Slow Stone Gentle Falls ironic name | No strong Olympic cases; used Gout Gout, Michael Rock, Gevvie Stone |
| chess grandmaster Bishop Knight Rook surname FIDE | Klaus Bischoff |
| poker player Bluff Chip Deal Hendon Mob | Chip Reese, Barny Boatman |
| penguin darts player Bullseye snooker player Pot Frame | Ray Reardon (Pot Black wins) |
| Olympedia sailor Wind Sail Row Boat skipper | Henning Wind, Conn Findlay (rower/sailor, name not apt—skipped) |
| Olympedia equestrian Rider Horse Gallop Canter | Rosalind Canter excluded (already in dataset) |
| site:olympedia.org athlete surname Jump Long Run Fast Dash | Willie Steele, Carl/Jack Archer |
| Olympic athlete Moist Endurance Leeper aptronym swimmer | Lewis Moist, Endurance Abinuwa, Nathan Leeper |
| site:olympedia.org swimmer Rivers Lake Sea Wade Waters | Karen Riveros, Khemo Rivera, Megan Rivers, R. P. Waters |
| site:olympedia.org OR site:boxrec.com boxer Strong Hook Armstrong | See above |
| Olympedia weightlifter Strong wrestler Savage Bear Lyon | Mark Henry, Doc Strong, Jim Armstrong |
| Olympedia archer Bowman Archer Marksman shooter Gunn | Janine Bowman, Russell/Lauryn Mark, Charles Palmer, Dick Gunn |
| poker player Chip Reese Bluff surname professional | Chip Reese |
| Formula 1 driver Race Speed Rush Turbo motorsport | Scott Speed excluded; no new F1 apt names confirmed |
| site:olympedia.org Fleet Quick Rush Dash runner hurdler | Martin Rush, Ernst Fast |
| Shirley Strickland hurdler Olympedia apt Olympic names list | Strickland not apt enough—skipped |
| site:olympedia.org shooter Gunn Archer Marksman | Charlie Gunn (race walker—weak), Charles Palmer |
| Layne Beachley excluded surfer Wave Ocean Waters Olympedia | Layne Beachley excluded; Oceana Mackenzie added |
| site:olympedia.org gymnast Turner wrestler Strong Armstrong | Frank Turner, Doc Strong |
| triathlete Run Swim Bike Olympedia climber Rock Stone Peak | Oceana Mackenzie, Michael Rock |
| Endurance Abinuwa Olympedia Olympics 2012 London | Endurance Abinuwa |
| Kim Yoo Suk pole vaulter Olympedia Korean | Kim Yu-Seok |
| sports commentator apt name Speed Rush Court Bowman | Red Rush, Bob Rathbun (Courtland) |
| slow runner athlete Olympic Gentle boxer climber Falls | Gout Gout (ironic), Michael Rock |
| esports player King Bishop chess Scrabble champion Word | Emmanuel King, Gwendolyn Sherard-Bishop |
| apt name Olympian swimmer runner boxer archer historical | Malcolm Champion, Walter Bathe, Ernst Fast, topendsports list |
| George Ball-Greene Olympedia tennis 1908 | George Ball-Greene |
| Olympia Aldersey Olympics.com rower Australia | Olympia Aldersey |
| Gout Gout sprinter Wikipedia Australian record | Gout Gout |
| site:olympedia.org Steele long jump Waters Knight athlete | Willie Steele, R. P. Waters, Bianca Knight |
| site:olympedia.org athlete surname Archer Gunn Lance Sword Knight | Simon/Sandy Archer, Adam/Charlie Gunn |
| site:olympedia.org skater Skate Slide Glide Ice Snow | Chad Hedrick (Hedrick not apt—skipped) |
| site:olympedia.org weightlifter lifter Strong Power Lift | Paul Anderson, Mark Henry |
| site:olympedia.org rower oarsman Sail Boat Ship | Olympia Aldersey, Megan Rivers |
| Margaret Court tennis Olympedia Anna Smashnova | Margaret Court excluded (already in canonical.csv); Anna Smashnova added |
| Charlie Gunn Olympic shooter Olympedia | Race walker—not shooter; included as weak/borderline |
| Andreas Wank ski jumper Olympedia | Included as borderline phonetic |
| Christian Poser bobsledder | Included as borderline ironic |

## Name-first searches

| Surname idea | Search | Found |
| --- | --- | --- |
| Swift | worldathletics.org + Olympedia | Eugene, Greggmar, Bailey Swift |
| Leeper | Olympedia | Nathan Leeper |
| Bathe / Moist / Fish | Olympedia + NPR apt-names article | Walter Bathe, Lewis Moist, Erik Fish |
| Spear | Olympedia fencing | Jeff and Will Spear |
| Frost / Frostad | Olympedia winter | Lis Frost, Axel Frost, Tormod Frostad |
| Green / Bird / Byrd | PGA + Wikipedia | Multiple golfers |
| Court / Smashnova | Wikipedia + tennis databases | Anna Smashnova (Margaret Court already in canonical) |
| Champion | Olympedia | Malcolm Champion |
| Apt / Apted | Olympedia + World Athletics | Ruth Apt, Manfred Apt, Todd Apted |
| Wind | Olympedia sailing | Henning Wind |
| Wheeler / Hill | Olympedia cycling | Chris Wheeler, Charlie/Harry Hill |
| Hook / Armstrong / Payne / Gunn | BoxRec + Olympedia | Combat sports entries |
| Bischoff | Wikipedia FIDE | Klaus Bischoff |
| Chip Reese | Wikipedia NYT obit | Chip Reese |
| Olympia | Olympics.com AOC profile | Olympia Aldersey |
| Gout | Wikipedia + ESPN 2026 | Gout Gout |
| Rivers / Riveros / Rivera | Olympedia | Swimmer and hockey entries |
| Rock / Stone | Olympedia + Team USA | Michael Rock, Gevvie Stone (ironic) |
| Endurance | Olympedia + Wikipedia | Endurance Abinuwa |
| Flip | Olympedia tumbling | Rowland Wolfe |
| Rush | Olympedia race walk + Wikipedia Red Rush | Martin Rush, Wesley "Red" Rush |
| Bowman / Mark | Olympedia shooting | Janine Bowman, Russell/Lauryn Mark |

## Sources examined (yield)

| Source | New candidates |
| --- | --- |
| Olympedia athlete pages | ~55 |
| Wikipedia biographies | ~20 |
| BoxRec | 4 |
| Sherdog | 2 |
| World Athletics / Olympics.com / Team USA | 8 |
| PGA Tour / European Tour | 5 |
| NPR / topendsports apt-name lists | 6 (discovery; verified on Olympedia/Wikipedia) |
| FIDE / Wiktionary (Bischoff) | 1 |
| Hendon Mob / Scrabble players org | 3 |
| Bobby George site / Ray Reardon Wikipedia | 2 (borderline) |

## Rejected candidates

| Person | Reason |
| --- | --- |
| Usain Bolt, Margaret Court, Jeff Float, Layne Beachley, Rosalind Canter, Marina Stepanova, Tennys Sandgren, Katie Volynets, Tiger Woods, Scott Speed, Dylan Rieder, Chris Moneymaker, Sina Movahed, Jeremy Wade, Ocean Ramsey, Tracy/Nancy Caulkins | Already in dataset per task brief |
| Nathan Leeper (duplicate row) | Single entry kept |
| Shirley Strickland | Strickland not semantically apt |
| Markus Prock | Prock not apt for luge |
| Frank Turner (strong) | Turner only weakly apt—kept at score 2 |
| Chad Hedrick | Hedrick not apt |
| Thor Meeks | Baseball, outside domain |
| Joe Beevers | Beevers not apt for poker |
| Andreas Wank (almost dropped) | Kept as borderline phonetic per English-media joke |
| Listicle-only names without primary verification | Not recorded |

## Score distribution

| Score | Count |
| --- | --- |
| 5 | 6 |
| 4 | 38 |
| 3 | 24 |
| 2 | 15 |
| 1 | 0 |

## Strongest finds

1. **Malcolm Champion** — Olympedia explicitly calls the swimmer "aptly named"; Olympic relay gold.
2. **Olympia Aldersey** — Named for the 1992 Olympics during the Barcelona Opening Ceremony; became a three-time Olympic rower.
3. **Nathan Leeper** — Olympedia: "one of the most apt names ever for an athlete"; high jump.

## Gaps for next pass

- More **motorsport** (Race, Turbo, Pitman surnames on FIA/F1 historical entry lists).
- **Surfing** post-Olympic era (Beachley excluded; search Wave, Surf, Break surnames on WSL).
- **Esports** with piece/card names (verified Liquipedia/FIDE crossovers).
- **Olympedia deep scroll** on 1900–1920 athletics entries (many DNS athletes with apt surnames like Ball-Greene).
- **Translation cases** in non-English sports (Strelec-type names in European football-adjacent individual sports).
- **Ironic slow/heavy names** for sprinters and swimmers — few confirmed Olympians beyond Endurance Abinuwa and Gout Gout.
