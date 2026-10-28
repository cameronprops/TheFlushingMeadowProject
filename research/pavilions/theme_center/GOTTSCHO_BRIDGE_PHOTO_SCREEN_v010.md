# Theme Center actual archival photographic edge screen v010

**2026-10-27. Status: tested real-source pixel-domain screen; NOT camera calibrated or certified historical geometry.**

This is the next increment after v009. A real CC0 1939 **Samuel H. Gottscho / Met 1987.1100.403** photograph was retrieved as the unchanged Wikimedia Commons 960 × 1177 *derivative* by Wolfram, and a crop was inspected. Wikimedia lists the 3138 × 3847 full scan as CC0; this workflow **has not acquired and SHA-256-hashed that original JPEG's bytes**. It has preserved the decoded **960 px pixel-array SHA-256** as an exact source identity: `4b618f1f2531684e0e35006cf0f775f3cef5d6ae7160787c002ae4f5e41a5777`. A decoded pixel-array digest is *not* the original JPEG-byte digest.

### Photographic finding

The actual image shows a **smooth concave underside of the OPEN ELEVATED RETURN BRIDGE** near the Perisphere, with a rounded projecting tip, slim vertical supports, and an upper railing with visitors. This is not a hypothetical Art Deco truss. The adjacent **ground-level lettered PERISPHERE ENTRANCE canopy is partly obstructed by foreground tree branches and crowds**. No actual street entrance jamb intersections are sufficiently exposed for confident photogrammetric coordinates. The second Met Gottscho 1987.1100.404 from a different distant viewpoint cannot presently be treated as a 3D stereo match for entrance or bridge detail.

The Wolfram pixel-array image edge screen scanned 13 vertical columns near the dark-skin/bright-sky lower bridge silhouette. The operator selected the strongest absolute vertical intensity gradient inside a **manually predicted ±22px window** on the actual displayed 960px image. Only five relatively clear and stronger-contrast screen edge candidates **x=600..680 px** are admitted, after reviewing the historical crop. The remaining eight are review/reject due to weaker contrast, trees, people, columns or competing edges. This is a real-photo *2D* curve, not a 3D projection solution or surveyed geometry. Stored pixel guesses, picks and absolute gradients are auditable.

### Output

`research/GOTTSCHO_BRIDGE_EDGE_ANNOTATIONS_v010.json` contains all 13 sampled real-photo source pixels, source rights metadata, the hash, analyst guess windows, explicit decisions and exclusions. `tools/bridge_edge_screen_v010.py` performs an immutable source/dimension/observation check, fits an in-domain quadratic, and computes leave-one-out 2D residuals. `reports/BRIDGE_2D_SCREEN_v010.json` is generated. Tests deliberately reject fake source hash, changing imaging dimensions, out-of-bound points, weak accepted edges, outlying fit, and attempts to claim an acquisition or photo camera pose.

**No new 3D arch profile**, canopy dimension, entrance position, stair riser or 1939 grade was inferred. No source CAD/GLBs were edited. The 2D quadratic is **not to be extruded or assumed to describe real architectural curvature**.

### Run

From the v010 package directory: `python -m unittest discover -s tests -v` and `python tools/bridge_edge_screen_v010.py research/GOTTSCHO_BRIDGE_EDGE_ANNOTATIONS_v010.json reports/BRIDGE_2D_SCREEN_v010.json`. Runtime needs Python and NumPy, not the unavailable `game-dev` CLI. The pixel selections were performed in connected Wolfram on the original Commons thumbnail, not re-extracted by this standalone script.

### Next source acquisition

Obtain the exact CC0 original scan and independently photograph its exposed left bridge attachment and right terminal from different viewpoints, or use a dated dimensioned site control. The current photo's bridge underside silhouette is valuable for rendering/perspective residual tests, but cannot fix the unknown focal length, the 3D curve, and the grade entrance width simultaneously. To actually lock a doorway to 2–3 inches, obtain noncoplanar real 3D site controls, camera intrinsics, matched points, holdouts, and a full X/Y/Z error budget. Get the actual RIBA stair photo original and verify every step nose before replacing v008 provisional stairs. Existing v009 23-step compatibility with proposal-level 64/52 ft is not a substitute for as-built evidence.

**Rights:** Gottscho Met CC0 image is documented; no photographic image bytes or crops are included in this package (image delivery unavailable to container in this session). The JSON stores a rights-cleared source URL and working image digest; original source JPEG archive to Drive is **PENDING**, and rights-provenance must remain with later binary upload.
