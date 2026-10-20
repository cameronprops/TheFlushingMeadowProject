# WF0028 v008 interpretive waypoint repair (2026-10-20)

Based on the preserved v004 76-part interpretive GLB, v005 AABB collision audit and v007 candidate route generator. All 14 source waypoint route edges retained. Source and architectural meshes **unchanged**.

A deterministic local repair pass moves only three proposed route endpoints:
- `MAN_ENTRY`: (-40,-8) -> (-40,-8.5) m, shift 0.5 m.
- `COURTYARD_WEST`: (-18,6) -> (-18.25,6) m, shift 0.25 m.
- `SCIENCE_ENTRY`: (42,-8) -> (42,-8.5) m, shift 0.5 m.

After candidate planning: **12 of 14 CANDIDATE_AABB_CLEAR**, one `ENDPOINT_BLOCKED` (`MAN_COURTYARD_FACE` to `COURTYARD_WEST`), one `NO_ROUTE_IN_SEARCH_WINDOW` (`COURTYARD_WEST` to `COURTYARD_CROSS`). The v007 baseline was eight AABB-clear candidates and six blocked endpoints.

Six local Python unit tests pass: edge retention, non-destructive status, no false full-collision certification, candidate count, preservation of unresolved failures, and clear relocated waypoints.

**Limits:** The method uses simplified inflated plan-view bounding boxes and a gridded rerouter, not mesh intersection, floor elevation, swept capsule, or Unreal NavMesh. Candidate routes can run outside actual floor surfaces or away from door centers. Zero architectural walls, door cuts, and meshes were changed. No historic correctness claim.

ZIP SHA256: `cfb325c3706c5bda3fccf3f643122d3470fad88b139bf3613b3a57021c2c0101`. Local package includes the entire v004/v005/v007 Python and geometry chain, v008 implementation, JSON output, and passing test suite.

Next step: diagnose the Medical/courtyard western interface with actual support-surface and vertical threshold checks, and propose separate geometry connectors only if the historical plan evidence supports them.
