# WF0028 v010: separate hypothetical walking support surfaces

2026-10-20. Built from previous v004 building assembly and v008 candidate route JSON, using v009 support screen as baseline. Generated 97 additive interpretive walking-strip meshes; all original 76 v004 building meshes retained with unique IDs. The added strips are *not historically sourced*, and several may overlap walls or float relative to surveyed terrain.

The centerline support AABB check now reports **14/14 sampled routes fully supported** versus **10/14** in v009. This result depends on checking each strip using the existing PUBLIC_WALK_PROVISIONAL classification; an initial run missed this classification and gave false negatives. Added parts are individually watertight; original part preservation and uniqueness assertions passed.

**Not certified**: full walking-width support, threshold lips, continuity of surface elevations, 3D swept-capsule clearance, collisions, architectural correctness, or Unreal NavMesh traversal. Thus route usability remains *partially validated* despite 14/14 on the single diagnostic metric.

Local package `WF0028_1939_Support_Repair_v010.zip` SHA256 `9f47aa881ab35b8a793b2e2372482ea0c65c99eb43aad2616ef7fe8aa871d17a`. Includes v010 GLB and Python builder, route/source manifests and v009 history. Binary package generated in current conversation; no Drive upload claimed unless separately confirmed.

Next: swept-footprint support and continuous body collision checks over true rotated polygons; reconstruct missing threshold ramps as a separate variant only after identifying obstruction coordinates.
