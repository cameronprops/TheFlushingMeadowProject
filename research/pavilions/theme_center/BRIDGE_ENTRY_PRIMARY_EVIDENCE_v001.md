# WF0001 / WF0002 / WF0004: the actual 1939 entrance, bridge, and Trylon escalator interior

**2026-10-20. Status: evidence researched; model comparison implemented and tested; bridge architecture NOT reconstructed.** No generative image can serve as evidence. No v005 or historic/print geometry was modified.

## Critical finding: two different stacked passages

Period fair publicity expressly described **an open bridge above an enclosed escalator chamber** between the Trylon and Perisphere. Two escalators connected the Trylon lobby to different platform entrances. On exiting Democracity the upper-level spectators descended a stair to the open return bridge; the lower-level spectators stepped onto that bridge directly. Crossing back through Trylon led onto Helicline. The public **ground-level PERISPHERE ENTRANCE canopy**, ticket control, and aluminum-lined lobby are architecturally separate from the two provisional upper-level return apertures. Do not conflate them.

The period guide also describes *proposed* entry heights 52 and 64 ft. Those figures are not independent as-built measurement; do not adjust present geometry to them without a final survey/plan revision.

## Primary sources and authoritative leads

| ID | Source | What it establishes | Caution |
|---|---|---|---|
| E01 | [The Met: Gottscho, entrance, accession 1987.1100.403](https://www.metmuseum.org/art/collection/search/265469); [CC0 original scan on Wikimedia Commons](https://commons.wikimedia.org/wiki/File:-1939_New_York_World%27s_Fair,_Entrance_to_Perisphere-_MET_DP103124.jpg) | Distinct public entrance at Trylon base, visible period photograph | No doorway dimensions inferred yet |
| E02 | [The New Yorker, Apr 15 1939 issue](https://www.newyorker.com/magazine/1939/04/15/stanley-in-the-perisphere) | Contemporary firsthand account of **two Trylon escalators** and an elevated Perisphere side entrance | Report says 50 ft walk-up during preview, not a measured as-built survey |
| E03 | [1939 Fair publicity in period Pennsylvania Railroad visitor guide](https://www.rgusrail.com/fairs/nywf1939_prr/nywf1939_prr.pdf) | Explicit **open bridge above enclosed escalator chamber**, two Perisphere entry levels | 52/64-ft figures and 900-ft Helicline may describe proposal, not built revisions |
| E04 | [NYPL Theme Center U-6 archival finding aid](https://worldsfair.nypl.org/containerlist.pdf) | Box **1660 folders 2-5**, escalators/moving platforms/elevators; box 1659/4 architects; construction photo records | Catalog existence does not prove sheet dimensions |
| E05 | [Driving for Deco historical photo reproductions](https://drivingfordeco.com/vanished-new-york-city-art-deco-the-trylon-and-perisphere-part-two-1939-1941/) | NYPL lobby photo, turnstiles, return bridge photos and NYPL component diagram indexed together. Secondary author describes **aluminum-lined lobby** | Original NYPL image IDs not yet recovered; reproduction is not dimensional survey |
| E06 | [Historic exterior photograph reproduced by Modernist Collection](https://www.modernistcollection.com/deco/twa-ticket-counter-saarinen-s9rn8-ey24z-sbwdb-j7w7r-w787a-7w2lf) | Visible smooth **concave underside of upper passage**, modest entrance structure and lettering | Need original scan and camera calibration for curvature; no fictional Deco buttresses |
| E07 | [NYPL construction photographic record](https://old-digitalcollections.nypl.org/items/917ab9c3-76b6-1637-e040-e00a180679d6) | Dedicated Trylon/Perisphere construction photographs | Individual frame/phase must be determined before tracing |

## Exact v005 model comparison, not artist concept

Executed source-locked scan against `FMP_ThemeCenter_Assembled_Runtime_v005.glb`, SHA256 `de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439`. Run `python tools/world_build/inspect_theme_center_bridge_entry_v001.py /path/to/v005.glb /path/to/out` to regenerate the section and measurements. Outputs include `GLB_REAL_SECTION_v001.png` and `GLB_BRIDGE_ENTRY_MEASUREMENTS_v001.json`.

- `Trylon_Lobby_Floor_Envelope`: actual model Y approximately **0–0.12 m**; public canopy/sign/turnstiles and documented aluminum lining are **not authored**.
- `Escalator_1_Envelope`: X **-49.07 to -20.89 m**, Y **1.34 to 15.85 m**, model-local. This is a modeled envelope, **not an archival engineering profile**.
- `Escalator_2_Envelope`: X **-49.07 to -23.30 m**, Y **2.26 to 19.51 m**, model-local. Same uncertainty.
- `Return_Bridge_Deck`: around X **-36.27 to -17.07 m** and Y **15.64 to 15.85 m**. Exact observed Y extent ~**0.21336 m**. This component is essentially a flat **deck proxy**, not the photographed arched architectural outer bridge or the enclosed escalator chamber.
- Earlier v006 return-portal infill is a *provisional elevated exit* geometry test, **not** the ground-level public entrance.

## Required production sequence

1. Acquire original NYPL lobby photograph and return-bridge closeup, independently identify their item IDs, photographer, dates, copyright and phase.
2. Register at least two photographs against known built Trylon/Perisphere dimensions and the same camera geometry. Solve curvature, elevation and taper with uncertainty, instead of guessing an arc or copying the prior AI illustration.
3. Develop separate **editable** `Trylon_Public_Entry`, `Trylon_Ticket_Turnstiles`, `Trylon_Lobby_Interior`, `Escalator_Enclosure_1_2`, `Bridge_Arched_Underside`, `Bridge_Open_Return_Deck`, `Perisphere_Low_High_Apertures`, and `Trylon_Helicline_Return` families. Version them as derived or provisional as appropriate, retaining original masters.
4. Make actual-model matching camera render comparisons, check internal passage connections and steel clearance, then run native Unreal visitor tests before promotion.

**Do not claim:** that any unmeasured interior, bridge profile, doorway or unexamined drawing is now historically reconstructed. Historical photo evidence is sufficient to invalidate the existing generic bridge, **not yet sufficient to lock a precise BREP without calibration**.
