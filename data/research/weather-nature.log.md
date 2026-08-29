# Weather & nature research log

Agent domain: weather, environment, natural world. Target: 90+ verified rows; 30+ broadcast meteorology.

## Search strategy

### Concept-first (aptronym / nominative determinism)

| Query | Source examined | Yield |
| --- | --- | --- |
| `Washington Post fitting names weather meteorologist Sprinkle Raines` | WaPo Capital Weather Gang 2016 list; Treehugger mirror | Led to Dallas Raines, Larry Sprinkle, Amy Freeze (master), Storm Field (master) |
| `meteorologist named Frost Snow Rain Gale site:weather.gov` | NWS glossaries; staff histories | Jack Frost (NWS Lubbock history); no active Snow/Wind surnames |
| `nominative determinism weather forecaster` | Wikipedia aptronym; WaPo PFLN archives | Pattern confirmation; cross-check only |
| `German Wetter Regen Schnee meteorologist` | de.wikipedia | Ben Wettervogel; Adrian Leyser Sturm (LinkedIn only—rejected) |
| `Finnish meteorologist Pouta fair weather` | fi.wikipedia | Pekka Pouta |
| `glaciologist surname Snow Ice Glacier` | NSIDC; GEUS; SLF | Tasha Snow; Camilla Snowman Andresen; Martin Schneebeli |
| `IPCC author surname Rain Snow Storm climate` | IPCC people pages; SciLine | Confirmed scientists (Otto, Wehner, etc.)—weak surnames, kept at score 1–2 |
| `storm chaser Reed Timmer TVN` | Wikipedia; AAE speakers | Reed Timmer—surname not apt, rejected |
| `beekeeper Beekman aptronym` | Sioux Honey; Modesto Bee | Matt Beekman |
| `ornithologist Swann Robin Bird staff` | DOI papers; BTO | Robert L. Swann; David Bird (master) |

### Name-first (surname / first-name mining)

| Query | Source examined | Yield |
| --- | --- | --- |
| `meteorologist Winters OR Winter TV` | KCRG meet-the-team; biographies.net | Joe Winters; George Winterling; John Winter; Braeden Winters (NWS) |
| `meteorologist Flood William KKCO` | kkco11news.com author page | William Flood |
| `meteorologist Lake Mackenzie KEYT` | keyt.com meet-the-team | Mackenzie Lake; Heather Lake (FOX 5) |
| `Steve Pool KOMO weather` | Wikipedia; komonews obit | Steve Pool |
| `meteorologist Bright Brighton Spectrum` | spectrumlocalnews.com | Brooke Brighton |
| `meteorologist Schwind wind Kentucky Mesonet` | kymesonet.org/about | Billy/William Schwind |
| `USDA Farmer Field Crop staff site:nrcs.usda.gov` | NRCS directory; FSA leadership | Kevin Farmer; Trina Brake (Field Operations—ironic) |
| `National Park Service ranger Forest Woods Green site:nps.gov` | NPS history pages | Forest Townsley; Phyllis Green; Kelly Woods |
| `forestry technician Woods USDA` | Humboldt thesis ack; fs.usda.gov | Natalie-Francesca Woods |
| `Sunshine Brosi forest ecologist` | usu.edu directory; USDA oak symposium PDF | Sunshine Brosi |
| `zookeeper Fox Wolf Nashville Columbus` | Nashville Zoo blog; Village Reporter | Megan Fox; Carrie Wolf Ritchie |
| `conservationist Hunter ironic Alaska` | Alaska Conservation Foundation | Celia Hunter |
| `USGS seismologist Shake Quake staff` | USGS staff profiles | Elizabeth Cochran (Quake Catcher); Douglas Given (ShakeAlert)—project-name links, score 2 |
| `Audubon ornithologist Bird Hawk site:audubon.org` | Audubon staff bios | Nat Seavy, Erik Johnson—weak; Nicole Michel—surname not apt |
| `RSPB warden Bird Hawk site:rspb.org.uk` | RSPB news | Sarah Dalrymple—surname not apt |
| `Ange Noiret TF1 meteorologist` | fr.wikipedia; 20minutes.fr | Presenter verified; Noiret not weather word—rejected |
| `Carol Kirkwood BBC weather` | BBC News retirement 2026 | Verified person; Kirkwood weak—score 1 |
| `Flip Spiceland meteorologist CNN` | AJC Radio/TV Talk | Flip Spiceland—score 2 |
| `Sven Sundgaard KARE meteorologist` | bringmethenews.com lawsuit coverage | Sven Sundgaard—Scandinavian sund |
| `Val Castor Amy Castor News 9 storm chaser` | news9.com; CBS News; OSU alumni | Val & Amy Castor |
| `Ocean Ramsey shark conservationist` | Wikipedia | Ocean Ramsey (not in master) |
| `Amy Storm meteorologist` | Wikipedia Storm Amy cyclone | No person—rejected |
| `Bill Giles BBC weather` | Guardian climate op-ed | Bill Giles—weak score 2 |
| `Ivan Gardner RHS horticulturist` | LinkedIn only—rejected for verification |
| `Kimberly Schwind WHIO meteorologist` | LinkedIn only—rejected |
| `meteorologist named Fairweather` | DOI climate-health paper | Victoria Fairweather (researcher, not forecaster) |

## Sources mined exhaustively

- **Washington Post / Treehugger** weather aptronym listicles (discovery only; each person re-verified on employer/Wikipedia).
- **NWS** Lubbock office history (Jack Frost); Anchorage Aware PDF (Nicole Sprinkles); Grand Junction staff (Braeden Winters).
- **TV station bios:** KABC (Dallas Raines), WATE (Ken Weathers), WCNC (Larry Sprinkle), KEYT (Mackenzie Lake), FOX 5 SD (Heather Lake), KCRG (Joe Winters), KKCO (William Flood), WWAY (Summer Trolli), WFTV (Tom Terry—weak), WUSA (Topper Shutt).
- **UK/International:** BBC Wikipedia bios; ITV Storm Huntley; Finnish Pekka Pouta; German Ben Wettervogel; Jersey Met (Matthew Winter).
- **USDA/USFS/USGS:** NRCS Kevin Farmer; FSA Trina Brake; Forest Service oak-silviculture author lists; USGS ShakeMap/ShakeAlert staff.
- **Conservation:** Oregon Encyclopedia (Finley); Audubon crane profile (Archibald); Alaska Conservation (Celia Hunter).

## Rejected candidates

| Name | Reason |
| --- | --- |
| Amy Freeze, Sara Blizzard, Storm Dunlop, Storm Field, Daniel Snowman, Elizabeth Weatherhead | Already in `aptronyms.csv` |
| David Bird, Jeremy Wade, Mark Avery, Carla Dove, Dustin Partridge, Keith Weed, Bob Flowerdew | Already in master |
| Reed Timmer | Real storm chaser; surname not apt |
| Nicole Mitchell | AMS profile; Mitchell not weather |
| Bill Giles (almost) | Kept at score 2—Giles not inherently weather |
| Ange Noiret | TF1 presenter verified; surname not apt |
| Ivan Gardner, Kimberly Schwind | LinkedIn-only verification |
| Ortrun Wetterteufelchen, Adrian Leyser Sturm | LinkedIn-only German candidates |
| William Wind | No such forecaster located |
| Susan Powell, Matt Taylor, Tomasz Schafernaker | Verified broadcasters; surnames not apt (score 1 if included) |
| Alan Heavens | In master as astronomer |
| George Archibald | Leading crane conservationist; surname not bird-related (score 2) |

## Output summary

- **Rows written:** 104 (`weather-nature.csv`)
- **Broadcast meteorology / weather presenters:** 56 (field `weather` with forecaster/meteorologist/presenter/storm-tracker occupation)
- **Score distribution:** 5→20, 4→30, 3→15, 2→27, 1→12
- **Validation:** `python3 scripts/merge.py --check` — no problems attributed to `weather-nature.csv`

## Strongest finds

1. **Dallas Raines** (score 5) — chief meteorologist whose surname is literally rains.
2. **Tasha Snow** (score 5) — glaciologist; NSIDC profile notes the name explicitly.
3. **Ben Wettervogel** (score 5) — German broadcast meteorologist; surname compounds Wetter + Vogel.

## Gaps for next pass

- **Environment Canada / Met Office / Bureau of Meteorology** staff directories by weather surname (Rain, Snow, Frost, Wind) barely scraped.
- **French/Spanish/Dutch** broadcast mets beyond Pouta and Wettervogel (Pluie, Nieve, Regen, Wind).
- **Beekeepers, gardeners, farmers** with direct surnames (Gardner, Field, Honey, Bloom)—Ivan Gardner needs RHS or employer page.
- **Storm chasers** beyond Castors—most famous chasers lack apt surnames.
- **IPCC/NFCCC delegates** with Weather/Climate/Rain surnames—many lead authors have ordinary surnames.
- **Score-1 rows** (12) should be reviewed for pruning before merge to master.
