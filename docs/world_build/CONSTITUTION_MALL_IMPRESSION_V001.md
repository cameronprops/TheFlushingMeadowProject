# FMP | Constitution Mall Impression v0.1

Status: **BUILT**, interpretive scene geometry; not survey-aligned. Built 2026-10-18.
This is a historical impression, not an as-built plan. User authorized best-guess artistic reconstruction.

## Deliverables

- [Combined world ZIP on FMP Google Drive](https://drive.google.com/file/d/1u75ZMxVmh3vnKVAe3drx3T42ggxF0byC/view?usp=drivesdk)
- Generator: [tools/world_build/build_constitution_mall_v001.py](../../tools/world_build/build_constitution_mall_v001.py)
- ZIP contents: existing Theme Center + Constitution Mall combined GLB, complete object manifest, generator source, plan preview, README.
- Input: FMP_ThemeCenter_Staging_v001.glb, Google Drive source ID 197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl (staged model, not a period-sourced survey).

## Real 3D geometry added

416 scene nodes appended to 510 preserved source nodes (total 926).

- 381-meter extension of interpreted mall ground beyond existing Theme Center grounds, with overlap connection.
- Three rectangular reflecting basins with rims, separate traversable cross-promenade connectors and open edge walks.
- Oval lagoon with concentric ornamental water-jet rings.
- 66 physical fountain nozzles plus 66 static modeled water-arc effects (no simulation).
- 48 trees composed of trunks and stylized canopies, arranged symmetrically.
- 38 period-inspired pathway lamps, comprising posts and luminaires.
- Six unidentified contextual pavilion masses with facades, entry arcades and low architectural crown volumes. Their identities and dimensions are NOT asserted as historical.
- Connecting pedestrian plazas, grass panels, broad avenues and a blank sculpture plinth awaiting sourced identity.

## Geometry/coordinate approach

- Original staging scene axes: glTF Y-up metres.
- Added long-axis scenery extends toward local +X from the existing Perisphere at local X=0 and Trylon approximately X=-46. This is a local *impression* direction, **not** a survey claim that the real Constitution Mall ran geodetic east.
- Existing source JSON nodes/meshes/materials/accessors/bufferViews preserved unmodified, and existing binary bytes retained exactly. Only appendages and required outer buffer-length updates occur.
- Persistent UUIDv5 for every new object, with per-object classification: INTERPRETIVE, unregistered local coordinates, preview collision untested.
- Old Theme Center included in the same world GLB, not replaced with a generic schematic.

## Validation

- Original source SHA256: `a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5`
- Combined GLB SHA256: `277e3b93f4829569e6ea8bd12f2af05e922b4c2fa8242f09d168e57ab93ae923`
- Combined ZIP SHA256: `7e9a8269215f2b3e6a43b8eb76038b1efaf199dab7a3b60ec7c28642e752a158`
- Rebuilt twice; byte-identical outputs.
- Combined GLB reloaded in trimesh 4.11.1: 926 nodes, 917 mesh nodes, no structural load failure.
- Source bin prefix preserved exactly and source metadata arrays unchanged; all 416 new IDs unique.
- Approximate combined bounds (metres, local X,Y,Z): `[-172.5,-0.35,-251.5] to [566.0,185.93,173.5]`.
- No runtime claims for collision, walking, lighting, shaders, water behavior, engine import or Worldwright.

## Evidence and authorship

This is a scenic interpretation based on documented 1939 fair visual vocabulary: grand Constitution Mall axial layouts, formal reflecting water, sculptural landscapes, and neighboring exhibition structures.

References:
- https://www.tclf.org/landscapes/new-york-worlds-fair
- https://www.worldsfairphotos.com/nywf39/book-sample-pages.pdf
- https://s-media.nyc.gov/agencies/lpc/lp/1925.pdf

Source references support the general architectural vocabulary, not exact new geometry placement. Do not promote new anonymous pavilion names to archival records. No speculative 2039/2064 structure assets are included.

## Next world-first work

- Add approach/junction continuity on the inherited grounds and test player path widths.
- Build pavilion context from dated photo/plan evidence, swapping anonymous masses for real geometry when researched.
- Preview in Unreal and Worldwright, confirming Y-up conversion, local scale and visibility, then add collision proxies.
- Continue reconstruction sections building-by-building without blocking on full survey registration.

## 2026-10-19: v002 input integrity gate

The existing position-controlled `build_constitution_mall_v002.py` now requires the preserved 510-node source GLB SHA-256 `a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5` **before parsing or appending geometry**. Node-count verification by itself was insufficient: unrelated or altered GLBs could have the same number of nodes. The original source remains read-only. The v002 build continues to exclude the six anonymous pavilion masses from the original interpretive release.

Added `tools/world_build/test_constitution_mall_v002_source.py` covering wrong-source refusal, source nonmutation on rejection and missing-source rejection. The tests were committed but **not executed in an installed Python environment in this change**; only the repository edits were verified through the GitHub connector. Run:

```bash
python -m unittest -v tools.world_build.test_constitution_mall_v002_source
```

Next artifact gate: regenerate v002 from the verified source GLB, archive the model and manifest, then inspect ground and walkable junction continuity before reporting any route as traversable. Do not mark collision, Unreal import, physical accessibility, site registration, or period footprint accuracy certified.

## 2026-10-19: v002 pedestrian connection diagnostic

Added `tools/world_build/audit_constitution_mall_paths.py`. This enumerates actual generated `PEDESTRIAN_PATH`, `PEDESTRIAN_CROSSING` and `PLAZA` boxes, computes adjacency by non-corner plan contact, screens height differences (provisional 0.15 m threshold), and reports graph components, isolated surfaces and height mismatches. No geometry or historic source was altered.

```bash
python -m tools.world_build.audit_constitution_mall_paths --output out/mall_paths.json
python -m unittest -v tools.world_build.test_constitution_mall_paths
python -m unittest -v tools.world_build.test_constitution_mall_v002_source
```

Five focused new regressions and three prior source integrity regressions exist as code, but **have not been executed in this connector session**. The diagnostic is deliberately conservative and limited: it does not evaluate water, parapets, obstacles, sloped surfaces, complete Theme Center connections, capsule clearance, actual historical site registration or native Unreal navmesh/traversal. The graph is a local ground-element planning aid, not a declaration of a walkable fairground.

Next concrete gate: run the diagnostic in the same Python environment used for GLB generation, fix only verified local discontinuities in separate appendage geometry without changing the original 510 nodes, regenerate the source-hash-verified v002 GLB, then perform Unreal collision and navigation acceptance. No new release GLB was generated by this connector-only update.
