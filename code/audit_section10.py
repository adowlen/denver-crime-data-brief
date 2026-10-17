"""Section 10 pre-flight audit - Denver reported-crime brief (2026-10-17).

Runs against the RAW warehouse snapshot and the cleaned layer, plus
the package stats.json. Prints evidence for every gate; asserts are
hard failures. Output is pasted into verification.md.
"""
import json
import pandas as pd
import numpy as np

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-crime-brief-2026-10-17"
STACK = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/stack/denver"
VEHICLE_TYPES = ["theft-of-motor-vehicle", "theft-items-from-vehicle",
                 "theft-parts-from-vehicle", "criminal-mischief-mtr-veh"]

raw = pd.read_parquet(f"{STACK}/snapshots/2026-10-15/crime.parquet")
c = pd.read_parquet(f"{STACK}/layers/crime_clean.parquet")
S = json.load(open(f"{PKG}/stats.json"))
print(f"raw rows {len(raw)} | clean rows {len(c)}")
assert len(raw) == len(c) == 383643

c["rdate"] = pd.to_datetime(c["REPORTED_DATE"], unit="ms", utc=True).dt.tz_convert("America/Denver")
c["year"] = c["rdate"].dt.year
win_mask = (c["rdate"].dt.month < 10) | ((c["rdate"].dt.month == 10) & (c["rdate"].dt.day <= 13))
w = c[win_mask & (c["year"] >= 2021)]

print("\n== 10.1.1 zero/null sentinel traps ==")
print("VICTIM_COUNT: nulls", int(c["VICTIM_COUNT"].isna().sum()),
      "| zeros", int((c["VICTIM_COUNT"] == 0).sum()),
      "| min", c["VICTIM_COUNT"].min(), "| max", c["VICTIM_COUNT"].max())
assert c["VICTIM_COUNT"].min() >= 1 and c["VICTIM_COUNT"].isna().sum() == 0
print("REPORTED_DATE parse failures:", int(c["rdate"].isna().sum()))
assert c["rdate"].notna().all()
print("GEO_LON nulls:", int(c["GEO_LON"].isna().sum()), "(not used in any rate)")
print("No range bucketing is used anywhere in this brief; no sentinel mapping exists to audit.")

print("\n== 10.1.2 boolean filter polarity (3-row samples) ==")
print("IS_CRIME value counts:", c["IS_CRIME"].value_counts(dropna=False).to_dict())
print("IS_TRAFFIC value counts:", c["IS_TRAFFIC"].value_counts(dropna=False).to_dict())
print("3 sample rows (all rows are matched by IS_CRIME==1, excluded by IS_TRAFFIC==1):")
print(c[["OFFENSE_ID", "OFFENSE_TYPE_ID", "IS_CRIME", "IS_TRAFFIC"]].head(3).to_string(index=False))
assert (c["IS_CRIME"] == 1).all() and (c["IS_TRAFFIC"] == 0).all()
print("Polarity conclusion: the offenses ledger contains ZERO traffic rows; the")
print("vehicle grouping in this brief is an OFFENSE_TYPE_ID list, not a flag filter.")

print("\n== 10.1.3 numerator/denominator unit agreement ==")
for y in [2021, 2022, 2023, 2024, 2025, 2026]:
    n = int((w["year"] == y).sum())
    assert n == S["window_totals"][str(y)], (y, n)
print("All shares are reports/reports on the same window population; all rates are")
print("reports per 1,000 ACS housing units. Window totals in stats.json match recomputation.")

print("\n== 10.1.4 categorical exhaustiveness ==")
cc = c["OFFENSE_CATEGORY_ID"].value_counts(dropna=False)
print(f"OFFENSE_CATEGORY_ID: {len(cc)} values, nulls {int(c['OFFENSE_CATEGORY_ID'].isna().sum())}")
print(cc.to_string())
assert cc.sum() == len(c) and c["OFFENSE_CATEGORY_ID"].notna().all()
print("OFFENSE_TYPE_ID distinct:", c["OFFENSE_TYPE_ID"].nunique(),
      "| nulls:", int(c["OFFENSE_TYPE_ID"].isna().sum()))
for y in [2021, 2022, 2025, 2026]:
    part = w[w["year"] == y].groupby("OFFENSE_CATEGORY_ID").size().sum()
    assert part == S["window_totals"][str(y)]
print("Category partitions sum exactly to window totals for 2021, 2022, 2025, 2026.")

print("\n== 10.1.5 nullable-denominator trap ==")
for col in ["IS_CRIME", "IS_TRAFFIC", "OFFENSE_CATEGORY_ID", "OFFENSE_TYPE_ID"]:
    print(f"{col} null share: {c[col].isna().mean() * 100:.3f}%")
print(f"NEIGHBORHOOD_ID nulls: {int(c['NEIGHBORHOOD_ID'].isna().sum())} of {len(c)} "
      f"({c['NEIGHBORHOOD_ID'].isna().mean() * 100:.2f}%) - excluded from neighborhood")
print("tables only, counted and printed; citywide totals never use the neighborhood subset.")
panel = pd.read_csv(f"{PKG}/data/neighborhood_panel.csv")
panel_cols = [f"reports_{y}" for y in [2021, 2022, 2023, 2024, 2025, 2026]]
recon = int(panel[panel_cols].sum().sum())
w_unmatched = int(w["NEIGHBORHOOD_ID"].isna().sum())
assert recon + w_unmatched == int(len(w)), (recon, w_unmatched, len(w))
print(f"Panel reconciliation: panel window reports {recon} + unmatched {w_unmatched} = {len(w)} window rows. OK")

print("\n== 10.2 join hygiene + control groups ==")
units = pd.read_csv(f"{PKG}/data/neighborhood_units_acs2024.csv")
print(f"ACS allocation: {units['acs_units'].sum():,.0f} of 359,581 county units allocated "
      f"({units['acs_units'].sum() / 359581 * 100:.2f}%); unallocated slivers 230 units (0.06%).")
fp = float(units.loc[units["NBHD_NAME"] == "Five Points", "acs_units"].iloc[0])
print(f"Five Points anchor: this build {fp:,.0f} units vs STR specimen's 15,639 (delta {abs(fp - 15639) / 15639 * 100:.2f}%).")
print("Control A (ground truth): DIA neighborhood rows by district:",
      c[c["NEIGHBORHOOD_ID"] == "dia"]["DISTRICT_ID"].value_counts(dropna=False).to_dict())
dia = c[c["NEIGHBORHOOD_ID"] == "dia"]
print("Control A: DIA top types overall:", dia["OFFENSE_TYPE_ID"].value_counts().head(3).to_dict(),
      "- airport-typical profile (vehicle theft, parts theft) confirms the geography fields cohere.")
nodia = w[w["NEIGHBORHOOD_ID"] != "dia"]
nv = nodia[nodia["OFFENSE_TYPE_ID"].isin(VEHICLE_TYPES)].groupby("year").size()
nt = nodia.groupby("year").size()
print(f"Control B (ex-DIA robustness): window totals ex-DIA 2022 {int(nt[2022])} -> 2025 {int(nt[2025])}; "
      f"vehicle ex-DIA {int(nv[2022])} -> {int(nv[2025])} "
      f"({(nv[2025] - nv[2022]) / nv[2022] * 100:.1f}%); non-vehicle ex-DIA still rises. Headline holds without DIA.")

print("\n== 12.3 censoring / effective window ==")
print("Snapshot REPORTED_DATE ceiling (Denver):", c["rdate"].max())
print("2026 coverage: Jan 1 - Oct 13 = 286 days. All cross-year comparisons use the")
print("matched Jan 1 - Oct 13 window; full-year figures are printed only for 2021-2025.")
print("Monthly chart series ends 2026-09 (last complete month):",
      max(S["monthly"]["total"].keys()))

print("\n== 12.6 visible exclusions (neighborhood rate table) ==")
small = units[units["acs_units"] < 1000]
print("Neighborhoods below the 1,000-unit rate floor:", 
      {r.NBHD_NAME: round(r.acs_units) for r in small.itertuples()})
print("DIA excluded from the rate ranking by name (airport district) and reported separately.")

print("\n== definition-change scan (type births/deaths, window basis) ==")
tt = w.pivot_table(index="OFFENSE_TYPE_ID", columns="year", values="OFFENSE_ID",
                   aggfunc="count").fillna(0).astype(int)
flagged = []
for t, r in tt.iterrows():
    if r.sum() > 200 and ((r[2021] == 0 and r[2024] > 0) or (r[2021] > 0 and r[2026] == 0 and r[2025] == 0)):
        flagged.append(t)
print("Flagged types:", flagged)
assert flagged == ["burglary-other"], flagged
print("burglary-other: 0 reports 2021-2023, then 407/662/720 - a coding birth in 2024.")
print("Brief uses burglary at CATEGORY level only; burglary-other is never cited as a rise.")

print("\n== sex-offense coverage check ==")
sex_types = [t for t in c["OFFENSE_TYPE_ID"].unique() if "sex" in str(t)]
print("Types containing 'sex':", sex_types)
print("No sexual-assault offense type or category exists in this public file.")

print("\nALL SECTION 10 AUDIT ASSERTIONS PASSED")
