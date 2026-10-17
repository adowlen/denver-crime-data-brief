# Denver reported offenses brief - package README

Topic (Alex's evening pick, 2026-10-16): how have reported offenses in Denver changed by category and neighborhood since 2021, and how much of the change is traffic (IS_TRAFFIC) vs criminal (IS_CRIME)?

Status: BUILT, NOT PUBLISHED. Presented at the 2026-10-17 06:30 QA run for Alex's approval.

## Contents
- brief-draft.md - the brief (publishable text)
- stats.json - every figure used in the brief and social copy, produced by code/build_stats.py
- verification.md - Section 10 pre-flight audit output, Section 11 review record, warehouse deposit record
- reviewer-notes.md - claims most likely challenged, Section 11.3 flags, open items
- sources.md - dataset citations and access notes
- social-drafts.md - LinkedIn page post, personal repost comment, X thread (drafts only)
- substack-draft.md - Substack cross-post draft
- hero.png - hero graphic (generated illustration + composited verified figure; code/hero_composite.py)
- charts/ - chart_windows.png, chart_monthly.png, chart_categories.png, chart_neighborhood_rates.png
- data/ - neighborhood_panel.csv, neighborhood_units_acs2024.csv, acs_b25001_tracts_denver.json,
  traffic_accidents_service_counts.json, audit_output.txt, tl_2024_08_tract.zip (TIGER tracts)
- code/ - build_stats.py, denominators.py, audit_section10.py, charts.py, hero_composite.py, deposit_warehouse.py
- hero_source/ - the raw generated illustration before compositing

## Dependencies (match code imports)
python 3.12; pandas, numpy, pyarrow (parquet), matplotlib, Pillow (hero composite),
geopandas, shapely, pyogrio (denominators.py only). Working venv: ./.venv in this folder.

## Rebuild order
1. code/denominators.py (writes data/neighborhood_units_acs2024.csv)
2. code/build_stats.py (writes stats.json + data/neighborhood_panel.csv)
3. code/audit_section10.py (Section 10 gates; output to data/audit_output.txt)
4. code/charts.py, code/hero_composite.py

## Data provenance
Offenses: warehouse stack/denver/snapshots/2026-10-15/crime.parquet via layers/crime_clean.parquet
(reused as-is; vintage and ceiling recorded in verification.md). Traffic sizing: count-only REST
queries archived in data/. Denominators: ACS 2024 5-year B25001 via Census Reporter + TIGER 2024 tracts.
Warehouse deposit from this study: layers/crime_neighborhood_panel.parquet and
layers/acs_neighborhood_units.parquet (see verification.md).
