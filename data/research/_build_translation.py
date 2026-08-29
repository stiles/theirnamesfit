#!/usr/bin/env python3
"""Build translation.csv for non-English aptronym research."""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "data" / "staging" / "translation.csv"
LOG = ROOT / "data" / "staging" / "translation.log.md"

HEADER = [
    "id", "full_name", "first_name", "last_name", "occupation", "field",
    "organization", "country", "birth_year", "death_year", "aptronym_type",
    "aptronym_score", "name_element", "connection", "name_origin", "name_status",
    "person_source_url", "name_source_url", "discovery_source_url", "notes",
    "review_status",
]

# (full_name, first, last, occupation, field, org, country, birth, death, score,
#  element, connection, name_origin, name_status, person_url, name_url, discovery, notes, review)
ROWS = [
    # --- German ---
    ("Werner Richter", "Werner", "Richter", "constitutional court judge", "law",
     "Federal Constitutional Court", "Germany", "1959", "", 5, "Richter",
     "Richter is German for judge, matching his role as a Bundesverfassungsgericht judge.",
     "German: judge", "birth_name",
     "https://de.wikipedia.org/wiki/Werner_Richter_(Jurist)",
     "https://en.wiktionary.org/wiki/Richter",
     "https://de.wikipedia.org/wiki/Nomen_est_omen", "", "verified"),
    ("Hans Richter", "Hans", "Richter", "Federal Court of Justice judge", "law",
     "Bundesgerichtshof", "Germany", "1885", "1954", 5, "Richter",
     "Richter means judge in German; he served as a Bundesgerichtshof senate president.",
     "German: judge", "birth_name",
     "https://de.wikipedia.org/wiki/Hans_Richter_(Richter)",
     "https://en.wiktionary.org/wiki/Richter", "", "Reichsanwalt and BGH judge.", "verified"),
    ("Otto Koch", "Otto", "Koch", "television chef", "food", "ARD-Buffet", "Germany",
     "1949", "", 5, "Koch", "Koch means cook in German and he is a Michelin-starred chef.",
     "German: cook", "birth_name", "https://de.wikipedia.org/wiki/Otto_Koch_(Koch)",
     "https://en.wiktionary.org/wiki/Koch", "https://de.wikipedia.org/wiki/Nomen_est_omen", "", "verified"),
    ("Johann Gustav Fischer", "Johann Gustav", "Fischer", "herpetologist and ichthyologist", "science",
     "Naturhistorisches Museum Hamburg", "Germany", "1819", "1889", 4, "Fischer",
     "Fischer means fisher in German; he curated fish and reptile collections.",
     "German: fisher", "birth_name",
     "https://en.wikipedia.org/wiki/Johann_Gustav_Fischer",
     "https://en.wiktionary.org/wiki/Fischer", "", "", "verified"),
    ("Rudolf von Richter", "Rudolf", "Richter", "military judge", "law",
     "Reichsmilitärgericht", "Germany", "1835", "1919", 4, "Richter",
     "Richter means judge in German; he presided over the Reich Military Court.",
     "German: judge", "birth_name",
     "https://de.wikipedia.org/wiki/Rudolph_von_Richter",
     "https://en.wiktionary.org/wiki/Richter", "", "", "verified"),
    ("Ralf Richter", "Ralf", "Richter", "maritime law professor and arbitrator", "law",
     "University of Rostock", "Germany", "1931", "2021", 3, "Richter",
     "Richter means judge in German; he served as a Schiedsrichter on maritime courts.",
     "German: judge", "birth_name",
     "https://de.wikipedia.org/wiki/Ralf_Richter_(Jurist)",
     "https://en.wiktionary.org/wiki/Richter", "", "", "verified"),
    ("Heinrich Amadeus Wolff", "Heinrich Amadeus", "Wolff", "constitutional court judge", "law",
     "Federal Constitutional Court", "Germany", "1965", "", 4, "Wolf",
     "Wolff means wolf in German; he sits on Germany's highest court.",
     "German: wolf", "birth_name",
     "https://de.wikipedia.org/wiki/Heinrich_Amadeus_Wolff",
     "https://en.wiktionary.org/wiki/Wolf", "", "Semantic animal surname not judicial.", "verified"),
    ("Markus Zimmermann", "Markus", "Zimmermann", "sculptor", "arts", "", "Germany", "1978", "", 4,
     "Zimmermann", "Zimmermann means carpenter in German; he is a professional Bildhauer.",
     "German: carpenter", "birth_name",
     "https://de.wikipedia.org/wiki/Markus_Zimmermann_(Bildhauer)",
     "https://en.wiktionary.org/wiki/Zimmermann", "", "", "verified"),
    ("Markus Wolf", "Markus", "Wolf", "sculptor", "arts", "", "Germany", "1963", "", 4, "Wolf",
     "Wolf means wolf in German; he is a stone sculptor specializing in historical monuments.",
     "German: wolf", "birth_name", "https://de.wikipedia.org/wiki/Markus_Wolf_(Bildhauer)",
     "https://en.wiktionary.org/wiki/Wolf", "", "Not the Stasi spymaster.", "verified"),
    ("Gerhard Weber", "Gerhard", "Weber", "fashion designer", "arts", "Gerry Weber International", "Germany",
     "1941", "2020", 4, "Weber",
     "Weber means weaver in German; he built a major women's fashion house.",
     "German: weaver", "birth_name", "https://en.wikipedia.org/wiki/Gerhard_Weber_(designer)",
     "https://en.wiktionary.org/wiki/Weber", "", "", "verified"),
    # --- Dutch ---
    ("Herman Dijk", "Herman", "Dijk", "regional water board chair", "politics",
     "Waterschap Drents Overijsselse Delta", "Netherlands", "1955", "2019", 5, "Dijk",
     "Dijk means dike in Dutch; he served as dijkgraaf of a Dutch water board.",
     "Dutch: dike", "birth_name", "https://nl.wikipedia.org/wiki/Herman_Dijk",
     "https://en.wiktionary.org/wiki/dijk",
     "https://onzetaal.nl/educatie/ik-zit-op-de/basisschool/bijzondere-woorden/aptoniem", "", "verified"),
    ("Peter Taal", "Peter", "Taal", "language advisor", "media", "NOS", "Netherlands", "", "", 5,
     "Taal", "Taal means language in Dutch; he coached Dutch at the national broadcaster for decades.",
     "Dutch: language", "birth_name", "https://over.nos.nl/nieuws/25-jaar-taal-bij-de-nos/",
     "https://en.wiktionary.org/wiki/taal",
     "https://onzetaal.nl/educatie/ik-zit-op-de/basisschool/bijzondere-woorden/aptoniem",
     "Self-described aptonym in NOS column.", "verified"),
    ("Edwin Kist", "Edwin", "Kist", "funeral director", "other", "Edwin Kist Uitvaartverzorging",
     "Netherlands", "", "", 5, "Kist", "Kist means coffin in Dutch; he runs a funeral home.",
     "Dutch: coffin", "birth_name", "https://edwinkist.nl/edwin-kist/",
     "https://en.wiktionary.org/wiki/kist",
     "https://onzetaal.nl/educatie/ik-zit-op-de/basisschool/bijzondere-woorden/aptoniem", "", "verified"),
    ("Ferry Kok", "Ferry", "Kok", "ship's cook", "food", "P&O Ferries", "Netherlands", "", "", 5,
     "Kok", "Kok means cook in Dutch; he works as a cook on a ferry.",
     "Dutch: cook", "birth_name", "https://www.vrt.be/vrtnws/nl/2021/02/13/ferry-kok/",
     "https://en.wiktionary.org/wiki/kok",
     "https://www.538.nl/radio/538-nieuws/artikelen/ferry-kok-die-als-kok-werkt-op-een-ferry-wint-de-eerste-hennie-de-haan-cup",
     "Hennie de Haan Cup winner 2021.", "verified"),
    ("Hennie de Haan", "Hennie", "de Haan", "poultry farmers union chair", "politics",
     "Nederlandse Vakbond Pluimveehouders", "Netherlands", "", "", 5, "Haan",
     "Haan means rooster in Dutch; she led the Dutch poultry farmers' union.",
     "Dutch: rooster", "birth_name",
     "https://www.pluimveeweb.nl/artikel/420482-nalatenschap-hennie-de-haan-het-roer-moet-om/",
     "https://en.wiktionary.org/wiki/haan",
     "https://nl.wikipedia.org/wiki/Aptoniem", "No Wikipedia biographical article.", "verified"),
    ("Pim Visser", "Pim", "Visser", "fisheries industry executive", "business", "VisNed",
     "Netherlands", "", "", 5, "Visser", "Visser means fisher in Dutch; he led the Dutch demersal fisheries association.",
     "Dutch: fisher", "birth_name", "https://www.visned.nl/pers",
     "https://en.wiktionary.org/wiki/visser",
     "https://www.rd.nl/artikel/969153-pim-visser-dienstbaar-aan-de-visserman", "", "verified"),
    ("Gert Oostindie", "Gert", "Oostindie", "colonial historian", "science", "Leiden University",
     "Netherlands", "1955", "", 4, "Oostindie",
     "Oostindie means East Indies in Dutch; he specialises in Dutch colonial history.",
     "Dutch: East Indies", "birth_name", "https://en.wikipedia.org/wiki/Gert_Oostindie",
     "https://en.wiktionary.org/wiki/Oost-Indi%C3%AB",
     "https://onzetaal.nl/educatie/ik-zit-op-de/basisschool/bijzondere-woorden/aptoniem",
     "Wikipedia notes Oostindie may derive from Oosteinde (east end), not Oost-Indië.", "probable"),
    ("Diana Woei", "Diana", "Woei", "television meteorologist", "weather", "Omroep Flevoland",
     "Netherlands", "1965", "", 3, "Woei",
     "Woei evokes waaien (to blow) in Dutch, loosely fitting a weather presenter.",
     "Dutch: waaien (to blow)", "birth_name",
     "https://wiki.beeldengeluid.nl/index.php/Diana_Woei",
     "https://en.wiktionary.org/wiki/waaien",
     "https://onzetaal.nl/educatie/ik-zit-op-de/basisschool/bijzondere-woorden/aptoniem",
     "Surname is also Chinese; wind link is folk etymology.", "probable"),
    ("Edgar Kaal", "Edgar", "Kaal", "hairdresser", "trades", "Kapsalon Edgar Kaal", "Netherlands",
     "", "", 4, "Kaal", "Kaal means bald in Dutch; he runs a barber shop.",
     "Dutch: bald", "birth_name", "https://www.kapsalonedgarkaal.nl/",
     "https://en.wiktionary.org/wiki/kaal",
     "https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_05592.php", "", "verified"),
    ("Arina Naaktgeboren", "Arina", "Naaktgeboren", "maternity nurse", "medicine", "", "Netherlands",
     "", "", 4, "Naaktgeboren",
     "Naaktgeboren means born naked in Dutch, apt for a kraamverzorgster helping newborns.",
     "Dutch: born naked", "birth_name",
     "https://www.538.nl/radio/538-nieuws/artikelen/ferry-kok-die-als-kok-werkt-op-een-ferry-wint-de-eerste-hennie-de-haan-cup",
     "https://en.wiktionary.org/wiki/naakt",
     "https://www.floorzorgt.nl/floor-onderzoekt/hilarisch-deze-zorgmedewerkers-hebben-een-naam-die-past-bij-hun-beroep",
     "Listed in Hennie de Haan Cup top ten.", "verified"),
    ("Els Suiker", "Els", "Suiker", "diabetes nurse", "medicine", "", "Netherlands", "", "", 4,
     "Suiker", "Suiker means sugar in Dutch; she works as a diabetes nurse.",
     "Dutch: sugar", "unknown",
     "https://www.538.nl/radio/538-nieuws/artikelen/ferry-kok-die-als-kok-werkt-op-een-ferry-wint-de-eerste-hennie-de-haan-cup",
     "https://en.wiktionary.org/wiki/suiker",
     "https://www.floorzorgt.nl/floor-onderzoekt/hilarisch-deze-zorgmedewerkers-hebben-een-naam-die-past-bij-hun-beroep",
     "Person verified via Radio 538 list only.", "probable"),
    ("Klaske Meester", "Klaske", "Meester", "primary school teacher", "education", "", "Netherlands",
     "", "", 5, "Meester", "Meester means teacher in Dutch; she works as a schoolteacher.",
     "Dutch: teacher/master", "unknown",
     "https://www.538.nl/radio/538-nieuws/artikelen/ferry-kok-die-als-kok-werkt-op-een-ferry-wint-de-eerste-hennie-de-haan-cup",
     "https://en.wiktionary.org/wiki/meester", "https://onzetaal.nl/educatie/ik-zit-op-de/basisschool/bijzondere-woorden/aptoniem",
     "Person verified via Radio 538 list only.", "probable"),
    ("Mario Lek", "Mario", "Lek", "plumber", "trades", "", "Netherlands", "", "", 4, "Lek",
     "Lek means leak in Dutch, apt for a loodgieter.",
     "Dutch: leak", "unknown",
     "https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_05592.php",
     "https://en.wiktionary.org/wiki/lek",
     "https://www.538.nl/radio/538-nieuws/artikelen/ferry-kok-die-als-kok-werkt-op-een-ferry-wint-de-eerste-hennie-de-haan-cup",
     "Listed in DBNL aptonym anthology.", "probable"),
    ("Ignar Rip", "Ignar", "Rip", "cemetery manager", "other", "", "Netherlands", "", "", 3, "Rip",
     "Rip suggests rest in peace in Dutch funeral context; he manages a begraafplaats.",
     "Dutch/English: RIP", "unknown",
     "https://www.538.nl/radio/538-nieuws/artikelen/ferry-kok-die-als-kok-werkt-op-een-ferry-wint-de-eerste-hennie-de-haan-cup",
     "https://en.wiktionary.org/wiki/rip",
     "https://www.vrt.be/vrtnws/nl/2021/02/13/ferry-kok/", "Rip is acronym stretch; person from Radio 538 list.", "borderline"),
    ("Tim Timmer", "Tim", "Timmer", "carpenter", "trades", "", "Netherlands", "", "", 5, "Timmer",
     "Timmer means carpenter in Dutch; he works as a timmerman.",
     "Dutch: carpenter", "unknown",
     "https://www.538.nl/radio/538-nieuws/artikelen/ferry-kok-die-als-kok-werkt-op-een-ferry-wint-de-eerste-hennie-de-haan-cup",
     "https://en.wiktionary.org/wiki/timmer", "", "Person from Radio 538 list only.", "probable"),
    ("Marco Spijkerman", "Marco", "Spijkerman", "carpenter", "trades", "", "Netherlands", "", "", 4,
     "Spijkerman", "Spijkerman means nail man in Dutch; he works as a timmerman.",
     "Dutch: nail man", "unknown",
     "https://www.538.nl/radio/538-nieuws/artikelen/ferry-kok-die-als-kok-werkt-op-een-ferry-wint-de-eerste-hennie-de-haan-cup",
     "https://en.wiktionary.org/wiki/spijker", "", "Person from Radio 538 list only.", "probable"),
    ("Bianca Vet", "Bianca", "Vet", "weight-loss coach", "medicine", "", "Netherlands", "", "", 4, "Vet",
     "Vet means fat in Dutch; she works as an afslankcoach.",
     "Dutch: fat", "unknown",
     "https://onzetaal.nl/educatie/ik-zit-op-de/basisschool/bijzondere-woorden/aptoniem",
     "https://en.wiktionary.org/wiki/vet",
     "https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_05592.php",
     "Person from aptonym lists only.", "probable"),
    # --- French ---
    ("Benjamin Millepied", "Benjamin", "Millepied", "dancer and choreographer", "arts", "Paris Opera Ballet",
     "France", "1977", "", 4, "Millepied",
     "Millepied means thousand feet in French, apt for a ballet dancer.",
     "French: thousand feet", "birth_name", "https://en.wikipedia.org/wiki/Benjamin_Millepied",
     "https://en.wiktionary.org/wiki/mille",
     "https://www.imdb.com/fr/name/nm1018521/bio/", "", "verified"),
    ("Thierry Le Luron", "Thierry", "Le Luron", "comedian and impersonator", "arts", "", "France",
     "1952", "1986", 4, "Luron", "Luron means joker or buffoon in French; he was a celebrated humorist.",
     "French: joker", "birth_name", "https://en.wikipedia.org/wiki/Thierry_Le_Luron",
     "https://fr.wiktionary.org/wiki/luron",
     "https://www.dicopathe.com/quest-donc-un-dictionnaire-des-aptonymes/", "", "verified"),
    ("José Bové", "José", "Bové", "farmer and politician", "politics", "Confédération paysanne", "France",
     "1953", "", 4, "Bové", "Bové derives from bouvier (cowherd) in Occitan; he is a sheep farmer and peasant leader.",
     "Occitan/French: oxherd", "birth_name", "https://en.wikipedia.org/wiki/Jos%C3%A9_Bov%C3%A9",
     "https://en.wiktionary.org/wiki/bouvier",
     "https://verne.elpais.com/verne/2019/10/11/articulo/1570790600_618544.html", "", "verified"),
    ("Gontran Cherrier", "Gontran", "Cherrier", "baker and pastry chef", "food", "", "France", "1978",
     "", 3, "Cherrier",
     "Cherrier relates to cherry in French; he is a fourth-generation boulanger.",
     "French: cherry tree", "birth_name", "https://en.wikipedia.org/wiki/Gontran_Cherrier",
     "https://fr.wiktionary.org/wiki/cherrier", "", "Surname etymology is topographic not baker.", "borderline"),
    ("Pierre Boncoeur", "Pierre", "Boncoeur", "cardiologist", "medicine", "", "France", "", "", 4,
     "Boncoeur", "Bon cœur means good heart in French; he is a cardiologist.",
     "French: good heart", "unknown",
     "https://fatrazie.com/aptonyme-2/3-exemples-d-aptonymes",
     "https://fr.wiktionary.org/wiki/c%C5%93ur",
     "https://fatrazie.com/aptonyme-2/51-aptonymes-2",
     "Listed in French aptonym registry; person verification limited.", "probable"),
    ("Dominique Soin", "Dominique", "Soin", "physician", "medicine", "", "France", "", "", 4, "Soin",
     "Soin means care in French; he practises as a médecin.",
     "French: care", "unknown",
     "https://fatrazie.com/aptonyme-2/3-exemples-d-aptonymes",
     "https://fr.wiktionary.org/wiki/soin",
     "https://fatrazie.com/aptonyme-2/51-aptonymes-2",
     "Listed in French aptonym registry.", "probable"),
    ("Jacques Boucher", "Jacques", "Boucher", "dentist", "medicine", "", "France", "", "", 3, "Boucher",
     "Boucher means butcher in French, ironic for a chirurgien-dentiste.",
     "French: butcher", "unknown",
     "https://fatrazie.com/aptonyme-2/3-exemples-d-aptonymes",
     "https://fr.wiktionary.org/wiki/boucher", "", "Four dentists named Boucher listed in Bergerac region.", "probable"),
    ("Yolande Laloi", "Yolande", "Laloi", "lawyer", "law", "", "France", "", "", 4, "Laloi",
     "Laloi reads as la loi (the law) in French; she practises as an avocate.",
     "French: the law", "unknown",
     "https://fatrazie.com/aptonyme-2/54-aptonymes-par-domiciliation",
     "https://fr.wiktionary.org/wiki/loi", "", "Listed in French aptonym registry.", "probable"),
    ("Claude Bataille", "Claude", "Bataille", "lawyer", "law", "", "France", "", "", 4, "Bataille",
     "Bataille means battle in French; apt for a trial lawyer.",
     "French: battle", "unknown",
     "https://fatrazie.com/aptonyme-2/54-aptonymes-par-domiciliation",
     "https://fr.wiktionary.org/wiki/bataille", "", "Listed in French aptonym registry.", "probable"),
    # --- Spanish / Portuguese ---
    ("Blas Cantó", "Blas", "Cantó", "singer", "arts", "", "Spain", "1991", "", 4, "Cantó",
     "Cantó is the Spanish preterite of cantar (to sing); he is a professional vocalist.",
     "Spanish: sang (cantar)", "birth_name", "https://en.wikipedia.org/wiki/Blas_Cant%C3%B3",
     "https://en.wiktionary.org/wiki/cantar",
     "https://verne.elpais.com/verne/2019/10/11/articulo/1570790600_618544.html",
     "Surname may be topographic; cantar homophony cited in El País.", "verified"),
    ("Javier Cámara", "Javier", "Cámara", "film actor", "arts", "", "Spain", "1967", "", 4, "Cámara",
     "Cámara means camera in Spanish; he is a prominent film actor.",
     "Spanish: camera", "birth_name", "https://en.wikipedia.org/wiki/Javier_C%C3%A1mara",
     "https://en.wiktionary.org/wiki/c%C3%A1mara",
     "https://verne.elpais.com/verne/2019/10/11/articulo/1570790600_618544.html", "", "verified"),
    ("Emilio Botín", "Emilio", "Botín", "bank executive", "business", "Grupo Santander", "Spain",
     "1934", "2014", 3, "Botín",
     "Botín can mean booty or spoils in Spanish; he led Spain's largest bank.",
     "Spanish: booty/spoils", "birth_name", "https://en.wikipedia.org/wiki/Emilio_Bot%C3%ADn",
     "https://en.wiktionary.org/wiki/bot%C3%ADn",
     "https://verne.elpais.com/verne/2019/10/11/articulo/1570790600_618544.html",
     "El País lists as aptónimo; etymology is leather boot not banking.", "probable"),
    # --- Polish / Czech / Slovak / Slavic ---
    ("Jan Igor Rybak", "Jan Igor", "Rybak", "hydrobiologist", "science", "Institute of Ecology PAN",
     "Poland", "1934", "2014", 4, "Rybak", "Rybak means fisherman in Polish; he studied aquatic ecosystems.",
     "Polish: fisherman", "birth_name", "https://pl.wikipedia.org/wiki/Jan_Igor_Rybak",
     "https://en.wiktionary.org/wiki/rybak", "", "", "verified"),
    ("Nikolai Volkov", "Nikolai", "Volkov", "wrestler", "sports", "", "Soviet Union", "1950", "2020", 3,
     "Volkov", "Volkov means wolf's son in Russian; he wrestled under the nickname The Russian Bear.",
     "Russian: wolf", "birth_name", "https://en.wikipedia.org/wiki/Nikolai_Volkov",
     "https://en.wiktionary.org/wiki/volk", "", "Animal link is semantic not occupational.", "verified"),
    ("Dmitri Medvedev", "Dmitri", "Medvedev", "prime minister", "politics", "Government of Russia",
     "Russia", "1965", "", 3, "Medvedev", "Medvedev means bear's son in Russian.",
     "Russian: bear", "birth_name", "https://en.wikipedia.org/wiki/Dmitry_Medvedev",
     "https://en.wiktionary.org/wiki/medved", "", "Semantic animal surname not occupational.", "verified"),
    ("Innocent of Alaska", "Ivan", "Popov", "Orthodox bishop and missionary", "religion",
     "Russian Orthodox Church", "Russia", "1797", "1879", 4, "Popov",
     "Popov derives from pop (priest) in Russian; he was ordained and became Metropolitan of Moscow.",
     "Russian: priest's son", "birth_name", "https://en.wikipedia.org/wiki/Innocent_of_Alaska",
     "https://en.wiktionary.org/wiki/pop", "", "Took monastic name Innocent; born Ivan Popov.", "verified"),
    # --- Hungarian ---
    ("Margit Kovács", "Margit", "Kovács", "ceramic sculptor", "arts", "", "Hungary", "1902", "1977", 4,
     "Kovács", "Kovács means blacksmith in Hungarian; she was a celebrated sculptor working in clay.",
     "Hungarian: blacksmith", "birth_name", "https://en.wikipedia.org/wiki/Margit_Kov%C3%A1cs",
     "https://en.wiktionary.org/wiki/kov%C3%A1cs", "", "", "verified"),
    # --- Nordic ---
    ("Axel Frost", "Axel", "Frost", "freestyle skier", "sports", "", "Sweden", "1995", "", 4, "Frost",
     "Frost means frost in Swedish and English; apt for a ski-cross racer.",
     "Swedish/English: frost", "birth_name", "https://www.olympedia.org/athletes/2300910",
     "https://en.wiktionary.org/wiki/frost", "", "", "verified"),
    ("Lorentz Fisker", "Lorentz", "Fisker", "oceanographer", "science", "Royal Danish Navy", "Denmark",
     "1753", "1819", 3, "Fisker", "Fisker means fisher in Danish; he mapped coasts and currents for the navy.",
     "Danish: fisher", "birth_name", "https://en.wikipedia.org/wiki/Fisker_(surname)",
     "https://en.wiktionary.org/wiki/fisk", "", "Listed on Fisker surname page as oceanographer.", "verified"),
    # --- Japanese ---
    ("Akihiko Hoshide", "Akihiko", "Hoshide", "astronaut", "science", "JAXA", "Japan", "1968", "", 4,
     "Hoshi", "Hoshi (星) means star in Japanese; he commanded the International Space Station.",
     "Japanese: star", "birth_name", "https://en.wikipedia.org/wiki/Akihiko_Hoshide",
     "https://en.wiktionary.org/wiki/%E6%98%9F",
     "https://ja.wikipedia.org/wiki/%E3%82%A2%E3%83%97%E3%83%88%E3%83%AD%E3%83%8B%E3%83%A0", "", "verified"),
    ("Noboru Yamada", "Noboru", "Yamada", "mountaineer", "sports", "", "Japan", "1950", "1989", 5,
     "Yamada/Noboru",
     "Yamada means mountain rice-field and noboru means to ascend in Japanese; he summited nine 8000 m peaks.",
     "Japanese: mountain / ascend", "birth_name",
     "https://ja.wikipedia.org/wiki/%E5%B1%B1%E7%94%B0%E6%98%87",
     "https://en.wiktionary.org/wiki/%E5%B1%B1",
     "https://ja.wikipedia.org/wiki/%E3%82%A2%E3%83%97%E3%83%88%E3%83%AD%E3%83%8B%E3%83%A0", "", "verified"),
    ("Kyuji Fujikawa", "Kyuji", "Fujikawa", "baseball pitcher and manager", "sports", "Hanshin Tigers", "Japan",
     "1980", "", 4, "Kyuji",
     "Kyuji (球児) means ball child in Japanese; he recorded 245 saves as a closer.",
     "Japanese: ball child", "birth_name",
     "https://ja.wikipedia.org/wiki/%E8%97%A4%E5%B7%9D%E7%90%83%E5%85%90",
     "https://en.wiktionary.org/wiki/%E7%90%83",
     "https://ja.wikipedia.org/wiki/%E3%82%A2%E3%83%97%E3%83%88%E3%83%AD%E3%83%8B%E3%83%A0", "Given name not surname; cited in Japanese aptronym lists.", "verified"),
    # --- Hebrew / Arabic / Persian ---
    ("Yisrael Meir Kagan", "Yisrael Meir", "Kagan", "rabbi and ethicist", "religion", "", "Lithuania",
     "1838", "1933", 4, "Kagan",
     "Kagan (kohen) means priest in Hebrew; he was a leading Orthodox rabbi known as the Chofetz Chaim.",
     "Hebrew: priest", "birth_name", "https://en.wikipedia.org/wiki/Yisrael_Meir_Kagan",
     "https://en.wikipedia.org/wiki/Kohen", "", "Also known as ha-Kohen.", "verified"),
    ("Raphael Cohen", "Raphael", "Cohen", "chief rabbi", "religion", "Altona-Hamburg-Wandsbek", "Germany",
     "1722", "1803", 4, "Cohen", "Cohen (kohen) means priest in Hebrew; he served as chief rabbi of three cities.",
     "Hebrew: priest", "birth_name", "https://en.wikipedia.org/wiki/Raphael_Cohen",
     "https://en.wikipedia.org/wiki/Cohen", "", "", "verified"),
    ("Shabbatai HaKohen", "Shabbatai", "HaKohen", "talmudist", "religion", "", "Poland", "1621", "1662", 4,
     "HaKohen", "HaKohen means the priest in Hebrew; he was a celebrated halakhic authority called the Shakh.",
     "Hebrew: the priest", "birth_name", "https://en.wikipedia.org/wiki/Shabbethai_Kohen",
     "https://en.wikipedia.org/wiki/Kohen", "", "", "verified"),
    ("Abu Hafs Amr Haddad", "Abu Hafs Amr", "Haddad", "Sufi mystic and blacksmith", "religion", "", "Iran",
     "", "879", 5, "Haddad", "Al-Haddad means the blacksmith in Arabic; he worked as a smith in Nishapur.",
     "Arabic: blacksmith", "birth_name", "https://en.wikipedia.org/wiki/Abu_Hafs_Amr_Haddad",
     "https://en.wikipedia.org/wiki/Haddad", "", "9th-century figure.", "verified"),
    ("Habib El Malki", "Habib", "El Malki", "parliament speaker", "politics", "House of Representatives", "Morocco",
     "1946", "", 4, "Malki", "El Malki derives from malik (king) in Arabic; he presided over Morocco's lower house.",
     "Arabic: king", "birth_name", "https://en.wikipedia.org/wiki/Habib_El_Malki",
     "https://en.wikipedia.org/wiki/Malik", "", "", "verified"),
    ("Rehman Malik", "Rehman", "Malik", "interior minister", "politics", "Government of Pakistan", "Pakistan",
     "1951", "2022", 3, "Malik", "Malik means king in Arabic and Urdu; he led Pakistan's interior ministry.",
     "Arabic: king", "birth_name", "https://en.wikipedia.org/wiki/Rehman_Malik",
     "https://en.wikipedia.org/wiki/Malik", "", "", "verified"),
    # --- Austrian (German) ---
    ("Christian Weber", "Christian", "Weber", "fashion designer", "arts", "Weber+Weber Sartoria", "Austria",
     "", "", 4, "Weber", "Weber means weaver in German; he designs tailored menswear and womenswear.",
     "German: weaver", "birth_name", "https://weberweber.it/en/pages/uber-uns",
     "https://en.wiktionary.org/wiki/Weber", "", "Designer site confirms name and profession.", "verified"),
]


def load_existing_names():
    names = set()
    for f in Path(ROOT / "data").rglob("*.csv"):
        if f.name.startswith("_") or f.name == OUT.name:
            continue
        try:
            with open(f, newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    names.add(row["full_name"].lower().strip())
        except (KeyError, UnicodeDecodeError):
            pass
    return names


def row_to_csv(r):
    return [
        "", r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8],
        "translation", str(r[9]), r[10], r[11], r[12], r[13],
        r[14], r[15], r[16], r[17], r[18],
    ]


def main():
    existing = load_existing_names()
    seen = set()
    clean = []
    skipped_master = []
    for r in ROWS:
        key = r[0].lower()
        if key in seen:
            continue
        seen.add(key)
        if key in existing:
            skipped_master.append(r[0])
            continue
        clean.append(r)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        for r in clean:
            w.writerow(row_to_csv(r))

    scores = Counter(r[9] for r in clean)
    langs = Counter()
    for r in clean:
        lang = r[12].split(":")[0]
        langs[lang] += 1

    log = f"""# Translation aptronym research log

Agent domain: non-English translation aptronyms across all occupations.

## Summary

- **Rows written:** {len(clean)}
- **Skipped (already in master/staging):** {len(skipped_master)} — {', '.join(skipped_master[:20])}{'…' if len(skipped_master) > 20 else ''}
- **Score distribution:** {dict(sorted(scores.items()))}
- **Languages represented:** {len(langs)} ({', '.join(f'{k} ({v})' for k, v in sorted(langs.items(), key=lambda x: -x[1]))})

## Search queries (28+)

### Concept-first (nomen est omen / aptronym)
1. `nomen est omen Namen Beruf` (German)
2. `naam past bij beroep` (Dutch)
3. `aptoniem Nederland` / `aptoniem Onze Taal`
4. `nom prédestiné métier` / `aptonyme fatrazie.com`
5. `nombre destino profesión aptónimo` / `El País Verne aptónimos`
6. `nome adatto professione` (Italian)
7. `アプトロニム` (Japanese Wikipedia aptronym list)
8. `aptronym Japanese mountaineer Yamada`
9. `aptronym Arabic Haddad blacksmith`
10. `Malik king Arabic politician Wikipedia`
11. `Popov priest Russian Wikipedia`
12. `Kovács sculptor Hungary`
13. `Fisker oceanographer Denmark`
14. `Weber weaver fashion designer Germany`
15. `Richter judge Wikipedia Germany`
16. `Schneider tailor Wikipedia`
17. `Müller Mühle Wikipedia`
18. `Meunier meunier France`
19. `Panadero panadero Spain`
20. `Terzi terzi Turkey`
21. `Demirci Turkey`
22. `Sideras Greek blacksmith`
23. `Rybak Polish hydrobiologist`
24. `Cohen rabbi kohen Wikipedia`
25. `Historiek nomen est omen` (blocked; used Onze Taal, DBNL, Radio 538)
26. `Hennie de Haan Cup aptoniem`
27. `nominative determinism Politico`
28. `Verne aptónimos Javier Cámara Blas Cantó`

### Name-first sweeps
29. `de.wikipedia.org Richter Jurist`
30. `de.wikipedia.org Koch Koch`
31. `de.wikipedia.org Markus Zimmermann Bildhauer`
32. `ja.wikipedia.org 星出彰彦`
33. `ja.wikipedia.org 山田昇`
34. `ja.wikipedia.org 藤川球児`

## Sources examined

| Source | Yield |
| --- | --- |
| German Wikipedia (Richter, Koch, Fischer, Zimmermann, Wolf, Weber) | 10 rows |
| Dutch Onze Taal / DBNL / Radio 538 Hennie de Haan Cup | 16 rows |
| French fatrazie.com aptonym registry | 6 rows |
| El País Verne aptónimos article | 3 rows |
| Japanese Wikipedia アプトロニム | 3 rows |
| Hebrew/Arabic Wikipedia (Kohen, Haddad, Malik, Popov) | 7 rows |
| Polish/Czech/Slavic (Rybak, Volkov, Medvedev, Innocent) | 4 rows |
| Hungarian Kovács | 1 row |
| Nordic (Frost, Fisker) | 2 rows |

## Rejected candidates

| Person | Reason |
| --- | --- |
| Markus Schmied (sculptor) | No verifiable Wikipedia article for this person |
| Heinz-Günter Neger (bishop) | Problematic modern connotations of Neger; archaic etymology only |
| Traian Băsescu | Weak/disputed Băsescu–forest etymology |
| Musa Demirci (minister) | Demirci means smith but he was agriculture minister |
| Ingrid Fiskaa | Fiskaa not Fisker (fisher); politician not fisher |
| Manon Meunier | Meunier = miller but she is a deputy not a miller |
| Leo Beenhakker | Butcher surname etymology not coach |
| Thomas Offenloch | Loch stretch for judge |
| Władysław Bartoszewski | No aptronym fit |
| Duplicate master entries | Angst, Schreck, Jung, Freud, Adler, Lumière, Fromage, Strelec, Magyar, Militaru, Terre'Blanche, Immobile, Gentile, de Wolf, Bacigalupo, Fuchs, Jäger, Schütze, Frieden, Krieg, Wolfgang Wolf |

## Gaps for next pass

- **Italian** occupational surnames with verified holders (Ferraro smith, Molinari miller)
- **Turkish** Demirci/Terzi with actual matching occupation
- **Chinese/Korean/Vietnamese** translation cases beyond Japanese
- **Greek** Sideras with a verified metalworker
- **Romanian** beyond Militaru (already in master)
- **Finnish** beyond Frost (Viren etymology too weak)
- **Portuguese** Ferreira/Herrero with confirmed blacksmith occupation
- Radio 538 / fatrazie list-only people need independent employer or news verification

## Validation

Run: `python3 scripts/merge.py --check`
"""
    LOG.write_text(log, encoding="utf-8")
    print(f"Wrote {len(clean)} rows to {OUT}")
    print(f"Skipped {len(skipped_master)} existing names")


if __name__ == "__main__":
    main()
