# Theme Center framed portals v007

This is a separate provisional runtime architecture build from the preserved v006 winding-repaired model. It builds the missing elements; it is not a historical reconstruction certification.

## Built
- Trylon: a facade-aligned infill wall within the existing large opening, containing two framed 2.4 m wide by 2.4 m high doorways. Full-depth jambs meet the existing cut brace caps; headers and trim complete the openings. Two cut Helicline rail ends return into the exit jambs.
- Perisphere: two 2.35 m wide by 2.4 m high doorway assemblies with deep jamb reveals, headers, thresholds and solid curved collars meeting the sphere. The original closed lower-shell geometry is used to create precise Boolean apertures, replacing broad triangle deletion. A local spherical wall patch closes inherited oversized gaps around the new frames (outer radius 27.444 m, inner radius 27.328 m, overlapping the existing approximately 27.432/27.34 m shell); these patch dimensions are explicit runtime fitting allowances. The printable source remains unchanged.
- Upper Perisphere approach: a new outer landing and repositioned 23-tread stair with rails, posts and wall returns keep the rail starts outside the doorway throat.
- Superseded single stair and eight old portal trim guides are disabled. Source node identities are retained for replacements. No hinged door leaves are supplied.

Threshold finish is 1 mm above the inherited slab to avoid coplanar rendering artifacts. This small modeling offset is explicit, not a surveyed historic detail. Materials are neutral provisional finishes.

## Verification
`check_portals.py` verifies preserved source binary prefix, unchanged inherited mesh/material records, retained node identities/transforms, closed consistent new solids, brace-cap alignment with jambs, and a discrete sphere-cover body screen of 51 poses per opening (204 total, 2,652 sphere samples). Body: 0.6 m diameter and 1.8 m height, with 0.05 m floor lift. All active scene meshes near those poses are included. It is not continuous movement, global route certification or native Unreal testing.

`test_portals.py` has six regression tests for complete frames, clear dimensions, obsolete geometry exclusion, brace-jamb contacts, recorded body screens and closed shell/collars. Contact is geometry evidence, not a calculated structural load path.

Wolfram independently checked opening areas (5.76 and 5.64 square metres), the 12.4968 m Trylon infill height and Perisphere surface x-ranges used for reveal depth. No structural analysis was run. Game Development Studio CLI/Blender were unavailable; local Trimesh, Manifold and EGL/Pyrender were used. Renders are generated directly from the GLB with local section cropping and neutral diagnostic materials; no AI imagery.

## Reproduce
Requires Python with numpy, trimesh, manifold3d, rtree, scipy, shapely, pyrender, Pillow and an EGL-capable runtime.

Inputs (preserve bytes):
- `inputs/ThemeCenter_v006.glb`, SHA256 b7d59c46d66f26d93873f4ccde5f6bffcc45d4c4f7b5c4a146e888de7d2d3cc9. Available in the previous asset-fixes release.
- `inputs/Original_staging.glb`, SHA256 a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5. Existing staged original.

```
python build_portals.py
python check_portals.py
python -m unittest -v test_portals
python render_portals.py
```

Open `output/ThemeCenter_Framed_Portals_v007.glb` as the complete assembled scene. Do not layer it over v005 or v006; it already contains the retained geometry and replacements.

## Limits
The new wall, door framing, frame-member connections and rail returns are explicit provisional geometry fitted to the existing model. They do not establish the original entrance canopy, lettering, Art Deco bridge arch, historical door dimensions, structural engineering or original finishes. Source-derived historical entrance/bridge reconstruction is a distinct pending task. Native Unreal import, collision and full traversal remain untested. This file is not a print master or construction document.

Input archives: [v006 asset fixes](https://drive.google.com/file/d/1ofasHEQ3b9sQoqWM6rSGoQ7VVKZKqkYc/view), [original staging GLB](https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view). Inputs are linked rather than duplicated in this release ZIP.

## Validation hardening, 2026-10-20
The checker now binds its report to the exact GLB SHA256 and exits unsuccessfully on recorded contacts. Regression tests reject stale hashes, missing/duplicate/incomplete portal screens, absent contact results and failed geometry checks. Run `python check_portals.py` before `python -m unittest discover -p 'test_*.py' -v`. All 12 tests passed after a fresh 204-position screen of the unchanged v007 GLB. This remains a discrete surface check. Game Development Studio CLI is unavailable; local Python validation was used. No new mathematical geometry inference required Wolfram.

The Drive v007 ZIP remains the immutable original release. These updated validators and report are maintained in Git; overlay the current repository scripts when reproducing this hardening.
