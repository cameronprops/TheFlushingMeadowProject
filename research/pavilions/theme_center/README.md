# The 1939 Theme Center as an existing construction asset

**Status 2026-10-19:** This is the FMP master example for **every building's** evidence-based reconstruction workflow. The Trylon and Perisphere are NOT restarted. They already exist together with Democracity and the Helicline as a preserved, multi-part scene and earlier Rhino builders.


## Latest usable assembly: v005 (2026-10-20)

[Download the assembled runtime package](https://drive.google.com/file/d/1OzFZRkHCxN3jMBGwH3Lwdbx0pFJIJhM0/view). Open its single GLB to inspect the full Theme Center with v004 circulation already applied. [Assembly manifest](ASSEMBLED_RUNTIME_v005.json).

The derivative retains all 510 source nodes, original object IDs, materials, textures, hierarchy and source binary data. Five superseded source mesh bindings are disabled; 62 overlay nodes and one grouping node are appended. The scene has 573 reachable nodes and 558 visible mesh-bearing nodes. Original staging remains unchanged.

Validation: loaded through Trimesh and compared all 558 retained/added mesh nodes against their respective input. Vertex arrays, triangle arrays and world transforms match; the five superseded meshes do not render. glTF scene reachability, mesh/accessor references and buffer ranges checked. Source binary, source arrays, transforms and metadata preservation are asserted by the assembler. Bounds are X [-172.5,172.5], Y [-0.35052,185.927994], Z [-251.5,173.5] metres.

Reproduce with `python tools/world_build/assemble_theme_center_v005.py SOURCE_STAGING.glb V004_OVERLAY.glb OUTPUT_DIR`. Exact input hashes are enforced.

**Limits:** provisional aperture dimensions, frame cut ends, rail returns and historical bridge levels remain unresolved. No Unreal import, collision, navigation or playability claim. This is not a print master.

**Next executable step:** import this single assembled GLB into Unreal; inspect scale, materials and object hierarchy, then configure collision and test visitor traversal. Resolve structural reframing and rail return details against supporting evidence before treating these openings as finished architecture.

## Recover the ORIGINAL geometry before drawing anything new

- [510-node Theme Center staging GLB](https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view) — SHA-256 `a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5`, **Y-up, metres**. Preserve all 510 existing scene nodes.
- [Original v0.9.2 model](https://drive.google.com/file/d/1S-fMjZlzHSAo_H-8bp4YT9Iqw8nS2vlI/view) and [original notes](https://drive.google.com/file/d/1HzqV9lQQjOGY8YyJujWMC0DopYnGQJzl/view).
- [Full BIM-ready master dimensions workbook](https://docs.google.com/spreadsheets/d/1YnjHL9NIw7_jGvLc7Cs4-AUXcLnWKEgN/edit) — F001–F067 values and source/approval fields, preserve revisions and provenance.
- [2026-09-17 truth audit](https://drive.google.com/file/d/1IWHAdUS_prVnM71ErlFOcSrdSAaYAIuc/view) — distinguishes verified dimensions from provisional as-built details.
- [2026-09-17 numerical audit](https://drive.google.com/file/d/1LC5vECuII2wUCV9L5xcXDqHon96bwBr3/view) — 950ft centerline solver, structure, soffit and entrance issues.
- [StructureGraph reuse policy](https://drive.google.com/file/d/1TXVFFLhLUKxlmGrmuf_-jyzxnn-roBLe/view) — reusable recipe stages, geometry QA and Rhino integration; no blind rewrite in Worldwright.
- [Prepared 510-node scene and persistent-ID notes](https://github.com/cameronprops/TheFlushingMeadowProject/blob/main/docs/THEME_CENTER_STAGING.md).

## Built dimensions, not early publicity

| ID | Component | Built model constraint | Source type |
|---|---|---|---|
| F001 | Trylon height | 610 ft = 185.928 m | Institution of Structural Engineers, 1938 |
| F009 | Frame-to-plate transition | 480 ft = 146.304 m | Period technical paper |
| F010 | Upper plate tower | 130 ft = 39.624 m | Period technical paper |
| F012 | Tip width | 2 ft 7 in = 0.7874 m | Period technical paper |
| F021 | Perisphere diameter | 180 ft = 54.864 m | Smithsonian museum |
| F022 | Perisphere clearance over pool | 17 ft = 5.1816 m | FMP audited truth workbook; datum requires confirmation |
| F023 | Eight Perisphere columns | 8 | 1939 Architectural Record construction article |
| F025 | Foundation piles | 528 | Period article; positions unknown |
| F027 | Ring girder | 72 ft = 21.9456 m diameter | Period article; girder centerline not outer bbox |
| F028 / 029 | Sphere trusses | 32 meridians; 15 horizontal | Period article |
| F034 | Spectator platforms | Two moving in opposite directions | Period article |
| F045 | Public escalators | Two | FMP audited workbook and period sources |
| F058 / 059 | Helicline centerline and width | 950 ft long, 18 ft wide | Smithsonian, Carnegie study |

**Rejected built-state inputs:** NYPL's collection summary contains 700-ft Trylon and 200-ft Perisphere **early conception figures**; actual final built geometry is 610/180. The 52/64-ft entrance elevations in the surviving proposal-era material are **not locked** for the as-built scene.

## Reproducible audit

```bash
python3 tools/building_program/audit_archival_glb.py \
  --model /path/to/FMP_ThemeCenter_Staging_v001.glb \
  --constraints research/pavilions/theme_center/THEME_CENTER_ASBUILT_CONSTRAINTS_v001.json \
  --out /path/to/theme_center_audit
```

Produces node-level register, model-space plan and elevation projections, period-constrained measurement/QA checks, and JSON. **8 directly measurable constraints pass, 8 need more than bounding geometry** on the reviewed 510-node source. Eight local tests passed using the original file, including expected hash refusal. The pre-existing source GLB is not rewritten.

## Associated identities and their ownership

- **WF0001 Trylon** — independent vertical architectural shell and approach/lobby/escalator staging.
- **WF0002 Perisphere** — sphere shell and cage, support ring, moving visitor decks, arrival and exit.
- **WF0003 Democracity** — nested sculptural/miniature city under interior Perisphere; separate interpretation layer. Roughly 293 scene nodes currently descend from it. No distinct pavilion.
- **WF0004 Helicline** — circulation, not a new pavilion building.
- **WF0005 Theme Center pool and grounds** — landscape/site interface, not a pavilion.
- The shared bridge joins Trylon and Perisphere; its exact structural boundaries and entrance levels remain unresolved.

The site model is **not georeferenced**. No Unreal character-collision or live visitor navigation tests have passed.

## Strong period structural sources

- [1938 *The Structural Engineer*: Theme Structures](https://www.istructe.org/journal/volumes/volume-16-%28published-in-1938%29/issue-11/theme-structures-of-new-york-world-s-fair/)
- [1939 *Architectural Record*: Design Trends theme center construction](https://www.worldsfairphotos.com/nywf39/articles/design-trends.pdf)
- [Smithsonian description of realized monuments](https://americanhistory.si.edu/collections/object/nmah_1129345)
- [NYPL World's Fair corporate records and engineering plans](https://archives.nypl.org/mss/2233)
- [Carnegie architectural studies and Helicline width](https://carnegiemuseums.org/magazine-archive/1997/sepoct/feat6.html)
- [ASCE structural engineering paper, 1941](https://ascelibrary.org/doi/10.1061/TACEAT.0005368)

**Next actual architectural work:** reconcile Trylon bay schedule/base portal and steel profile changes; solve Perisphere meridian/ring stations and bridge levels; confirm Helicline exact site path/footing positions from period plans; test public walk/collision in Unreal; author historically grounded materials + optional stylized skin. Preserve the long-running Rhino and StructureGraph geometry.

## Subsequent visitor-shell and circulation update

[Guest-flow v002](THEME_CENTER_GUEST_FLOW_V002.md) adds an **interior/egress preview only** (two modeled exit frames, handrails, solid *unapplied* CAD cutter guides, provisional scene hotspot coordinates, Helicline endpoint proximity check). It **never overwrites** the watertight original print shells. Native Unreal collision/visitor traversal and real physical print apertures remain separate engineering acceptance gates.

## 2026-10-20: Wolfram + Game Development Studio preflight v001

A new **read-only** cross-tool handoff checks v005 manifest lineage, historical numerical constraints and v004 provisional aperture/body arithmetic. The calculation was independently reproduced with the Wolfram Language evaluator. The pipeline includes [handoff instructions](../../../docs/THEME_CENTER_ENGINE_HANDOFF_v001.md), the [machine-readable gate](ENGINE_HANDOFF_GATE_v001.json), a stdlib-only [preflight script](../../../tools/world_build/preflight_theme_center_v005.py), and [seven passing hermetic regression tests](../../../tools/world_build/test_preflight_theme_center_v005.py).

The default mode is **metadata-only**. Supplying the exact v005 GLB additionally checks byte hash and static glTF structure. Neither mode substitutes for actual Unreal import, full continuous collision/traversal, Game Development Studio inspection/packaging or historical as-built opening evidence. Do not promote the v004 435 clear sampled poses into a navigation certification. Preserve original watertight print models.

Next executable gate: run the byte-level preflight against the exact archived v005 GLB, then separately obtain authorization and a configured local Game Development Studio/Unreal runtime for native checks.

## Mathematical constraint solver v0.1 (2026-10-20)

Source and tests are now in [tools/theme_center_constraints](../../../tools/theme_center_constraints/README.md), with the [Wolfram audit and game handoff](../../../docs/THEME_CENTER_SOLVER_V001.md). The [complete portable working bundle](https://drive.google.com/file/d/1lVtPOlNAyZWt-IEnroNxEqAk-QmPi_IT/view) is backed up in the project Drive archive (SHA-256 `e32a683127e2dc248832ba1065402d5224d0089a63e6471577b7e8b34963e0f2`).

A frozen export of all 68 BIM master facts is checked against verified values, Code_Drive status, stable registered element IDs and geometric constraints. The solver emits 60 unique constraint element records, a JSON open-constraint report, and an engine-neutral overlay referencing **existing assembled runtime v005**, not new replacement geometry. Twelve local regression tests passed; the separate analytic sphere GLB is only a dimensional comparator. The project retains its original Y-up/metre 573-node v005 scene unchanged. Underdetermined Trylon base, bridge levels, Helicline path and other gaps remain blocked. Game Development Studio's local CLI was not available for package admission, nor was Unreal available for import/collision/navigation testing.
