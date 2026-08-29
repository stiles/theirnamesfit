# Research log: sports-gaps

Date: 2026-08-29  
Output: `data/staging/sports-gaps.csv` (26 rows)  
Domain: Sports gaps — officials, historical/college/minor league, women's sport, motorsport, non-anglophone sport, ironic names, coaches and support roles not covered in prior passes.

---

## Concept-first searches

| Query | Source examined | New candidates |
| --- | --- | --- |
| `aptronym cricket umpire` | Wikipedia Aptronym | Dickie Bird |
| `aptronym sumo wrestler` | Wikipedia | Ishiyama, Yamamotoyama |
| `ironic inaptronym sports Short Strong` | ThoughtCo, dictai.org | Peter Short |
| `apt names sport Canter eventing` | The People's Friend, Wikipedia | Rosalind Canter |
| `Chuck Long aptronym football` | The People's Friend | Chuck Long (confirmed, not in master) |
| `Tennys Sandgren aptronym` | Wikipedia, People's Friend | Tennys Sandgren (not in master despite prior log mention) |
| `Steve Slowly sprinter` | World Athletics, Wikipedia relay page | Steve Slowly |

## Name-first: MLB umpires (Retrosheet register)

Parsed `retrosheet.org/downloads/csvumpires.html` (~1,386 umpires). Probed surnames: Ball, Fair, Pull, Soar, Call, Plate, Strike, Block, Judge, Out, Safe, Tag, Runge, Walk, Foul, Count, Score.

| Surname hit | Person | Yield |
| --- | --- | --- |
| Ballanfant | Lee Ballanfant | Included — Ball + fair-foul |
| Fair | Paul Fair | Included |
| Soar | Hank Soar | Included |
| Runge | Brian Runge | Included |
| Plate | Plate (one game) | Included |
| Pulli | Frank Pulli | Rejected — pull/tag link too weak |
| Denkinger | Don Denkinger | Rejected — famous safe call is biography, not name fit |
| Montague | Ed Montague | Rejected — substring "tag" in Montague is invented |
| Walk | Harry Walker (walkh901) | Rejected — confusable with famous player/manager Harry Walker; could not verify separate person page |
| Fairchild | Chad Fairchild | Skipped — Paul Fair is the cleaner Fair umpire |

## Name-first: NBA/NFL/other officials

| Query | Source | Yield |
| --- | --- | --- |
| `Mike Callahan NBA referee` | Basketball-Reference, NBA.com PR | Included |
| `NFL referee surname Judge Field` | Wikipedia List of NFL officials, PFR | No apt-surname official kept |
| `FIFA referee Stark` | Wikipedia, DFB | Wolfgang Stark included (translation, score 3) |
| `boxing judge Score Graham BoxRec` | BoxRec event pages | No judge surname Score/Graham kept |
| `tennis chair umpire Judge Call` | Wikipedia Official (tennis) | No apt surname |
| `ICC umpire Wide Out` | Wikipedia Umpire (cricket) | No apt surname |
| `GAA referee Judge Field` | Irish Examiner, Wikipedia Referee | James Judge GAA refs exist but weak pages; skipped |

## Women's sport

| Query | Source | Yield |
| --- | --- | --- |
| `NWSL goalkeeper Swift Save Strong` | Web search | Mollee Swift (LSU → Iceland) only strong find |
| `Paris Bowdler wicket-keeper` | Wikipedia | Rejected — Bowdler ≠ bowl; surname not apt |
| `WNBA Guard Block` | Wikipedia blocks leaders | No apt surname |
| `LPGA Bird surname` | Wikipedia | Birdie Kim uses chosen first name, not surname |

## Motorsport

| Query | Source | Yield |
| --- | --- | --- |
| `Ken Rush NASCAR` | Wikipedia, racing-reference | Included (Anthony Rush NFL already in master) |
| `Carlos Pace F1` | Wikipedia | Included |
| `Scott Speed Lake Speed` | aptronyms.csv grep | Already in master — skipped |
| `Will Power IndyCar` | aptronyms.csv | Already in master — skipped |
| `Phil Hill Graham Hill F1` | Motorsport Magazine | Rejected — Hill is ordinary surname per audit guidance |

## Historical / college / minor league

| Query | Source | Yield |
| --- | --- | --- |
| `John Strike pitcher 1886` | Baseball-Reference | Included |
| `George Block catcher Western League` | Howard DB, diamondsinthedusk | Included |
| `Jad Oestrike catcher` | Baseball-Reference register, NCSA | Included |
| `1912 Spokesman-Review Names Figure in Sports Careers` | Chronicling America (timeout), Wikipedia Aptronym | Not extracted — Ten Million, Fielder Jones, Home Run Baker already in master |
| `John Field Yale coach 1911` | Wikipedia | Rejected — Field is common surname without pointed fit (anti-padding rule 7) |

## Non-anglophone / niche sport

| Query | Source | Yield |
| --- | --- | --- |
| `Shane Hurley hurling goalkeeper` | Wikipedia | Included |
| `Bernard Hurley Cork goalkeeper` | Wikipedia | Skipped — redundant second Hurley after Shane |
| `Mienoumi Ishiyama sumo` | Wikipedia | Included (birth name row) |
| `Yamamotoyama sumo yama` | Wikipedia | Included |
| `John Stone curler` | Wikipedia, World Curling | Excluded — norm_name dedupe would collapse with geologist John Stone (apt-0647) in master |
| `kabaddi sepak takraw biathlon orienteering apt surname` | Web search | No verified apt roster hits |

## Ironic / inaptronymic

| Query | Source | Yield |
| --- | --- | --- |
| `Steve Slowly sprinter` | World Athletics | Included |
| `Peter Short rugby 6 foot 5` | Wikipedia | Included |
| `Peter Bowler batsman` | aptronyms.csv | Already in master |
| `slow athlete Swift Strong Tall` | World Athletics, college rosters | Bailey/Eugene/Greggmar Swift already in master; no verified slow Strong/Tall keeper |

## Broadcasters / coaches / support

| Query | Source | Yield |
| --- | --- | --- |
| `Harry Caray aptronym cheer` | Wikipedia, SABR | Already in master as probable; chosen Anglicization — skipped |
| `Marty Springstead spring training` | Wikipedia | Rejected — spring/springstead stretch |
| `Art Passarella pass ball umpire` | Wikipedia | Rejected — Passarella/pass link weak |

**Total distinct search queries run: 35+**

---

## Rejections (selected)

| Candidate | Reason |
| --- | --- |
| Don Denkinger | 1985 safe call is biography; Denkinger has no safe/out name link |
| Frank Pulli | Pull/pull tag at first base needs a sentence of rationalizing |
| Ed Montague | "Tag" inside Montague is invented etymology |
| Chad Fairchild | Fairchild compound; Paul Fair is the direct Fair umpire |
| Harry Walker (umpire) | Same name as famous player; no clean standalone source |
| Charlie Spikes | Spikes/cleats is generic equipment, score 2–3 |
| John Field (Yale coach) | Common surname Field |
| Carlos Pace considered borderline | Kept at 4 — pace/speed is direct for F1 |
| Wolfgang Stark | Kept at 3 — stark=strong is legitimate translation |
| Paris Bowdler | Bowdler is not bowl |
| Harry Caray | Professional pseudonym; Caray≠cheer |
| Graham Hill / Phil Hill | Ordinary surname per audit |
| John Stone (curler) | Valid apt row but excluded — merge.py dedupes on full_name and would merge with geologist John Stone |
| Swin Cash | Cash is not a basketball term |

---

## Unfinished leads (promising for next pass)

1. **1912 Spokesman-Review article** ("Names Figure in Sports Careers", 7 Jan 1912, p. 28) — Chronicling America timed out; OCR via Washington State digital newspapers could yield historical names beyond those already in master.
2. **BoxRec judge surname mining** — Howard Foster, Jerry Roth lack apt surnames; need systematic judge-name grep.
3. **College football/basketball name-first** — Probe Strike, Rush, Long, Guard at NCAA stats sites; enormous haystack.
4. **Women's cricket/rugby officials** — ICC and World Rugby referee lists barely searched.
5. **Motorsport beyond Pace** — Carlos Pace is the best new F1 add; Will Power and Scott Speed already captured.
6. **Kabaddi, sepak takraw, biathlon, orienteering** — No verified apt roster hits this pass.
7. **Groundskeepers, kit managers, mascot performers** — No authoritative apt-surname finds.
