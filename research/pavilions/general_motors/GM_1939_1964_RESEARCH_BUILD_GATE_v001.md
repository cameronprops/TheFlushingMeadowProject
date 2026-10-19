# FMP GM: two distinct pavilion reconstruction targets

Research prepared 2026-10-18. Neither has a valid FMP site transform, source-reviewed full construction set, or playable interior. Do NOT collapse into one model; 1939, 1940, 1964 and 1965 are independently versioned states.

## GM 1939-1940 (WF0012)
Historical exhibition **General Motors: Highways and Horizons**. The pavilion contained Norman Bel Geddes's **Futurama**, but the *building* and the exhibit are separate data records. Harry Ransom Center identifies **Albert Kahn** as architect of the building in the 29 blueprints of Job 381. Bel Geddes designed the Futurama production and integrated show, with building presentation and flow drawings among its archives.

### Archival acquisition list: first request
Harry Ransom Center, Norman Bel Geddes Papers, Job 381:
- Flat files 381.8a-b: **29 Albert Kahn building blueprints and Bel Geddes details**. These are the highest-value envelope source.
- Flat files 381.2a-b and 381.3: **96 working drawings** for building 100-199. Cross-index with the 29 Kahn drawings; do not assume all 96 concern the exterior.
- Flat file 381.9: **6 floor-plan photocopies** for the GM building. Critical for explorable public entry and accessible interior.
- Flat file 381.1a-e: **95 preliminary drawings** of show sections, ramps, theater and surrounding full-size built street sets. Preliminary drawings are not certified as-built.
- Box 19b folders 381.23-26: **32 flow/platform sketches**; useful for traffic/crowd circulation.
- Box 19c folder 381.28a-e: **13-part GM building specifications**, materials/structure likely but must inspect.
- Photo box 10 folders 381.15-16: 1938-1939 **construction documentation**.
- Photo box 10b-c folders 381.47-55: **GM building model photographs**.
- Box 19e folders 381.49-53a: period visitor guides, promotional maps and 1940 revisions.
Original finding aid: https://research.hrc.utexas.edu/NBGpublic/details.cfm?id=307

### First usable building output
1. Identify actual entrance orientation + 1939 footprint from dated fair plan, cite plan ID.
2. Trace Kahn shell floor outline, roof surface, entrance and main elevation bay rhythm, cite sheets and archive image hash.
3. Extract full-size intersection/show buildings and the separate spectator conveyor from Job 381; rooms may be marked provisional until sections arrive.
4. Add facade materials and night lighting from color film/photos after correcting for period film exposure. Do not interpret B&W brightness as paint colors.
5. Build a walkable public-access interior proxy that avoids breaking the Futurama ride's historical circulation.
6. Realistic and stylized skin variations use the SAME source-backed geometry IDs, entrance volumes and collider meshes.

## GM 1964-1965 (FMP64SUBJ0064)
**Futurama II**, a distinct pavilion, not a retrofit of 1939.
Contemporary GM/NYWF Corporation publicity reproduced in a historical postcard gives:
- building length **680 feet** = 207.264 meters (reported)
- entrance sculptural canopy **110 feet high** = 33.528 meters, **39 spars**
- revolving roof indicator **40 feet wide** = 12.192 meters
- Futurama II exhibit ride path **1,700 feet**, NOT the pavilion footprint
- building **nearly 230,000 square feet**, area type not specified
Period caption: https://www.flickr.com/photos/autohistorian/51976263794/
Official model-photo catalog: https://www.gettyimages.com.au/detail/news-photo/an-architectural-model-of-the-general-motors-pavilion-news-photo/98446361
Period pavilion tour: https://www.worldsfairphotos.com/nywf64/general-motors.htm

The 40-foot *revolving indicator* may be an identification lead for the owner's memory of a rotating, pyramid-like floating object, but that is NOT enough evidence that the object was actually a pyramid or that it was the intended structure. The owner can confirm from photos. Do not model an assumed pyramid in the canonical fair world.

### Building use
- 1964 main canopy fins and display dome should be drafted as separate parametric components; avoid fabricating curvature and the exact 39 spar profiles until better photos/drawings.
- The rooftop indicator can have a separate mechanical/animation identity, location and documented **revolving** behavior; the rotation speed, mechanical support and 3D form are unverified.
- Model the ride separately from its housing; preserve access route/queue and optional interactive interior for a future alpha.
- Historical photos and renderings are research references and NOT necessarily licensed textures to distribute.

## Source-backed modeled dimensions and materials
Current normalized values: catalog/building_geometry_parameters.csv, source evidence in catalog/building_evidence.csv.
Cinematic material observation seeds (not historical material measurements): catalog/building_surfaces.csv.
Multi-view matching work queue: catalog/building_visual_observations.csv.
Canonical dual-skin and voxel export plan: docs/buildings/PROCEDURAL_CINEMATIC_AND_VOXEL_PIPELINE_v001.md.

## Build QA
1. Separate 1939, 1940, 1964, 1965 geometries and provenance; no swapping pavilions.
2. Target scene-local metres consistent with period site registration; do not invent building XY coordinates.
3. Mesh geometry must be watertight where physical shell demands it; accessible interior geometry may use discrete wall/floor/door surfaces and intentional openings.
4. Preserve stable model object IDs for Rhino/Worldwright -> Unreal; materials and stylization override surface slots.
5. No public-explorer release until measured avatar clearances, collision, navigation, level loading and actual hardware performance are exercised in Unreal.
