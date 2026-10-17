# Substack draft - Denver reported offenses (2026-10-17)

Status: DRAFT ONLY, not posted. Cross-post decision is Alex's (pattern from prior briefs).

---

# Denver's Crime Reports Fell. Everything Not Involving a Car Rose.

Denver's reported offenses peaked in 2022 and have fallen since. Decomposed, the fall is one story, not a general one: reports involving a motor vehicle dropped by half between the 2022 and 2025 reporting windows, while every other kind of report rose, in every year measured, including the partial 2026 window. The city's crime ledger is two trends moving in opposite directions, and the total only shows the larger one.

All figures below come from the Denver Police Department's published offenses file (ODC_CRIME_OFFENSES_P): 383,643 offense records (one record per offense; an incident can carry several, see Methods) with reported dates running from December 31, 2020 through October 13, 2026. Every comparison below uses January 1, 2021 onward, and because 2026 is a partial year, every cross-year comparison uses the same matched window, January 1 to October 13, unless a figure is labeled a full year. Counts are offenses recorded by DPD, not a count of crimes committed; what the file can and cannot show is stated in the data notes.

## Finding 1: None of the change is traffic. The offenses file contains no traffic at all.

The offenses file carries two flags, IS_CRIME and IS_TRAFFIC. Across all 383,643 records, IS_CRIME is set on every row and IS_TRAFFIC is set on none. That is partly by construction (this layer is DPD's crime slice of its records), and it is still the direct answer to the question this brief was asked: whatever explains the movement in this ledger, it is not traffic, because this ledger holds zero traffic records. No traffic or DUI offense type appears among the file's 173 offense types either; traffic citations and DUI arrests are enforcement records outside an offenses file.

Traffic accidents live in a separate DPD service (ODC_CRIME_TRAFFICACCIDENTS5YR_P), sized here on that service's own timestamps (UTC): 106,035 accident reports between January 1, 2021 and October 13, 2026, running at roughly 18,000 a year (18,472 in 2021; 17,879 in 2025). In the 2025 matched window the accident file holds 13,574 reports against 47,548 offense reports, about one accident report for every 3.5 offense reports. The two files are published side by side and are easy to conflate; they are counted in separate services, and this brief does not link them.

## Finding 2: The entire net decline is four vehicle offense types.

Reported offenses in the matched window peaked at 58,455 in 2022 and fell to 47,548 in 2025, a decline of 10,907 reports (-18.7 percent). Over the same span, four offense types that all involve a motor vehicle (vehicle theft, theft of items from a vehicle, theft of parts from a vehicle, and criminal mischief to a vehicle; three small vehicle-involving types sit outside this grouping and are named in Methods) fell by 14,296 reports, more than the whole net decline. Everything outside those four types rose by 3,389 reports (+11.2 percent), offsetting part of the vehicle drop.

The vehicle share of the ledger has halved: 48.3 percent of all reports in the 2022 window, 29.3 percent in 2025, and 24.8 percent in the 2026 window. Auto theft reports fell 62.2 percent between the 2022 and 2025 windows (11,946 to 4,518) and fell again in 2026 (3,394). Theft from motor vehicles fell 44.7 percent (11,376 to 6,294).

Reports not involving a vehicle rose in every window measured: 28,391 in 2021, 30,236 in 2022, 31,663 in 2023, 33,389 in 2024, 33,625 in 2025, and 36,362 in the 2026 window. That is why the headline decline has stalled: the 2026 window total, 48,331 reports, is 1.6 percent above the 2025 window, the first increase since the 2022 peak year. Vehicle reports kept falling (-14.0 percent in the 2026 window) and non-vehicle reports rose faster (+8.1 percent). The 2026 rise is concentrated: six offense types (simple assault, theft-other, criminal trespassing, disturbing the peace, theft from buildings, and drug possession) supply 2,178 of the 2,737 additional non-vehicle reports, and several of the six are among the most sensitive lines in the file to reporting and enforcement practice (Finding 3).

Grouping sensitivity, printed because the headline depends on it: the four-type grouping counts criminal mischief to a vehicle (a type DPD files under public disorder) as vehicle-involved, because the property damaged is the vehicle. Under a narrower grouping of only the three theft types, vehicle reports fall by 12,402 between the 2022 and 2025 windows, still more than the whole net decline, and the rest of the ledger still ends the period higher (35,334 in 2022 to 36,829 in 2025); under that grouping the residual dips in 2025 rather than rising, and in the main grouping the 2024 to 2025 step is small (+236 reports). The decomposition conclusion does not depend on the grouping; the year-by-year rhythm of the residual does.

Window completeness: the snapshot was pulled October 15, 2026, and DPD's data carries a processing lag. Reports filed for October 1 to 13 run at 0.86 of the late-September rate in 2026, against 0.94 to 1.03 in prior years, implying roughly 200 reports (about 0.4 percent of the window) not yet in the file for the 2026 tail. The 2026 figures are therefore, if anything, understated, and the increase is a conservative reading.

On a rate basis the pattern is the same: non-vehicle reports were 84.1 per 1,000 housing units in the 2022 window and 93.6 in the 2025 window, using the ACS housing denominators of Finding 4, so the rise is an increase in reports per unit of housing, not only in raw counts.

Full calendar years tell the same story at lower resolution: 65,200 reports in 2021, a peak of 73,320 in 2022, then 71,197 in 2023, 65,106 in 2024, and 60,458 in 2025.

## Finding 3: The categories that rose are led by larceny, and larceny is the largest category in the file.

Change by category, matched windows (reports):

| Category | 2022 | 2025 | 2026 | Change 2022 to 2025 |
|---|---|---|---|---|
| Auto theft | 11,946 | 4,518 | 3,394 | -62.2% |
| Theft from motor vehicle | 11,376 | 6,294 | 5,858 | -44.7% |
| Public disorder | 9,306 | 7,865 | 7,841 | -15.5% |
| Larceny | 7,879 | 9,121 | 9,870 | +15.8% |
| All other crimes | 5,556 | 7,018 | 7,778 | +26.3% |
| Burglary | 3,903 | 3,255 | 3,055 | -16.6% |
| Drug and alcohol | 2,291 | 2,908 | 3,567 | +26.9% |
| Aggravated assault | 2,159 | 2,036 | 1,893 | -5.7% |
| Other crimes against persons | 1,961 | 2,469 | 3,039 | +25.9% |
| Robbery | 1,008 | 743 | 713 | -26.3% |
| White collar crime | 876 | 1,151 | 1,180 | +31.4% |
| Arson | 143 | 134 | 108 | -6.3% |
| Murder | 51 | 36 | 35 | -29.4% |

Larceny, at 9,870 reports in the 2026 window, is the largest single category, a position it took in the 2025 window; in 2022 it ranked fourth. Inside larceny, shoplifting reports more than doubled between the 2022 and 2025 windows (1,337 to 2,733). Shoplifting counts are sensitive to retailer reporting practices, and the file cannot separate a change in theft from a change in reporting; the doubling is printed as a reporting fact, not an incidence claim.

The persons categories split. Robbery reports fell 26.3 percent (1,008 to 743) and aggravated assault fell 5.7 percent (2,159 to 2,036) between the 2022 and 2025 windows. Murder reports are small counts that move on individual incidents: 51 in the 2022 window, 36 in 2025, 35 in 2026. But other crimes against persons rose 25.9 percent, driven by simple assault, which rose in every window year (1,798 in 2022; 2,215 in 2025; 2,709 in 2026).

Drug and alcohol reports rose 26.9 percent between the 2022 and 2025 windows and jumped again in 2026 (3,567). Drug categories are the most enforcement-sensitive lines in the file: paraphernalia possession reports went from 199 in the 2021 window to 722 in 2022 and 1,315 in 2025, a pattern that tracks enforcement and coding practice at least as much as use. These lines are printed for completeness and should not be read as a measure of drug activity. The same caution applies to criminal trespassing, inside the all-other-crimes category, which rose from 1,407 reports in the 2022 window to 2,224 in 2025 and 2,568 in 2026: trespass counts move with enforcement practice, including encampment response, at least as much as with offending.

## Finding 4: The decline is uneven across neighborhoods, and the downtown core did not share it.

Five Points recorded the most reports of any neighborhood in the 2025 window (3,627) and rose 4.7 percent against 2022 while the city fell 18.7 percent. Civic Center rose 35.1 percent (927 to 1,252) and North Capitol Hill rose 10.2 percent (1,127 to 1,242). The steepest declines are in the car-oriented south and east: Hampden South fell 45.2 percent (1,068 to 585), Kennedy 48.3 percent (422 to 218), Southmoor Park 49.0 percent (357 to 182), and University Park 54.3 percent (560 to 256). The neighborhood pattern is what the decomposition implies arithmetically: in the 2025 window, vehicles were involved in 8.6 percent of Civic Center reports and 13.8 percent of CBD reports, against 39.6 percent in Gateway - Green Valley Ranch. Neighborhoods whose ledgers were built on vehicle offenses had the most to lose when vehicle reports collapsed.

Measured per 1,000 housing units (ACS 2024 5-year housing units allocated to the city's statistical neighborhoods; basis printed in Methods), the highest 2025 window rates are the CBD (443.5 reports per 1,000 units, 1,683 reports), Civic Center (433.2, 1,252 reports), Elyria Swansea (327.5, 703 reports), Globeville (318.6, 588 reports), and Lincoln Park (270.6, 1,108 reports). These rates are reports per housing unit, not per resident or per person present: downtown neighborhoods host far more daily activity than their housing counts suggest, and their rates reflect that. Rates are printed only for neighborhoods with at least 1,000 housing units; Auraria (107 units) and Sun Valley (503 units) are excluded from the rate table by that rule and counted in the count tables. The DIA neighborhood (1,711 reports in the 2025 window) is excluded from the rate ranking by name for a different reason: it is a single-use airport district with essentially no residential function, and its reports are dominated by vehicle theft and parts theft at the airport (41.9 percent vehicle share). DIA also carries a data note: it recorded 6,355 reports in full-year 2023 against 3,241 in 2022 and 3,121 in 2024, a one-year surge in vehicle theft and theft-of-services reports at the airport. Citywide findings were recomputed without DIA and hold unchanged.

## Data notes: what this file is and is not

- These are reports recorded by DPD, on the date the report was taken (the median gap between occurrence and report is about 6 hours; 0.2 percent of reports arrive more than a year after occurrence). A change in reports can reflect a change in offending, in victims' willingness to report, in retailer or agency reporting practice, or in police recording and enforcement practice. The file cannot separate those, and this brief does not try.
- Sexual assault: no sexual-assault offense type appears among this layer's 173 offense types, so sexual-assault reports are not in any total this brief prints. DPD's dataset documentation states that addresses for sexual assaults are withheld in its published data, and DPD reports sex-offense information through its own channels. The sex-related lines that do appear in this layer are sex-offender registration violations (1,275 records), indecent exposure (755), and sexual-nature harassment (588).
- DPD's documentation also states that child-abuse cases and crimes involving juveniles (as victims, suspects, or witnesses) are not reported in this data. The persons categories in Finding 3 are shaped by that exclusion, and no total here should be read as covering them.
- DPD describes this dataset as dynamic: records are added, deleted, and modified, and a later pull of the same period will differ from this snapshot. Small counts and small percent changes should be read with that in mind.
- One offense type, burglary-other, appears in the file only from 2024 (0 reports in the 2021 to 2023 windows, then 407, 662, and 720). Sibling burglary types fell over the same step, the signature of a coding change. Burglary is therefore used at category level only in this brief.
- Reports carry the location of the report as recorded by DPD; 381 of 383,643 rows (0.1 percent) carry no neighborhood and are counted in citywide totals but excluded from neighborhood tables.
- The accident service used for Finding 1 carries its own notice that its data will be revised by the end of Q4 2026 with slight changes; its counts here are as of October 16, 2026.

## What this might mean

This section is interpretation; the findings above are the measurements.

The 2022 peak looks, in this decomposition, like a vehicle-report wave laid over a slowly rising baseline of everything else. Public argument that treats "crime" as a single number will keep misreading Denver: the total can fall for years while the non-vehicle ledger grows, which is exactly what happened from 2022 to 2025, and in 2026 the two trends netted to a small increase. Prevention aimed at the 2022 problem (vehicle theft and break-ins) is aimed at the shrinking half of the ledger. The growing half is diffuse: shoplifting, trespassing, simple assault, theft from buildings, and a long tail of smaller categories, several of them themselves sensitive to enforcement and reporting practice, and none of which has a single lever. The reporting-practice question cuts both ways: some of the vehicle fall could also be reporting or recording practice (for example, how thefts from vehicles get reported) rather than offending. How much of either movement is offending and how much is practice is the open question this file cannot answer, and it is the question that decides what the trends mean.

## Who can act

- Denver City Council, during the 2027 budget deliberation now open (final budget proposal due October 19; public hearing October 26; amendment vote November 2; final passage November 9). The decision this decomposition informs is specific: public-safety lines justified by the 2022 vehicle wave (auto-theft and break-in prevention) and lines aimed at today's growth categories (retail-theft reporting coordination, trespass and disorder response) are different appropriations, and the ledger the budget is argued over is two trends, not one. Cost class: no new cost to use the decomposition; it is an argument about existing lines. How we would know it worked: the same offenses ledger, compared on next year's matched window, shows whether the funded categories moved.
- The Denver Police Department, which publishes both ledgers. The offenses file's name invites the traffic question this brief had to answer from a second file; a coverage note on the dataset page (what the layer includes, that traffic accidents are a separate service, and how sexual-assault and juvenile-involved cases are handled in DPD's published data) would prevent the most likely misreadings. Cost class: staff time only. How we would know it worked: the note is on the catalog page, checkable by any reader.
- Retailers and business improvement districts. Shoplifting reports doubled in three years; retailer reporting policy is one of the inputs to that number, and the districts that coordinate reporting can say how much of the change is theirs. Cost class: no public cost. How we would know it worked: districts publish their reporting policies, and the shoplifting line in the next matched window can be read against them.
- Neighborhood associations. The residual risk profile in this ledger has changed: vehicle reports are half their 2022 level, while the categories still rising (theft from buildings, trespassing, simple assault) are the ones local prevention actually touches. Cost class: none. How we would know it worked: those categories are tracked at neighborhood level in this brief's panel, republished with each refresh of the data.

## Methods

- Dataset: ODC_CRIME_OFFENSES_P (Denver Open Data Catalog, ArcGIS FeatureServer), 383,643 records, snapshot pulled October 15, 2026. Reported dates run December 31, 2020 to October 13, 2026 (America/Denver); 31 records filed on December 31, 2020 fall outside every analysis window, and all comparisons use January 1, 2021 onward.
- Unit of count: one record is one offense record. DPD describes the data as NIBRS-based: an incident can carry several offense records, and crimes against persons record all victims. The 383,643 records sit on 358,980 distinct incidents; 21,000 incidents (5.8 percent) carry more than one offense record, and 11.9 percent of records belong to a multi-offense incident. Counts here are offense counts and will exceed incident-based totals published elsewhere. OFFENSE_ID is unique across the file. Records are not weighted by victim count (mean victims per record 1.02). DPD reports on a NIBRS basis throughout the period covered, so the national reporting-system changeover of 2021 does not break this series; an audit scan for offense types appearing or disappearing mid-series found one coding birth (burglary-other, from 2024; see Data notes) and no other structural type change.
- Time basis: REPORTED_DATE converted from UTC epoch milliseconds to America/Denver local dates. Comparisons use matched January 1 to October 13 windows for every year; full-year figures are labeled and printed only for 2021 to 2025. 2026 is a partial year everywhere it appears.
- Vehicle grouping: OFFENSE_TYPE_ID in {theft-of-motor-vehicle, theft-items-from-vehicle, theft-parts-from-vehicle, criminal-mischief-mtr-veh}. The grouping is an offense-type list, not the IS_TRAFFIC flag (see Finding 1), and its sensitivity is printed in Finding 2. The auto-theft category additionally contains theft of stolen vehicle trailers (920 records overall) and construction equipment (61), which are counted in the category table and not in the four-type vehicle grouping. Three small vehicle-involving types also sit outside the grouping, named here so the boundary is explicit: arson-vehicle (229 records), theft-fail-return-rent-veh (652), and weapon-fire-into-occ-veh (373). The grouping is the narrower, reproducible definition.
- Categories and types are DPD's own fields (OFFENSE_CATEGORY_ID, 13 values; OFFENSE_TYPE_ID, 173 values), counted exhaustively; category counts sum exactly to window totals.
- Neighborhoods: the city's 78 statistical neighborhoods, joined on NEIGHBORHOOD_ID (99.9 percent of rows carry one; unmatched rows counted and excluded from neighborhood tables only).
- Rates: reports per 1,000 housing units. Denominators are ACS 2020-2024 5-year estimates (table B25001) at tract level for Denver County (359,581 units), allocated to statistical neighborhoods in proportion to tract area inside each neighborhood polygon (359,351 units allocated; 230 units, 0.06 percent, fall in boundary slivers and are not assigned). The allocation reproduces the Five Points denominator used in the October 16 STR specimen (15,648 vs 15,639 units, a 0.06 percent difference). Denominators are a single recent cross-section applied to all years; rates compare neighborhoods within a year, not years within a neighborhood.
- Accident counts: ODC_CRIME_TRAFFICACCIDENTS5YR_P, counted on the service's own UTC timestamps via the service's count queries on October 16, 2026, and archived with this package.
- Verification: a pre-flight audit script (Section 10 gates) ships in this package's code folder and its output is recorded in verification.md; decisive figures were independently recomputed from the raw snapshot, and the package passed an adversarial review before publication. Dispositions are recorded in verification.md.

## Sources

- Denver Open Data Catalog, ODC_CRIME_OFFENSES_P (crime offenses), ArcGIS FeatureServer layer 324. Snapshot October 15, 2026.
- Denver Open Data Catalog, ODC_CRIME_TRAFFICACCIDENTS5YR_P (traffic accidents), ArcGIS FeatureServer layer 325. Counted October 16, 2026.
- US Census Bureau, American Community Survey 2020-2024 5-year estimates, table B25001 (housing units), tract level, Denver County, via Census Reporter.
- Denver statistical neighborhood boundaries (city published layer, warehouse copy).
