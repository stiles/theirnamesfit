# Arts, media and letters research log

Agent run: 2026-08-29. Target: 90+ verified rows for `data/staging/arts-media.csv`.

## Strategy A — Concept-first (aptronym / nominative determinism literature)

| Query | Source | New candidates |
| --- | --- | --- |
| `aptronym arts media novelist poet musician journalist` | Wikipedia [Aptronym](https://en.wikipedia.org/wiki/Aptronym) | DeWitt, Pressman, Rock, Music, Image, Starlin, Winehouse, Leandoer, Mickey Bass |
| `site:theguardian.com aptronym writer musician artist journalist` | Guardian 2024 aptronym piece | Confirmed Wordsworth, Prose, Slaughter, Vowell, Loud (already in master); led to Weller follow-up |
| `site:theguardian.com nominative determinism Colin Bass` | Guardian Mind Your Language 2014 | Colin Bass pattern (already in master); led to BBC/Guardian arts lists |
| `novelist poet musician aptronym nominative determinism` | Herald & News, Slate, New Scientist refs | Longfellow, Goldsmith, Webster, Burns |
| `composer Verdi green translation aptronym` | The New World etymology blog | Verdi, Mahler surname = Maler |
| `Mickey Bass bassist aptronym` | Wikipedia aptronym list | Mickey Bass |
| `Akira Kurosawa surname meaning black` | Wikipedia Kurosawa (surname) | Akira and Kiyoshi Kurosawa |
| `journalist Wolf Blitzer Stone Phillips aptronym` | Wikipedia Wolf Blitzer (Barak/blitz) | Blitzer, Phillips |
| `C. Sharpe Minor organist aptronym Paul Dickson` | LA Daily Mirror, AFI Catalog | C. Sharpe Minor |
| `AuthorAptronyms tomfolio` | Gwen Foss book-dealer list | Twining Lynes, author-title pairs (used Lynes only) |
| `Liniker Brazilian musician Gary Lineker Guardian` | Guardian Dec 2024 | Liniker |
| `oakland aptronyms Michael Bang musician` | Oaklandside 2026 | Michael Bang |
| `Vivien Goldman journalist music` | Wikipedia, official site | Vivien Goldman |
| `Mary Brush architect aptronym` | brusharchitects.com | Mary Brush |
| `Roger Light painter Alison Light` | Artist websites | Roger Light, Alison Light |
| `Anthony Weller novelist poet musician` | anthonyweller.com, Boston Globe obit | Anthony Weller |
| `Robert Burns surname meaning stream` | scotch.scot surname page | Robert Burns |
| `David Rodigan reggae DJ Guardian` | Guardian 2017 profile | David Rodigan |
| `Patience Scales piano teacher nominative determinism` | Nominative determinism Wikipedia | Patience Scales (probable) |
| `Gary Oldman Gary Numan aptronym` | Wikipedia aptronym inaptronym note | Paired Oldman/Numan row |

## Strategy B — Name-first (surname × occupation directories)

| Surname cluster | Search approach | Verified finds |
| --- | --- | --- |
| Press, Headline, Herald, Tribune | Masthead grep + Wikipedia | Pressman (new); Headline already in master |
| Rock, Music, Song, Bass, Beat | AllMusic / Wikipedia musician search | Rock, Music, Bass, Beat |
| Glass, Cage, Zimmer, Verdi, Mahler | Composer Wikipedia + Wiktionary | Glass, Cage, Zimmer, Verdi, Mahler, Strauss, Liszt, Mozart |
| Wordsworth, Prose, Reade, Goldsmith, Webster, Longfellow | Literary Wikipedia | Goldsmith, Longfellow, Webster, Burns, Blake (Prose/Reade/Wordsworth in master) |
| Webb, Starlin, Image, Winehouse | Wikipedia aptronym cross-check | Starlin, Image, Winehouse (Webb in master) |
| Light, Brush, Stone, Carpenter, Arch | RIBA/AIA adjacent + artist sites | Mary Brush, Roger/Alison Light, Carpenter, Christopher Wren |
| Blitzer, Tapper, Phillips, Amanpour, Huffington | Broadcast Wikipedia | Blitzer, Phillips, Tapper, Amanpour, Huffington, Shepard Smith, Peter Baker |
| Lang, Herzog, Visconti, Kurosawa, Manet, Monet | Non-English translation via Wiktionary/Wikipedia | Lang, Herzog, Visconti, Kurosawa×2, Manet, Monet, Lange, Spiegelman |
| Houdini, Copperfield, Jillette, Astaire | Performance Wikipedia | Houdini, Copperfield, Jillette, Astaire, Pavlova |
| Sting, Bono, Ringo Starr, Yung Lean | Stage-name status checks | Sting, Bono, Ringo Starr, Leandoer |

## Master-file deduplication

Checked `cut -d, -f2 data/aptronyms.csv` and staging files before recording. **Excluded** (already in master or canonical staging): William Wordsworth, Francine Prose, Charles Reade, Colin Bass, David Loud, Karin Slaughter, Sarah Vowell, Marc Webb, Max Schreck, Lumière brothers, Frank Beard, Rem Koolhaas, William Headline, Sunny Hostin, Marilyn vos Savant, Emily Wines, Lionel Tiger/Robin Fox.

## Sources examined (yield)

| Source | Rows added |
| --- | ---: |
| Wikipedia biographies | ~95 |
| Wiktionary / etymonline (translation rows) | ~25 |
| Guardian / Boston Globe / Oaklandside / LA Daily Mirror | ~12 |
| Official artist/architect sites | 4 |
| Tomfolio AuthorAptronyms (discovery → Wikipedia/other verify) | 1 |
| AFI Catalog (C. Sharpe Minor) | 1 |

## Rejected candidates

| Name | Reason |
| --- | --- |
| Cardinal Rapsong | Cited only in New Scientist anecdote; could not verify as real Vatican spokesman |
| Peter Baker (journalist) | Weak fit; kept at score 2 borderline only after NYT bio confirmed |
| Claude Monet (first draft) | Required Wiktionary monnaie citation; kept as probable homophone pun |
| Alfred Hitchcock (ACPO spokesman) | Already in master as different person; used film director instead |
| Joséphine Bacon | In master as food writer |
| Dr. Dre / Dr. Drai | Medicine/music crossover; outside brief |
| Vivien Goldman "Goldman=gold records" | Kept at score 3; almost rejected as stretch |
| Many "borderline" painters (Magritte, O'Keeffe) | Kept with score 2 and borderline status rather than dropped |

## Not reached / next pass

- **Paired-name deep dive:** more co-author pairs like Tiger/Fox in arts (e.g. Horn/Excell hymn editors from Tomfolio — need person-level verification).
- **Historical scribes:** medieval scriptorium names (e.g. literary "Scribe" surnames in British Library catalogues).
- **Chinese/Japanese/Korean:** beyond Kurosawa, Lang Lang, Takemitsu, Miyazaki — search conductor 音 (sound) surnames, Korean novelist named Ha (하).
- **Architecture:** Bridge, Arch, Tower surnames in RIBA/AIA directories (Mary Brush found; Bridge/Arch not yet).
- **Ironic critics:** Deaf/Blind surnames among art/music critics — no confirmed cases after NYT/Guardian search.
- **Magicians:** searched Trick, Vanish — no verified professional names beyond Houdini/Copperfield/Jillette.
- **Press surnames:** Herald, Chronicle, Gazette among bylined reporters — high promise, needs masthead trawl.

## Output summary

- **122 rows** in `arts-media.csv`
- **Score distribution:** 5→7, 4→27, 3→56, 2→32
- **Review status:** verified 84, probable 6, borderline 32
- Validation: `python3 scripts/merge.py --check` — arts-media.csv passes isolated validation (Salvador Dalí translation row fixed with Wiktionary URL)
