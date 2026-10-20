# Trylon passage visual review v001
**Date:** 2026-10-20
**Asset:** `FMP_ThemeCenter_Assembled_Runtime_v005.glb` (`de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439`)
**Status:** **ARCHITECTURAL PORTALS NOT ACCEPTED.** The provisional circulation path is visible and its screened route has no reported triangle-surface contacts, but historical aperture sizes, jamb/head closure, structural transfer and Unreal traversal remain unverified.

## Direct mesh findings
- The original preserved `Trylon_Hollow_Exterior` and active replacement `Trylon_Hollow_Exterior__RUNTIME_SHARED_APERTURES_v004` have **geometrically identical 49 vertices and 102 triangles**. Their vertex and triangle order differs, but sorted triangles match. Their source and replacement volumes also agree within floating-point precision. Thus **v004 did not make a new cut in the exterior cladding**.
- A pre-existing broad lower-front gap in the original Trylon shell contains both preview portal envelopes. Orthographic elevation of the actual mesh at the return elevation shows a much wider central void than two completed door apertures.
- The active `Trylon_Face_3_Frame__RUNTIME_SHARED_APERTURES_v004` *was* modified relative to the original `Trylon_Face_3_Frame`, and the negative Helicline rail was modified. The frame replacement volumes in `SHARED_PORTALS_v004.json` are 28.214792168190325 m³ source and 28.112507299889653 m³ replacement. This is provisional removal of intersecting braces; it **does not** establish a historically engineered reframe or a finished facade.
- The opening envelopes currently used for return crossings are `TRYLON_RETURN_ENTRY` and `TRYLON_RETURN_EXIT` with centers `[-36.7, 17.0496, 3.048]` and `[-36.7, 17.0496, -3.15]` metres respectively, dimensions **3.4 (model X depth) × 2.4 (Y vertical) × 2.4 (Z width) metres**, model-local Y-up. These are **provisional test envelopes**, *not* proven 1939 dimensions or modeled jambs.
- Rendered view: entrance and exit inside the Trylon's triangular plan outline, with the orange `PROVISIONAL_ReturnViaTrylon_01..04` deck and bridge route. Front elevation of this actual v005 GLB still exposes steel framing projected through the wide cladding void. The fact that members appear inside an elevation opening does not independently show physical interference; some beams may sit behind the preview envelope in depth. Review in 3D with both collision and line-of-sight before changing steel.

## Interpretation and blockers
**The provisional route does not have to traverse solid exterior cladding where it enters/exits, because the cladding is already absent there. However this is not proof that the proper Trylon architectural passage has been modeled.** The two intended crossing points currently sit inside a shared oversized void. Door-specific shell topology, finish, steel reframing, returns, rails, real built dimensions and circulation joins remain unresolved.

Existing v004 return screen reported 435 clear sampled body poses. The later offline v001 return-route continuity audit excludes surface contact along the specified sample interpolations under assumptions, but does not prove the model is architecturally accurate or certify native Unreal collision, body occupancy, egress or full historic visitor circulation.

## Next actual geometry repair, without touching archival/print masters
1. Acquire/interpret 1939 architectural section and portal plan evidence; distinguish documented as-built passage from interpretive fallbacks and retain uncertainty.
2. Model two **explicit** provisional door opening assemblies with jamb/head/sill and genuine shell-side topology rather than relying on the broad original void. If actual source proves one shared opening instead, model that configuration instead of inventing two historic doors.
3. Design steel transfers and revised frame topology in a separately versioned runtime derivative; keep source members and untouched print shells recoverable and preserve object IDs.
4. Render front elevation, interior, entry and exit for side-by-side visual signoff; run static full-scene collision plus native Unreal traversal and sightline QA.
5. Do not mark passage construction `PASS` until geometry, historical uncertainty and body collision are reviewed separately.

**Audit source:** Exact v005 GLB stored in [Drive archive](https://drive.google.com/file/d/1OzFZRkHCxN3jMBGwH3Lwdbx0pFJIJhM0/view). Rendered locally from its actual transformed Trimesh/VTK scene geometry, not generative image synthesis. Source, print variants and v005 binaries were not altered in this audit.
