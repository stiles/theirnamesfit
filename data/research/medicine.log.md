# Medicine domain research log

Research agent pass for `data/staging/medicine.csv`. Target: 80+ rigorously sourced rows.

## Searches (by strategy)

### Concept-first (scholarly / nominative determinism)

1. `Limb Limb Limb Limb nominative determinism hospital medicine 2015`
2. `Abel Influence of Names on Career Choices in Medicine Names 2010`
3. `Splatt Weedon urethral syndrome British Journal Urology 1977`
4. `Bennett Calling Dr Doctor JAMA 1992`
5. `Keaney Brady Bunch nominative determinism BMJ 2013 authors`
6. `BMJ Christmas issue nominative determinism doctors aptronym`
7. `nominative determinism doctors Brain neurologist`
8. `Thomas Edward Kill Jirgensohn doctor name change`
9. `Slovenko Kill Jirgensohn would-be doctor`
10. `Dr Pain surgeon UK GMC general surgery`
11. `Pelham Dennis dentist implicit egotism`
12. `Evening Standard nominative determinism Rash Knee Couch Bone`
13. `New Scientist Hugh Seymour optometrist nominative determinism`
14. `Smith Wesson addiction medicine physician`
15. `CK Payne urologist chronic pelvic pain`
16. `NF Flood urologist incontinence`
17. `Marie Harte cardiologist Dublin`
18. `COVID public health official apt name Corona Rintawan`

### Name-first (NPI / GMC / directories)

19. `Dr. Chopp urologist Austin Texas`
20. `urologist Burns Waterfall Ball Koch GMC register UK`
21. `C Limb R Limb D Limb orthopaedic surgeon UK`
22. `Christopher Limb surgeon GMC UK`
23. `Catherine Limb doctor nominative determinism GMC`
24. `Dr. Knee rheumatologist physician`
25. `Dr. Couch psychiatrist nominative determinism`
26. `Dr. Bone orthopaedic surgeon physician verified`
27. `physician surname Doctor GMC OR NPI verified`
28. `dermatologist Rash American Directory Physicians verified`
29. `rheumatologist Knee physician verified`
30. `Mark Payne cardiologist Dublin OR UK verified`
31. `urologist Koch GMC UK consultant`
32. `surgeon Butcher OR Blunt GMC consultant UK`
33. `veterinarian Wolfe OR Barker DVM verified university faculty`
34. `midwife Stork OR nurse Healy NHS verified`
35. `Hugh Seymour optometrist ophthalmologist nominative determinism`
36. NPI API: `last_name=Tooth&taxonomy=Urology`
37. NPI API: `last_name=Toothaker&taxonomy=Dentist`
38. NPI API: `last_name=Hart&taxonomy=Cardiovascular Disease`
39. NPI API: `last_name=Payne&taxonomy=Urology`
40. NPI API: `last_name=Payne&taxonomy=Cardiovascular Disease`
41. NPI API: `last_name=Stone&taxonomy=Urology`
42. NPI API: `last_name=Cox&taxonomy=Urology`
43. NPI API: `last_name=Dick&taxonomy=Urology`
44. NPI API: `last_name=Skinner&taxonomy=Dermatology`
45. NPI API: `last_name=Sleeper&taxonomy=Anesthesiology`
46. NPI API: `last_name=Sharp&taxonomy=Anesthesiology`
47. NPI API: `last_name=Stork&taxonomy=Obstetrics`
48. NPI API: `last_name=Kinder&taxonomy=Pediatrics`
49. NPI API: `last_name=Gore&taxonomy=Surgery`
50. NPI API: `last_name=Carver&taxonomy=Plastic Surgery`
51. NPI API: `last_name=Couch&taxonomy=Psychiatry`
52. NPI API: `last_name=Dennis&taxonomy=Dentist`
53. NPI API: `last_name=Fang&taxonomy=Dentist`
54. NPI API: `last_name=Doctor&taxonomy=Obstetrics`
55. NPI API: `last_name=Nurse&taxonomy=Registered Nurse`
56. NPI API: `last_name=Blood&taxonomy=Registered Nurse`
57. NPI API: `last_name=Koch&taxonomy=Urology`

## Sources examined → new candidates

| Source | Yield |
| --- | --- |
| Limb et al. 2015 (doi/abstract + Wikipedia table + David Limb CV) | 12 rows (Limb family + paper surname examples) |
| Splatt & Weedon 1977 BJU + David Weedon Wikipedia | 1 row (dermatopathologist Weedon; Splatt skipped as in master) |
| Abel 2010 Names (abstract) | 1 row (Aaron Doctor pattern) |
| Bennett 1992 JAMA + Balestra reply | 3 rows (Bennett, Smith, Wesson) |
| Keaney et al. 2013 BMJ + Table 1 refs | 8 rows (authors + Harte, Rash, Knee, Couch, Bone, Flood, Payne) |
| Evening Standard 2011 (Highfield) | 2 rows (Hugh Seymour, discovery links for Rash/Knee/Couch) |
| NPI Registry API (CMS) | 45+ rows (name-first verified clinicians) |
| NHS/GMC/employer pages (Leeds, Sussex, BAUS, Bupa, OSU, Auburn, etc.) | 20+ rows with stronger person_source_url |
| Wikipedia (Kill/Jirgensohn, Thomas Neill Cream) | 2 rows |

**Final row count: 89** (after removing Randall Toothaker duplicate with `canonical.csv`).

## Deliberately excluded

| Candidate | Reason |
| --- | --- |
| Jules Angst, Russell Brain, Willard Bliss, Adam Weiner, A.J. Splatt, D. Weedon, Andrew Waterhouse, Corona Rintawan, Alexander Burns Wallace, Carla Dove | Already in master dataset per task brief |
| Randall Toothaker DDS | Duplicate of `canonical.csv` entry |
| Dr. Couch (psychiatrist) without first name from New Scientist | Could not tie to a single named individual beyond NPI-listed Deborah Couch MD |
| Waterfall, Pump, Blunt, Mole (UK) as named individuals | Limb paper cites surnames in aggregate; no identifiable practitioner found without guessing |
| Hugh Dick / Brian Cox / Brian Dick | Verified via NPI taxonomy only; marked `probable` where employer not confirmed |
| Margaret Boyle, David Gore, Sheila Boyle, Richard Carver | NPI confirms specialty but not employer; `probable` |
| LinkedIn-only profiles | Not used as sole person_source_url |
| Listicle / Reddit aptronym galleries | Discovery only; never used as person_source_url |

## Gaps for a later pass

- **Midwives and nurses:** only 3 nurse/midwife-adjacent rows (Blood, Nurse, Stork OB/GYN). NMC register searches for Midwife, Cradle, Labour, Wren surnames would help.
- **Pathology / forensics / pharmacy:** no verified coroner or pharmacist rows despite NPI searches for Mortimer, Pill, Dose returning no strong hits.
- **Limb paper aggregate surnames:** Horn, Hussey, Woodcock, Waterfall, Pump, Safe, Warning, Boys, Gal, Child, Hickey — need GMC individual lookups.
- **Full Limb et al. PDF:** RCS paywall blocked automated fetch; table extracted via Wikipedia + doi abstract only.
- **Historical physicians:** Thomas Neill Cream only; Dr. Doctor as a specific named physician not isolated from Abel aggregate data.
- **COVID era:** Corona Rintawan excluded (in master); no second verified public-health apt name found.

## Score distribution

| Score | Count |
| --- | --- |
| 5 | 16 |
| 4 | 37 |
| 3 | 33 |
| 2 | 3 |
| 1 | 1 |

## Review status

| Status | Count |
| --- | --- |
| verified | 75 |
| probable | 14 |

Validation: `python3 scripts/merge.py --check` passes with 0 problems attributed to `medicine.csv`.
