# 1939 Theme Center — visitor-circulation correction, v0.1

**Buildings:** WF0001 Trylon + WF0002 Perisphere. **Related places:** WF0003 Democracity, WF0004 Helicline.

**Status:** source-model derived **provisional guest-continuity pass**. It is not a surveyed period floor plan, a historical portal/bridge dimension proof, a baked collision solution, or a native Unreal walkthrough. Original source **FMP_ThemeCenter_Staging_v001.glb** (510 scene nodes; SHA256 `a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5`) is unchanged.

## Historical circulation correction

Contemporary and photographic sources support this sequence:

1. Enter at base of the Trylon and take two escalators to Perisphere viewing levels.
2. Experience Democracity on two moving spectator platforms.
3. **Lower platform exit:** directly to a connecting return bridge.
4. **Upper platform exit:** descend a staircase to the return bridge.
5. Cross back **through Trylon** to the Helicline and descend to the fairgrounds.

This is important: the previous model's `Helicline_Bridge_Transition_Hypothesis` implies a shortcut directly from the bridge to the Helicline. Retain that source geometry for provenance but **hide it in the corrected real-time preview**. The entry escalators and exit bridge are separate circulation functions; do not inadvertently treat all bridge decks as bidirectional guest transit.

Source leads:
- New Yorker contemporary preview, 1939-04-15, escalators reaching elevated rotating platforms: https://www.newyorker.com/magazine/1939/04/15/stanley-in-the-perisphere
- Photo-led review of upper-exit staircase / lower-exit direct bridge and passage through Trylon: https://drivingfordeco.com/vanished-new-york-city-art-deco-the-trylon-and-perisphere-part-two-1939-1941/
- NYPL fair construction archive for plans and final drawings: https://archives.nypl.org/mss/2233
- Period illustration and design-history references are not necessarily *as-built* proofs. In particular, **52/64-foot proposed entrance elevations remain F047 PROVISIONAL and must not silently become historical truth**.

## Geometry changes; deliberately non-destructive

The supplemental **Unreal-only override** replaces the source node `Perisphere_Lower_Removable_Shell` with `Perisphere_Lower_Removable_Shell__UNREAL_PORTALS_v001`. It removes 216 source triangles from the negative-X arrival flank to open two **preview entrances** at the original model's lower and upper viewing platform levels. It also creates:
- Twenty-three individually named tread proxies for the **upper-platform exit** to the bridge. Source-modeled platform-to-bridge drop is 3.68808 m; current preview horizontal stair run 8.24401 m; 0.16035 m nominal riser, 0.35844 m horizontal going. This is **NOT period stair engineering**.
- A short upper landing connector.
- A return-bridge segment through the existing Trylon-side portal region.
- A three-part return passage from the Trylon interior toward the existing Helicline deck head.
- Debug node markers and a machine-readable route graph.

The 510-node source GLB remains untouched. The ORIGINAL **watertight** Perisphere shell is the retained printable/fabrication parent. The runtime skin intentionally has **open portal boundaries**, so it is NOT usable as a closed printable solid. The two aperture placeholders are **2.4 m high and 2.35 m wide**, both INTERPRETIVE (historical actual widths/heights unknown). Original portal/bridge elevations and railing geometry still need plan tracing.

### Source model-coordinate checks

- Lower landing center Y = approximately **15.77340 m**; bridge center Y = approximately **15.74292 m**. The 30.48 mm difference is a model-specific detail, not a documented historical step.
- Upper landing center Y = approximately **19.43100 m**.
- Existing Trylon east face has an opening in the source mesh at Y ~15.74 m and Z ~3.05 m: negative-X intersection test found only the far-side Trylon face, not a bridge-facing blocking face. This verifies **model geometry only**, not original opening dimensions.
- Helicline modeled head is near X=-32.5, Y=15.74, Z=-9.5; chosen return path and deck alignment remain speculative and must be adjusted from final drawings.
- Scale model and Unreal skin share the same model-local coordinates, but **project georeferencing remains unresolved**.

## Deliverables and validation

- `ThemeCenter_1939_Circulation_Portal_Delta_v001.glb` — source-aligned real-time override, stairs and additional deck previews; debug nodes prefixed `DEBUG_` (exclude from presentation).
- `ThemeCenter_1939_Circulation_Contract_v001.json` — machine-readable source hash, window parameters, original nodes, route graph, source status and blockers.
- `A111_ThemeCenter_Circulation_Delta_ModelLocal_v001.dxf` and diagram SVG/PNG — plan/elevation projected into the source GLB's **Y-up metre** frame, not historical surveyed fairground coordinates.
- `build_circulation_delta.py`, `make_circulation_drawings.py`, and `test_circulation_delta.py` — reproducible local builder and nine validations.

**Local source-GLB tests: 9/9 passed.** The source SHA is confirmed, two openings are clear along the intended negative-X guest crossing, the far sphere wall remains intact, stair tread/progression math passes, the Trylon east-face opening was detected from source triangles, all generated meshes are finite, and the original source hash remains untouched.

**Unresolved acceptance before a visitor-ready claim:** final portal and stair drawings; actual Trylon exit portal/Helicline junction; double-sided Unreal shell normals/material import; collision and navigation meshes; photomatched facades; printed opening/assembly design. No native host acceptance or documented as-built certification yet.

## Pipeline handoff

The **master building database retains source geometry** and archives; the route delta can be registered as a new source-linked Unreal overlay once its GLB is stored in the production asset location. Use a distinct `asset_id`, never silently replace the printable shell parent. No projection mapping logic is introduced by this pass.
