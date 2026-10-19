# Historical drawing georeferencing

Goal: align independently documented 1939 and 1964 source drawings to a shared projected reference frame for Rhino/Unreal, without inventing survey control.

## Coordinate policy (2026-10-18)
- Canonical FMP projected reference for New York: **EPSG:32118**, NAD83 New York Long Island, **metres**.
- Existing NYC GIS generally uses **EPSG:2263**, NAD83 New York Long Island, **US survey feet**. It is the same projection parameterization with a different unit. Conversion factor: **1200 / 3937 metres per US survey foot**.
- **EPSG:26918** (NAD83 UTM 18N) is an alternate metre-based coordinate system supported by the solver; never mix it with EPSG:32118 inside one control batch.
- EPSG:4326 latitude/longitude is **in degrees**; it must not be placed into metre fields.
- Historical drawings may use older geographic and vertical datums. These require authenticated datum transformation research, not just multiplying coordinates. Contemporary streets and features may have moved.
- No global origin has been certified. Choose a fixed local 3D origin only once trustworthy survey coordinates exist. Keep the canonical world coordinates as double-precision metadata to prevent accumulated drift in engine/local floats.

NYC DCP metadata confirms EPSG:2263 and US-foot units: https://www.nyc.gov/assets/planning/download/pdf/data-maps/open-data/dcm.pdf
CRS 2263: https://epsg.io/2263
CRS 32118: https://epsg.io/32118

## Files
- fmp_georef.py: six-parameter 2D affine least-squares fit on metre world coordinates. Numerical stability uses pixel centering/scaling. Outputs residual vectors, RMSE of fitting controls, and RMSE of independent check points.
- fmp_import_nyc_state_plane.py: strictly converts EPSG:2263 US-foot coordinates to EPSG:32118 metres, maintaining all other point and provenance fields.
- FMP_Point_Digitizer_v0_1.html: browser-based local source-image observation capture.
- test_fmp_georef.py: 12 synthetic unit tests, including bad holdout, misdeclared foot/degree data, degenerate controls and duplicate/nonfinite input. **Synthetic tests are not proof of historical alignment.**

## Workflow
1. Digitize a legally acquired original plan scan, retaining the source document's catalog ID, revision, resolution and rights metadata.
2. Determine independent surveyed correspondence for at least 3 non-collinear control points and 2 **different** check points.
3. If surveyed world coordinates are from NYC State Plane EPSG:2263, create CSV with source_crs,world_x_ftus,world_y_ftus plus the digitizer's id,role,pixel_x,pixel_y fields. Conversion is explicit:

    python3 tools/georeferencing/fmp_import_nyc_state_plane.py points_ftus.csv points_m.csv

4. If metre coordinates are already known, provide CSV fields id,role,pixel_x,pixel_y,world_x_m,world_y_m,crs directly, all using the same metre-based EPSG code.
5. Fit:

    python3 tools/georeferencing/fmp_georef.py points_m.csv --output transform.json

6. Inspect check_rmse_m and the independent residual vectors. A low control RMSE alone can mask extrapolation and incorrectly matched landmarks. The script **never certifies** a transformation.
7. Repeat for the other period's scan. Keep separate per-image matrices plus shared EPSG:32118 coordinates; do not align by copying features from one speculative reconstruction.

Test with: cd tools/georeferencing && python3 -m unittest -v

## What remains blocked
No archival survey measurements or surveyed cross-era control pairs have been acquired or qualified. The NYPL 1939 XM-250 public download is only a small preview; 1964 Operations Manual sheets are rights-restricted derivatives. This code does not solve vertical grading, camera perspective, or historical NAD27 to NAD83 transformations.
