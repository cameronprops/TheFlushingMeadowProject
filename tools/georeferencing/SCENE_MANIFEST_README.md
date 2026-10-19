# FMP shared site coordinates and Unreal export

The scene manifest turns **already fitted** historical plan image coordinates into local site coordinates and Unreal centimeters. It never estimates geographic positions itself.

## Status
- Implemented: 2D image-pixel → NAD83 NY Long Island Easting/Northing (EPSG:32118) → site-local meters → Unreal XY centimeters
- Implemented: inverse mapping, source-by-source numeric RMSE status and mandatory local origin provenance
- Not implemented or certified: horizontal survey validation, source rights, geodetic datum transforms, real-world origin selection, or any Z/vertical-datum placement
- No historical asset has been positioned with this pipeline yet. All demonstration values are **synthetic only**.

## Commands

First run `fmp_georef.py` on each original scanned plan using externally surveyed, verified coordinates and **EPSG:32118**. To convert EPSG:2263 foot coordinates, use the previously committed `fmp_import_nyc_state_plane.py`. Do not use UTM EPSG:26918 coordinates directly: that requires a real projected CRS transformation, not unit conversion.

Then choose a documented, genuinely surveyed site origin (E, N in meters). Run:

```bash
python3 tools/georeferencing/fmp_scene_manifest.py \
  --fit XM250_1939=path/to/1939_fit.json \
  --fit OPS64_S03=path/to/1964_fit.json \
  --origin-easting-m YOUR_VERIFIED_EASTING \
  --origin-northing-m YOUR_VERIFIED_NORTHING \
  --origin-source 'your survey document, page, point ID' \
  --max-check-rmse-m YOUR_PROJECT_SPECIFIED_TOLERANCE \
  --output path/to/fmp_scene.json
```

`--max-check-rmse-m` is optional; without it, numerical QA status is UNASSESSED. Passing that numeric threshold **does not** certify historical accuracy. Specify it according to the model's purpose, source resolution, and documented QA policy.

## Field definitions
- `pixel_to_projected_m` = `E=ax*u+bx*v+tx`, `N=ay*u+by*v+ty`, where `u` is original raster pixel X and `v` is original raster pixel Y.
- `pixel_to_local_site_m` = projected metres minus the explicitly sourced site origin.
- `pixel_to_unreal_cm` = those site-local XY values times exactly 100. The manifest's *project-specific* convention is X=east, Y=north; no universal Unreal world orientation is implied.
- `projected_m_to_pixel` and `local_site_m_to_pixel` are independent mathematical inverses of the fitted affine, for traceable hotspot/asset markup.
- `vertical.status=UNRESOLVED` means the pipeline does not move/sculpt elevation; Z must be independently modeled after confirming its vertical datum.
- `use_status=PREVIEW_ONLY...`: source survey and rights review are still required.

## QA

```bash
cd tools/georeferencing
python3 -m unittest -v test_fmp_scene_manifest
```

Tests are synthetic; they check round trips, unit conversion and origin subtraction, multi-map scenes, rejection of wrong CRS, singular matrices, bad input and unsupported certification claims.

## Branch and world-state separation
The same local coordinate frame can be used by historical 1939 and 1964 worlds, a present-day park environment, and the four fictional 2039/2064 locations (good and bad branches). No fictional asset becomes part of the historical evidence register. This export works on source-map IDs, not on world-story branches; world-state assignment belongs in the separate scene/world registry.
