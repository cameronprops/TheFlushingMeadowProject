# FMP shell-first architecture release — 2026-10-19

The user's current production requirement is EXTERIOR SHELLS, PUBLIC INTERIOR SHELLS and scaled 3D-print outputs. Steel is evidence metadata and a future OPTIONAL exposed-construction animation layer, never a default dependency.

## Original Trylon/Perisphere model retained

Source: https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view
SHA-256: a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5
510 nodes; metres, Y-up, site coordinates not georegistered. Source geometry is not changed. 1939 built sizes are 610ft Trylon and 180ft Perisphere.

Run shell kit:
    python3 tools/building_program/build_shell_kit.py --source path/to/FMP_ThemeCenter_Staging_v001.glb --out out/theme_center_shells

Product parts: THREE exterior shell nodes (Trylon, upper and lower Perisphere); TEN interior projection/guest-viewing objects; FIVE circulation objects (bridge/Helicline/escalator previews); SIXTY optional steel/structural objects. Combined real-time preview has the first 18 only and omits steel. Dated dimensions/source facts remain in source database. All GLBs re-imported locally; native Unreal is untested.

## Printable shell exports (STL is unitless, slicer units MUST be millimeters)

- Trylon 1:800 full height: 26.50 × 31.24 × 232.41 mm.
- Perisphere upper and lower hemispheres 1:800: 68.57 × 68.57 × 34.29 mm each.
- Perisphere upper and lower hemispheres 1:250: 219.43 × 219.43 × 109.73 mm each.
- Perisphere upper and lower hemispheres 1:200: 274.28 × 274.28 × 137.16 mm each; too wide for standard 256mm beds.
- The Trylon at 1:200 would be roughly 930mm tall and must be split; no misleading shortcut segmentation was performed.

All SEVEN exported print meshes are watertight and positive-volume with consistent winding. This is NOT a successful slicer/physical print certificate: wall thickness, resin suction, support orientation, print-bed margins, tolerance, keyed joins, magnets, exact assembly are outstanding. A watertight mesh is not necessarily a good print.

## Additional pavilions use the same extraction interface

Generic script: tools/building_program/export_shell_layers.py. Inputs are an existing GLB plus dated JSON profile specifying source SHA and unambiguous node-pattern roles.

- WF0020 Westinghouse: 326 exterior tower/facade meshes + 57 public interior-preview meshes, from the existing 383-component model.
- WF0014 Ford: 133 exterior, 4 interior, 128 Road of Tomorrow, 12 Cycle of Production, 33 garden/site mesh components, from existing 310-component v0.3.
- No steel has been invented for either pavilion.
- Both remain photographic/interpretive models: registered placement, finished material surfaces, accurate floorplan and Unreal collision have NOT been verified.

Example:
    python3 tools/building_program/export_shell_layers.py --model Westinghouse_1939_Visitor_Access_Proxy_v002.glb --profile tools/building_program/profiles/WF0020_Westinghouse_1939.json --out out/westinghouse

## All 195 building-candidate dossiers now use one policy

Migration database/migrations/011_shell_first_production.sql provides building_reconstruction_policy for all 195 candidate records, defaults structural_frame_priority=OPTIONAL_DOCUMENT_IF_SOURCED, and records exact historical source nodes for the Theme Center. The modified tools/export_building_dossiers.py reports these parts and their roles. This is a production default: no evidence is implied for unevidenced buildings, and no source file or child attraction is promoted to a new pavilion automatically.

## QA and next steps

Nine shell/export tests passed locally, with complete original source hash checks. Full SQLite migration against a complete checkout and Unreal/Rhino/Worldwright host testing are pending. Next: source-backed shell aperture/door refinement; real print wall checks; optional keyed Trylon segmentation; realistic/stylized material instances; first visitor movement test. Construction-sequence animation may be built from the preserved steel layers if chronological sequencing is substantiated.
