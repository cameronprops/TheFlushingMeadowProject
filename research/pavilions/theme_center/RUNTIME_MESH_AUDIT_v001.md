# Theme Center v005: actual GLB static-geometry audit v001

**Date:** 2026-10-20. **Scope:** The single 1939 Theme Center v005 **runtime derivative**, retrieved from the existing FMP Google Drive archive. This is a byte-verified inspection of the actual assembled GLB, not a new architectural interpretation or Unreal playtest.

## Exact evidence

- Drive source: [FMP_ThemeCenter_Assembled_Runtime_v005.zip](https://drive.google.com/file/d/1OzFZRkHCxN3jMBGwH3Lwdbx0pFJIJhM0/view)
- Acquired ZIP SHA-256: `d55522c3877638e1e3566ca63a18b0f072c2a6279ca3b5da4620836b547586b2`
- Contained GLB: `FMP_ThemeCenter_Assembled_Runtime_v005.glb`, 47,126,840 bytes
- GLB SHA-256: `de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439` (matches v005 manifest)
- The existing `preflight_theme_center_v005.py` **passed its exact GLB check**: glTF header, binary length, object IDs, unique identities, 573 nodes, 558 active mesh references, and explicitly disabled source meshes.
- `audit_theme_center_mesh_v005.py` inspected this exact GLB with Python, NumPy and Trimesh, no repair or export. Full machine-readable findings: [RUNTIME_MESH_AUDIT_v001.json](RUNTIME_MESH_AUDIT_v001.json).
- Local tests: 7 new synthetic tests and 7 existing preflight tests, **14/14 passing**. These unit tests are not Unreal tests; the separate production-model scan is direct inspection evidence.

## Geometry findings

| Metric | Observed | Meaning |
| --- | ---: | --- |
| glTF scene nodes | 573 | Source plus 62 circulation nodes and one runtime grouping node |
| Active visible meshes | 558 | 558 unique active mesh records |
| Active triangles | 1,000,323 | High-detail preview assembly; not a platform performance measurement |
| Preserved but **unreferenced** meshes | 275 / 102,958 triangles | Deliberately retained historic/source geometry, not rendered by active nodes |
| Explicit material bindings | 403 active meshes | Another 155 active meshes use implicit glTF default material behavior |
| Active meshes lacking explicit NORMAL attributes | 267 | Requires normal-generation/import handling review |
| Active primitives with `COLOR_0` | 125 | Vertex color import/material support must be visually checked |
| Materials / embedded image textures | 15 / 6 | Embedded asset content, not proof of correct native shading |
| Non-finite active vertex coordinates | 0 meshes | None found |
| Zero-area active triangles at 1e-18 m^4 cross-norm-squared threshold | 0 | None found at declared absolute threshold |
| Very-small nonzero triangles | 2 | Both in inferred painted landscape terrain; not yet a failure |
| Visible meshes not watertight | 285 | Includes deliberate display/open scenic surfaces; **not** 285 failed collision objects |
| Visible meshes with inconsistent winding | 5 | Inferred river/orchard/road geometry; inspect orientation/culling in Unreal |

**Priority components:** Both runtime replacement Trylon shells, the runtime rail replacement, the main Helicline deck, the transition solid, return bridge deck and original upper Perisphere shell are watertight and winding-consistent as inspected. The runtime *lower Perisphere shell is nonwatertight intentionally*, owing to open entry/exit apertures. That runtime mesh must never replace the watertight physical print source.

### Immediate engine import risks

1. **Handedness.** Existing model-local convention is right-handed Y-up metres. The documented Unreal preview mapping `[X,Z,Y] * 100 cm` swaps two axes (determinant **-1**), so importer winding, normal direction and backface culling must be verified in native Unreal. Wolfram Language independently confirmed this determinant and mapped the two existing Trylon portal centers; those coordinates are illustrative model-local values, **not** georeferenced site coordinates.
2. **Normals/materials.** Do not assume missing explicit normal attributes and material bindings will render as authored. Set an explicit import/material/vertex-color policy; check both sides of the opened Perisphere shell, Trylon frame and bridge in actual lit scenes.
3. **Collision/navigation.** 435 prior sampled v004 body poses reported no triangle-surface contacts for the provisional Trylon return path, but neither continuous swept capsule motion nor native Unreal collision/character navigation has been run. Explicit collision geometry and live test traversal are still needed.
4. **Runtime bloat.** The v005 archival derivative keeps 275 unused source meshes, by design. **Do not edit or destructively clean this asset.** If a lean shipping derivative is later authorized, prune unused records **only in a separately hashed, reproducible derivative**, preserving source object IDs and a link to the full master. The 1,000,323 active triangles also merit LOD/streaming review once measurements exist.
5. **Unverified architecture.** Original portal levels/sizes, cut brace transfers, rail returns, historical registration and era-specific presence remain unknown and must not be promoted by game-engine tests.

## Reproduction

From project root, using NumPy and Trimesh and the **exact extracted v005 GLB** and accompanying `manifest.json`:

```bash
python3 -m tools.world_build.audit_theme_center_mesh_v005 \
  /path/to/FMP_ThemeCenter_Assembled_Runtime_v005.glb \
  --manifest /path/to/manifest.json \
  --out /path/to/runtime_mesh_audit_v001.json

python3 -m unittest -v \
  tools.world_build.test_audit_theme_center_mesh_v005 \
  tools.world_build.test_preflight_theme_center_v005
```

The audit is strictly read-only; it neither normalizes meshes nor changes original glTF, sources, print parts or materials. It refuses unexpected input SHA-256. The CLI does not require an Unreal project.

## Acceptance and next real gate

- **PASS:** Actual v005 GLB identity, static glTF validity and measured mesh statistics, including key runtime topology as described.
- **OPEN:** Native Unreal import, normal/material review, collision setup and full traversable guest circulation.
- **NOT RUN:** Game Development Studio local CLI, GPU capture, hardware timings and canonical package admission (the `game-dev` binary was unavailable here).

When an Unreal runtime is available, first import the preserved v005 derivative into an isolated staging level. Capture asset count, transform/scale, material and normal visuals, and verify actual player capsule clearance at Trylon entry, bridge, Perisphere lower/upper exits, return through Trylon and Helicline. Preserve the output under a new acceptance receipt, not as an amendment to the preserved source/print GLB.
