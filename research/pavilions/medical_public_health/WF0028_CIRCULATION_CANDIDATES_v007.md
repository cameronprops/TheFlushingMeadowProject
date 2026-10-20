# WF0028 v007: actual v004 model route candidate audit

Date 2026-10-20. The v005 archive was reloaded and the preserved v004 builder executed locally. The audit used 14 original proposed path edges, radius 0.45m, pedestrian height 1.8m, obstacle XY AABBs after vertical filtering, and a 0.5m diagonal 8-neighbor A* grid (no corner cutting).

Results: **8/14 CANDIDATE_AABB_CLEAR; 6/14 ENDPOINT_BLOCKED; 0 NO_ROUTE_IN_SEARCH_WINDOW**. The results do not necessarily correspond to the original 5 unblocked edges, because the A* algorithm re-routes around obstacles.

Blocked endpoints in particular: MAN_SOUTH_DOOR -> MAN_ENTRY; MAN_ENTRY -> MAN_WEST_DISPLAY; MAN_COURTYARD_FACE -> COURTYARD_WEST; COURTYARD_WEST -> COURTYARD_CROSS; SCIENCE_WEST_DISPLAY -> SCIENCE_ENTRY; SCIENCE_ENTRY -> SCIENCE_SOUTH_DOOR. Several endpoints lie inside conservative expanded obstacle bounds, so alternate routing alone cannot resolve them. The candidate routes need a swept 3D test, support surface/height validation, and separate native Unreal navigation.

Artifacts: local archived package WF0028_Circulation_Candidates_v007.zip, SHA256 2a7ebb7df6af36ffda5ef9d686e319bf3b39d4478baefe6e734d42111843e26c; contains original v004 build chain, v005 audit, v007 route generator and JSON results. Four result invariants were checked locally. This run **does not** alter the historical sources or any mesh and **does not** claim v007 geometry.

Next repair: inspect blocked node coordinates, shift only explicitly speculative waypoints as a separate proposal, then repeat with robust XY geometry rather than broad AABBs; never modify original historic plan evidence just for a pass.
