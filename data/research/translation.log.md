# Translation aptronym research log

Agent domain: non-English translation aptronyms across all occupations.

## Summary

- **Rows written:** 138 (55 original research + 83 imported from sibling staging files, deduped against `data/aptronyms.csv` only)
- **Score distribution:** 2→9, 3→41, 4→68, 5→20
- **Review status:** verified 105, probable 23, borderline 10
- **Languages represented:** 25 (Arabic, Chinese, Czech, Danish, Dutch, Finnish, French, German, Greek, Hebrew, Hungarian, Italian, Japanese, Latin, Lithuanian, Occitan/French, Persian, Polish, Romanian, Russian, Serbo-Croatian, Slovak, Spanish, Turkish, Yiddish/German)

## Search queries (34)

### Concept-first (nomen est omen / aptronym)
1. `nomen est omen Namen Beruf` (German)
2. `naam past bij beroep` / `aptoniem Nederland` / `aptoniem Onze Taal`
3. `nom prédestiné métier` / `aptonyme fatrazie.com`
4. `nombre destino profesión aptónimo` / El País Verne aptónimos
5. `nome adatto professione` (Italian)
6. `アプトロニム` (Japanese Wikipedia aptronym list)
7. `aptronym Arabic Haddad blacksmith`
8. `Malik king Arabic politician Wikipedia`
9. `Popov priest Russian Wikipedia Innocent Alaska`
10. `Kovács sculptor Hungary`
11. `Fisker oceanographer Denmark`
12. `Weber weaver fashion designer Germany`
13. `Richter judge Wikipedia Germany`
14. `Schneider tailor Wikipedia`
15. `Müller Mühle Wikipedia`
16. `Meunier meunier France`
17. `Panadero panadero Spain`
18. `Terzi terzi Turkey`
19. `Demirci Türkiye milletvekili`
20. `Sideras Greek blacksmith`
21. `Rybak Polish hydrobiologist`
22. `Cohen rabbi kohen Wikipedia`
23. `Historiek nomen est omen` (Cloudflare-blocked; used Onze Taal, DBNL, Radio 538)
24. `Hennie de Haan Cup aptoniem`
25. `nominative determinism Politico`
26. `Verne aptónimos Javier Cámara Blas Cantó`
27. `山田昇 登山家 Wikipedia`
28. `星出彰彦 宇宙飛行士 Wikipedia`
29. `藤川球児 セーブ Wikipedia`

### Name-first sweeps
30. `de.wikipedia.org Richter Jurist`
31. `de.wikipedia.org Otto Koch Koch`
32. `de.wikipedia.org Markus Zimmermann Bildhauer`
33. `de.wikipedia.org Markus Wolf Bildhauer`
34. `site:de.wikipedia.org Müller Mühle`

## Sources examined

| Source | New candidates yielded |
| --- | --- |
| German Wikipedia (Richter, Koch, Fischer, Zimmermann, Wolf, Weber) | 10 |
| Dutch Onze Taal / DBNL / Radio 538 Hennie de Haan Cup | 16 |
| French fatrazie.com aptonym registry | 6 |
| El País Verne aptónimos (2019) | 3 |
| Japanese Wikipedia アプトロニム | 3 |
| Hebrew/Arabic Wikipedia (Kohen, Haddad, Malik, Popov) | 7 |
| Polish/Slavic (Rybak, Volkov, Medvedev, Innocent of Alaska) | 4 |
| Hungarian Kovács (Margit Kovács) | 1 |
| Nordic (Frost, Lorentz Fisker) | 2 |
| Sibling staging CSVs (arts-media, politics-military, etc.) | 83 imported |

## Strongest original finds (this pass)

1. **Herman Dijk** — Dutch *dijk* (dike) + dijkgraaf of a water board (score 5)
2. **Noboru Yamada** — Japanese 山 (mountain) + 昇 (ascend) + Himalayan mountaineer (score 5)
3. **Abu Hafs Amr Haddad** — Arabic *haddad* (blacksmith) + 9th-century Sufi who was a smith (score 5)

## Rejected candidates

| Person | Reason |
| --- | --- |
| Markus Schmied (sculptor) | No verifiable Wikipedia article |
| Heinz-Günter Neger (bishop) | Problematic modern connotations; archaic etymology only |
| Traian Băsescu | Weak/disputed forest etymology |
| Musa Demirci | Demirci = smith but agriculture minister |
| Ingrid Fiskaa | Fiskaa ≠ fisker; politician not fisher |
| Manon Meunier | Meunier = miller but deputy not miller |
| Leo Beenhakker | Butcher surname not coach |
| Thomas Offenloch | Loch stretch for judge |
| Master duplicates | Angst, Schreck, Jung, Freud, Adler, Lumière brothers, Fromage, Strelec, Magyar, Militaru, Terre'Blanche, Immobile, Gentile, de Wolf, Bacigalupo, Fuchs, Jäger, Schütze, Frieden, Krieg, Wolfgang Wolf |

## Gaps for next pass

- Italian occupational surnames with verified holders in that trade (Ferraro, Molinari)
- Turkish Demirci/Terzi with actual matching occupation
- Chinese/Korean/Vietnamese beyond arts names already in staging
- Greek Sideras with verified metalworker
- Portuguese Ferreira/Herrero with confirmed blacksmith occupation
- Radio 538 / fatrazie list-only Dutch and French entries need independent verification

## Validation

```
python3 scripts/merge.py --check
```

No row-level problems attributed to `translation.csv` (issues only in `historical.csv`).
