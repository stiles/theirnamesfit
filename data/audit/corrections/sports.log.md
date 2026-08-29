# Sports slice audit log

**Auditor:** quality-gate subagent  
**Slice:** `data/audit/sports.csv` — 303 rows  
**Date:** 2026-08-29

## Coverage

| Metric | Count |
| --- | --- |
| Rows read (full slice) | 303 |
| Rows individually adjudicated | 303 |
| Source URLs fetched or API-checked | 68 |
| Accepted without fetch (BBRef/PFR/Olympedia/Wikipedia roster pages) | ~45 |
| Corrections written | 46 |

### Fetch sample (68 URLs)

Includes Wikipedia/Olympedia/BBRef/PFR/API checks for: Andy Carroll, Eric Hollies, Arsène Wenger, James Trafford, Mel Garside-Wight, Kobbie Mainoo, Paul McStay, Dixie Dean, Tim Cahill, Jimmy McGrory, Bekim Kastrati, Ashleigh Johnson, Charles Palmer (Olympedia), Christiane Endler, Mark De Man, Mark Henry (Olympedia), Pardeep Narwal, Ray Reardon, Scott Goodyear, Darren Potter, Graham Potter, Ty Long, Terrell Suggs, Joachim Löw, and 44 additional spot-checks across score-4/5 rows, hedging-language rows, and translation rows.

## Verdict counts

| Verdict | Count |
| --- | --- |
| reject | 30 |
| rescore | 12 |
| fix | 4 |
| keep | 0 |

## Rejection patterns

1. **Stat substituted for etymology (8 rows):** Carroll, Dean, McGrory, Cahill — headed-goal totals pasted onto surnames with no lexical link. Hollies — Bradman duck anecdote instead of name meaning.

2. **Invented homophones and splits (10 rows):** Mainoo/Man U, Suggs/sacks, Kingson/king of saves, Runyan/run+yan, Lechler/leeching kick, De Man/marking a man, Endler/Ende, Palmer/to palmer, Henry/strong as Henry, Kastrati/groin injury pun.

3. **Club/geography coincidence dressed as aptronym (5 rows):** Trafford/Old Trafford, Potter/Wolves vs Potters, Wolfe/Wolves, Goodyear/tire brand, Wenger/Arsenal destiny.

4. **Meta or self-referential padding (3 rows):** Manfred Apt, Ruth Apt, Todd Apted (partial — Apted rescored not rejected).

5. **Explicitly weak rows kept by agents (2 rows):** Ashleigh Johnson (connection admits no fit), Red Barber (notes admit no fit).

6. **Wrong sport/weapon/element (2 rows):** Janine Bowman (archer ≠ pistol), Ray Reardon (Pot Black ≠ surname).

## Rescore patterns

- **Generic English surnames at 4–5:** Hand, Fields, Foote, Snow — apply to any athlete in role.
- **Echo surnames:** Jeter, Swift family — 4→3 or 4→2.
- **Club-mascot coincidences scored as 5:** de Wolf 5→4, Møller Wolfe 5→2.

## Fixes applied

- Ernst Fast: semantic→ironic (marathon vs fast).
- Jake Striker: drop erroneous `direct` type.
- Harry Caray: `birth_name`→`unknown` (born Carabina).
- Dietmar Schütze: replace zxc.wiki source with Wikipedia.

## Systemic problems (apply dataset-wide)

1. **ESPN/listicle harvesting:** Rows sourced from ESPN aptronym listicles (37577543, NYT Athletic club-name pieces) cluster fabricated club-coincidence and header-stat entries. Re-audit all slices with those discovery URLs.

2. **`birth_name` default (280/303 here):** Agents mass-tagged without checking. Boxing/wrestling/broadcast Anglicizations need systematic downgrade to `unknown`, `legal_name`, or `professional_name`.

3. **Hedging language as smoke alarm:** 97/303 connections use evoke/suggest/loosely/faint/echo — nearly all need rescore or reject. Auto-flag in merge check.

4. **Profession-XI padding:** ESPNcricinfo profession/tradesman XI entries (Cook, Barber, Merchant, etc.) are profession surnames, not sport-specific aptronyms — score 2 max unless role matches (Bowler/bowler OK).

5. **Unacceptable person sources:** zxc.wiki, houseofnames.com, topendsports listicles used as verification. Run source-domain blocklist in merge.

6. **Header-goal fabrication cluster:** Carroll, Dean, McGrory, Cahill share identical failure mode — biography stats replacing etymology. Search other slices for this template.

## Five worst entries

1. **apt-0081 Arsène Wenger** — "destiny by name" at Arsenal; no Wenger meaning.
2. **apt-0104 Bekim Kastrati** — groin-injury pun on testicle fracture.
3. **apt-0829 Mel Garside-Wight** — "wight shift" pun invented from positional change.
4. **apt-0189 Charles Palmer** — fictional "to palmer" shooting verb.
5. **apt-0085 Ashleigh Johnson** — connection admits surname irrelevant; kept anyway.

## Genuinely strong (verified, not corrected)

Usain Bolt, Walter Bathe, Fielder Jones, Jim Pitcher, Lance/Andrew Painter, Thomas Bowler, Suani Save, Piloo Reporter, Scott Speed, Wolfgang Wolf, Christian Fuchs, Chris Moneymaker, Nathan Leeper, Noboru Yamada, Olympia Aldersey, Mat Sadler, Willie Thrower, Lloy Ball, Home Run Baker.
