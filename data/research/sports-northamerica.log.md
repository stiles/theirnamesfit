# Research log: sports-northamerica

Date: 2026-08-29  
Output: `data/staging/sports-northamerica.csv` (91 rows)  
Domain: North American team sports (MLB, NFL, NBA, NHL, Negro leagues, college football, broadcasters)

Excluded per task brief (already in master dataset): James Outman, Josh Outman, Cecil Fielder, Prince Fielder, Fielder Jones, Early Wynn, Grant Balfour, Bob Walk, Larry Playfair, Michael Ball, Peter Bowler, Frank Beard.

---

## Concept-first searches

| Query | Source examined | New candidates |
| --- | --- | --- |
| `aptronym baseball pitcher` | Wikipedia Aptronym, Providence Journal | Jeter, Fielder patterns (many excluded) |
| `"When the name fits the game" baseball` | Providence Journal 2019 | Derek Jeter stealth aptronym |
| `nominative determinism baseball pitcher` | DOI 10.1179/175622709x462478 | Clyde Kluttz ironic example |
| `"best names in baseball history"` | 1075thefan listicle (discovery only) | Urban Shocker, Catfish Hunter, Johnny Dickshot |
| `Beyond the Box Score "When The Stats Match The Name"` | beyondtheboxscore.com (no direct article hit) | — |
| `Home Run Baker nickname SABR` | SABR journal article | Home Run Baker |
| `Harry Caray broadcaster SABR` | SABR BioProject | Harry Caray |
| `Red Barber Ford Frick Award` | baseballhall.org | Red Barber (weak fit) |

## Name-first searches (Baseball Reference)

| Query / surname probe | Source | Yield |
| --- | --- | --- |
| `site:baseball-reference.com Pitcher` | register search | Jim Pitchter |
| `Painter`, `Striker`, `Strike`, `Score`, `Foulke`, `Diamond`, `Roof`, `Clear` | BR search API via curl | 12 MLB rows |
| `Homer` (given name) | BR | Smoot, Bush, Thompson, Spragins |
| `Pinch Thomas` | BR | Pinch Thomas |
| `Batter`, `Bunt`, `Catch`, `Glove`, `Mitt`, `Slider`, `Curve`, `Fastball`, `Knuckle`, `Sacrifice`, `Loser`, `Rookie` (surname) | BR curl | Rookie Davis; no surname Batter/Bunt/Catch |
| `Base`, `Ball` (surname) | BR | Basabe variants only; Michael Ball excluded |
| `Puckett`, `Paige`, `Bell`, `Suttles`, `Poles` | BR | Negro leagues + Troy/Kirby Puckett |
| `Glasscock`, `Dickshot`, `Podres`, `Kluttz`, `Baumann`, `Pole`, `Batchelor`, `Steele` | BR | 8 rows |
| `Judge` (surname) | BR | Aaron Judge (ironic vs umpire) |
| `Curvelo` | BR register | Luis Curvelo |
| `Bench`, `Shocker`, `Boyd`, `Hunter`, `Young Cy`, `Fingers`, `Lyle`, `Bottomley` | BR | 7 rows |

## Name-first searches (Pro Football Reference)

| Query / surname | Source | Yield |
| --- | --- | --- |
| `Long` punter | PFR | Ty Long |
| `Fields`, `Goodburn`, `Gardocki`, `Guy`, `Hekker`, `Lechler` | PFR | 6 punter rows |
| `Rush` | PFR | Thomas, Clive, Anthony, Cooper, Jerry, Darius Rush |
| `Foote` | PFR | Larry Foote |
| `Runyan` | PFR | Jon Runyan (Jr. dropped — dedupes with father on merge) |
| `Sack` | PFR | John Sack (guard, ironic) |
| `Suggs`, `Sweat`, `Young Chase` | PFR | 3 defensive rows |
| `Goode`, `Gardner` | PFR | 8 rows |
| `Mayfield` | PFR | Baker Mayfield |
| `Guard`, `Tackle`, `Blitz`, `Punt`, `Kicker`, `Fumble`, `Helmet`, `Center` (surname) | PFR curl | No exact-surname NFL players found |
| `Hand`, `Snapp`, `Blocker`, `Swift` (NFL) | PFR | Stromile Swift is NBA; no NFL Swift apt case kept |

## Name-first searches (Hockey Reference)

| Surname probe | Source | Yield |
| --- | --- | --- |
| `Frost`, `Snow`, `Winter`, `Blade`, `Ice`, `Puck`, `Stick`, `Skate`, `Save`, `Slap`, `Checker`, `Hitman`, `Freeze` | HR search | Morgan Frost, Garth/Aaron Snow, Ryan Winterton, Hank Blade, Blade Jenkins, Harry Frost |
| `Playfair` | HR | Jim Playfair only (Larry excluded) |

## Name-first searches (Basketball Reference)

| Surname probe | Source | Yield |
| --- | --- | --- |
| `Post`, `Hooper`, `Swish`, `Court`, `Guard`, `Hoop`, `Dribble`, `Dunk`, `Shooter` | BBRef search | Quinten Post, Bobby Hooper, Deward Dopson (Swish), Courtney Lee, World B. Free, Stromile Swift, J.R. Smith, Lavor Postell |
| `Dunn`, `Rimmer`, `Baskett`, `Shotwell`, `Jump` | BBRef | No apt-surname matches kept |

## Other sources

| Source | Yield |
| --- | --- |
| NYT City Room 2011 (Jeter = French "to throw") | Derek Jeter etymology |
| Wiktionary `podrido` | Johnny Podres (borderline) |
| SABR bioproj (Caray, Kluttz, Barber, Shocker) | 4 supporting citations |

**Total distinct search queries run: 42+**

---

## Rejected candidates (real people not recorded)

| Name | Reason |
| --- | --- |
| Jon Runyan Jr. | Dedupes with Jon Runyan on merge (`norm_name` strips Jr.) |
| Jack Glasscock as strong aptronym | "Glass" link unsupported; nickname is Pebbly Jack for picking pebbles |
| Tris Speaker | "Speaker" has no credible baseball connection |
| Justin Steele as steal pun | Homophone too weak at score 2; kept with low score |
| Yadier Molina / Iván Rodríguez | Surname not apt; search noise from "catcher" query |
| Shane Battier | Surname unrelated to basketball court |
| Kirby Puckett as hockey pun | Baseball player; kept with low score as cross-sport puck echo |
| NFL player surname `Kicker`, `Guard`, `Tackle`, `Blitz`, `Punt`, `Fumble` | No matching surnames in PFR |
| Baseball surname `Catcher`, `Batter`, `Bunt`, `Ball` (MLB) | No exact-surname MLB players |
| Hockey surname `Puck`, `Stick`, `Ice`, `Goalie` | No exact-surname NHL players |
| Red Barber as apt broadcaster | Surname unrelated to broadcasting; kept borderline score 2 only |
| Johnny Dickshot | Marginal fit; odd-name curiosity, score 2 borderline |

---

## Score distribution

| Score | Count |
| --- | --- |
| 5 | 5 |
| 4 | 24 |
| 3 | 44 |
| 2 | 18 |

Review status: 86 verified, 1 probable, 4 borderline.

---

## Gaps / next pass

- **Umpires and officials:** BR Bullpen has no surname index for Ball/Strike/Fair; Retrosheet umpire register worth mining.
- **Softball / college lacrosse:** Name-first on NCAA.com roster search (`surname=Hoop`, `Stick`, `Draw`) not attempted.
- **Spokesman-Review Jan 1912 "Names Figure in Sports Careers"** — article not retrieved; likely rich 19th-century leads.
- **Inaptronyms:** Slow RB named Swift, pitcher Walk/Balfour already in master; hunt more `ironic` cases (e.g. kicker named Miss, punter named Short).
- **Coaches:** Dusty Baker, Tommy Lasorda — weak fits; better coach targets might be `Steelman`, `Ball`, `Run`, `Field` surnames in coaching trees.
