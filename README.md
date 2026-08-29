# Aptronyms

A sourced, reviewable database of real people whose names are unusually apt for their work.
Usain Bolt the sprinter. Amy Freeze the meteorologist. Igor Judge, Lord Chief Justice of
England and Wales. James Outman, outfielder.

The point is not to reproduce the list that circulates on the internet. It is to build
something you can check: every person has a source URL, every score has a stated basis, and
every entry that failed review is still in the file with the reason it failed.

## The numbers

| | |
| --- | --- |
| People | 1,325 |
| Reviewed as real, scoring 3 or better | 691 |
| Rejected on review, retained with reasons | 294 |
| Fields covered | 17, from sports to funeral direction |
| Countries | 76 |
| Earliest birth year that survived review | 85 BC |
| Source URLs machine-checked | 2,184, of which 2 are dead — both on rejected rows |

Run `make stats` for the current breakdown, which is generated from the data rather than
typed here.

## Files

```
data/aptronyms.csv          the master dataset, one row per person
data/aptronyms.db           SQLite copy, with a publishable view and a types join table
data/schema.md              field definitions, conventions and the scoring rubric
data/research/              raw per-domain research output and each researcher's log
                            (two _build_*.py are inert one-off generators kept for provenance)
data/audit/                 review slices, correction files and reviewer logs
data/url_check.csv          HTTP status of every source URL
data/wikipedia_enrichment.csv  what the Wikipedia pass changed and why
.cursor/docs/research-log.md   searches run, sources mined, rejections, open gaps
.cursor/docs/research-brief.md the instructions the research agents worked from
```

## Reading a record

```
apt-1312,Rosalind Canter,Rosalind,Canter,eventing rider,sports,Great Britain equestrian
team,England,1986,,semantic,5,Canter,"Canter names a horse gait, the rhythm eventing riders
manage in her Olympic discipline.",English: horse gait,unknown,
https://en.wikipedia.org/wiki/Rosalind_Canter,,,2024 Paris Olympics team eventing gold,verified
```

Two fields do the analytical work, and they are deliberately independent:

- **`aptronym_score`, 1 to 5** rates how well the name fits the work. 5 is Usain Bolt. 3 needs
  a sentence of explanation. 1 is speculative.
- **`review_status`** rates how well the claim is sourced: `verified`, `probable`, `borderline`
  or `rejected`.

A famous name can be well sourced and still score 2. An obscure dentist named Payne can score
4 and sit at `probable` because the only source is his employer's page. Keeping the two apart
is what makes the file reviewable.

`aptronym_type` is pipe-delimited and multi-valued: `direct`, `wordplay`, `semantic`,
`phonetic`, `translation`, `ironic`, `other`. Inaptronyms — Rob Banks the police officer,
Jimmy Doolittle who led the Tokyo raid — are tagged `ironic` and kept in the same table.

`name_status` is the third field worth reading before quoting anything, because a name chosen
after entering the profession is a different thing from a name someone was born with. Where it
says `unknown`, nobody has checked. `data/schema.md` sets out exactly how the value is arrived
at and where the inference can be wrong.

## Querying it

```sql
-- The strongest entries, ready to use
SELECT full_name, occupation, connection FROM publishable WHERE aptronym_score = 5;

-- Which professions attract apt names?
SELECT field, count(*) n, round(avg(aptronym_score), 2) avg_score
FROM people WHERE review_status <> 'rejected' GROUP BY field ORDER BY n DESC;

-- Aptronyms that only work in translation
SELECT p.full_name, p.country, p.name_origin FROM people p
JOIN aptronym_types t USING (id)
WHERE t.aptronym_type = 'translation' AND p.review_status = 'verified';

-- Why things were rejected
SELECT full_name, notes FROM people WHERE review_status = 'rejected' LIMIT 20;
```

## Rebuilding

```
make rebuild   # replay research -> apply audit corrections -> merge -> integrity sweeps
make enrich    # Wikipedia pass: fill dates, detect birth names   (network)
make urls      # re-check every source URL                        (network, ~3 min)
make db        # rebuild the SQLite copy
make stats     # print the summary
make check     # validate without writing
```

`make rebuild` is deterministic and idempotent. It replays the research files in a fixed order
so that record ids stay stable, because the audit correction files are keyed by id.

## How it was built

Research ran in three waves of parallel agents, split by domain: canonical sources first, then
occupational sweeps, then a targeted pass at the gaps the first two left. Agents worked from
`.cursor/docs/research-brief.md` and were told to work name-first as well as concept-first —
picking a surname that would be apt for a job and then searching a roster, register or court
listing to find out whether such a person actually exists.

Then five reviewers audited the result against the rubric, with authority to rescore or reject
but not to add. They rejected 265 of the first 1,265 rows. That was the most useful stage of
the project, and the reasons are worth reading in `.cursor/docs/research-log.md`, because the
failure modes are systematic: invented etymology, reasoning backwards from a famous name, and
treating an eponym as an aptronym when the unit was named after the person rather than the
person happening to suit the unit.

## Known limitations

- **`name_status` is thin.** Researchers mass-defaulted it to `birth_name` without checking, so
  all unverified values were reset to `unknown`. A Wikipedia pass then established 552 of them
  and flagged 10 chosen names, including two that undercut well-known examples: Faith Popcorn
  was born Faith Plotkin, and Frank Field the weatherman was born Franklyn Feld. The remaining
  `unknown` values are genuinely unchecked, not assumed.
- **Verification is single-source for most rows.** The brief required one reliable source, not
  two. Rows resting on an employer page, a licence registry or a consumer physician directory
  are capped at `probable` and noted.
- **The link check cannot prove a page says what we claim.** It proves the page exists. 244 of
  the 2,184 references sit behind bot walls — Olympedia, Baseball Reference and LinkedIn all
  refuse automated requests — so those were confirmed by hand when the row was written but
  cannot be rechecked automatically. That gap hid three guessed Baseball Reference ids through
  several rounds of checking, because a bot wall and a missing page look identical from outside.
- **Nicknames were systematically mishandled** until a late pass caught it. A nickname awarded
  for the trait it describes is not an aptronym, and 17 rows had it backwards, including Frank
  "Home Run" Baker at a score of 5. They are rejected or downgraded now, but the same error
  could survive elsewhere in any row whose `name_status` is `professional_name`.
- **Coverage is Anglophone-heavy.** Half the records are American. 179 rows turn on translation
  across 25 languages, which is better than any published list, but Chinese, Korean, Vietnamese
  and most African and South Asian languages are barely touched.
- **The `sports` field is over-represented** at a quarter of the file, because league rosters are
  the most searchable name-first source in existence. That is a property of the sources, not of
  the world.
- **One early merge collapsed same-name people.** Deduping on name alone fused a horror director
  with a fifteenth-century bishop. Both were restored, the key now includes `field`, and
  cross-field name collisions are reported on every merge. Any remaining same-name pair inside
  a single field could still be two people.

## Requirements

Python 3.10 or newer. No third-party packages: the scripts use only the standard library, so
`make rebuild` works on a clean machine. `make enrich` and `make urls` need network access.
