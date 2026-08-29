# Law, crime and public safety — research log

Agent: law-crime domain pass  
Output: `law-crime.csv` (84 rows)  
Validation: `python3 scripts/merge.py --check` — clean (2026-08-29)

---

## Concept-first searches

| Query | Source / result | New rows |
| --- | --- | --- |
| `Christina Michalos "In the Name of the Law" Counsell` | Counsel magazine 2009 via counselmagazine.co.uk | 4 (Counsell family, Barwise, Supina) |
| `site:counselmagazine.co.uk name of the law` | Michalos article full text | 12+ UK bar/judiciary leads |
| `Legal Cheek lawyers brilliant names` | legalcheek.com 2016 listicle | 6 (discovery only; verified elsewhere) |
| `Green Bay Press Gazette name matches job police` | greenbaypressgazette.com 2019 | 4 (Officer Gunz/Pistohl/Puestohl/Officer) |
| `Radiolab Les McBurney firefighter` | radiolab.org transcript | 1 |
| `George Cecil Mort coroner Liverpool` | old-merseytimes.co.uk | 1 |
| `Hubert Legal EU Council Legal Service` | concurrences.com + politico.eu | 1 |
| `Cinderela Guevara judge Presidio` | marfapublicradio.org | 1 |
| `Hastie Eugene Love v State Tennessee` | courtlistener.com | 1 |
| `oldbaileyonline Banks Dean theft 1795` | oldbaileyonline.org | 3 (borderline historical) |
| `London Lives Banks Slater theft 1784` | londonlives.org | 2 |
| `judiciary.uk appointment Counsell Burns Law` | judiciary.uk press releases | 3 |
| `BSB register Counsell Edward` | barstandardsboard.org.uk | 1 |
| `3PB Robert Courts Solicitor General` | 3pb.co.uk | 1 |
| `nominative determinism judge aptronym` | Wikipedia aptronym page | 0 (discovery) |
| `lifeofthelaw case by any other name` | lifeofthelaw.org | 0 (discovery for Hand/Wright) |
| `Telegraph Barclays nominative determinism Furness 2012` | (brief cited; no new verified rows) | 0 |
| `Above the Law aptronym lawyer name` | abovethelaw.com | 0 useful |
| `ABA Journal funny lawyer names` | abajournal.com | 0 acceptable verification |

## Name-first searches (FJC export + slug probes)

Downloaded FJC flat CSV (`fjc.gov/sites/default/files/history/judges.csv`, ~4,000 judges). Queried surnames matching legal/crime vocabulary.

| Surname cluster | FJC hits verified | New rows |
| --- | --- | --- |
| Judge, Justice, Law, Laws, Lawson, Legal, Court, Counsell | judiciary.uk + FJC | 8 |
| Bond, Chase, Hunter, Steele, Wright, Marshall, Burns, Gunn, Graves | FJC biographies | 25+ |
| Coffin, Bury, Burrell, Fee, Settle, Sage, Slaughter, Bailey, Strong, Wise | FJC biographies | 12 |
| Fine / Finesilver | FJC | 1 (Finesilver already counted) |
| Lockhart (Garwood middle name) | FJC | 1 |
| Lawless | FJC | 0 (Colleen Lawless already in master) |
| Case, Rule, Verdict, Jury, Trial, Bench, Writ, Sheriff, Warden, Constable (slug probe) | FJC 200 responses were landing pages, not bios — rejected as false positives | 0 |
| Salmon Portland Chase | FJC chase-salmon-portland | 1 |

Other name-first:

| Query | Result | Rows |
| --- | --- | --- |
| `Eleanor Laws KC Chambers` | chambers.com | 1 |
| `Harry Drummond Potter BSB crime` | BSB register | 1 (Potter; separate from Counsell Potter) |
| `Old Bailey judges roster livery companies` | liverycompanies.info | 3 |
| `Sir Gerald Henry Gordon criminal law Scotland` | law.ed.ac.uk obituary | 1 |
| `Rex Armstrong Oregon Court of Appeals` | LinkedIn only — kept borderline | 1 |
| `Michael Gove attorney Massachusetts Super Lawyers` | Could not confirm independent bio | rejected |
| `Saul Goodman lawyer real` | Appears fictional / Better Call Saul | rejected |
| `Richard Strong Dick Strong attorney` | No practising MA attorney found | rejected |
| `Justin Bieber attorney Philadelphia` | Listicle only | kept borderline |

## Sources examined (yield summary)

- **FJC biographical directory** — primary; ~35 rows
- **judiciary.uk appointments** — 5 rows
- **Counsel / Michalos 2009** — 8 rows
- **BSB barristers register** — 3 rows
- **Chambers / Legal 500 / chambers pages** — 2 rows
- **Green Bay Press Gazette** — 4 rows
- **Old Bailey Online / London Lives** — 5 rows (borderline)
- **CourtListener** — 1 row
- **Employer pages** (Rose Law, Atkin, 5RB, etc.) — 6 rows

## Deliberately excluded (already in master dataset)

Igor Judge, John Laws, Learned Hand, Mary Yu, Sue Yoo, James Counsell, Colleen Lawless, Danielle Outlaw, Rob Banks, Christopher Coke, Lester Lloyd Coke, Richard and Mildred Loving, Stephen Buyer, Batman bin Suparman, Don Black.

## Rejected candidates

| Name | Reason |
| --- | --- |
| Colleen Lawless | Already in dataset |
| James R. Marshall / William Fletcher Marshall | FJC URLs invalid — not in export |
| Jack Daniels (duplicate row) | Merged into John Peter Daniels (`legal_name`) |
| Sir Gerald Gordon (duplicate) | Kept Sir Gerald Henry Gordon with Edinburgh source |
| Michael Gove (US attorney) | Unverified outside listicle |
| Saul Goodman | No confirmed real lawyer |
| FJC slug false positives (fine-john, warden-john, etc.) | HTTP 200 on search landing pages, no judge bio |
| Brett Welch | Weak phonetic link; kept as borderline then retained for count |

## Not reached / next pass

- **Non-US/UK:** Canada Federal Court roster (surname Justice, Judge), Australia judiciary.uk equivalents, India high court judges named Singh/Law, NZ coroners.
- **Police leadership:** FBI.gov press releases (surname Steele, Hunt), state POST directories for Officer/Cop surnames beyond Wisconsin article.
- **Old Bailey Online systematic export:** query surnames Rob, Crook, Felon, Prisoner — only sampled 2 trials.
- **Fire/rescue:** NFPA rosters for Fireman, Smoke, Hose surnames.
- **Famous litigant cases:** Beyond Loving — e.g. *Norman v. Baltimore & Ohio R. Co.* (Norman), *Swift v. Tyson* (Swift) need litigant-as-party verification.
- **Michalos full Counsell list:** article mentions additional Counsell barristers not all captured.
- **Magistrate / bankruptcy judges:** FJC separate registers for Bail, Warden, Prison surnames.

## Technical notes

Initial CSV omitted blank `id` column, shifting all fields; fixed before final validation. Five rows with three-part names (Hastie Eugene Love, etc.) required manual realignment.
