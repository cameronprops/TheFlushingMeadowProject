# Theme Center: Source-registered 3D controls and photo-alignment intake v001

**2026-10-20 · WF0001/WF0002/WF0004 · implemented and locally tested.**

This package uses the exact v005 Theme Center scene, GLB SHA-256 `de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439`. It does **not** alter the original 1939 master, the v005 runtime scene, or print models. The generated **six-node reference-only GLB** is a measuring aid, not missing historic architecture.

## Why it matters

The visible smooth concave side/underside profile of the elevated return bridge in period photographs is absent from the current flat `Return_Bridge_Deck`. A two-escalator lobby model exists, but neither public entrance canopy with `PERISPHERE ENTRANCE` sign nor historically matched enclosed escalator chamber has been built. Earlier AI-generated illustrative images are specifically excluded from the evidence graph.

The source-linked controls are wireframe world-space bounding boxes around six **already existing** v005 scene nodes: Trylon exterior, Perisphere lower shell, lobby floor, the two escalators and bridge deck. These are **derived from the currently modeled geometry**, not measured 1939 positions. Model frame is unregistered right-handed Y-up metres. Every wire node is named `REFERENCE_ONLY__...` to prevent mistaken import as historic architecture.

## Curated photographic evidence and rights

| Record | Original/copy | Identifies | Rights/limitations |
| --- | --- | --- | --- |
| MET 1987.1100.403 | [Met catalog](https://www.metmuseum.org/art/collection/search/265469) / [CC0 original on Commons](https://commons.wikimedia.org/wiki/File:-1939_New_York_World%27s_Fair,_Entrance_to_Perisphere-_MET_DP103124.jpg) | Samuel H. Gottscho's circa-1939 photograph of public Perisphere entrance, 3,138 × 3,847 scan | Original Commons copy documented CC0. Download and hash before digitizing. Met catalog itself restricts downloading its displayed reproduction. |
| MET 1987.1100.404 | [Met catalog](https://www.metmuseum.org/art/collection/search/265470) / [Commons copy](https://commons.wikimedia.org/wiki/File:Trylon_and_Perisphere,_New_York_World%27s_Fair_MET_DP103125.jpg) | Another named Gottscho view of the Trylon/Perisphere | Establish photographic phase and useful visible features before calibration |
| NYPL U-6 | [NYPL construction image record](https://old-digitalcollections.nypl.org/items/917ab9c3-76b6-1637-e040-e00a180679d6) | Photographic Theme Center architectural/construction series | NYPL rights unresolved; original dates and individual items require identification |
| Secondary reproduction of Gottscho | [Modernist Collection](https://www.modernistcollection.com/deco/twa-ticket-counter-saarinen-s9rn8-ey24z-sbwdb-j7w7r-w787a-7w2lf) | Visible bridge arch, rail and compact entrance signage in one photo | Commercial reproduction, **not an acquired calibration scan**; do not redistribute this reproduction |
| Lobby photo locator | [Driving for Deco source discussion](https://drivingfordeco.com/vanished-new-york-city-art-deco-the-trylon-and-perisphere-part-two-1939-1941/) | Period image of Trylon interior aluminum-lined lobby, turnstiles, two escalators; cites NYPL | Must identify corresponding original NYPL image before measuring details |

**Important false match:** Other 1939 Fair postcards and records name an unrelated **“Bridge of Tomorrow”** with independent designers and catalog entries. That name must **not** be applied to the Trylon–Perisphere upper connecting return bridge or used to calibrate its architectural profile. Compare [MCNY postcard collection](https://collections.mcny.org/CS.aspx?DocRID=24U39YCPMOJ&PN=1315&VBID=&VP3=DamView) with [fair building index](https://www.brightontoymuseum.co.uk/index/New_York_World%27s_Fair_%281939%29).

## Actual new deliverables

- `FMP_ThemeCenter_Bridge_Registration_Controls_v001.glb`: six differently colored, separately named bounding guides only, no invented arch or canopy mesh. Generated from source with strict SHA refusal; resulting GLB reloaded and each guide bounding extent rechecked.
- `FMP_Bridge_Registration_Controls_v001.json`: source/object identity, color, world X/Y/Z bounds, source GLB digest, output digest and untested claims.
- `FMP_Bridge_Registration_Control_Board_v001.png`: measured X/Y reference drawing (projected AABBs, **not** a historical section).
- `build_bridge_registration_controls_v001.py`, `render_bridge_controls_v001.py`: reproducible construction and survey-board generators.
- `solve_theme_center_photo_pose_v001.py`: optional OpenCV pose solver. It refuses to run with unknown intrinsics, no archived photo hash, fewer than six distinct non-coplanar 3D/image correspondences, mismatched model identity, bad image bounds or large residuals. It returns **provisional camera pose**, not historical dimensions, and writes **no geometry**.
- `PHOTO_REGISTRATION_TEMPLATE_v001.json`: **deliberately empty** correspondence list. The 3,138 × 3,847 px MET source is described but has not been acquired into the solver working directory or posed. No registration has been faked.

## Reproduce from project root

Python dependencies: `trimesh`, `numpy`, `matplotlib`, `scipy`, `opencv-python`.

```sh
python3 tools/world_build/build_bridge_registration_controls_v001.py /path/to/FMP_ThemeCenter_Assembled_Runtime_v005.glb /path/to/control_out
python3 tools/world_build/render_bridge_controls_v001.py /path/to/control_out/FMP_Bridge_Registration_Controls_v001.json /path/to/control_out/FMP_Bridge_Registration_Control_Board_v001.png
python3 -m unittest -v tools.world_build.test_bridge_registration_controls_v001 tools.world_build.test_solve_theme_center_photo_pose_v001
# ONLY after authentic photo, camera intrinsics, measured 2D/3D correspondences:
python3 tools/world_build/solve_theme_center_photo_pose_v001.py /path/to/populated-registration-input.json /path/to/pose_report.json
```

## Results and next gate

**Implemented and verified:** source hash, six control nodes, world-coordinate bounds, exported GLB reimport and rechecked; **13/13** focused synthetic/geometry tests passed. No Game Development Studio CLI, Unreal runtime or historical photographic camera fit was executed.

**Open:** Acquire original Met CC0 3,138 × 3,847 scan and original NYPL lobby/bridge photographs; ensure at least six **physically identifiable** 3D construction controls (not bbox corners masquerading as surface features), obtain camera calibration and solve actual image pose with residual/uncertainty. Then trace the source photo's bridge soffit and entrance using true projection geometry and only then generate a reversible historical/derived candidate BREP/mesh. If controls cannot be established, keep silhouette provisional rather than invent precise dimensions.
