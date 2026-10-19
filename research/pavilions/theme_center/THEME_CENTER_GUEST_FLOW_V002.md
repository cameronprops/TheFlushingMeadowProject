# FMP / WF0001 + WF0002 — circulation and shell refinement v0.2

**2026-10-19: provisional modeled geometry; native Unreal and printed assembly not certified.**

## Build inputs
- Original reviewed [510-node Theme Center model](https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view) SHA256 `a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5` is read-only.
- Original source is right-handed Y-up **metres**, model-local; not registered against a surveyed fairground datum.
- Retains existing v001 runtime-only Perisphere exit apertures, upper staircase, Trylon return passage and 23 stair treads (all estimated).

## v002 changes
1. Derive portal positions from the actual first- and second-platform landing meshes, not from conjectural 52/64-ft historic entrance data.
2. Model separate jamb/head/sill preview geometry for **two 2.35m wide x 2.40m high** provisional exit openings, and two stair handrails with 18 posts. These are **editorial preview geometry**, not measured 1939 portal sizes, textures or handrail profiles.
3. Create two **closed solid cutter guides**, exported as a separate GLB and NOT applied to printable Perisphere source shells. The runtime open shell is not watertight or fit to print.
4. Generate four model-local hotspot candidates and `[X,Z,Y]*100` Unreal-centimetre preview mappings. These do **not** replace any master interactive point's presently unknown fairground/architectural registration.
5. Test distance from the provisional Trylon-to-Helicline route endpoint to actual ramp mesh vertices: ~0.06186m. This is a local mesh proximity check only; clearance, collision and traversability have not been measured in Unreal.
6. Preserve the source watertight Trylon/Perisphere shell variants for physical model production; calculate envelopes for 1:250 and 1:800 printing without assuming wall thickness or printer fit.

## Architecture and source references
Contemporary reporting from [April 1939 in *The New Yorker*](https://www.newyorker.com/magazine/1939/04/15/stanley-in-the-perisphere) describes entering the Trylon and encountering two escalators serving rotating platforms. The [historic annotated cutaway and photographs summarized here](https://drivingfordeco.com/vanished-new-york-city-art-deco-the-trylon-and-perisphere-part-two-1939-1941/) show the guest bridge, upper-platform stair exit, return through Trylon and down Helicline. Contemporary text supports topology, not the exact modeled door sizes.

**New primary-source acquisition lead:** Lot 418 in [World's Fair Auction catalog 19](https://www.worldsfairauction.com/catalogs/catalog-19.pdf) describes approximately 40 period drawings/blueprints/engineering documents attributed to Theme Center chief engineer Alfred J. Dillon. This list includes a Perisphere blueprint and *Theme Bldg Section*. **Current possession, authenticity of individual plan sheets, year/revision, reproduction rights and access are not established.** Do not promote sale-catalog titles into acquired historical dimensions.

## How to regenerate and test
```sh
python3 tools/world_build/build_theme_center_guest_flow_v002.py \
    /path/to/FMP_ThemeCenter_Staging_v001.glb /path/to/output
FMP_THEME_CENTER_GLB=/path/to/FMP_ThemeCenter_Staging_v001.glb \
    python3 -m unittest -v tools.world_build.test_theme_center_guest_flow_v002
```

Dependencies: Python, `numpy`, `trimesh`. Companion previous source is `tools/world_build/build_theme_center_guest_flow_v001.py`. The input SHA256 is enforced.

## Runtime display and print plan
- Display v002 overlay `ThemeCenter_1939_GuestFlow_Trim_v002.glb` **in place of** the original `Perisphere_Lower_Removable_Shell` inside the **Unreal visitor view only**. Avoid duplicate shell rendering and disable temporary debug waypoints before guest view.
- **Do not** use open runtime sphere for printing. Use original three watertight source nodes. Copy the printable lower shell before trying the separate cutter solids. A real printable doorway needs wall thickness, rim closure, boolean validity, segmentation, keyed assembly and real slicer tests.
- The material slots of generated portal frames and rails are placeholders for cinematic look development. They are not a manufacturer's or historic finish specification.
- The Trylon and Perisphere remain the master assembly, shared with Democracity and the Helicline, not two disconnected structures.

## QA and next actual modeling gates
**10/10** local direct-original-GLB tests passed, including source SHA invariant, original closed print shells, intentionally open runtime shell, closed cutter solids, named frame/handrail parts, coordinate conversion, print scales and missing-source rejection.

Still outstanding: period plan tracing; exact Trylon east return opening; schematic vs built elevation; actual visitor route clearance, collisions/Unreal navigation, physical print fit/Boolean; final site-position origin and projector registration. No model-specific historical certification implied.

Next logical build: traced/registered architectural openings once original plans can be obtained, otherwise parallel development of the RCA pavilion based on cataloged architectural elevations/sections without inventing unmeasured site geometry.
