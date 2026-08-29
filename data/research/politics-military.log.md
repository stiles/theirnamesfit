# Politics & military research log

Date: 2026-08-29  
Output: `data/staging/politics-military.csv` — **94 rows**, 0 validation errors

## Searches (grouped by strategy)

### Concept-first / listicle mining
- `Politico brief history names that sound like jobs politicians 2018`
- `Chad Pergram Speaker's Lobby General Admiral Fox News 2018`
- `Slate Timothy Noah aptronym politics nominative determinism`
- `Wikipedia aptronym politics military`
- `nominative determinism politician aptronym`
- `White House press secretary aptronym name fitting spokesperson`
- `Barney Frank franking privilege aptronym congress`
- `Stephen Buyer congress insider trading aptronym`
- `Donald Trump aptronym trump card winning name`
- `Moses Blah Liberia vice president aptronym`
- `Mike Hookem UKIP fisheries spokesman aptronym`
- `Bill Cash MP aptronym expenses`
- `General Coward British army aptronym`
- `George Marshall Marshal Marshall general aptronym`
- `Roman consul aptronym cognomen fitting name politician`
- `Gnaeus Julius Agricola Roman general name meaning farmer`
- `politician aptronym translation German Frieden Krieg`

### Name-first / bioguide.congress.gov
- `site:bioguide.congress.gov King senator representative`
- `site:bioguide.congress.gov Major representative senator`
- `site:bioguide.congress.gov Captain congressman`
- `site:bioguide.congress.gov COLONEL congressman`
- `site:bioguide.congress.gov SERGEANT congress`
- `site:bioguide.congress.gov SPEAKER congressman`
- `site:bioguide.congress.gov GENERAL surname congress`
- `site:bioguide.congress.gov Freeman Justice Hunter Bowman Archer Steele representative`
- `Joseph Gurney Cannon Speaker House cannon surname bioguide`
- `John Sergeant congressman Pennsylvania bioguide`
- `James Earl Major congressman Illinois bioguide`
- `Gouverneur Morris senator aptronym govern`
- `Baron Hill congressman Indiana bioguide`
- `Brian Mast congressman Florida veteran bioguide`
- `Howard Cannon senator Nevada bioguide`
- `Jim Justice West Virginia governor senator bioguide`
- `John Doolittle congressman California bioguide`
- `Francis E. Warren senator Wyoming Fort Warren bioguide`
- `Preston Brooks congressman bioguide South Carolina`
- `Peter King congressman New York bioguide`
- `Kelly Armstrong congressman North Dakota Wikipedia`
- Grep of Congress.gov bioguide ID list for: Cannon, Major, King, Hunter, Bowman, Archer, Steele, Strong, Wise, Knight, Lance, Camp, Levy, Savage, Slaughter, Marshall, McGovern, Franks, Bond, Cloud, Brooks, Grimm, Armstrong, Chamberlain

### UK / EU / non-Anglophone
- `Michael Lord House of Lords Conservative peer`
- `Luc Frieden Luxembourg prime minister Wikipedia`
- `Ivo Krieg German politician Grünen Landtag`
- Politico EU article names: Cheesley, Von Essen, Marinus, Hookem, Moses Blah, Hubert Legal (Legal already in master)

### Military rosters
- `Major-General J.J. Major Canadian Army bio`
- `Karl B. Major USAF test pilot airandspace.si.edu`
- `CAPT Albert S. Major Jr USN usnamemorialhall`
- `Andrew Hull Foote admiral Civil War Wikipedia`
- `Gouverneur Kemble Warren general Civil War`

## Sources examined (new candidates yielded)

| Source | Yield |
| --- | --- |
| Politico EU nominative-determinism column (Apr 2018) | Moses Blah, Mike Hookem, Amanda Cheesley, Garlich Von Essen, Lieselot Marinus |
| Wikipedia Aptronym page | George McGovern, Stephen Buyer, Donald Trump, Leon Brittan, Danielle Outlaw (excluded — in master) |
| Fox News Pergram "General Admiral" (Dec 2018) | Kevin Admiral (excluded — in master); Marshall Marshal Marshall anecdote |
| Slate / Ukiah Daily Journal on Barney Frank | Barney Frank |
| bioguide.congress.gov member ID grep | ~40 surname-first congress hits (Major, Cannon, King, Hunter, Camp, etc.) |
| history.house.gov biographies | Sergeant, Cannon, Brooks, Preston Brooks, Jack Brooks |
| members.parliament.uk / Wikipedia | Michael Lord, William Cash |
| de.wikipedia.org / gouvernement.lu | Luc Frieden, Ivo Krieg |
| Roman Wikipedia entries | Catus, Pius, Strabo, Agricola, Publicola, Spinther |
| warren.af.mil base history | Francis E. Warren |

## Rejected candidates

| Name | Reason |
| --- | --- |
| Chad Pergram | Pergram has no documented name–job link; he only reported on others' aptronyms |
| Kevin Admiral, Josh Earnest, Larry Speakes, etc. | Already in `data/aptronyms.csv` |
| Danielle Outlaw, Jaime Sin | Already in master (law/religion fields); removed after dedupe check |
| Preston Brooks | Brooks is geographic; no credible aptronym reading for cane assault |
| Louise Slaughter | Kept at score 2/borderline — stretch for legislator |
| Pierre Salinger, Jay Carney, Scott McClellan, Dana Perino | Weak phonetic links; kept at borderline only as press-secretary sub-genre samples |
| Samuel Foote (congress) | Foot Resolution is wordplay on Foot surname but very weak |
| Elizabeth Warren, Rick Scott, Tim Scott | Common surnames; score 2 borderline padding only |
| Hubert Legal | In master file |

## Score distribution

| Score | Count |
| --- | --- |
| 5 | 6 |
| 4 | 28 |
| 3 | 33 |
| 2 | 27 |

Fields: 82 politics, 12 military.

## Gaps / next pass

- **Spy/Secret/Shadow surnames**: no verified intelligence officials found on bioguide; try CIA press releases and UK MI5 obituaries.
- **Vote/Ballot/Lobby/Tax/Treasury surnames**: sparse in Congress; state legislator directories (Open States) likely richer.
- **More press secretaries**: Jen Psaki, Karine Jean-Pierre, Kayleigh McEnany lack strong name links; Ari Fleischer similarly weak.
- **Non-Anglophone ministers**: hunt Polish `Wojna`/`Pokój`, Spanish `Guerra`/`Paz`, Italian `Soldato`, French `Ministre`-homophone surnames with official government bios.
- **bioguide.congress.gov direct API**: site blocks some browser fetches; retro.congress.gov or history.house.gov grep productive.
- **Irony bucket**: defence ministers named Peace, generals named Coward (Charles Coward added); search CWGC and UK MOD for more.
