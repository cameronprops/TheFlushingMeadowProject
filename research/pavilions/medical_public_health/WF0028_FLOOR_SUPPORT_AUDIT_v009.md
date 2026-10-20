# WF0028 v009 floor-support audit

2026-10-20. Recovered v008 GLB, v004 generator, and v008 route JSON. Audited all 14 route candidates against source-derived **interpretive model support AABBs**, not measured historical floorplans.

Sampling every <=0.20m on centerlines using the highest top-Z of authored FLOOR, PUBLIC_WALK_PROVISIONAL, PROVISIONAL_ENTRY_APPROACH, LANDSCAPE, and PUBLIC_ENTRY bounds produced:
- **10 / 14** fully centerline supported;
- **4 / 14** routes with unsupported samples;
- COURTYARD_EAST -> SCIENCE_COURTYARD_FACE just **0.012 supported fraction**;
- COURTYARD_WEST -> COURTYARD_CROSS **0.6482 supported fraction**, with modeled 0.16m support transition;
- both street approach -> door links **0.8919 supported fraction**.

Six local regression tests passed. The unchanged v008 overlay/model remains in package. New audit code, tests, per-route JSON, preserved model and sources are packaged as `WF0028_1939_Floor_Support_Audit_v009.zip`, SHA256 `78625fd8e3d7b8616cf2aad753b9691e18892e46141ad6bb75be963acbfb3cbe`.

Do not report Unreal traversal or collision certification. This is **centerline** support testing: does not certify full foot radius, continuous capsule intersection or intentional ramps; higher overlapping floor volumes can trigger false steps. No building walls or source master changed. Next: create *separate* provisional connection surfaces across four gaps, then rerun support and true swept-envelope audits, and native Unreal test.
