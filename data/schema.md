# Aptronym database schema

One record per person. CSV, UTF-8, comma-delimited, quoted where needed. Column order is fixed
and must match exactly in staging files so `scripts/merge.py` can concatenate them.

| Column | Type | Notes |
| --- | --- | --- |
| `id` | string | Assigned at merge time (`apt-0001`...). Leave blank in staging files. |
| `full_name` | string | Name as commonly rendered. Required. |
| `first_name` | string | Given name, or null. |
| `last_name` | string | Surname, or null. |
| `occupation` | string | Specific role, e.g. `sprinter`, `urologist`, `Lord Chief Justice`. |
| `field` | enum-ish | Broad domain: `sports`, `medicine`, `science`, `law`, `politics`, `military`, `weather`, `arts`, `media`, `business`, `food`, `religion`, `education`, `trades`, `crime`, `transport`, `other`. |
| `organization` | string | Employer, team, court, university, label. Null if not applicable. |
| `country` | string | Nationality, not birthplace, when they differ. |
| `birth_year` | int | Null if unknown. |
| `death_year` | int | Null if living or unknown. |
| `aptronym_type` | multi | Pipe-delimited from: `direct`, `wordplay`, `semantic`, `phonetic`, `translation`, `ironic`, `other`. |
| `aptronym_score` | int 1-5 | 5 = extraordinary fit, 1 = highly speculative. |
| `name_element` | string | The part of the name doing the work, e.g. `Bolt`, `Outman`, `Terre'Blanche`. |
| `connection` | string | One sentence on why the name is apt. |
| `name_origin` | string | Etymology or translation when the connection needs it. Null otherwise. |
| `name_status` | enum | `birth_name`, `legal_name`, `professional_name`, `pseudonym`, `unknown`. |
| `person_source_url` | url | Best source verifying identity and occupation. Required. |
| `name_source_url` | url | Source for translation/etymology. Required when `aptronym_type` includes `translation` or `name_origin` is non-null. |
| `discovery_source_url` | url | Where the candidate was first seen, if different from the above. |
| `notes` | string | Caveats, disputes, alternate readings, name-change history. |
| `review_status` | enum | `verified`, `probable`, `borderline`, `rejected`. |

## Conventions

- Null is an empty cell, never `N/A`, `unknown` or a guess.
- `aptronym_type` uses `|` as the separator because commas collide with CSV quoting in practice.
- `ironic` covers inaptronyms (Rob Banks the police officer). They are kept in the same table
  rather than split out, since the boundary is often a judgement call.
- `review_status` = `rejected` rows stay in the file. Rejections that never became records at all
  are logged in `.cursor/docs/research-log.md` instead.

## How `name_status` is set

The column matters more here than in most datasets: a name chosen after entering the profession
is a different phenomenon from a name someone was born with, and conflating the two is how
Faith Popcorn ends up cited alongside Usain Bolt.

Values come from one of three places.

1. **A reviewer checked it.** Treated as authoritative and never overwritten by automation.
2. **Inferred from a Wikipedia lead** by `scripts/enrich_wikipedia.py`, which only ever writes
   over `unknown`. The rule: if the article's title contains every token of the recorded name
   and the lead paragraph gives no alternate name, record `birth_name`. If the lead does give an
   alternate — the "born X" or "né X" construction — record `professional_name` or `pseudonym`
   and put the birth name in `notes`.
3. **`unknown`**, meaning nobody has checked. This is the default and it is honest; 1,087 rows
   once carried an unchecked `birth_name` and were reset.

Rule 2 is an inference, not a citation, and it can be wrong in two ways. Wikipedia leads state
"born X" reliably for stage names but not for every biography, so a quiet legal name change can
read as a birth name. And the title-token requirement exists because an earlier version matched
on surname alone and attributed Frank Field's birth name, Franklyn Feld, to his daughter Allison
on the same article. Where the distinction carries the aptronym, the row says so in `notes`
rather than relying on this column alone.

## Scoring rubric

| Score | Test |
| --- | --- |
| 5 | An English speaker gets it instantly and the fit is close to exact: Usain Bolt, sprinter. |
| 4 | Clear and strong, maybe a beat of thought: Amy Freeze, meteorologist. |
| 3 | Legitimate but needs a sentence of explanation, including most translation cases. |
| 2 | Weak or arguable; the link is loose or the surname only glances at the job. |
| 1 | Highly speculative. Kept for review, not for publication. |

Score the name-to-work fit, not the person's fame. `review_status` tracks sourcing confidence
separately, so a well-known name can be `verified` with a score of 2.
