# FMP bounded asset fixes: tasks 2, 3 and 4

## Delivered
- Three actual-mesh Trylon entry/cutaway/Helicline approach renders. Orange marks runtime replacement objects, cyan marks provisional route surfaces. These are diagnostic local crops, not historic illustrations. The cutaway explicitly hides the exterior shell. Other views retain it. Camera position and clipping planes are reproducible in render_views.py.
- Separate ThemeCenter_WindingRepair_v006.glb: five scenic meshes repaired, 1,898 triangle windings reversed and normals regenerated on these meshes only. Original vertices, materials, node hierarchy, IDs, transforms and complete original binary prefix retained. All other mesh records unchanged. Same active triangle count. Shared-edge consistency verified; this does not establish outward orientation for every disconnected open component.
- WF0028_RuntimeFiltered_v015.glb: 37 diagnostic/reference/zone/proxy objects removed from active geometry; 46 modeled components retained. Diagnostic mesh records removed, node identities retained, raw buffers preserved. Runtime exporters/importers must consume the active scene. This is not a tested Unreal collision asset.
- Six passing regressions covering real assets, source preservation, unknown kind refusal, hash mismatch refusal, unregistered mesh refusal and synthetic v016 reference-only flags.

## Architecture findings
The model has a visible opening. Rendered brace ends remain cut and unreframed, and rail returns/edge protection remain unfinished. The renders do not prove historically correct portal proportions or complete architecture. No portal or structural geometry was changed in this pass. No native Unreal testing.

## Version scope
Theme Center input v005 SHA-256 de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439.
WF0028 input v015 SHA-256 7b18fcf22833e7a77c33aa73f3cbe6b5ccd052881cafab906eaac474dde2efa3.
A concurrent v016 courtyard study exists. Its reference-only flag is covered by a synthetic test; this release does not claim to have exported the actual v016 bytes. Unknown new component types stop the filter.

## Reproduce from this package
Python packages: numpy, trimesh, scipy, shapely, pyrender, Pillow, PyOpenGL. EGL is required for offscreen rendering. Game Development Studio CLI and Blender were unavailable; local Trimesh and EGL/Pyrender performed these checks. No paid generation or AI imagery used. Source rights remain inherited and unresolved where the project has not established them; this package adds no license grant.

```
python asset_fixes.py repair inputs/ThemeCenter_v005.glb output/ThemeCenter_WindingRepair_v006.glb
python asset_fixes.py filter inputs/WF0028_v015.glb output/WF0028_RuntimeFiltered_v015.glb --manifest inputs/WF0028_v015.json
python -m unittest -v test_asset_fixes
python render_views.py
```

Next: resolve visible brace transfers and rail termination details from historical evidence; run isolated Unreal import/collision tests when an engine is available. Do not treat these diagnostic images as a structural approval.
