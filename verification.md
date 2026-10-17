# Verification - Denver reported offenses brief (2026-10-17)

## Build record
- Builder implementation: code/build_stats.py (stats.json), code/denominators.py (ACS denominators),
  code/charts.py, code/hero_composite.py. All brief figures trace to stats.json.
- Source layer REUSED AS-IS per the warehouse deposit rule: stack/denver/layers/crime_clean.parquet,
  whose raw snapshot is stack/denver/snapshots/2026-10-15/crime.parquet (Phase 2 pull, 2026-10-15).
  Vintage: snapshot 2026-10-15; REPORTED_DATE ceiling 2026-10-13 (America/Denver). No re-pull:
  the ceiling is 2 days behind the brief date and the matched-window design (Jan 1-Oct 13)
  makes the comparison set identical either way; a re-pull would add Oct 14-16 rows that no
  comparison uses.
- Traffic sizing: count-only REST queries against ODC_CRIME_TRAFFICACCIDENTS5YR_P (layer 325)
  run 2026-10-16/17, archived at data/traffic_accidents_service_counts.json and deposited in
  the warehouse (below). Counts as of query time; the service warns of a Q4 2026 revision.

## Pre-flight audit (Section 10) - code/audit_section10.py output, run 2026-10-17

raw rows 383643 | clean rows 383643

== 10.1.1 zero/null sentinel traps ==
VICTIM_COUNT: nulls 0 | zeros 0 | min 1 | max 19
REPORTED_DATE parse failures: 0
GEO_LON nulls: 1 (not used in any rate)
No range bucketing is used anywhere in this brief; no sentinel mapping exists to audit.

== 10.1.2 boolean filter polarity (3-row samples) ==
IS_CRIME value counts: {1: 383643}
IS_TRAFFIC value counts: {0: 383643}
3 sample rows (all rows are matched by IS_CRIME==1, excluded by IS_TRAFFIC==1):
        OFFENSE_ID         OFFENSE_TYPE_ID  IS_CRIME  IS_TRAFFIC
DP2021595526299900 criminal-mischief-other         1           0
DP2025630814299900 criminal-mischief-other         1           0
DP2021487459299900 criminal-mischief-other         1           0
Polarity conclusion: the offenses ledger contains ZERO traffic rows; the
vehicle grouping in this brief is an OFFENSE_TYPE_ID list, not a flag filter.

== 10.1.3 numerator/denominator unit agreement ==
All shares are reports/reports on the same window population; all rates are
reports per 1,000 ACS housing units. Window totals in stats.json match recomputation.

== 10.1.4 categorical exhaustiveness ==
OFFENSE_CATEGORY_ID: 13 values, nulls 0
OFFENSE_CATEGORY_ID
theft-from-motor-vehicle        63149
larceny                         62080
public-disorder                 60493
auto-theft                      56687
all-other-crimes                46993
burglary                        27425
drug-alcohol                    20188
other-crimes-against-persons    16677
aggravated-assault              15160
white-collar-crime               7089
robbery                          6478
arson                             867
murder                            357
OFFENSE_TYPE_ID distinct: 173 | nulls: 0
Category partitions sum exactly to window totals for 2021, 2022, 2025, 2026.

== 10.1.5 nullable-denominator trap ==
IS_CRIME null share: 0.000%
IS_TRAFFIC null share: 0.000%
OFFENSE_CATEGORY_ID null share: 0.000%
OFFENSE_TYPE_ID null share: 0.000%
NEIGHBORHOOD_ID nulls: 381 of 383643 (0.10%) - excluded from neighborhood
tables only, counted and printed; citywide totals never use the neighborhood subset.
Panel reconciliation: panel window reports 313455 + unmatched 321 = 313776 window rows. OK

== 10.2 join hygiene + control groups ==
ACS allocation: 359,351 of 359,581 county units allocated (99.94%); unallocated slivers 230 units (0.06%).
Five Points anchor: this build 15,648 units vs STR specimen's 15,639 (delta 0.06%).
Control A (ground truth): DIA neighborhood rows by district: {'7': 11265, '5': 7622, 'U': 15, '3': 1, nan: 1}
Control A: DIA top types overall: {'theft-of-motor-vehicle': 4908, 'theft-parts-from-vehicle': 2389, 'theft-items-from-vehicle': 2103} - airport-typical profile (vehicle theft, parts theft) confirms the geography fields cohere.
Control B (ex-DIA robustness): window totals ex-DIA 2022 56040 -> 2025 45837; vehicle ex-DIA 26669 -> 13206 (-50.5%); non-vehicle ex-DIA still rises. Headline holds without DIA.

== 12.3 censoring / effective window ==
Snapshot REPORTED_DATE ceiling (Denver): 2026-10-13 16:53:00-06:00
2026 coverage: Jan 1 - Oct 13 = 286 days. All cross-year comparisons use the
matched Jan 1 - Oct 13 window; full-year figures are printed only for 2021-2025.
Monthly chart series ends 2026-09 (last complete month): 2026-09

== 12.6 visible exclusions (neighborhood rate table) ==
Neighborhoods below the 1,000-unit rate floor: {'Auraria': 107, 'Sun Valley': 503}
DIA excluded from the rate ranking by name (airport district) and reported separately.

== definition-change scan (type births/deaths, window basis) ==
Flagged types: ['burglary-other']
burglary-other: 0 reports 2021-2023, then 407/662/720 - a coding birth in 2024.
Brief uses burglary at CATEGORY level only; burglary-other is never cited as a rise.

== sex-offense coverage check ==
Types containing 'sex': ['sex-off-fail-to-register', 'sex-off-registration-viol', 'harassment-sexual-in-nature']
No sexual-assault offense type or category exists in this public file.

ALL SECTION 10 AUDIT ASSERTIONS PASSED

## Section 11 review record

### Independent verifier (separate implementation, raw snapshot only)
Recomputed every decisive figure from snapshots/2026-10-15/crime.parquet with its own scripts,
without reading the builder code or stats.json until after computing.
RESULT: every decisive figure CONFIRMED exactly - totals, flags, full-year and window totals,
vehicle decomposition (-10,907 total / -14,296 vehicle / +3,389 non-vehicle), all 13 category
window counts for 2022/2025/2026, type-level series (shoplift, simple assault, paraphernalia,
burglary-other), neighborhood spot checks (Five Points, Civic Center, DIA surge, null count 381),
report lag (median 0.246 days; 884 rows > 365 days), and the ex-DIA robustness recompute
(ex-DIA vehicle -13,463 vs total -10,203; non-vehicle +3,260 and still monotonic).
Three defects found, all dispositioned below (V1-V3).

### Adversarial reviewer (claims, framing, DPD documentation)
Read the full brief, stats.json, social drafts, audit output, standards sections 9-12, and DPD's
published documentation (dataset description mirrors + Crime Information page; the layer-324
Hub description itself returned no extractable text - flagged in reviewer-notes.md).
Verdict: publishable after fixes; the core decomposition is robust to the grouping challenge,
DIA exclusion, and the 2026 tail shortfall. Four blocking + eleven should-fix/nit findings.
Reviewer-quoted figures were treated as claims and recomputed by the builder before use
(Section 12.7): every one reproduced exactly (INCIDENT_ID counts, 3-type sensitivity series,
S11 type counts, tail ratios, riser concentration 2,178 - whose total the reviewer printed as
2,727; the recomputed total is 2,737 and the brief prints 2,737).

### Dispositions (count / mechanism / treatment)

V1 Coverage start (verifier). COUNT sustained: 31 records carry December 31, 2020 Denver
reported dates. MECHANISM: UTC-to-Denver boundary at the file start. TREATMENT: brief edited
(intro + Methods) to state the true range and that the 31 records fall outside every window.

V2 / B1 Sexual-assault note. COUNT sustained: the note omitted harassment-sexual-in-nature
(588 records); sex-related types are registration violations (1,275), indecent exposure (755),
harassment-sexual-in-nature (588); no sexual-assault type exists (both reviewers confirm).
MECHANISM sustained in part: "not in this file at all" is an inference from the layer's type
inventory; DPD's own documentation speaks of withheld addresses. TREATMENT: note reworded to
the inventory fact + DPD's documented wording, counts printed; the DPD Who-can-act bullet
re-aimed from "excluded" to a coverage note describing how such cases are handled.

B2 Unit of count. COUNT sustained (builder-recomputed): 383,643 records on 358,980 distinct
INCIDENT_IDs; 21,000 incidents (5.8%) multi-offense; 11.9% of records in multi-offense incidents.
MECHANISM sustained: NIBRS offense-level rows; "one record is one report" was imprecise.
TREATMENT: Methods now states the NIBRS counting rule with the incident figures; intro noun
changed to "offense records"; NIBRS continuity across the window stated (no 2021 system break).

B3 Grouping sensitivity / title. COUNT sustained (builder-recomputed): without
criminal-mischief-mtr-veh, vehicle falls 12,402 (still > net decline 10,907); the residual
series dips in 2025 (37,301 to 36,829); the main grouping's 2024-to-2025 step is +236.
MECHANISM sustained: the "rose every year" rhythm is grouping-dependent. TREATMENT: grouping
kept (disclosed, reproducible, physically grounded); sensitivity printed in Finding 2 with
both decompositions; title changed to "Everything Not Involving a Car Rose" (true under both
groupings over the period); social "every year" claims re-cut to the robust form.

B4 Verification record. Sustained as a process point: at the reviewer's listing, verification.md
did not yet exist (builder created it during the review window). TREATMENT: this file now
contains the audit output and this full record before any publication; the Methods sentence
is accurate as of publication.

S1 Finding 1 framing. Partially sustained. TREATMENT: construction acknowledged in Finding 1;
"do not overlap" replaced with the separate-services/no-linkage statement; UTC basis stated in
Finding 1; a grounded sentence added (no traffic or DUI offense type exists among the 173 types;
citations/DUI arrests are enforcement records outside an offenses file).

S2 Missing documented exclusions. Sustained. TREATMENT: Data notes now carry DPD's documented
child-abuse and juvenile-involvement exclusion and the dynamic-dataset caveat, attributed to
DPD's documentation.

S3 2026 tail completeness (Section 12.3). COUNT sustained (builder-recomputed): Oct 1-13 vs
Sep 18-30 filing ratio 0.862 in 2026 vs 0.94-1.03 in 2021-2025, implying roughly 200 reports
(about 0.4%) missing at the tail. TREATMENT: quantified note added to Finding 2, direction
stated (2026 understated; the increase reading is conservative).

S4 Point-of-claim caveats. COUNT sustained (builder-recomputed): six types supply 2,178 of the
2,737 additional non-vehicle reports in 2026. TREATMENT: concentration sentence added at the
Finding 2 claim; trespassing enforcement caution added in Finding 3; the interpretation list
now flags its own practice-sensitive members.

S5 Interpretation asymmetry. Sustained. TREATMENT: "vehicle-crime wave" reworded to
"vehicle-report wave"; the reporting/recording alternative for the vehicle fall is now stated
in the same interpretation paragraph.

S6 Rate exposure caveat. Sustained. TREATMENT: Finding 4 now states in place that rates are
reports per housing unit, not per resident or person present, that downtown rates reflect
non-residential activity, and that DIA's exclusion is categorical (single-use airport, no
residential function) rather than a matter of degree.

S7 Citywide denominator. Partially sustained. TREATMENT: citywide companion rates added to
Finding 2 (non-vehicle 84.1 per 1,000 housing units in the 2022 window, 93.6 in 2025, same
ACS cross-section), showing the rise on a rate basis as well as counts.

S8 Who can act format (Section 5). Sustained. TREATMENT: each bullet now names the decision
or lever, a cost class, and an outcome measure with its dataset. The four budget dates are
sourced from the city's 2027 budget calendar as tracked in the goal records; attaching the
city calendar citation to the published repo is a pre-publication check in reviewer-notes.md.

S9 Social overclaims. Sustained. TREATMENT: "The decline is real" cut; every-year claims
re-cut per B3; sexual-assault line aligned to B1 wording.

S10 Finding 4 identity. Sustained. TREATMENT: reworded as arithmetic implication; Hale dropped
(its share is not tabled elsewhere in the brief).

S11 Grouping boundary. COUNT sustained (builder-recomputed): arson-vehicle 229,
theft-fail-return-rent-veh 652, weapon-fire-into-occ-veh 373. TREATMENT: named in Methods with
counts, and a first-use pointer added in Finding 2.

N1 Arson percent. NOT sustained as a change: the table prints counts adjacent to every percent
(Section 3 satisfied) and the brief makes no arson claim in prose; murder's percent is kept for
the same reason and is additionally fenced in text. Recorded as a considered disagreement.
N2 "first increase since 2022" - EDITED to "first increase since the 2022 peak year" (brief + social).
N3 = V1. N4 larceny "now" - EDITED (position taken in the 2025 window, stated in text and title).
N5 small-neighborhood percents - KEPT with reason (counts printed, bases above 30).

### Fix-loop re-verification
- stats.json defect (verifier): vehicle_complex.overall_share_of_all_rows_pct was computed over
  window rows (38.3) under an all-rows label. Fixed in code/build_stats.py to the full file;
  recomputed value 38.5 matches the verifier's 147,877 / 383,643. Full stats diff after the fix:
  exactly one field changed; Section 10 audit re-run, ALL ASSERTIONS PASSED.
- Every new number introduced by the fixes was computed from the raw layer in the adjudication
  pass (incident counts, 3-type series, tail ratios, type counts, concentration, citywide rates
  84.1 / 93.6) and is printed above with its disposition.
- All publishable files re-grepped: zero en/em dashes; zero "[truncated" markers; brief read
  end to end after edits (20,367 bytes).

## Warehouse deposit (standing rule, 2026-10-16)
- Source pull: the crime layer was REUSED AS-IS (Phase 2 snapshot 2026-10-15, REPORTED_DATE
  ceiling 2026-10-13) - vintage and ceiling recorded above per the rule; no re-pull.
- Traffic sizing archived as a dated snapshot: stack/denver/snapshots/2026-10-16/
  traffic_accidents_service_counts.json (count-query responses, 2026-10-16/17).
- Derived layers deposited on the neighborhood spine:
  * layers/crime_neighborhood_panel.parquet (468 rows: 78 neighborhoods x 6 matched windows;
    reports, vehicle reports, vehicle share, ACS units, rate per 1,000 units).
    Join rate: crime NEIGHBORHOOD_ID matched to the 78 statistical neighborhoods for 99.90%
    of records (381 of 383,643 null, excluded and counted).
  * layers/acs_neighborhood_units.parquet (78 rows: ACS 2024 5-year B25001 housing units,
    area-weighted tract allocation; county total 359,581, allocated 359,351 = 99.94%,
    230 units in boundary slivers unassigned; Five Points cross-check 15,648 vs the
    2026-10-16 STR specimen's 15,639, delta 0.06%).
- manifest.json updated (22 layer entries); entry added to stack/denver/verification.md.

## Close-out pass (2026-10-17, separate agent, after the build coordinator ended without a final report)

Independent recompute from the raw snapshot (snapshots/2026-10-15/crime.parquet) with a
fresh implementation that did not read build_stats.py or stats.json before computing:
- Total 383,643 records; Denver reported dates 2020-12-31 to 2026-10-13; 31 records on
  2020-12-31 (V1 confirmed). IS_CRIME = 1 on all rows; IS_TRAFFIC = 1 on zero rows.
- Matched Jan 1-Oct 13 windows: 2021 51,258 / 2022 58,455 / 2023 56,876 / 2024 51,308 /
  2025 47,548 / 2026 48,331. Full years: 65,200 / 73,320 / 71,197 / 65,106 / 60,458.
- Decomposition 2022 to 2025: total -10,907 (-18.7%); vehicle four-type -14,296;
  non-vehicle +3,389 (+11.2%). Three-type sensitivity: -12,402, residual 35,334 to 36,829.
  Vehicle share of all rows 38.5% (147,877 / 383,643 - the fixed stats field is correct).
- All 13 category window counts for 2022 / 2025 / 2026 reproduce the brief's table exactly;
  category partitions sum to window totals. Type series confirmed: shoplifting 1,337 to
  2,733; simple assault 1,798 / 2,215 / 2,709; drug-poss-paraphernalia 199 / 722 / 1,315;
  criminal trespassing 1,407 / 2,224 / 2,568; burglary-other 0 (2021-2023), 407 / 662 / 720.
- Six-type concentration of the 2026 non-vehicle rise: risers sum to 2,178 of 2,737
  (assault-simple +494, theft-other +494, criminal-trespassing +344, disturbing-the-peace
  +310, theft-from-bldg +298, drug-pcs-other-drug +238).
- Unit of count: 358,980 distinct INCIDENT_IDs; 21,000 multi-offense incidents (5.8%);
  11.9% of records in multi-offense incidents; OFFENSE_ID unique; mean victims 1.02.
- Sex-related inventory: registration violations 1,275 combined (1,233 + 42), indecent
  exposure 755, harassment-sexual-in-nature 588. No sexual-assault type exists.
- Neighborhoods: Five Points 3,465 to 3,627 (+4.7%, the 2025 window maximum); Civic Center
  927 to 1,252 (+35.1%, vehicle share 8.6%); North Capitol Hill +10.2%; Hampden South -45.2%;
  Kennedy -48.3%; Southmoor Park -49.0%; University Park -54.3%; DIA 1,711 in the 2025
  window, 41.9% vehicle share, full-year surge 3,241 (2022) / 6,355 (2023) / 3,121 (2024);
  Gateway - Green Valley Ranch vehicle share 39.6%; CBD 13.8%. 381 rows carry no
  NEIGHBORHOOD_ID. Rates reproduced from data/neighborhood_units_acs2024.csv: CBD 443.5,
  Civic Center 433.2, Elyria Swansea 327.5, Globeville 318.6, Lincoln Park 270.6; Five Points
  denominator 15,648 units. Non-vehicle citywide rates 84.1 (2022) and 93.6 (2025) per 1,000
  units on 359,351 allocated units.
- Report lag: median 0.246 days; 884 rows (0.23%) over 365 days. 2026 tail ratio 0.862 vs
  0.941-1.027 for 2021-2025 (S3 confirmed). Ex-DIA robustness: 56,040 to 45,837; vehicle
  26,669 to 13,206 (-50.5%).
- Traffic sizing confirmed against the LIVE layer-325 service at close-out: count queries
  returned 106,035 (2021-01-01 to 2026-10-14 00:00 UTC) and 13,574 (2025 window), identical
  to the archived data/traffic_accidents_service_counts.json; by-year 18,472 (2021) and
  17,879 (2025) match the archive.
- Section 10 audit re-run at close-out: ALL ASSERTIONS PASSED; output byte-identical to
  data/audit_output.txt recorded above.
- Every figure quoted in social-drafts.md and substack-draft.md cross-checked against this
  recompute: all match. Charts read visually: window totals and vehicle-share labels match
  stats.json; category deltas match; neighborhood rate bars match the panel; monthly series
  ends 2026-09 as labeled. Hero (48.3% to 24.8%) is legible in brand palette; the subtitle's
  second line sits over the illustration's street grid but remains readable - a nit, not a
  defect.
- File integrity: brief-draft.md read end to end at close-out (20,367 bytes); zero en/em
  dashes and zero truncation markers in brief-draft.md, social-drafts.md, substack-draft.md.
  (The single "[truncated" string in this verification.md is the audit sentence quoting the
  marker it checked for.)
- Warehouse deposit confirmed on disk, not just in the record: layers/
  crime_neighborhood_panel.parquet (468 rows = 78 x 6 windows; Five Points rows spot-checked
  against the recompute), layers/acs_neighborhood_units.parquet (78 rows), snapshots/
  2026-10-16/traffic_accidents_service_counts.json, manifest.json entries for both new
  layers (22 total), and the "Study deposit" entry in stack/denver/verification.md with
  verification status.
- Pre-publication check 1 from reviewer-notes.md (dataset-description wording) CLOSED at
  close-out: the live layer-324 service description (saved to data/
  dataset_description_layer324.txt) carries the dynamic-dataset wording the brief cites,
  and the mirrored DPD dataset description carries the withheld-data passage: addresses of
  sexual assaults are not included, and child-abuse cases and crimes involving juveniles
  as victims, suspects, or witnesses are not reported at all. Both Data-notes sentences in
  the brief match that documented wording.
- Still open for the morning QA (already flagged in reviewer-notes.md, non-blocking): a
  citable public city source for the four 2027 budget dates in "Who can act" (currently
  traced to the goal's tracked budget calendar), and the [REPO LINK] placeholder, which
  resolves when Alex creates the repo.

Close-out verdict: no blocking defect found. The package is ready for Alex's morning approval.
