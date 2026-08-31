PY ?= python3

# Research files from the first two passes, whose row order defines the id space that the
# audit correction files are keyed to. Order matters: rebuild always replays these first.
GEN1 = canonical.csv law-crime.csv medicine.csv sports-individual.csv \
       sports-northamerica.csv sports-world.csv science.csv politics-military.csv \
       weather-nature.csv arts-media.csv business-food-faith-trades.csv translation.csv \
       historical.csv

# Third-pass research, merged on top with sticky ids. Append only: inserting a file earlier in
# this list would hand new ids to people who already have them.
GEN2 = sports-gaps.csv archives.csv translation-gaps.csv professions-gaps.csv restored.csv \
       sports-skipped.csv skubal.csv

.PHONY: all rebuild check urls enrich npi dates db stats site-data clean-db

## Rebuild the master dataset from scratch, deterministically.
rebuild:
	$(PY) scripts/merge.py --fresh --key name --only $(GEN1) | tail -4
	$(PY) scripts/audit.py apply
	$(PY) scripts/merge.py --only $(GEN2) | tail -6
# Applied twice on purpose. The first pass is what the auditors reviewed and defines the gen-1
# id space; the second lets a correction target a gen-2 row, whose id does not exist yet above.
# audit.py apply is idempotent, so the repeat is free.
	$(PY) scripts/audit.py apply
	$(PY) scripts/integrity.py --apply | tail -8
	$(PY) scripts/merge.py --check | tail -4

## Everything, including the network passes. Slow.
all: rebuild enrich db site-data stats

check:
	$(PY) scripts/merge.py --check

## Confirm every source URL still resolves. Writes data/url_check.csv.
urls:
	$(PY) scripts/check_urls.py

## Fill dates and detect birth names from Wikipedia leads.
enrich:
	$(PY) scripts/enrich_wikipedia.py --apply

# The two passes below write correction files rather than the master, so their output goes
# through data/audit/corrections/ and lands on the next `audit.py apply`.

## Repoint NPI rows from the registry homepage to the provider record.  (network)
npi:
	$(PY) scripts/resolve_npi.py

## Check recorded dates against the Wikipedia lead each row cites.      (network, ~3 min)
dates:
	$(PY) scripts/check_dates.py

## Build the queryable SQLite copy.
db:
	$(PY) scripts/build_db.py

## Regenerate the website's data snapshot. Commit the result; the deploy runs Node only.
site-data:
	$(PY) scripts/build_site_data.py

stats:
	$(PY) scripts/stats.py

clean-db:
	rm -f data/aptronyms.db
