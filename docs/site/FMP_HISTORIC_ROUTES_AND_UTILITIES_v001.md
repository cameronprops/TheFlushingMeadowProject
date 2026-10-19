# FMP — Historic pedestrian, street, service and utility networks

**Production order:** RCA source-backed pavilion shell first, then the full fairground network. The schema/source acquisition can proceed beforehand, but published lines MUST remain UNTRACED until a period plan is registered.

## Requirement: walk where you want

The named network represents *historical ground truth and optional wayfinding*, not an artificial movement constraint. Unreal visitors may freely leave a mapped sidewalk and explore any safe modeled terrain. The path graph helps with destinations, automated visitor/camera paths and route finding; it must not impose invisible walls. Historic gates/service restrictions remain tagged, usable for period interpretation and optional scripted access modes.

The mapped data must include:
- Public pedestrian footpaths, sidewalks, promenades, plazas, road crossings, bridges, approach ramps and every fairground entrance.
- Named avenues and streets (historical spellings), major service roads, rear alleys, restricted loading lanes, staff passages, maintenance entrances, emergency access, tram/bus roadways as appropriate.
- **Utilities as distinct toggleable layers**: potable-water trunk mains, building-service laterals, sanitary sewer, storm drainage, sewage pumping, fountain water/pumps, gas, telephone/TV conduit, power distribution, area/street lighting, public-address zones. Never merge sanitary and storm pipes without confirming a source marks a combined sewer.
- Nodes for intersections, culverts, valves, handholes, manholes, gates, steps and entrances, with depth/invert elevation/pipe diameter and Z *only where plans actually give these*.
- Per-feature references to dated source drawing(s), precision/uncertainty, usage rights and state of digitization.

## What is committed NOW

- `database/migrations/015_dated_site_networks.sql` — connected nodes, route segments, dated feature identity, pipe depth and surveyed/non-surveyed status, and explicit cross-era lineage records. Database only routes `navigable=1` public records with traced positions/endpoints.
- `catalog/site_network_layers.csv` — **19** independent ACCESS/UTILITY/TOPOGRAPHY/CONTROL layers.
- `catalog/site_network_sheets.csv` — **43** concrete period plans, archived manuals, guide maps and finding-aid pointers.
- `catalog/site_network_features.csv` and `site_network_segments.csv` — **19** documented or provisional *named* route IDs in 1939 or 1964, all **UNTRACED, no invented centerlines**.
- `catalog/site_network_nodes.csv`, `site_network_era_relations.csv` — empty and ready for traced intersections and supported 1939/1940/1964/1965/2026 continuity.
- `tests/test_site_networks.py` — schema/integrity/safety tests, including era mismatch and false historical linkage rejection.
- Master database `tools/build_db.py` consumes this network and exposes `site_walkable_edges`, `site_utility_segments` and `site_network_progress` views.

### Major 1939–40 source leads
- NYPL *1939 World's Fair General Plan*: https://old-digitalcollections.nypl.org/items/926ff6bc-5ff8-0931-e040-e00a180628c4
- NYPL *Map of the World's Fair and approaches*: https://old-digitalcollections.nypl.org/items/b07fa8e0-35d3-0131-4020-58d385a7bbd0
- NYPL *All roads lead to the World's Fair*: https://old-digitalcollections.nypl.org/items/b8678170-35d3-0131-ce10-58d385a7bbd0
- NYPL World's Fair 1939–40 Corporation Engineering Records: https://worldsfair.nypl.org/containerlist.pdf, construction engineering and utilities series around boxes 1723–1728. Includes sewers, storm drains, pumping, 20-in/48-in water-main categories. These are **catalog pointers**, not scanned centerline drawings.
- Contemporary account (June 14, 1939): https://living-church-back-issues.s3.us-east-2.amazonaws.com/tlc/1939/6.14.1939.pdf names Constitution Mall, Avenue of Patriots, Avenue of Pioneers, Street of Wheels and Street of Wings. This PDF has not been completely scanned/verified in this run; names require period map cross-check.

### Major 1964–65 source leads
- [1964–1965 Fair **Operations Drawing Manual**](https://www.worldsfairphotos.com/nywf64/operations-drawings-manual/index.htm):
  - Sheets **3–4** general plan; **7** pedestrian entrances and turnstiles.
  - Sheets **28–30** water distribution; **31–33** storm drains; **34–36** sanitary sewers.
  - **37** fountain pump locations; **38–39** gas mains.
  - **11–15** primary/secondary electric; **16–21** street/open-space lighting; **22–24** telephone manholes/conduit; **26** public address zones; **27** television connections.
  - Unmodified sheet contents can be accessed from the site index. The exact reproduction/usage rights need checking; links in our index do **not** imply permission to redistribute sheets.
- [Official 1964–65 Fair guide/site map](https://butkus.org/information/worlds_fair_1964/world_fair_1964-1.pdf) documents public street names including Avenue of Progress, Avenue of Commerce, Avenue of Enterprises, Avenue of Travel, Promenade of Industry and Truman Promenade.
- NYPL 1964 Fair Corporation construction records (finding aid): https://nyplorg-data-archives.s3.amazonaws.com/uploads/collection/pdf_finding_aid/nywf64.pdf, boxes **177–179** for streets/roads/walks and **180** for water mains/sewers.
- 1965 must be reconciled against 1965 revisions. A 1964 street map is not proof the exact 1965 route remained unchanged.

## Register maps first, then trace—one route at a time

1. Acquire full-resolution period site plans and operations sheets. Log date/revision and store byte hashes and reproduction rights.
2. Pick surveyed ground-control points shared between dated historic plans and modern geodesy. Candidate site projected datum EPSG:32118; historical vertical datum unknown until engineering benchmarks are checked. Do not call old raster pixels survey measurements.
3. Fit transforms with at least 4 noncollinear points, record residuals and uncertainty; prefer registration tests on additional withheld points. Keep every map's georeferencing and local-datum provenance.
4. Digitize named public path boundaries and centerlines, public ramps/steps, loading/service lanes, access-restricted corridors, junction nodes and entrances. Preserve street widths, level changes, slope, bridges and over/underpasses, not just XY line drawings.
5. Separate buried utility network alignments on their actual sheets; add manhole/valve/pump nodes and pipe properties. Where Z is unknown, leave it blank. Do NOT assume modern NYC underground utility continuity or extrapolate water mains from generic campus infrastructure.
6. Promote an edge into `site_walkable_edges` only after topology/connectivity, geometry and period source review. For Unreal, use source graph to drive optional wayfinding and navmesh annotations, without preventing users from exploring off the path.
7. Rebuild and compare each temporal version: 1939, 1940, 1964, 1965 and 2026. Only link physically continuous/realigned/reused segments across eras with `site_network_era_relations`, evidence and confidence. Similar appearances alone are `POSSIBLE_LINK`, not `ALIGNMENT_PERSISTED`.
8. Export layer-tagged geometry to Worldwright and Unreal, separate visible pathway meshes from underground utility overlays; print-scale site model uses the same coordinates. Optional construction/show animations can expose historical utilities beneath fairground shell without pretending unknown manholes existed.

## Immediate production gates

- **RCA:** Its source catalog has a high-resolution original drawing access gate. A 29-component provisional shell/room preview exists; do not mark final measured RCA shell completed.
- **Network:** 43 sheet records, 19 layer definitions and 19 period name entries are ready; **zero surveyed/traced segment geometries**. First tracing pass after RCA should start with 1939 General Plan, then 1964 General Plan sheets 3/4, then 1964 water/storm/sanitary sheets 28–36.
- **Utility safety:** Historical utility linework should be visualized for interpretation; do not treat it as verified present-day dig-safe infrastructure. Current utilities must come from official modern utility owners/markout services, not this reconstruction database.
