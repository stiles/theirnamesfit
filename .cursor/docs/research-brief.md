# Aptronym research brief (for research agents)

Read this in full before searching. It defines what counts, how to source it and the exact
output format.

## What we are collecting

An **aptronym** is a real person whose name is unusually appropriate to their occupation, role,
achievement or another well-documented aspect of their life.

Canonical examples:

- Usain Bolt, Jamaican sprinter — "bolt" means to move suddenly and fast
- Amy Freeze, American TV meteorologist
- Igor Judge, Lord Chief Justice of England and Wales
- James Outman, MLB outfielder — "out man"
- William Wordsworth, poet — his surname contains "words"
- Eugène Terre'Blanche, South African white nationalist — French for "white land"

We also collect **inaptronyms** (names amusingly contrary to the person's work: Rob Banks the
police officer, Jimmy Doolittle the bombing-raid commander). Tag those `ironic`.

## Hard rules

1. **Real, identifiable people only.** No fictional characters, no charactonyms, no anonymous
   anecdotes ("a plumber named Mr. Leek in Ohio"), no people whose existence you cannot confirm.
   Businesses and place names do not count — this is a database of people.
2. **Every row needs a reliable source URL** establishing who the person is and what they do.
   Acceptable: Wikipedia, official league/team/club sites, university and employer pages,
   government sites, courts, professional bodies, journal articles with DOIs, obituaries and
   articles from reputable news organizations, established reference works.
   Not acceptable as verification: listicles, "funny names" galleries, Reddit, Quora, X posts,
   AI-generated content farms. Those are *discovery* sources only — record them in
   `discovery_source_url` and then verify the person elsewhere.
3. **Never invent an etymology.** If the connection depends on a foreign word, an obscure word
   or a name meaning, cite a separate source for that meaning in `name_source_url`. Wiktionary is
   acceptable; a dictionary, onomastic reference or scholarly source is better. If you cannot
   source the meaning, either drop the candidate or set `review_status` to `borderline` with a
   note saying the etymology is unverified. A surname that merely *looks* suggestive is not
   evidence.
4. **Check that the name is genuine.** If the relevant name is a stage name, pen name, ring name,
   pseudonym, religious name, Anglicization or a name adopted after entering the profession, say
   so in `name_status` and `notes`. Those entries stay in the database but must be flagged. If a
   Wikipedia article gives a different birth name, that matters — record it.
5. **No URL invention, including plausible ones.** Only record URLs you actually retrieved. The
   commonest failure is not a wild guess but a reasonable one: adding a disambiguation suffix
   that does not exist (`Joshua_Bell_(violinist)` for a man whose article is just `Joshua Bell`),
   assuming a person has an article because they are notable, or assuming a surname has its own
   Wiktionary entry (`/wiki/beekman`, `/wiki/loiseau` — neither exists; cite the word that
   carries the meaning). Resolve the title through the Wikipedia search or query API and paste
   what it returns. Every URL in this dataset is machine-checked, so a guess will be found.
6. **Do not pad.** A sourced score-2 entry is welcome. A fabricated or unverifiable entry poisons
   the dataset. When in doubt, lower the score or the review status rather than dropping the row,
   unless the person cannot be verified at all.

## Classification

`aptronym_type` — pipe-delimited, one or more of:

| Type | Meaning | Example |
| --- | --- | --- |
| `direct` | The name literally is the occupation or activity | Igor Judge, judge |
| `wordplay` | The name forms a pun or phrase in the person's field | Katie Volynets, tennis ("volley nets") |
| `semantic` | The meaning of the name relates to the work | Usain Bolt, sprinter |
| `phonetic` | The link depends on how the name sounds | Sina Movahed, chess ("seen a move ahead") |
| `translation` | The link appears once the name is translated | Dávid Strelec, striker ("shooter" in Slovak) |
| `ironic` | The name is amusingly contrary to the person | Rob Banks, police officer |
| `other` | Nothing above fits | |

`aptronym_score` — 1 to 5, scoring the name-to-work fit only, never the person's fame:

| Score | Test |
| --- | --- |
| 5 | Instantly obvious, near-exact fit, hard to call strained. Usain Bolt. |
| 4 | Clear and strong, maybe a beat of thought. Amy Freeze. |
| 3 | Legitimate but needs a sentence of explanation. Most translation cases land here. |
| 2 | Weak or arguable; the surname only glances at the job. |
| 1 | Highly speculative. Kept for later review. |

`review_status` — sourcing confidence, tracked separately from score:

- `verified` — person and occupation confirmed by an authoritative source, and any needed
  etymology is sourced too
- `probable` — person confirmed, but a detail (etymology, name status, which specialty) is soft
- `borderline` — the person is real but the aptronym reading is a stretch, or the etymology is
  unsourced
- `rejected` — turned out to be fictional, misattributed or wrong; keep the row and explain in
  `notes`

## Anti-padding rules

These come from a five-reviewer audit that rejected 275 of the first 1,265 rows. Every one of
these failures was committed by a previous research agent working from this same brief. Read
them as prohibitions, not suggestions.

1. **No hedging.** If your `connection` sentence needs the words *evokes*, *suggests*,
   *resembles*, *faintly*, *loosely*, *echoes*, *vaguely* or *arguably* to work, the aptronym
   does not work. Drop the candidate. An automated check now caps any row containing that
   language at `borderline`, so hedged rows are wasted effort. Rejected examples: "Zimmer is
   German for room, and he scores the rooms of cinema"; "Fellini suggests feline grace";
   "Groening resembles groningen or mourning in Dutch".
2. **No famous-name rationalising.** Do not start from a celebrity and reason toward an
   aptronym. Mozart, Dalí, Monet, Mahler, Sting and Rembrandt were all rejected because an
   agent worked backwards from fame. If the person is well known and no reliable source has
   ever remarked on their name, that is evidence against, not a gap for you to fill.
3. **Watch the direction of causation.** If a unit, law, disease, procedure or place is named
   *after* your candidate, the name did not fit the work — the work took the name. An entire
   cluster (Newton, Joule, Watt, Ohm, Hertz, Ampère, Kelvin, Faraday, Boyle, Hooke, Bessemer,
   Parkinson, Hodgkin) was rejected on this ground. The same applies to Roman cognomina and
   epithets awarded for a deed: Pompey *Magnus* earned that name by conquest.
4. **Nicknames are the hardest case of rule 3, and almost always fail it.** A nickname is
   usually awarded *because of* the trait, which makes it a description rather than a
   coincidence. Frank "Home Run" Baker was named for his home runs; "Cy" Young for the fastball
   that wrecked a fence; "Mule" Suttles for his hitting power; "Swish" for shooting. Seventeen
   rows were rejected or downgraded for this after the fact. A nickname only qualifies if you
   can source that it predates or is unrelated to the work — a childhood or family name that
   later happened to fit. Ring names, stage names and station-assigned brands never qualify:
   "Stormy" and "Sunny", two Denver weather presenters, were branded by their employer
   specifically to pair with each other.
5. **The name must describe the work, not the person's biography.** A footballer named Carroll
   who scored a lot of headers is not an aptronym. Statistics are not etymology.
6. **Licence registries, directories and listicles do not verify a person.** An NPI lookup
   proves a licence number exists. LinkedIn is self-reported. houseofnames.com and
   surnamedb.com sell surname stories. A search-results page identifies nobody. Rows sourced
   this way are automatically capped at `probable`; if that is the best you have, say so in
   `notes` rather than marking the row `verified`.
7. **Do not assume `birth_name`.** Agents mass-defaulted this field and 1,087 rows had to be
   downgraded. Use `unknown` unless a source states the birth name. Check performers,
   wrestlers, rappers and clergy specifically — chosen names are common and, where a name was
   chosen *because* it was apt, the coincidence is manufactured and the score should drop.
8. **A common surname plus a generic word is not an aptronym.** Field, Bell, Ball, Stone,
   Price, Marshall, Warren, Wright and Ward are among the commonest surnames in English. They
   need a pointed, specific fit to earn a place, and they never earn a 4 or 5 on their own.
9. **Never pad to hit a target.** If your domain yields 40 real entries, deliver 40. A stated
   row target is a ceiling on ambition, not a quota. Padding is the one failure that will get
   your whole file discarded.

## Method

Do not just reproduce known aptronym lists. Work both directions:

- **Concept-first:** search `aptronym`, `aptonym`, `nominative determinism`, `nomen est omen`,
  `perfect name for the job`, `fitting name`, `name matches profession`, `namephreak`, plus your
  domain. Try non-English equivalents where relevant.
- **Name-first:** think of surnames that would be apt in your domain, then search directories,
  rosters, staff pages, court listings, journal author lists and league databases to find out
  whether a real person with that name actually holds that job. This is where the genuinely new
  material comes from. Confirm before recording.
- When a page proves productive, fetch it and extract *every* plausible candidate, not only the
  ones a search snippet surfaced.
- Follow leads. One example suggests neighbouring surnames, neighbouring occupations and further
  sources.
- Run at least 25 distinct searches. Note them for the log.

## Output

### 1. The data file

Write a CSV to the path given in your task, with exactly this header and column order:

```
id,full_name,first_name,last_name,occupation,field,organization,country,birth_year,death_year,aptronym_type,aptronym_score,name_element,connection,name_origin,name_status,person_source_url,name_source_url,discovery_source_url,notes,review_status
```

- Leave `id` blank. It is assigned when files are merged.
- Empty cell means null. Never write `N/A`, `unknown`, `none` or a guess.
- `field` must be one of: `sports`, `medicine`, `science`, `law`, `politics`, `military`,
  `weather`, `arts`, `media`, `business`, `food`, `religion`, `education`, `trades`, `crime`,
  `transport`, `other`.
- `name_status` must be one of: `birth_name`, `legal_name`, `professional_name`, `pseudonym`,
  `unknown`. Use `unknown` when you did not check; use `birth_name` only when a source indicates it.
- `connection` is one plain sentence. No hedging filler.
- Quote any field containing a comma. Standard CSV escaping, UTF-8, no BOM.
- Keep diacritics in names (Eugène, Dávid, Müller).

Validate your file before finishing:

```
python3 scripts/merge.py --check
```

It prints per-row problems. Fix anything attributed to your file. Ignore problems in other files.

### 2. The log file

Write a markdown log next to your CSV at the path given in your task, containing:

- every search query you ran, grouped by strategy
- sources examined, with how many new candidates each yielded
- candidates you rejected and the specific reason
- what you did not get to, and which leads look most promising for a later pass

### 3. Your reply

Report row count, score distribution, your three strongest finds, anything you deliberately
excluded, and the gaps you would attack next. Keep it under 250 words.
