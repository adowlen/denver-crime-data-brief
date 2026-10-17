"""Build neighborhood housing-unit denominators for the Denver crime brief.

Source: ACS 2024 5-year estimates, table B25001 (total housing units),
tract level for Denver County (08031), via Census Reporter API
(archived JSON in package data/). Tract polygons: Census TIGER 2024.
Neighborhood polygons: warehouse layers/neighborhoods_clean.parquet.

Method: intersect tract polygons with statistical-neighborhood
polygons; allocate each tract's housing units to neighborhoods in
proportion to the intersected land area (area-weighted allocation).
Units in tract area falling outside every neighborhood polygon are
reported as unallocated, never silently redistributed.

Cross-check anchors (STR specimen, 2026-10-16, same ACS vintage):
citywide allocated total 357,551; Five Points 15,639 units.
"""
import json
import pandas as pd
import geopandas as gpd
from shapely import wkb

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-crime-brief-2026-10-17"
STACK = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/stack/denver"

# --- tracts + B25001 ---
acs = json.load(open(f"{PKG}/data/acs_b25001_tracts_denver.json"))
rows = []
for geoid, v in acs["data"].items():
    rows.append({"GEOID": geoid.split("US")[-1],
                 "units": v["B25001"]["estimate"]["B25001001"]})
units = pd.DataFrame(rows)
print("county B25001 total:", units["units"].sum(), "| tracts:", len(units))

tracts = gpd.read_file(f"{PKG}/data/tl_2024_08_tract.zip")
tracts = tracts[tracts["COUNTYFP"] == "031"][["GEOID", "geometry"]]
tracts = tracts.merge(units, on="GEOID", how="inner")
print("tracts joined:", len(tracts), "| units on joined tracts:", tracts["units"].sum())
tracts = tracts.to_crs(2877)  # Colorado State Plane Central (feet) for area math
tracts["tract_area"] = tracts.geometry.area

# --- neighborhoods ---
nb = pd.read_parquet(f"{STACK}/layers/neighborhoods_clean.parquet")
nb["geometry"] = nb["geometry_wkb"].map(wkb.loads)
nbg = gpd.GeoDataFrame(nb[["NBHD_NAME", "geometry"]], geometry="geometry", crs=4326).to_crs(2877)

inter = gpd.overlay(tracts, nbg, how="intersection")
inter["share"] = inter.geometry.area / inter["tract_area"]
inter["alloc_units"] = inter["units"] * inter["share"]
alloc = inter.groupby("NBHD_NAME")["alloc_units"].sum().reset_index()

county_total = units["units"].sum()
allocated_total = alloc["alloc_units"].sum()
print(f"allocated total: {allocated_total:,.0f} | unallocated: {county_total - allocated_total:,.0f} "
      f"({(county_total - allocated_total) / county_total * 100:.2f}%)")
print("Five Points allocated:", alloc.loc[alloc["NBHD_NAME"] == "Five Points", "alloc_units"].values)

alloc = alloc.rename(columns={"alloc_units": "acs_units"})
alloc["acs_units"] = alloc["acs_units"].round(1)
alloc.to_csv(f"{PKG}/data/neighborhood_units_acs2024.csv", index=False)
print("wrote", f"{PKG}/data/neighborhood_units_acs2024.csv", "rows:", len(alloc))
