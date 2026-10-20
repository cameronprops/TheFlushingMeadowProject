# WF0028 v011 full-width pedestrian envelope screen

Date 2026-10-20. Reused v010 GLB, v008 route candidates and v004 authored building component manifest. Script samples center plus 16 perimeter points at radius 0.45 m, pedestrian height 1.8 m and 0.20 m centerline increments. Floor supports selected from floor, walk, entry and landscape proxies; v010 added walkway GLB geometry loaded as axis-aligned bounding extents. Heights and collidable vertical obstruction boxes inspected.

**Results:** 14 links evaluated, 8 pass this preliminary sample-screen, six fail width support and/or surface step. Both street-approach links have elevation transitions. Man east display to north face, Man courtyard face to west courtyard, western courtyard crossing, and east courtyard to Science north face have support gaps. Western and eastern courtyard crossings also have steps. No collidable AABB contact detected, not equivalent to full 3D sweep.

Seven local unit tests pass. This is a conservative but imperfect approximation: rotated floor-strip AABBs may overstate support and sampled body checks may miss geometry. No Unreal NavMesh check. Geometry unchanged; the 76 historic-*hypothesis* elements remain distinct. No doors or floors should be asserted as real 1939 evidence.

Package: WF0028_1939_Body_Clearance_Audit_v011.zip; SHA256 `4c9eeb0abd3ea1b8f90c86744a3c934d68e08c972a9112c64e1081ad415fe9cd`. Contains v010 model, v011 scripts and JSON output, test results and prior builders.

Next v012: generate separate ramps/platform strips, match thresholds vertically, test actual oriented polygons rather than inflated AABBs, and rerun continuity. Keep all additions SIMULATED.
