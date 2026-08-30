# Research log: sports-skipped

Date: 2026-08-29  
Output: `data/research/sports-skipped.csv` (3 rows)  
Domain: North American team sports, cleanup pass

## Why this file exists

The sports-northamerica agent opened its log with a list of twelve names it excluded "per task
brief (already in master dataset)". Nine of them were. Three were not:

| Name | In master at the time |
| --- | --- |
| James Outman | no |
| Josh Outman | no |
| Grant Balfour | no |
| Cecil Fielder, Prince Fielder, Fielder Jones, Early Wynn, Bob Walk, Larry Playfair, Michael Ball, Peter Bowler, Frank Beard | yes |

James Outman is named in this repository's own README as one of the four headline examples, so
the gap was invisible in exactly the place it mattered most: the row was assumed to exist by
everybody downstream, including the README.

The failure mode is worth recording because it is not a research error. It is a coordination
error: the brief told the agent which names were already covered, the agent believed it, and
nobody checked the claim against the file. Any name on that exclusion list in any other domain
log could have gone the same way.

## Verification

| Name | Source | Established |
| --- | --- | --- |
| James Outman | en.wikipedia.org/wiki/James_Outman | Outfielder, MLB debut 31 July 2022 for the Dodgers, NL Rookie of the Month April 2023, born 1997 |
| Josh Outman | en.wikipedia.org/wiki/Josh_Outman | Pitcher, MLB 2008-2014 for Oakland, Colorado, Cleveland, the Yankees, born 1984 |
| Grant Balfour | en.wikipedia.org/wiki/Grant_Balfour | Australian relief pitcher, 2013 All-Star, 84 career saves, born 1977 |

## Scoring

Both Outmans are scored 4, matching Cecil Fielder at 4 rather than Fielder Jones at 5: "Outman"
describes the outcome the job produces rather than naming the position, so it takes a beat where
"Fielder" does not.

Balfour is scored 3 and typed `phonetic|ironic`, matching Bob Walk at 3. The fit needs the
surname said aloud, and a walk is the opposite of what a closer is for.

Josh Outman carries a note about his Oakland nickname, "Out-Man". The nickname is not the
aptronym and does not earn the row: he was born Outman, and the nickname is downstream of the
surname rather than of the pitching. Seventeen rows elsewhere in this project had precisely that
relationship backwards, so the row says so explicitly.

## Merged with

    python3 scripts/merge.py --only sports-skipped.csv

Appended last in `GEN2` so every existing id is untouched.
