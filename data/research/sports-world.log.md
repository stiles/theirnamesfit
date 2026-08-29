# sports-world research log

Agent domain: team sports outside North America (football, cricket, rugby, AFL, Gaelic games, field hockey, volleyball, netball, water polo, kabaddi).

## Searches (by strategy)

### Concept-first / listicle extraction
- `ESPN Toe Poke Daily Mark de Man Wolfgang Wolf ironic names football 2019`
- `Arsenal Wenger James Trafford football names clubs managers Athletic 2025`
- `football aptronym goalkeeper striker site:wikipedia.org`
- `cricket aptronym player name wicket bowler Wisden`
- `ESPNcricinfo XI cricketers names professions`
- `Appropriate Names in Sport topendsports apt`
- `Apt Names In Sport athletes The Peoples Friend`
- `rugby player aptronym surname Tackle Hooker Scrum site:wikipedia.org`
- `women's football player aptronym goalkeeper striker name`
- `kabaddi player aptronym name pro kabaddi apt surname`
- `netball player aptronym name`
- `water polo player surname Save Goal Pool wikipedia`
- `handball player aptronym surname`
- `GAA hurler goalkeeper aptronym surname`
- `AFL player aptronym surname Kick Goal Hunt afltables`

### Name-first (surname × role)
- Transfermarkt advanced search concepts: Goal, Keeper, Striker, Wolf, Jäger, Schütze, Wall, Stone, Cross, Hunt, Save
- `site:afltables.com player Hunt Kick Marks Goal Boot`
- `football player Schütze OR Jäger OR Vuković striker goalkeeper wikipedia`
- `football player surname matches club name Wolves Potter Saddlers Fuchs fox Leicester`
- `football goalkeeper surname Wall Stone Steel Hammer Cross site:wikipedia.org`
- `Transfermarkt football player surname Goal Keeper Striker`
- `cricketer surname Bowler Wicket Duck Runs aptronym site:espncricinfo.com`
- `rugby player surname Best Hook Tackle Scrum aptronym wikipedia`
- `Suani Save American Samoa goalkeeper`
- `Christian Schießer handball player Germany` (resolved to Scheffler/Dissinger; no Schießer athlete found)
- `Pardeep Narwal Dubki King`, `Naveen Kumar Naveen Express kabaddi`
- `Jimmy McGrory headed goals`, `Dixie Dean headed goals`, `Tim Cahill header`, `Andy Carroll header`
- `Mark Crossley goalkeeper`, `Mark Wallington goalkeeper`, `Johan Wallens goalkeeper`
- `Damien Fitzhenry Wexford goalkeeper`, `David Goodfield hockey`, `Lloy Ball volleyball`
- `Zhu Ting footballer shooting pronunciation`, `Suani Save OFC U20`

## Sources examined (new candidates yielded)

| Source | Yield |
| --- | --- |
| ESPN print id=37577543 (Oct 2019) | 8 football names (Casanova, Crouch, Conquest, Wisdom, Pique, England, Success, Kastrati) |
| NYT Athletic Aug 2025 (Spiers) | 12 club-name coincidences (de Wolf, Sadler, Fuchs, Trafford already in master, etc.) |
| Wikipedia Aptronym page | McStay, Sadler cross-check |
| ESPNcricinfo profession XI (Feb 2014) | 14 cricketers/umpires |
| ESPNcricinfo Onions/Beet-Root piece | 3 cricket names |
| topendsports apt list | Zhu Ting, Derek Kickett, George Best, Alan Ball, David Hookes |
| AFL Tables (Rex/Jayden/Josh/Taylor Hunt, Puncher, Archer, Sam Hunt, Kickett) | 8 AFL rows |
| Transfermarkt / OFC archives | Suani Save |
| Wikipedia translation trawl (Jäger, Schütze, Vuković, Bacigalupo, Löw, Fuchs) | 12 rows |
| Gaelic: Damien Fitzhenry | 1 |
| Field hockey: David Goodfield | 1 |
| Volleyball: Lloy Ball | 1 |
| Netball: Geva Mentor | 1 |
| Kabaddi: Pardeep Narwal, Naveen Kumar | 2 |
| Water polo: Ashleigh Johnson, Unai Aguirre | 2 |
| Rugby: Ethan Hooker, Rory Best, Nick Fenton-Wells, Tom Youngs, Steve Slater | 5 |
| Header specialists (William Hill / Finter compilations) | McGrory, Dean, Cahill, Carroll | 

## Rejected candidates

| Name | Reason |
| --- | --- |
| Arsène Wenger, James Trafford, Mark De Man, etc. | Already in `data/aptronyms.csv` |
| Ian Bishop (cricketer) | Duplicate full name with Church of England bishop in master |
| Christian Schießer (handball) | No verifiable athlete; Wikipedia 404 |
| Kelly Jackson (netball GK) | Jackson→guard stretch; no authoritative aptronym source |
| Mike Dean (referee) | Dean≠dean of referees; no semantic link |
| Marco Velo (cyclist) | Wrong sport |
| Bekim Kastrati | Included once as borderline; ESPN groin-injury pun too strained (kept as score 1) |
| Graham Alexander | Removed — manager/name link too weak |
| Jamie George | Removed — George surname not apt for hooker |
| Ann-Katrin Berger, Khiara Keating | No surname-role connection |
| Handball Mittún, Fis family | Family dynasty, not aptronym |
| Pawan Sehrawat "Hi-Flyer" | Nickname not surname |
| Gareth Barry / Barry Town | Never played for Barry Town — ironic non-fit, not aptronym |

## Output

- **File:** `data/staging/sports-world.csv`
- **Rows:** 92
- **Score distribution:** 5×7, 4×26, 3×42, 2×16, 1×1
- **Validation:** `python3 scripts/merge.py --check` — 0 problems attributed to sports-world.csv

## Not reached / next pass

- Sepak takraw and futsal: no verified surname-role pairs found (search `"futsal" player surname`, Thai surnames meaning kick/spike).
- Women's football beyond Mel Garside-Wight: Transfermarkt surname sweeps for Keeper/Save/Striker in Frauen-Bundesliga and WSL.
- Gaelic football (not hurling): Fitzhenry pattern — surnames Hurley/Hurl.
- Rugby league deeper: Tackle, Scrum as surnames (none found in World Rugby/Wikipedia).
- Slavic `Lovec`, `Brankár`, Hungarian `Kapus` as surnames on Transfermarkt.
- Referee/commentator seam: Whistle, Card, Linesman surnames.
- CricketArchive name-first for Duck, Wicket, Bowler, Stump surnames in minor counties.
- ironic/inaptronym expansion: Small (CB), Tall (GK), Miss (striker), Gap (defender) — need verified individuals.
- Club-name sub-genre: more Wolves/Wolf, Fox/Fuchs, Potters, Saddlers, Tigers beyond current set.
