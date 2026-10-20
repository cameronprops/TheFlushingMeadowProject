# WF0028 v005: conservative pedestrian route audit

2026-10-20. Audits *v004's unchanged, speculative geometry* and *v003's 14 proposed visitor route links*. No as-built claim and no new door placements.

- 15 route stations, 14 edges.
- Agent envelope: radius 0.45m, height 1.8m.
- Conservative line-segment intersection against obstacle XY bounding boxes inflated by agent radius, limited to parts intersecting walker's vertical span. Ground surfaces, roof and purely visual route markers excluded.
- **9 edges BLOCKED** due to modeled partitions, exhibits and side/perimeter walls. **5 edges NO_STATIC_AABB_HIT** (not certified).
- Both speculative north openings fail to connect to a continuous route across the courtyard and adjacent side walls. Courtyard path crosses Medical east perimeter and Science west perimeter.
- Eight automated regression assertions passed locally.
- Not a full 3D swept-capsule check, physical walking-surface test, historical plan trace or Unreal NavMesh verification.
- This is a *diagnostic only*. Preserve v004, don't delete historic or hypothesized walls to hide failures.

The self-contained v005 package includes original model builders and geometry, route audit script, JSON report and regression test. ZIP SHA-256 `dd645229429c58d64fb92bd8c8f2fd722493d68e31fc7b2494cf75150acc7c32`.

Next recommended modeling change: **separate alternate** that adds courtyard walk connectors and redesigns the explicitly hypothetical route around interior dividers, then rerun this diagnostic and a vertical floor/threshold study. Do not label unverified links as walkable.
