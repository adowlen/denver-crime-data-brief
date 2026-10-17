"""Charts for the Denver reported-crime brief. Dark brand style.
All figures from stats.json / neighborhood_panel.csv (never hand-typed).
"""
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-crime-brief-2026-10-17"
BG, AMBER, TEAL, FG, MUT = "#101417", "#f5a800", "#19b8a6", "#e8e6e1", "#9aa3ab"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.edgecolor": "#2a2f33", "axes.labelcolor": FG,
    "xtick.color": MUT, "ytick.color": MUT, "font.family": "DejaVu Sans",
    "axes.grid": True, "grid.color": "#23282c", "grid.linewidth": 0.6,
})
S = json.load(open(f"{PKG}/stats.json"))
OUT = f"{PKG}/charts"

# --- 1. Window totals: vehicle complex vs rest of ledger (stacked) ---
years = [2021, 2022, 2023, 2024, 2025, 2026]
veh = [S["vehicle_complex"]["window_counts"][str(y)] for y in years]
rest = [S["non_vehicle"]["window_counts"][str(y)] for y in years]
tot = [S["window_totals"][str(y)] for y in years]
fig, ax = plt.subplots(figsize=(9.2, 4.9))
ax.bar(years, veh, color=AMBER, width=0.62, label="Involving a motor vehicle (4 offense types)")
ax.bar(years, rest, bottom=veh, color=TEAL, width=0.62, label="All other reported offenses")
for x, t, v in zip(years, tot, veh):
    ax.annotate(f"{t:,}", (x, t + 1300), ha="center", fontsize=10.5, color=FG, fontweight="bold")
    ax.annotate(f"{v / t * 100:.0f}% vehicle", (x, v / 2), ha="center", va="center",
                fontsize=9, color="#101417", fontweight="bold")
ax.set_ylim(0, 66000)
ax.set_xticks(years)
ax.set_xticklabels([f"{y}\n(Jan 1-Oct 13)" if y == 2026 else str(y) for y in years], fontsize=9.5)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:,.0f}"))
ax.set_title("Denver reported offenses, matched Jan 1-Oct 13 windows",
             fontsize=13, color=FG, pad=12, loc="left")
ax.legend(frameon=False, fontsize=9.5, loc="upper right")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/chart_windows.png", dpi=200)
plt.close(fig)

# --- 2. Monthly totals with vehicle overlay ---
m = S["monthly"]
xs = pd.to_datetime(list(m["total"].keys()))
tv = pd.Series(m["total"])
vv = pd.Series(m["vehicle"])
fig, ax = plt.subplots(figsize=(9.2, 4.4))
ax.plot(xs, tv.values, color=FG, lw=1.8, label="All reported offenses")
ax.plot(xs, vv.values, color=AMBER, lw=1.8, label="Involving a motor vehicle")
ax.fill_between(xs, vv.values, color=AMBER, alpha=0.13)
ax.set_title("Reported offenses by month, Jan 2021 - Sep 2026 (last complete month)",
             fontsize=12.5, color=FG, pad=12, loc="left")
ax.legend(frameon=False, fontsize=9.5, loc="upper right")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/chart_monthly.png", dpi=200)
plt.close(fig)

# --- 3. Category change 2022 -> 2025 (window counts) ---
cats = S["categories_window"]
rows = sorted(((k, v["window_counts"]["2025"] - v["window_counts"]["2022"]) for k, v in cats.items()),
              key=lambda kv: kv[1])
fig, ax = plt.subplots(figsize=(9.2, 5.4))
names = [k.replace("-", " ") for k, _ in rows]
vals = [v for _, v in rows]
colors = [AMBER if v < 0 else TEAL for v in vals]
ax.barh(names, vals, color=colors, height=0.62)
for i, v in enumerate(vals):
    ax.annotate(f"{v:+,}", (v + (260 if v >= 0 else -260), i),
                ha="left" if v >= 0 else "right", va="center", fontsize=10, color=FG)
ax.axvline(0, color="#3a4046", lw=0.9)
ax.set_xlim(min(vals) * 1.28, max(vals) * 1.45)
ax.set_title("Change in reported offenses by category, 2022 to 2025 (matched windows)",
             fontsize=12.5, color=FG, pad=12, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/chart_categories.png", dpi=200)
plt.close(fig)

# --- 4. Neighborhood rates, 2025 window (units >= 1000, DIA excluded by name) ---
panel = pd.read_csv(f"{PKG}/data/neighborhood_panel.csv")  # already carries acs_units + rates
el = panel[(panel["acs_units"] >= 1000) & (panel["neighborhood"] != "DIA")]
top = el.nlargest(10, "rate_2025_per_1000_units").sort_values("rate_2025_per_1000_units")
fig, ax = plt.subplots(figsize=(9.2, 5.2))
ax.barh(top["neighborhood"], top["rate_2025_per_1000_units"], color=TEAL, height=0.6)
for i, (r, cnt) in enumerate(zip(top["rate_2025_per_1000_units"], top["reports_2025"])):
    ax.annotate(f"{r:.0f}  ({cnt:,} reports)", (r + 9, i), va="center", fontsize=10, color=FG)
ax.set_xlim(0, top["rate_2025_per_1000_units"].max() * 1.28)
ax.set_title("Reported offenses per 1,000 housing units, 2025 (Jan 1-Oct 13)",
             fontsize=12.5, color=FG, pad=12, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/chart_neighborhood_rates.png", dpi=200)
plt.close(fig)
print("charts written to", OUT)
