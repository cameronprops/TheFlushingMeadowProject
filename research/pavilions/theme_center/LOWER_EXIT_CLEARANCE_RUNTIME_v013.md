# FMP Theme Center — lower public exit clearance v013

**Status: implemented, read-only source preserved, 14 regression tests passed, 13/13 model-local doorway cross sections clear in derived runtime. Historical placement remains provisional.**

## Source and construction rationale
- Original assembled v005 GLB SHA256: `de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439` (47,126,840 bytes), Y-up metres / *UNREGISTERED* model coordinates.
- The RIBApix RIBA9908 actual photograph and prior v011 cropped evidence show the lower Perisphere public exit beside the solid upper-stair cheek, with doorway bottom occluded by railing. Function is very likely a lower public exit, not documented as a service door. Do not assert measured door dimensions from photograph.
- v012 found **two alternative provisional stairs** in the scene. Source legacy `PROVISIONAL_UPPER_EXIT_STAIR` is mesh-bound node 498 / mesh 643, while 23 separate `PROVISIONAL_UpperReturnStair_01..23` mesh proxies connect the upper landing to the bridge.

## Measured interference in the original ACTUAL GLB
- Lower portal framing defines the modeled empty threshold volume across X [-22.412722, -22.192722], Y [15.849600,18.249599], Z [1.873000,4.223000] metres.
- A conservative 30mm inset from sill, head and jambs leaves modeled interior cross section Y [15.879600,18.219599], Z [1.903000,4.193000]. Wolfram verifies **2.34m high × 2.29m wide** for this inset, but these are *existing provisional model* dimensions, not 1939 observations.
- All 13 separate X-slices through that framed opening intersect the old `PROVISIONAL_UPPER_EXIT_STAIR` mesh. Sampling exact scene triangles against the inset clear-passage 2D section isolates that node as sole interfering mesh. This is more specific than old broad-phase AABB-overlap claims.

## Derived candidate fix
- `repair_lower_exit_v013.py` validates source SHA, GLB 2 chunk lengths and **exact GLB node 498 / mesh 643 identity**, then removes ONLY that mesh reference in a DERIVED GLB, retaining all 573 nodes, all 833 mesh definitions, all transforms, existing newer 23 tread meshes, and **byte-for-byte identical entire binary geometry chunk**.
- `FMP_ThemeCenter_Runtime_LowerExit_Clear_v013.glb` is a runtime-preview derivative. `PATCH_REPORT_v013.json` retains the full original binding to restore; source v005 ZIP never modified. For actual v012 upper sidewall use its separate provisional overlay (v012 is **not** baked into this GLB).
- `check_lower_exit_v013.py` independently reopens original and derived GLBs and section-tests clear interior through lower exit: **before 13/13 blocked; after 0/13 blocked**, subject to 30mm inset and finite X-slice sampling.
- `test_lower_exit_v013.py`: **14/14 passed** including SHA source lock, exact original BIN preservation, mesh/node counts, immutable nonlegacy mesh bindings, 23 active replacement treads, wrong-source rejection, loader reopen, and 13-slice model-level clearance. Missing `game-dev` CLI means no native Game Development Studio / Unreal import, collision, whole-scene swept capsule or actual guest traversal claim.

## Status / future
**IMPLEMENTED, TESTED, PROVISIONAL model-space clearance repair.** Not a historically certified door location/size or Unreal-ready collision clearance. Next: integrate with v012 separate cheek and inspect upper stair full-volume interference; obtain accurate archive drawings for 1939 doorway location; run native Unreal player/agent sweeps and collision.

Source/provenance: https://www.ribapix.com/ (original RIBA item identification unresolved), secondary source https://drivingfordeco.com/vanished-new-york-city-art-deco-the-trylon-and-perisphere-part-two-1939-1941/ ; master v005 source released in existing Drive archive and same SHA in project research.
