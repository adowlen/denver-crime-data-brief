"""Warehouse deposit for the Denver crime brief (standing deposit rule, 2026-10-16).

Deposits two derived layers on the neighborhood spine:
1. layers/crime_neighborhood_panel.parquet - long panel: one row per
   neighborhood x matched window year (Jan 1-Oct 13), with report counts,
   vehicle-group counts and shares, ACS housing units, and rates per
   1,000 units. Built from layers/crime_clean.parquet.
2. layers/acs_neighborhood_units.parquet - ACS 2024 5-year B25001
   housing units allocated to the 78 statistical neighborhoods
   (area-weighted tract allocation; see code/denominators.py).

Also updates stack/denver/manifest.json with both layers.
"""
import json
import hashlib
import pandas as pd

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-crime-brief-2026-10-17"
STACK = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/stack/denver"

panel = pd.read_csv(f"{PKG}/data/neighborhood_panel.csv")
rows = []
for r in panel.itertuples():
    for y in [2021, 2022, 2023, 2024, 2025, 2026]:
        rows.append({
            "neighborhood": r.neighborhood,
            "neighborhood_slug": r.slug,
            "window_year": y,
            "window": "Jan 1-Oct 13 (matched)",
            "reports": int(getattr(r, f"reports_{y}")),
            "acs_units_2020_2024": float(r.acs_units),
        })
long = pd.DataFrame(rows)

# vehicle counts per neighborhood-year: recompute the 2025 vehicle fields and
# derive vehicle counts for all years from the crime layer for completeness
c = pd.read_parquet(f"{STACK}/layers/crime_clean.parquet",
                    columns=["REPORTED_DATE", "OFFENSE_TYPE_ID", "NEIGHBORHOOD_ID"])
c["rdate"] = pd.to_datetime(c["REPORTED_DATE"], unit="ms", utc=True).dt.tz_convert("America/Denver")
c["year"] = c["rdate"].dt.year
win = (c["rdate"].dt.month < 10) | ((c["rdate"].dt.month == 10) & (c["rdate"].dt.day <= 13))
VEH = ["theft-of-motor-vehicle", "theft-items-from-vehicle",
       "theft-parts-from-vehicle", "criminal-mischief-mtr-veh"]
w = c[win & (c["year"] >= 2021)].copy()
w["is_vehicle"] = w["OFFENSE_TYPE_ID"].isin(VEH)
import re, unicodedata
def slug(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
nb = pd.read_parquet(f"{STACK}/layers/neighborhoods_clean.parquet")[["NBHD_NAME"]]
name2slug = {n: slug(n) for n in nb["NBHD_NAME"]}
long["neighborhood_slug"] = long["neighborhood"].map(name2slug)
veh = w.groupby(["NEIGHBORHOOD_ID", "year"])["is_vehicle"].sum().reset_index()
veh_map = {(slug(k) if isinstance(k, str) else None, y): int(v)
           for k, y, v in veh.itertuples(index=False)}
long["vehicle_reports"] = [veh_map.get((s, y), 0) for s, y in
                            zip(long["neighborhood_slug"], long["window_year"])]
long["vehicle_share_pct"] = (long["vehicle_reports"] / long["reports"] * 100).round(1)
long["rate_per_1000_units"] = (long["reports"] / long["acs_units_2020_2024"] * 1000).round(1)
long.to_parquet(f"{STACK}/layers/crime_neighborhood_panel.parquet", index=False)
print("crime_neighborhood_panel:", long.shape)

units = pd.read_csv(f"{PKG}/data/neighborhood_units_acs2024.csv")
units = units.rename(columns={"NBHD_NAME": "neighborhood", "acs_units": "acs_units_2020_2024"})
units["neighborhood_slug"] = units["neighborhood"].map(name2slug)
units["source"] = "ACS 2024 5-year B25001 tract level, area-weighted allocation to statistical neighborhoods"
units[["neighborhood", "neighborhood_slug", "acs_units_2020_2024", "source"]].to_parquet(
    f"{STACK}/layers/acs_neighborhood_units.parquet", index=False)
print("acs_neighborhood_units:", units.shape)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

import os
man = json.load(open(f"{STACK}/manifest.json"))
names = [l["name"] for l in man["layers"]]
for entry in [
    {
        "name": "crime_neighborhood_panel",
        "title": "Reported offenses by statistical neighborhood and matched window year (derived)",
        "source_dataset": "Derived in the 2026-10-17 crime brief from ODC_CRIME_OFFENSES_P (layers/crime_clean) + ACS denominators (layers/acs_neighborhood_units)",
        "snapshot_date": "2026-10-17",
        "row_count": int(len(long)),
        "coverage": "78 statistical neighborhoods x matched Jan 1-Oct 13 windows, 2021-2026; REPORTED_DATE ceiling 2026-10-13",
        "key_fields": ["neighborhood_slug", "window_year"],
        "status": "derived layer (study deposit)",
        "refresh_cadence": "rebuild when crime_clean refreshes or the brief is re-run",
        "files": [{"path": "layers/crime_neighborhood_panel.parquet", "role": "derived layer",
                   "size_bytes": os.path.getsize(f"{STACK}/layers/crime_neighborhood_panel.parquet"),
                   "sha256": sha(f"{STACK}/layers/crime_neighborhood_panel.parquet")}],
        "notes": "Join rates: crime NEIGHBORHOOD_ID matched to neighborhoods 99.90% of rows (381 of 383,643 null, excluded). Vehicle group = 4 OFFENSE_TYPE_IDs (vehicle theft, items from vehicle, parts from vehicle, criminal mischief to vehicle). Rates use the ACS cross-section for all years; see brief verification.md.",
    },
    {
        "name": "acs_neighborhood_units",
        "title": "ACS housing units by statistical neighborhood (denominator layer)",
        "source_dataset": "US Census Bureau ACS 2024 5-year estimates, table B25001, tract level (Census Reporter), TIGER 2024 tract polygons",
        "snapshot_date": "2026-10-17",
        "row_count": int(len(units)),
        "coverage": "78 statistical neighborhoods; Denver County total 359,581 units, 359,351 allocated (99.94%), 230 in boundary slivers unassigned",
        "key_fields": ["neighborhood_slug"],
        "status": "derived layer (study deposit)",
        "refresh_cadence": "rebuild on each ACS 5-year release or when a study needs a fresher denominator",
        "files": [{"path": "layers/acs_neighborhood_units.parquet", "role": "derived layer",
                   "size_bytes": os.path.getsize(f"{STACK}/layers/acs_neighborhood_units.parquet"),
                   "sha256": sha(f"{STACK}/layers/acs_neighborhood_units.parquet")}],
        "notes": "Area-weighted allocation of tract housing units to neighborhood polygons. Cross-check: Five Points 15,648 units vs the 2026-10-16 STR specimen's 15,639 (0.06% delta). General-purpose denominator for any per-housing-unit rate on the neighborhood spine.",
    },
]:
    if entry["name"] not in names:
        man["layers"].append(entry)
man["built"] = "2026-10-17"
json.dump(man, open(f"{STACK}/manifest.json", "w"), indent=1)
print("manifest layers now:", len(man["layers"]))
