# Sources - Denver reported offenses brief (2026-10-17)

## Primary dataset
- Denver Open Data Catalog: ODC_CRIME_OFFENSES_P (reported crime offenses, Denver Police Department).
  ArcGIS FeatureServer layer 324:
  https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_CRIME_OFFENSES_P/FeatureServer/324
  Warehouse snapshot: stack/denver/snapshots/2026-10-15/crime.parquet (Phase 2 pull, 2026-10-15).
  Cleaned layer reused as-is: stack/denver/layers/crime_clean.parquet (383,643 rows).
  REPORTED_DATE coverage: 2021-01-01 to 2026-10-13 (America/Denver).

## Traffic sizing (Finding 1)
- Denver Open Data Catalog: ODC_CRIME_TRAFFICACCIDENTS5YR_P (traffic accidents).
  ArcGIS FeatureServer layer 325:
  https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_CRIME_TRAFFICACCIDENTS5YR_P/FeatureServer/325
  Count-only REST queries run 2026-10-16/17; responses archived in this package as
  data/traffic_accidents_service_counts.json and in the warehouse as
  stack/denver/snapshots/2026-10-16/traffic_accidents_service_counts.json.
  Service description warns the traffic data is being revised by end of Q4 2026 with slight changes.
  Note: despite the "5YR" name, the service's reported_date spans 2013-01-01 to 2026-10-14.

## Denominators (neighborhood rates)
- US Census Bureau, ACS 2024 5-year estimates (2020-2024), table B25001 (total housing units),
  tract level, Denver County (08031), via Census Reporter API; archived in this package as
  data/acs_b25001_tracts_denver.json.
- Tract polygons: US Census Bureau TIGER 2024, Colorado tracts (tl_2024_08_tract.zip), archived in data/.
- Neighborhood polygons: city statistical neighborhoods, warehouse layers/neighborhoods_clean.parquet.
- Allocation code: code/denominators.py (area-weighted tract-to-neighborhood allocation).

## Warehouse layers used
- layers/crime_clean.parquet (offenses; Phase 2)
- layers/neighborhoods_clean.parquet (statistical neighborhood names + polygons)
- Cross-reference only: files/gtm/str-operator-brief-specimen.md (Five Points ACS denominator anchor, 15,639 units)

## Budget timeline (Who can act)
- Denver 2027 budget milestones as tracked in the daily-civic-data-brief goal records:
  final budget proposal due Oct 19, 2026; public hearing Oct 26, 2026; amendment vote Nov 2, 2026;
  final passage Nov 9, 2026.
