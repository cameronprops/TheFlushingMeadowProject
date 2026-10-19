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

## 2026-10-19 corrective revision r1: floor-aligned exit headroom

The earlier generator centered its 2.4 m openings on the landing slab centers.
That left approximately half the intended opening height above the walking surface.
Both shell face-removal envelopes and portal frames/cutters now start at the
source landing mesh's upper Y bound and extend 2.4 m upward. Historical dimensions
remain provisional. The two source-model floor elevations are 15.849600 m and
19.507200 m, in local Y-up metres.

The v002 generator now writes **ThemeCenter_1939_GuestFlow_Trim_v002_r1.glb**,
**ThemeCenter_1939_CAD_PortalCutters_v002_r1.glb**, and the corresponding
**ThemeCenter_1939_GuestFlow_Contract_v002_r1.json**. Use these in place of
the earlier v002 preview outputs. The inherited v001 shell-cutting routine is
corrected too. Original staging/print source bytes are unchanged.

[Download corrected geometry, contract, generators and tests](https://drive.google.com/file/d/15v1yP_XlDS_jAP3PtUfBbidkrhfp5mu6/view).
Package SHA-256: `3cd168262c772a20731d39b73893690541bb9b3f00b8a3b4f78b55ca12c91898`.

Validation: fixed a syntax error in the committed test method name; **11 focused
tests pass** against the hash-verified original GLB. The added regression checks
frame head clearance, sill and cutter alignment to each landing, and absence of
remaining shell triangles overlapping the opening envelope. This is a conservative
triangle-envelope removal, not an exact architectural Boolean or a complete body
clearance test. It does not certify the full stair/bridge route or Unreal collision.

Next gate: validate the corrected overlay in Unreal, including the transitions
between landing, sill, stair and return bridge. If Unreal is unavailable, inspect
those joins against the actual meshes before extending the route.


## 2026-10-19 corrective revision r2: walking surfaces

Measured r1 mesh tops showed the upper connector 3.8 mm above its source landing
and the stair bottom/return slabs 26.68 mm below the bridge walking surface.
Slab endpoints now mean top surfaces, with slab thickness extending downward.
The upper landing and bridge use source mesh upper Y bounds. Stairs retain
uniform positive risers below 180 mm; their final tread meets the bridge level.
Handrail endpoints use those same walking levels. Interaction candidates now
reference landing/bridge surfaces rather than slab centers.

Use the **v002_r2** runtime GLB, cutter GLB and contract:
[geometry, generators and tests](https://drive.google.com/file/d/1osR0o85nkImiI-cllHh-mMp4YWLh-dnY/view).
ZIP SHA-256: `3ff31d1ce14f23961714951aeab1066f866afcddc38d3737f3dbdfa73af65309`.
The preserved source GLB hash is unchanged. r2 supersedes r1 preview outputs.

**12 focused software tests pass**, including surface-level alignment, uniform
stair risers, handrail endpoint heights, and honest reporting of the unresolved
Helicline join. This is not a claim that all geometry acceptance gates pass.

**Open geometry gate:** with the target raised to the bridge walking surface,
Helicline nearest-vertex distance is 0.122434 m, exceeding the retained 0.1 m
proximity threshold. The contract explicitly reports proximity_pass=false.
The former proximity assertion has been replaced by an independent measurement
and failure-status regression, not by a relaxed threshold. Vertex proximity does
not measure actual face contact or capsule clearance.

Next: inspect the Helicline top faces and route endpoint with surface-distance
and body-clearance checks before constructing any transition. Full route continuity,
headroom and Unreal traversal remain unvalidated. All revised circulation remains
provisional, not historically measured architecture.


## 2026-10-19: actual Helicline surface audit

Read-only audit of the preserved source GLB resolves the vertex-distance ambiguity:
nearest vertex 122.434 mm; nearest triangle 99.648 mm. Direct vertical projection
at the route endpoint finds the upward ramp surface **100.139 mm below** the
provisional route walking level. A 5 by 5 grid spans the 2.1 m route width and
0.5 m before/after its endpoint. All 25 samples find an upward face within the
1 m vertical search window; sampled drops range from **35.361 to 168.611 mm**.

This shows a sloping surface under the sampled region, not a certified continuous
join. No geometry changed. No full-scene obstructions, body sweep or Unreal tests
were performed. The r2 join gate remains open; proximity alone cannot close it.

Reproduce:
```bash
python tools/world_build/audit_helicline_join.py SOURCE.glb REPORT.json
python -m unittest -v tools.world_build.test_helicline_surface
```
Four focused synthetic tests pass: sloped interpolation, outside-triangle
rejection, soffit exclusion, level-window filtering and edge handling.
[Recorded measurements](HELICLINE_SURFACE_AUDIT_v001.json).
[Archived audit package](https://drive.google.com/file/d/1zaCmP3adCn_pqqJaqeYOkVNa89J2cCah/view),
SHA-256 `1f770207a5605b7dbaefef798f1a7d9f63d436267aecbb753f1c29918900d06a`.

Next: derive a separate provisional transition surface from the measured ramp
faces, preserving source geometry. Check its full width for support and adjacent
obstructions before any native-engine traversal acceptance. The measurements
describe model geometry, not historically surveyed construction.


## 2026-10-19: v003 provisional Helicline transition built

A new runtime-only 2.1 m wide, 1.0 m long transition replaces the last 0.5 m of
the flat return path and extends 0.5 m over the measured Helicline deck.
The shortened flat segment retains its node name; the new separate closed solid
is `PROVISIONAL_Helicline_Surface_Transition_r3`. The complete v003 overlay
replaces the r2 overlay, avoiding a flat slab protruding through the new slope.

Built from 903 surface samples. Maximum triangulated surface slope ratio:
0.0693124 (6.93%). This is a measured model property, not an accessibility or
historical compliance claim. The transition undersurface intentionally overlaps
the existing ramp; original source/print geometry remains unchanged.

**Five focused tests pass** against the exported GLB: closed consistent mesh,
85 seam samples at each end, 840 independent interior support samples,
single replacement node/explicit open acceptance status, and wrong-source refusal.
Entry seam distance is below 0.01 mm; exit seam distance below 1 mm under the
tested sample criteria. Sampled interior top penetration is bounded at 1 mm.
Discrete checks do not establish continuous body clearance.

The local cached source failed its hash guard during this run. It was not used.
A fresh Drive original matched the recorded
`a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5`
and was used for generation and testing. No alternate hash was accepted.

[Download v003 overlay, manifest, generators and tests](https://drive.google.com/file/d/1w4CgzhuZEigyOGTAANuIFLk44q2AEHkM/view).
Package SHA-256: `684c3b2c025cbeda0a26b1cd4551dc2f3dfde52b87b5ad5dbb8e59d48adf12bd`.
[Geometry manifest](HELICLINE_TRANSITION_v003.json).

```bash
python tools/world_build/build_helicline_transition.py SOURCE.glb OUT
FMP_THEME_CENTER_GLB=/absolute/path/SOURCE.glb python -m unittest -v tools.world_build.test_helicline_transition
```

Use `ThemeCenter_1939_GuestFlow_Trim_v003.glb` instead of the previous runtime
overlay. Continue hiding the original lower Perisphere display shell and legacy
shortcut as documented. This package is not a printable or historically certified
assembly. Native Unreal import, collision, navigation and complete-route body
clearance remain open. Next: check nearby source rails, shells and other geometry
against a defined player body envelope, then validate in Unreal.


## 2026-10-19: v003 transition body-clearance screen

Hash-verified original and v003 overlay were screened at 63 discrete positions
(21 along the transition, three lateral tracks). Provisional capsule dimensions:
radius 0.3 m, height 1.8 m, feet lifted 0.05 m above the sampled floor.
These are test assumptions, not configured Unreal character dimensions.

Thirteen spheres along each vertical capsule axis use a conservative covering
radius of 0.304138 m. All displayed source/overlay mesh nodes enter transformed
bounding-box filtering; only the documented original lower shell and legacy
shortcut are excluded. Three nearby nodes required triangle checks: Helicline
deck, new transition, and shortened return slab. No sampled surface contact was
detected. Minimum reported surface clearance is 45.225 mm, including the deliberate
floor lift; it is not a lateral clearance margin.

Four focused tests pass for wall contact/separation, translated obstacles,
tangency/batch handling and the explicitly demonstrated solid-containment limit.
This screen cannot detect a body entirely enclosed in a closed solid, does not
sweep between poses, and covers only the one-metre transition. It does not certify
the full route or Unreal collision/navigation. No model geometry changed.

[Detailed poses and results](TRANSITION_CLEARANCE_v001.json).
[Archived code, tests and results](https://drive.google.com/file/d/1q2hqMjcPeWWSKf5f9HjXkzHpkYk6JzZ6/view).
ZIP SHA-256: `f7b546c38296f56a53fae10c3c9fadd76f581e5f1d572b8078796d639a7f1891`.

```bash
python tools/world_build/audit_transition_clearance.py SOURCE.glb V003_OVERLAY.glb REPORT.json
python -m unittest -v tools.world_build.test_transition_clearance
```

Next acceptance gate: native Unreal collision and continuous capsule traversal with
the actual player configuration. If no engine runtime is available, apply the
existing offline screening approach to the wider Trylon return route rather than
repeat this completed local transition screen.
