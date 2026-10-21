# Upper Perisphere landing repair v008

The diagonal 1.85 m stair began partly beyond the v007 rectangular landing. Fifteen vertical support probes, 100 mm before its first tread, found only nine on the landing level. The outer stair corner projected 0.676524 m beyond the old landing minimum X, independently checked with Wolfram.

v008 replaces only `PROVISIONAL_UpperLandingToStair` with a closed 160 mm slab fitted to the existing stair and landing-rail footprint. A stair-width notch ends the landing at the first tread. The original GLB binary prefix, all old mesh records, all materials and every other node are preserved. Source inputs are unchanged. This is a provisional runtime repair, not original 1939 architecture or structural engineering.

Verification: four tests pass, including reproduction of the old defect, 15/15 supported approach probes, 15/15 probes on the first tread at its intended lower elevation, and exact preservation of unaffected scene data. The before/after PNG and SVG are actual mesh plan sections, visually inspected. Game Development Studio CLI is unavailable; local Trimesh/Manifold and Matplotlib were used. Native Unreal collision and full traversal remain untested.

## Reproduction layout

Keep this directory named `portal_approach_v008` next to `portal_build`. Populate `portal_build` with the previous [v007 archive](https://drive.google.com/file/d/1yF-mgJDTLaksGkV231E65VvXvVxSAZwr/view), including its output GLB/manifest. The inherited portal checker additionally needs the original v006 input named `portal_build/inputs/ThemeCenter_v006.glb`, available through the v007 README input links. Required Python packages: numpy, trimesh, scipy, rtree, manifold3d, matplotlib.

Run `python fix_landing.py`, then `python -m unittest discover -p test_landing.py -v`. Run `python check_landing.py ThemeCenter_UpperLanding_v008.glb after.json` and `python check_portals_v008.py`. `review_landing.py` creates the drawing from the model and before/after support reports.

Open `ThemeCenter_UpperLanding_v008.glb` as a complete scene, not an overlay. Source sha and output sha are recorded in `repair_manifest.json`. Existing reports concern discrete point/surface probes only.

Archive scope: code, SVG and JSON committed through GitHub; complete package saved to project Drive. PNG/GLB/ZIP Git binary copies remain pending because direct push lacks credentials and no binary release connector is exposed. The earlier workstream archive and transcript backfill remain open as recorded in the central register. No full conversation export is available.

Fresh v008 doorway screen: all 204 poses (2,652 sphere samples) have no recorded surface contacts. This is separate from the 30 landing/tread support rays.
