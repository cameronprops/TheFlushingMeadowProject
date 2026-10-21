# Theme Center v005: Return-route surface-continuity screen v001

**2026-10-20 · WF0001 Trylon / WF0004 Helicline · offline mathematical and mesh test only.**

## What's new

The archived v004 return-route screen tested **435 discrete poses** along four provisional return slabs at lateral offsets -0.6, 0, and +0.6 m. It reported no sampled triangle-surface contact and a minimum **0.2407057569062962 m** separation to its six *screened obstacle meshes*. A discrete result is not, by itself, evidence that the body remains separated from geometry between poses.

This v001 procedure uses the unchanged v004 report and the **exact, hash-matched v005 assembled GLB** to test the *interpolated path* without altering any geometry. It models a rigid vertical test capsule with 0.3 m radius, 1.8 m height and a 0.05 m floor lift, represented by 13 vertically spaced, conservatively inflated spheres of radius 0.30413812651491096 m. These are model-screen assumptions, not an Unreal character configuration or accessibility approval.

### Numerical results

| Gate | Evidence | Result |
| --- | --- | --- |
| Original test grid | 435 poses, 4 slabs × 3 tracks | Preserved; original status `NO_SAMPLED_SURFACE_CONTACTS` |
| Straight-track interpolation | 423 links with maximum 0.2479150449 m translation | Conservative **0.1167482345 m** minimum bound to *archived screened obstacles*; pass |
| Three track turns | Nine lateral-track links; longest jump 0.8486502293 m | Sixteen subdivisions per link, 17 pose locations per link; all 9 **surface-contact-excluded** |
| Corner active-scene crop | Scene's 558 visible mesh nodes; AABB-triangle screening includes world transforms | 224 candidate triangle checks aggregated across links; 7 links have candidate triangles, 2 links have none within the expanded swept corridor |
| Smallest computed bound to any **included corner candidate triangle** | 1.0151911639 m | Pass for candidates; excluded triangles are outside the conservative expanded swept corridor, but no numerical margin is claimed to them |
| Original model and print parts | v005 source-preserving GLB / independent print masters | No geometry edited or re-exported |
| Local tests | Prior preflight 7, mesh audit 7, new continuity tests 10 | **24/24 passing**; synthetic tests distinct from actual GLB evaluation |

### Why a bound, not just more poses?

Distance to a fixed triangle surface is **1-Lipschitz**. If both sampled capsule-cover-sphere centers are at least `c` metres from a screened surface, and the two consecutive centers translate by `d`, any interpolated center retains separation of at least `c - d/2`. For the archived straight tracks, the worst-case inequality is:

`0.2407057569062962 - 0.2479150448948797 / 2 = +0.11674823445885635 m`.

The v004 global expanded-bounds screen excludes triangles outside the entire capsule-center path corridor; the reported positive bound applies to the screened candidates, not to every distant surface. The original report remains pinned by SHA-256 to avoid accidentally accepting altered clearance numbers.

At corners, the old fixed-offset tracks have lateral jumps of approximately **0.636 to 0.849 m**, so direct interpolation from archived endpoints alone is inconclusive. The new script screens subdivided straight joining paths against **every active scene node's transformed bounding volume** and the triangle subsets that could be reached by the capsule-cover spheres. Sixteen subdivisions make the worst half-step approximately **0.02652 m**. Wolfram independently checked this value, the body-cover radius and the straight 0.116748 m bound. Eight subdivisions were also evaluated and returned `SURFACE_CONTACT_NOT_EXCLUDED` due to the near-floor return slabs, demonstrating that the test can be inconclusive without fabricating a pass.

**Result:** For exactly the specified centerlines and chosen straight corner links, no triangle-*surface contact* can occur under the conservative axis-cover and piecewise-linear translation assumptions. This **is not a valid Unreal walkability or clearance certification**: it does not detect an object wholly inside an enclosing solid, it assumes all 558 active meshes can be treated as triangle surfaces, it does not evaluate different user steering, player pivoting or traversal off those paths, and it does not test the actual Unreal character, movement mode, physics, navmesh, collision settings, or structural safety. Other routes (including the Perisphere exits, staircases, and final transition) require separate proof.

### Exact source identities

- [Runtime master package (Google Drive)](https://drive.google.com/file/d/1OzFZRkHCxN3jMBGwH3Lwdbx0pFJIJhM0/view): `FMP_ThemeCenter_Assembled_Runtime_v005.glb` SHA-256 `de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439`.
- [Archived v004 shared-portals package](https://drive.google.com/file/d/1Z01QmV6EfgElqiBhVUIg7nIvd_pucZdi/view): contains `Return_Route_Clearance_v004.json`, SHA-256 `0c81c8a35a6448027c73254c7e7ed8d083ccc04ea6b188e89b591965509cea9c`; same file in the [repository](RETURN_ROUTE_CLEARANCE_v004.json).
- [Machine-readable continuity report](RETURN_ROUTE_CONTINUITY_v001.json) generated from actual archived model and report.
- [Reproducible script](../../../tools/world_build/audit_theme_center_route_continuity_v001.py) and [regression tests](../../../tools/world_build/test_audit_theme_center_route_continuity_v001.py).

### Re-run

Run from repository root with Python, NumPy and Trimesh installed:

```bash
python3 -m tools.world_build.audit_theme_center_route_continuity_v001 \
  --glb /path/to/FMP_ThemeCenter_Assembled_Runtime_v005.glb \
  --manifest research/pavilions/theme_center/ASSEMBLED_RUNTIME_v005.json \
  --route research/pavilions/theme_center/RETURN_ROUTE_CLEARANCE_v004.json \
  --out /path/to/RETURN_ROUTE_CONTINUITY_v001.json

python3 -m unittest -v \
  tools.world_build.test_audit_theme_center_route_continuity_v001 \
  tools.world_build.test_preflight_theme_center_v005 \
  tools.world_build.test_audit_theme_center_mesh_v005
```

The new script **refuses** a modified source GLB, route audit or mismatched manifest; it is read-only with respect to inputs. It produces JSON only at the explicit `--out` destination and exits with status 2 if the defined contact-exclusion criterion does not pass.

## Next executable gate

Check the **junction into the one-metre Helicline transition and its entire route**, then the Perisphere-to-Trylon return sections and stair/bridge paths, using the same independently reviewable conservative method. Do not claim a completed visitor journey until a properly configured Unreal project actually loads the asset and runs continuous native capsule sweeps, stairs and navigation tests. The Game Development Studio local CLI and Unreal runtime are not present in this execution environment. Historical apertures and printed parts remain separate and unchanged.
