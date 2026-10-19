# FMP | Evidence-based procedural construction and cinematic materials, v0.1

## Creative and historical contract
The user wants an immersive cinematic world, with believable pavilion locations and both realistic and stylized skins. Reconstruction may fill missing facade/interior detail from educated guesses informed by multiple period photographs and Meshy, but every inferred datum must remain distinguishable from measured drawings. All downstream scenes reuse stable building IDs and a common source of truth. A stylized skin must never overwrite period evidence.

## Database feeds actual model generation
- Candidate IDs and era identity: reconstruction_subjects + building_dossiers (original 239 archived subjects; 195 building/venue/pavilion candidates, NOT 195 certified independent buildings).
- Building dimensions/parts: building_geometry_parameters. One row = component/parameter/year/value in canonical SI units, cited original value, source evidence link, uncertainty and editability.
- Surface observations: building_surface_research. Per-period material family and optional Unreal PBR numeric lookdev values; these are provisional shader values unless measured and explicitly documented.
- Photo evidence: building_view_observations. Record original image URI, era, view direction, camera estimate, visible parts, stable feature anchors, degree of uncertainty and whether a Meshy draft was used. Do not treat generated mesh as a primary source.
- Interiors/doors/collision: building_spaces and geometry_asset/worklog records. Room graphs and doors must be explicit, not inferred from exterior envelopes.
- Two skins: building_appearance REALISTIC and STYLIZED must share identical geometry, coordinates, entrances, wall and floor placement, collision proxies, scene identity and persistent interaction keys.
- Unidentified rotating object: unidentified_visual_leads FMP-VIS-ROTATING-PYRAMID-01, status UNIDENTIFIED. Do not create a wrongly named historical structure.

## Procedural sequence (per building per fair year)
1. Resolve identity and nested occupant/exhibit relations; distinguish GM's 1939 pavilion from its 1964 replacement.
2. Gather period maps, approved/as-built drawings, dated photos, construction photos and material/lighting studies. Associate each assertion with the individual evidence ID and rights status.
3. Solve correct world position (dated map) and shell geometry (polygons/curves, facade rhythm, sectional heights) independent of surface appearance.
4. Use constraints between photographs and plan/elevation lines to estimate missing dimensions and geometry. Suggested solver residual: weighted 2D image reprojection error for matched 3D landmarks with known camera model, plus outline, orthogonality, and dimension constraints. Distinguish camera/lens uncertainty from geometry uncertainty. Use multiple non-collinear and non-coplanar landmarks; keep alternative interpretations when evidence conflicts.
5. Generate parametric BRep/NURBS/mesh via Worldwright/Rhino; produce separated Unreal-ready meshes. Rebuild by deterministic ID and recipe hash, not by display names or array index.
6. Optional Meshy draft: feed crop references and dimension/shape constraints for unusual decorative/organic pieces; inspect topology and projected silhouettes; rebuild hard-surface architecture as clean CAD/quad surfaces as needed. Store Meshy model revisions and provenance; never silently import uncertain output into verified architecture.
7. Author two material presentations as **overrides by stable material slot**. Geometry/cache/collision/LOD mesh metadata are shared. Preserve source-linked authenticity grade per material. Add UVs and texel-density budget by distance/importance.
8. Import into Unreal as architecture plus staged public interiors. Test world scale, character capsule passage, collision, doorway widths, route graph, visibility/streaming and memory budget before declaring a building visitor-accessible.
9. Generate Minecraft from the canonical site and geometry, not by manually rebuilding; configure voxel resolution (e.g. 1 m/block) and mapping of material families to block palette. Voxel stair/slab approximations for curves, thresholds and glazing are separate style decisions. Export as structure/schematic or world chunks only after choosing Minecraft version, mod/edit tool, origin and block palette. THIS EXPORTER IS FEASIBLE BUT NOT YET IMPLEMENTED.
10. Keep year-specific changes keyed by building ID and period year. The present terrain never stands in as 1939 grading; 2039/2064 hypothetical scenes have separate branch IDs.

## Unreal cinematic acceptance
- Reality pass: neutral daylight reference under consistent exposure, physically-based base color/metallic/roughness/normal values, correct glass thickness/refraction and response, facade seam scale, proper UVs, nighttime signage and emissive illumination supported by separate light sources, wet/dry material variants only where authored.
- Cinematic pass: Lumen GI/reflections where scene/platform allows, Nanite on suitable dense static assets, virtual shadow maps or tested alternatives, volumetric haze when supported and directed, correct physical camera lens/FOV/DOF, controlled exposure/color management and consistent LUT choices. Use Sequencer for camera and time-of-day reference sequences.
- Keep photo matching independently of cinematic grading. Night photos contain blown highlights, film halation, underexposure and color shifts; do not bake these into albedo textures or claim they equal period paint colors.
- Realistic skin: evidence-informed materials with clean physically plausible PBR response. Stylized skin: shared geometry, author-selected palette and surface response, never a divergent source for geometry.
- Test hero shots, exterior walking, public interior traversal and accessible edges separately. A GLB existing or being loadable is NOT a playable Unreal build.

## Current FMP 007/008 additions
- WF0012: GM Highways and Horizons (1939/1940), HRC Norman Bel Geddes Job 381: architectural working plans by Albert Kahn; first archival acquisition targets. Futurama is a nested exhibit, not a second pavilion.
- FMP64SUBJ0064: the distinct 1964/1965 GM Futurama II pavilion; period specifications include 680-ft building length, 110-ft entrance canopy with 39 spars, 40-ft rotating sign and a 1,700-ft ride. These figures are translated to metres in building_geometry_parameters; plan polygon, orientation, material composition and motor RPM are NOT fabricated.
- Surface lookdev records for GM 1939/1964 and Westinghouse are provisional. Material roughness numbers are shader-starting targets, NOT archival paint tests.
- For the unidentified rotating pyramid-like structure, the 1964 GM rotating indicator and IBM's suspended ovoid theater are comparison leads, not a confirmed match.

## Source anchors
- HRC Job 381: https://research.hrc.utexas.edu/NBGpublic/details.cfm?id=307
- 1964 GM contemporary postcard transcription: https://www.flickr.com/photos/autohistorian/51976263794/
- 1964 GM photo/archive: https://www.worldsfairphotos.com/nywf64/general-motors.htm
- IBM Ovoid floating theater comparator: https://eamesfoundation.org/work/ibm-pavilion-ny-worlds-fair/
- Eames Think floating theater: https://eamesfoundation.org/work/think/

## Work still required
The JSON dossier generator now exports procedural_parameters, surface_research and photographic_observations, but no end-to-end procedural CAD mesh generator or Minecraft voxel exporter is implemented from those fields yet. No Unreal native material/lighting host benchmark run here. Store source-linked plan and rendering input data now to avoid reauthoring buildings later.
