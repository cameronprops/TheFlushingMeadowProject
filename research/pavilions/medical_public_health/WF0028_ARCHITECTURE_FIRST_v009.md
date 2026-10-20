# WF0028 interpretive architecture-first courtyard correction v009

Created and locally executed 2026-10-20. Rebuilt a **separate** geometry variant from v003 rather than changing v004/v008.

## Why the previous route was failing
The courtyard is positioned **between the east wall of Medical Hall and the west wall of Science Hall**, but v004 had put provisional courtyard entrances into their *north* walls. The east and west side walls therefore continued to block the cross-courtyard route. Route waypoint relocation did not correct this topological architectural problem.

## What changed
- Retained original v003 architectural/exhibit geometry except `MEDICAL_HALL_E_WALL` and `SCIENCE_HALL_W_WALL`, which were replaced **only in this alternate runtime model**.
- Added two side-wall opening assemblies (each with two wall segments and lintel), conjectural **3.6m wide x 3.2m high** at local Y=6m.
- Added a conjectural east courtyard threshold surface bridging the walk and Science Hall footprint.
- Added seven local route stations, six consecutive links across the courtyard; north-wall doors from v004 **not retained** in this alternative.
- 77 independent mesh components; GLB and JSON manifest in the release package. Original v003/v004 untouched.
- Six of six specific crossing segments had **no static 2D inflated-AABB obstacle intersection**; seven station positions overlapped modeled floor/walk footprints in XY.
- Six local Python regression tests pass, including v003 geometry preservation, side-opening placement, 2D route segments, floor footprint presence, false-certification guards and GLB reload.

## Limits
All structural dimensions, openings and routes are **hypothetical**. Ground overlaps are 2D, not confirmation of seamless vertical floor elevation or accessibility; no continuous swept capsule, hardware collision or Unreal NavMesh. This is an interpretive architectural improvement, not 1939 as-built geometry.

ZIP SHA256: `396db18dbbf1697bdec14f8cf09dac12289774965fabdc20c862ab9213b1aa42`.

Next: sample floor elevations along crossing segments and test a continuous 3D capsule against the full collision geometry. Then seek 1939 architectural drawing proof before treating these as actual doors.
