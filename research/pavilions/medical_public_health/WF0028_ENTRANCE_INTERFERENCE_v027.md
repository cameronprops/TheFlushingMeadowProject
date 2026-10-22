# WF0028 v027: Entrance-interface obstruction QA

Date 2026-10-22. This audit checks actual v026 GLB geometry, not hypothesized measured plans.

- 201 source nodes unchanged. Entry aperture x40.2–43.8 m = 3.6 m in provisional south wall, while repositioned 12-node curved frontage has bounding width 12.0476 m.
- **6 of 12** aligned curved witness nodes have positive AABB volume overlap with an existing south facade wall or entry lintel (6 node/wall pairs). Other 6 do not have AABB overlaps. This is conservative collision *screening*, not an exact mesh intersection.
- Curved reference reaches z=5m. Existing entrance lintel begins z=3.6m. The sculpture/facade geometry and lintel still have no historically evidenced interface.
- No modifications to original GLB, no facade boolean or room-partition edits, no as-built accuracy or Unreal collision/navigation claims.
- Source GLB SHA256 `8cbabed7d964f37d63e834ec9353cf8407405e149ff519cc6adc6bfd2e5c9e76`.
- Package `WF0028_Entrance_Interference_Audit_v027.zip` with CAD-coordinate plan PNG/PDF, AABB CSV, JSON, and README; ZIP SHA256 `11073d8722c40f7fc2cf9a8da0784ec76aeecdd3a618808a05ecc6906a2e042e`, 72,206 bytes.
- Git source script: `tools/world_build/wf0028_entrance_aabb_v027.py`.

**Next:** Obtain measured architectural elevations and identify correct curved-wall termination/offset and structural wall boundaries. Do not auto-cut architecture based on false registration.
