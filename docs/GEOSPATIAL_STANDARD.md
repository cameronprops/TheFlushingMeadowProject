# Survey, elevation, and terrain point of truth

The master **horizontal CRS and vertical datum are not yet selected**. No invented datum, offset, survey control, or local-to-UE alignment may be described as measured.

For each terrain, map, aerial or survey record, capture:
- Geographic coverage and survey/acquisition **date**, not merely publication date
- Source agency, document ID, original URI, Drive archive URI and checksum
- Horizontal CRS including EPSG/WKT where present, map projection, map units
- Vertical datum (NAVD88, NGVD29, local benchmark, etc.), geoid model, elevation units, bathymetry assumptions
- Resolution, accuracy, bounds, transformation software and residuals, uncertainties
- Legal reuse/download status and original metadata
- Exact year state(s) for which it is usable

Recommended processing:
1. Obtain survey controls and build a 2026 georeferenced baseline using documented contemporary terrain sources.
2. Locate historical survey sheets/contour maps and construction grading drawings, and fit them to period reference controls.
3. Build 1939, 1940, 1964, 1965 and 2026 terrain states separately.
4. Quantify changes around the fairground landfill, Meadow/Willow Lakes, parkways, stations, river, pools and rail embankments.
5. Declare an Unreal local origin and its invertible coordinates transform only after controlled registration.
6. Verify landscape/elevation seams, water levels, tunnels, accessibility and collision against test points.

**Existing Democracity/Theme Center mesh transforms are authoring transforms, not surveyed park georeferencing.**

Terrain sources and measured anchors live in the database's `surveys` and `control_points` tables when available.
