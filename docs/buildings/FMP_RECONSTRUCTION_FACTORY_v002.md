# FMP pavilion reconstruction factory (2026-10-19)

## Goal and scope
**One shared treatment for every building across 1939, 1940, 1964 and 1965**. The archive currently holds 239 research subjects and 195 physical-building/venue/exhibit candidates, **not 195 verified separate buildings**. Preserve the true relationships: a pavilion is an independent site structure; Democracity, Ford Cycle of Production and Futurama are **nested attractions**, while Helicline is **circulation**.

The Trylon + Perisphere work is the **master historical structural case study** and already includes a long-running Rhino/StructureGraph builder, the F001–F067 truth-audited dimension workbook, 510-node preserved GLB, trusses, skin, circulation and Democracity. Do not delete or reset it. Existing Ford, Westinghouse and GM assets likewise continue.

## Automated work chain (per historic year)
1. Create/resolve **building ID and parent relationships** in reconstruction_subjects, building_dossiers and building_linked_places.
2. Attach full primary evidence **per claim** in building_evidence: archival plans (exact sheet/date/revision), period photographs, original brochures, survey maps, exhibition drawings, historical materials and audiovisual sources. Store image rights and checksums. Search for filed plans; absence of surviving plans is not an automatic stop.
3. Add normalized **dimensional facts and explicit alternatives** in building_geometry_parameters. A drawing from a proposal is not an as-built dimension. Keep source units and SI. Unknown values stay blank; do not invent a rectangular footprint just to finish a record.
4. Populate **room/route schedules**, accessible vestibules, public exhibition path, connecting ramps, decks and mechanical ride paths in building_spaces. Realistically accessible *public sections* take priority over fabricated back-of-house.
5. Build or refine procedural geometry from the data; **import existing source assets first**. Output stable names and IDs, geometry separately from material skin, with BIM-ready component ownership. Every confidence assumption is an editable parameter.
6. Photomatch multiple images, camera model, silhouette, distinctive facade bays, terrain/topology and surviving dimensional anchors. Meshy can supply preliminary sculptural relief but is **not a source of measured as-built geometry**.
7. Publish equivalent **CAD plan/elevation/section sheets**, source-to-dimension register, visitor circulation map, PBR material schedule, realistic/stylized material overrides, preview GLB and Unreal-ready hierarchy.
8. Validate closed structural solids where intended, naked mesh boundaries, real-world scale, rendering materials and hero camera reference frames. Do not say visitor-ready until native Unreal traversal/collision/doors/level streaming have been tested.
9. Derive future Minecraft structures from approved source geometry by voxel/blocks conversion (possible, not yet implemented) without editing historic building coordinates.
10. Commit sources and machine-readable dossiers to GitHub; mirror big .glb/.blend/.3dm/texture/archives on project Google Drive with exact revision and hash. Do not claim Drive backup unless verified.

## Standard archive product for *each* candidate
`python tools/build_db.py --help` (see CLI in script) builds the source-linked SQLite DB.

`python tools/export_building_dossiers.py --database out/flushing_meadows.sqlite --output-dir out/building_program`

This produces a JSON dossier and **human-readable construction Markdown brief** for every candidate, backed by the same master tables, with detailed architecture and source citations, geometry parameters and source-class tags, interiors and public access state, existing asset URLs and linked related places, look-development notes and next actionable task. Candidates without solid geometry are intentionally **unmeasured** until source geometry is available.

The general 3D audit tool accepts any source model and evidence profile:

```bash
python tools/building_program/audit_archival_glb.py \
  --model /path/to/source.glb \
  --constraints research/pavilions/theme_center/THEME_CENTER_ASBUILT_CONSTRAINTS_v001.json \
  --out /path/to/audit
```

Outputs per-node inventory, numerical-only checks, model plan/elevation SVG/PNG, and JSON. The machine compares only constraints physically measurable from current GLB. It does **not** substitute for final stamped drawings.

## Proof: preserved 510-node Theme Center

Existing [source staging model on Drive](https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view) SHA-256 `a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5`.

- Audited components: 510 scene graph nodes, including 293 Democracity descendants, 64 Perisphere tagged nodes, Trylon, Helicline, bridge and exterior landscape.
- 16 sourced constraints. 8 directly testable on mesh and numerically pass (610-ft Trylon, 180-ft sphere within small tessellation tolerance, 17-ft clearance, 8 support columns, 32 meridian, 15 latitude trusses, 2 moving platforms, 2 escalator envelopes).
- 8 other dimensions/events cannot be validated by this mesh-only check: plate structure heights, tip width, 528 pile count, ring centerline diameter, Helicline true centerline length/width, proposal-era entrance elevations.
- **Eight local regression tests passed** using this specific GLB and provenance profile, including byte-level SHA guard. No original nodes or geometry were changed.
- Existing as-built design corrections: 610 ft built vs earlier proposed 700; 180 ft built vs proposed 200.

Source dossier [Theme Center](../../research/pavilions/theme_center/README.md). Existing legacy workbook and generated assets are part of the dossier, not competing reconstructions.

## Next work in scene order

1. **Trylon/Perisphere**: resolve base footprint and 1939 entry portal, lattice/plate transition bay scheduling, truss ring latitudes, actual bridge/Helicline supports, visitor/collision checks, nighttime projection material surfaces. Preserve all old data and staged geometry.
2. **Ford**: move current v0.3 modeled columns/road/turntable toward historically traced outer envelope and animated industrial scenes; annotate Road of Tomorrow period constraints.
3. **Westinghouse**: source footprint and entrance, refine floating tower and glazed wings, visitor hall prototype.
4. **RCA**: retrieve CRE351 original architectural sheet set and digitize floor plans/elevations, then turn into first architecture-traced public interior.
5. **GM 1939**: work from Harry Ransom Center Albert Kahn/Bel Geddes Job 381; model original Futurama and main building independently.
6. Continue by evidence completeness and district adjacency, with separate 1964 variants.

**Cinematic intent:** physically plausible PBR facades, texture/UV scale, controlled glass and lights, neon/illumination, night-show projection, Unreal Lumen and Sequencer, real pedestrian circulation; realistic and stylized looks are distinct surface skins over the same architectural/core coordinate geometry.
