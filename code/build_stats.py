"""Build stats.json + neighborhood panel for the Denver reported-crime brief.

Source: warehouse layers/crime_clean.parquet (Phase 2 snapshot of
ODC_CRIME_OFFENSES_P, pulled 2026-10-15; REPORTED_DATE ceiling
2026-10-13). Time basis: REPORTED_DATE in America/Denver local time.
Full years 2021-2025; matched windows Jan 1 - Oct 13 for 2021-2026
(2026 exists only as a window - the snapshot ends Oct 13, 2026).

Every figure in brief-draft.md and the social copy comes from the
stats.json this script writes. No hand-entered numbers.
"""
import json
import pandas as pd
import numpy as np

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-crime-brief-2026-10-17"
STACK = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/stack/denver"

VEHICLE_TYPES = ["theft-of-motor-vehicle", "theft-items-from-vehicle",
                 "theft-parts-from-vehicle", "criminal-mischief-mtr-veh"]
WINDOW_YEARS = [2021, 2022, 2023, 2024, 2025, 2026]
FULL_YEARS = [2021, 2022, 2023, 2024, 2025]

c = pd.read_parquet(f"{STACK}/layers/crime_clean.parquet")
c["rdate"] = pd.to_datetime(c["REPORTED_DATE"], unit="ms", utc=True).dt.tz_convert("America/Denver")
c["year"] = c["rdate"].dt.year
in_window = (c["rdate"].dt.month < 10) | ((c["rdate"].dt.month == 10) & (c["rdate"].dt.day <= 13))
w = c[in_window & (c["year"] >= 2021)].copy()
full = c[c["year"].isin(FULL_YEARS)].copy()

S = {"meta": {
    "dataset": "ODC_CRIME_OFFENSES_P (Denver Open Data, ArcGIS FeatureServer layer 324)",
    "snapshot": "warehouse snapshots/2026-10-15/crime.parquet (Phase 2 pull, 2026-10-15)",
    "rows": int(len(c)),
    "reported_date_min_denver": str(c["rdate"].min()),
    "reported_date_max_denver": str(c["rdate"].max()),
    "time_basis": "REPORTED_DATE converted to America/Denver local time",
    "window_def": "matched window = Jan 1 to Oct 13 inclusive, each year",
    "vehicle_types": VEHICLE_TYPES,
}}

# --- flags (Alex's question, answered at the ledger level) ---
S["flags"] = {
    "is_crime_1_rows": int((c["IS_CRIME"] == 1).sum()),
    "is_crime_other_rows": int((c["IS_CRIME"] != 1).sum()),
    "is_traffic_1_rows": int((c["IS_TRAFFIC"] == 1).sum()),
    "is_traffic_0_rows": int((c["IS_TRAFFIC"] == 0).sum()),
}

# --- totals ---
S["full_year_totals"] = {str(y): int((full["year"] == y).sum()) for y in FULL_YEARS}
S["window_totals"] = {str(y): int((w["year"] == y).sum()) for y in WINDOW_YEARS}
wt = S["window_totals"]
S["window_changes_pct"] = {
    "2021_to_2022": round((wt["2022"] - wt["2021"]) / wt["2021"] * 100, 1),
    "2022_to_2025": round((wt["2025"] - wt["2022"]) / wt["2022"] * 100, 1),
    "2025_to_2026": round((wt["2026"] - wt["2025"]) / wt["2025"] * 100, 1),
}
ft = S["full_year_totals"]
S["full_year_change_2022_to_2025_pct"] = round((ft["2025"] - ft["2022"]) / ft["2022"] * 100, 1)

# --- vehicle complex vs the rest of the ledger (window basis) ---
w["is_vehicle"] = w["OFFENSE_TYPE_ID"].isin(VEHICLE_TYPES)
veh = w[w["is_vehicle"]].groupby("year").size()
rest = w[~w["is_vehicle"]].groupby("year").size()
S["vehicle_complex"] = {
    "window_counts": {str(y): int(veh[y]) for y in WINDOW_YEARS},
    "share_of_window_pct": {str(y): round(veh[y] / wt[str(y)] * 100, 1) for y in WINDOW_YEARS},
    "change_2022_to_2025_pct": round((veh[2025] - veh[2022]) / veh[2022] * 100, 1),
    "change_2025_to_2026_pct": round((veh[2026] - veh[2025]) / veh[2025] * 100, 1),
    "overall_share_of_all_rows_pct": round(
        c["OFFENSE_TYPE_ID"].isin(VEHICLE_TYPES).mean() * 100, 1),
}
S["non_vehicle"] = {
    "window_counts": {str(y): int(rest[y]) for y in WINDOW_YEARS},
    "change_2022_to_2025_pct": round((rest[2025] - rest[2022]) / rest[2022] * 100, 1),
    "change_2025_to_2026_pct": round((rest[2026] - rest[2025]) / rest[2025] * 100, 1),
    "rose_every_window_year": bool(all(rest[y + 1] > rest[y] for y in WINDOW_YEARS[:-1])),
}
# decomposition of the 2022->2025 window change
S["decomposition_2022_to_2025"] = {
    "total_change": int(wt["2025"] - wt["2022"]),
    "vehicle_change": int(veh[2025] - veh[2022]),
    "non_vehicle_change": int(rest[2025] - rest[2022]),
}

# --- categories (window basis) ---
tab = w.pivot_table(index="OFFENSE_CATEGORY_ID", columns="year", values="OFFENSE_ID",
                    aggfunc="count").fillna(0).astype(int)
cats = {}
for name, row in tab.iterrows():
    cats[name] = {
        "window_counts": {str(y): int(row[y]) for y in WINDOW_YEARS},
        "change_2022_to_2025_pct": round((row[2025] - row[2022]) / row[2022] * 100, 1) if row[2022] else None,
        "change_2025_to_2026_pct": round((row[2026] - row[2025]) / row[2025] * 100, 1) if row[2025] else None,
        "share_of_2025_window_pct": round(row[2025] / wt["2025"] * 100, 1),
    }
S["categories_window"] = cats
S["category_counter_all_rows"] = {k: int(v) for k, v in
                                  c["OFFENSE_CATEGORY_ID"].value_counts().items()}

# --- offense types: top movers (window 2022 -> 2025 and 2025 -> 2026) ---
tt = w.pivot_table(index="OFFENSE_TYPE_ID", columns="year", values="OFFENSE_ID",
                   aggfunc="count").fillna(0).astype(int)
tt["d_22_25"] = tt[2025] - tt[2022]
tt["d_25_26"] = tt[2026] - tt[2025]
S["top_fallers_2022_2025"] = [{"type": i, "from": int(r[2022]), "to": int(r[2025]),
                               "change": int(r["d_22_25"])}
                              for i, r in tt.nsmallest(6, "d_22_25").iterrows()]
S["top_risers_2022_2025"] = [{"type": i, "from": int(r[2022]), "to": int(r[2025]),
                              "change": int(r["d_22_25"])}
                             for i, r in tt.nlargest(6, "d_22_25").iterrows()]
S["top_risers_2025_2026"] = [{"type": i, "from": int(r[2025]), "to": int(r[2026]),
                              "change": int(r["d_25_26"])}
                             for i, r in tt.nlargest(6, "d_25_26").iterrows()]
for t in ["theft-shoplift", "drug-poss-paraphernalia", "assault-simple",
          "criminal-trespassing", "criminal-mischief-mtr-veh"]:
    S.setdefault("type_window_counts", {})[t] = {str(y): int(tt.loc[t, y]) for y in WINDOW_YEARS}

# --- monthly series (complete months only: Jan 2021 - Sep 2026) ---
mm = c[(c["rdate"] >= "2021-01-01") & (c["rdate"] < "2026-10-01")].copy()
mm["ym"] = mm["rdate"].dt.strftime("%Y-%m")
mm["is_vehicle"] = mm["OFFENSE_TYPE_ID"].isin(VEHICLE_TYPES)
S["monthly"] = {
    "total": {k: int(v) for k, v in mm.groupby("ym").size().items()},
    "vehicle": {k: int(v) for k, v in mm[mm["is_vehicle"]].groupby("ym").size().items()},
}

# --- districts (window basis) ---
S["district_window_2025"] = {str(k): int(v) for k, v in
                             w[w["year"] == 2025]["DISTRICT_ID"].value_counts(dropna=False).items()}

# --- neighborhoods ---
nb = pd.read_parquet(f"{STACK}/layers/neighborhoods_clean.parquet")[["NBHD_NAME"]]
import re, unicodedata
def slug(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
slug2name = {slug(n): n for n in nb["NBHD_NAME"]}
units = pd.read_csv(f"{PKG}/data/neighborhood_units_acs2024.csv")
units_map = dict(zip(units["NBHD_NAME"], units["acs_units"]))
w["nbhd_name"] = w["NEIGHBORHOOD_ID"].map(slug2name)
w["is_vehicle_nb"] = w["OFFENSE_TYPE_ID"].isin(VEHICLE_TYPES)
panel_rows = []
for name, g in w.groupby("nbhd_name"):
    row = {"neighborhood": name, "slug": slug(name), "acs_units": round(float(units_map[name]), 0)}
    for y in WINDOW_YEARS:
        row[f"reports_{y}"] = int((g["year"] == y).sum())
    g25 = g[g["year"] == 2025]
    row["vehicle_2025"] = int(g25["is_vehicle_nb"].sum())
    row["vehicle_share_2025_pct"] = round(g25["is_vehicle_nb"].mean() * 100, 1) if len(g25) else None
    row["rate_2025_per_1000_units"] = round(len(g25) / units_map[name] * 1000, 1)
    row["change_2022_to_2025_pct"] = round((row["reports_2025"] - row["reports_2022"]) /
                                           row["reports_2022"] * 100, 1) if row["reports_2022"] else None
    row["change_2025_to_2026_pct"] = round((row["reports_2026"] - row["reports_2025"]) /
                                           row["reports_2025"] * 100, 1) if row["reports_2025"] else None
    panel_rows.append(row)
panel = pd.DataFrame(panel_rows).sort_values("reports_2025", ascending=False)
S["neighborhoods"] = {
    "unmatched_rows_window": int(w["nbhd_name"].isna().sum()),
    "unmatched_rows_all": int(c["NEIGHBORHOOD_ID"].isna().sum()),
    "top_by_count_2025": panel.head(10)[["neighborhood", "reports_2025", "reports_2022",
                                         "change_2022_to_2025_pct", "rate_2025_per_1000_units"]].to_dict("records"),
    "top_by_rate_2025_excl_dia": panel[panel["neighborhood"] != "DIA"].nlargest(10, "rate_2025_per_1000_units")[
        ["neighborhood", "reports_2025", "acs_units", "rate_2025_per_1000_units"]].to_dict("records"),
    "dia": panel[panel["neighborhood"] == "DIA"].to_dict("records"),
    "largest_count_gains_2022_2025": panel.nlargest(5, "change_2022_to_2025_pct")[
        ["neighborhood", "reports_2022", "reports_2025", "change_2022_to_2025_pct"]].to_dict("records"),
    "largest_count_drops_2022_2025": panel.nsmallest(5, "change_2022_to_2025_pct")[
        ["neighborhood", "reports_2022", "reports_2025", "change_2022_to_2025_pct"]].to_dict("records"),
}
panel.to_csv(f"{PKG}/data/neighborhood_panel.csv", index=False)

# --- traffic accidents sizing (archived REST counts) ---
S["traffic_accidents_service"] = json.load(open(f"{PKG}/data/traffic_accidents_service_counts.json"))

# --- victim counts ---
S["victims"] = {"total_victim_count_all_rows": int(c["VICTIM_COUNT"].sum()),
                "mean_per_report": round(float(c["VICTIM_COUNT"].mean()), 3)}

json.dump(S, open(f"{PKG}/stats.json", "w"), indent=1)
print("stats.json written")
print("window totals:", S["window_totals"], "| changes:", S["window_changes_pct"])
print("vehicle share:", S["vehicle_complex"]["share_of_window_pct"])
print("decomposition 22->25:", S["decomposition_2022_to_2025"])
print("non-vehicle rose every year:", S["non_vehicle"]["rose_every_window_year"])
print("panel rows:", len(panel))
