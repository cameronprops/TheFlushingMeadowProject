# FMP Fairground Atlas — historical layout, BIM and Unreal world placement

**Release:** v0.1, 2026-10-19. **State:** tested offline raster-tracing editor; site coordinates NOT yet historically registered.

## One master — many outputs

The existing FMP master SQLite/CSV database owns IDs and evidence for buildings, structures, water features, public services, horticulture, networks, printable parts and Unreal asset revisions. **Atlas adds dated placement and review data**, not a competing database. One entity can have 1939/1940/1964/1965 versions, with separate source map and location claims.

The Atlas can form the GIS/architectural portion of a Forma-like game BIM. Unreal owns render/interaction/streaming; future Worldwright owns CAD edits and potentially mapping/show control. Neither system should write an uncontrolled new coordinate for an existing building.

### FMP schema

- `atlas_reference_maps`: dated source map, original archive link, local raster fingerprint, control-point fit and source-image dimensions.
- `atlas_world_frames`: projected metre CRS, user-chosen Unreal-local origin, elevation datum and review status.
- `atlas_placements`: one historical feature, dated, with point, route polyline or footprint polygon and a source link. Contains **pixel** geometry and (only after georeferencing) **projected** geometry separately.
- `atlas_placement_reviews`: explicit researcher/source approval history.
- `atlas_unreal_ready`: source-checked, registered geometry + reviewed world frame + approval only. A raster trace does not appear here.

## Start tracing actual plans now

Open [the Fairground Atlas editor](../../tools/site/fairground_atlas.html) locally in your web browser. Select the year (1939, 1940, 1964, 1965), then download a period map raster from the indicated source and click **Load historic map image**. Select an object from the left catalog and mark a **Pin**, **Route**, or **Footprint**. This works for whole pavilions, fountains, pools, sculptural objects, park benches, streetlights, drinking fountains, planted areas, streets, service alleys or utilities.

The starter palette highlights the major buildings and features. Import [the full 260-entry FMP asset palette](../../tools/site/atlas_asset_catalog_v001.json) into the editor for remaining candidates and landscapes. Not every archival candidate is a verified independent building.

When marking something, attach the period archival source link, what you actually saw and any caveats. **Export layout JSON** periodically. The JSON preserves editable points/lines/polygons but does NOT redistribute the historic map image; keep that raster and its acquisition/rights record separately. To reopen, import the session JSON then load its original map raster again.

### Candidate high-value source maps

1. [NYPL World's Fair 1939 general site plan](https://old-digitalcollections.nypl.org/items/926ff6bc-5ff8-0931-e040-e00a180628c4), Corporation records; document catalog broadly dated 1935–1945. Verify which revision you're using.
2. [NYPL period fairground guide map](https://old-digitalcollections.nypl.org/items/b07fa8e0-35d3-0131-4020-58d385a7bbd0), created 1939–40, available with NYPL free-use download options, useful for first visual tracing but not a geometric survey.
3. [1964–65 Operations Drawing Manual](https://www.worldsfairphotos.com/nywf64/operations-drawings-manual/index.htm), general plans 3–4; physical furniture layout 8–10; street lighting 16–21; water 28–30; storm drains 31–33; sewers 34–36; fountains 37.

## Pixel alignment vs surveyed site location

1. Trace the reference image in the editor. The geometry is explicitly `RASTER_TRACE` in source pixel coordinates; there are initially **zero registered world positions**.
2. Georeference that exact raster using at least **3 control and 2 independent holdout points** with the existing `tools/georeferencing/fmp_georef.py`. Use metric EPSG:32118 or EPSG:26918. EPSG:2263 observations must pass the existing US-survey-foot converter. Consider [QGIS Georeferencer](https://docs.qgis.org/testing/en/docs/user_manual/working_with_raster/georeferencer.html) for preparing/inspecting control points and GeoTIFF layers.
3. Export a draft CSV from the Atlas JSON with `python3 tools/site/atlas_handoff.py csv draft.json --database out/flushing_meadows.sqlite --out out/atlas_placements_draft.csv`.
4. Optionally run `python3 tools/site/atlas_apply_georef.py out/atlas_placements_draft.csv --fit fit.json --map-id ATLAS-1939-GENERAL --output out/atlas_projected_preview.csv`. The independent-check RMSE must satisfy the threshold. **This is still a preview and does not approve locations.**
5. An independent historical review confirms the map revision, exact placement, uncertainty, common-frame origin and vertical datum. Only then can a reviewed row become `REGISTERED_REVIEWED`, with a named approval in `atlas_placement_reviews`.
6. Import reviewed records into canonical `catalog/atlas_placements.csv` and commit. Regenerate the database with `python3 tools/sync_master_database.py --once`.

Automatically derived outputs: `out/fairground_atlas/asset_catalog.json` and `out/fairground_atlas/unreal_approved_placements.json`. An empty Unreal-ready file is correct before approval; it is not a broken pipeline.

## Unreal: worldbuilding from existing source geometry

Use **World Partition** for large-area loading and One File Per Actor/Level Instancing for editability. **Data Layers** are per year and function: `1939/Buildings`, `1939/Paths`, `1939/Fountains`, `1939/Gardens`, `1939/PublicServices`, `1939/Underground`, with corresponding distinct 1940/1964/1965 layers. Utilities can remain hidden diagnostic layers unless intentionally presented in a construction or time-transition view.

A reviewed building footprint references its `building_id` and active GLB asset. A route polyline becomes an Unreal spline and navigation/guide-path input; pedestrians can leave the historic paths because traversal is controlled by terrain/collision, not by the database. Water polygons feed pool boundaries, water materials and fountain cue locations. Reviewed plant polygons and species/count data can drive PCG under **historical placement constraints**; unverified filler belongs on a separately labeled interpretive layer. Benches, sculptures and lightpoles are individual registered placements rather than copied generic scatter.

Projected survey X/Y are in **metres**. A reviewed frame stores a nearby metric origin; convert `(easting-originE, northing-originN, height-originZ) * 100` into Unreal **centimetres** to keep numeric precision. The `atlas_unreal_ready` exporter applies that translation and does not assert that native Unreal imports, collision or materials have been tested.

For 3D printing and future projection mapping, a building/feature uses the exact same reviewed placement and model ID but different geometry detail, print segmentation, surface materials and projector calibration. Worldwright can eventually participate as the parametric editor and show-control environment without reauthoring the site.

## Storyboarding and review

The Atlas is an evidentiary site-layout storyboard already: one can inspect the map, date, road, pavilion and its associated source/uncertainty. Planned next: saved camera bookmarks, shot-board sequences, map comparisons and time-transition review notes (a shot's pose is NOT survey evidence). No extra fictional themes or storytelling are authored by the Atlas.

## Release honesty

**Tested locally:** offline browser image loading, source selection, point/line/polygon drawing, editable evidence properties, year filtering, JSON export; 16 Python data/georef checks. No source map image is bundled; sample grid in tests is clearly marked synthetic. **Not yet completed:** registered historic map, world coordinate points, automatic real Unreal Actor spawning, production UI hosting, native world streaming/collision, multiuser storage, and physical projector calibration.

**Next actionable task:** select the highest resolution and most final 1939 site plan, resolve historical map revision, register at least five independent fixed control/check points, then trace the Theme Center, Ford, RCA, GM, Westinghouse, Fountain/Lagoon of Nations and primary site circulation from the actual drawing before propagating furniture and planting data.