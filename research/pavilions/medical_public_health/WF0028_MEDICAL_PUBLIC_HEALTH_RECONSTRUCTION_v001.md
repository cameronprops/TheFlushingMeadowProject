# WF0028 Medical and Public Health Building: measured reconstruction gate v001

Date: 2026-10-19. **Research acquired at catalog and public-reference level, not full-resolution original plan sheets. No as-built floorplan has been traced.**

## Significant discovery: two explicit plan holdings
1. New York State Library, Expositions, Fairs, Celebrations, and Ceremonies Collection, **Box 5 / Folder 11**: *Plan of the Medical and Public Health Buildings*, New York World's Fair 1939. Physical sheet **50.5 cm × 39.5 cm**. This is the *paper size*, not the building size. https://nysl.nysed.gov/msscfa/qc16514
2. New York Public Library, 1939/1940 World's Fair Inc. Records, **C2.3 Working Drawings and Models, Box 206 / Folder 10**: *Medical and Public Health Building*. Catalog folder description, not proof of each enclosed drawing's specific revision or content. https://worldsfair.nypl.org/containerlist.pdf

Both drawings/collections should be obtained, reviewed, and reconciled rather than using one small catalog image to infer walls.

## Photographic and facade controls
- Library of Congress Gottscho-Schleisner photograph, LC-G605-CT-00438, 1939 **or** 1940, architects **Mayers, Murray & Phillip**. https://www.loc.gov/pictures/item/2018750371/ . Rights advisory: no known restrictions on publication, but final use should check LOC guidance.
- International Hildreth Meière Association: documents a coordinated **Medicine and Public Health / Science and Education complex**, including a historical scale model and **nine** numbered artwork positions. The complex must be decomposed into source-backed constituent building envelopes, not two guessed standalone masses.
- Named entry facades: **Avenue of Patriots**, and corner at **Avenue of Patriots × Hamilton Place**. Site placement remains **unregistered**; the street names alone do not provide a metric transform.
- *The Picnic* on long garden-court facade: mural dimensions **14 ft high × 110 ft long** (~4.2672 × 33.528 m), per Meière Association description. Do not mistake mural extent for facade or building extent.
- Science and Education southern adjoining facade treatment: *The Family* and *The School* (silhouette mosaic); preserve their artwork assignments to the correct complex component.
- Other identified commissions in reference model: *Modern Medicine*, *Primitive Man and Modern Man*, *Hippocrates and the Dragon of Ignorance*, *Comte de Rochambeau*, *Tadeusz Kosciuszko*, *Man between the Past and the Future*. Exact geometry and locations require plan registration and image inspection.

## Proposed source-tracing coordinates, NOT geometry
- Plan-specific pixel frame: top-left image pixel, crop dimensions and native resolution retained, source Y increases downward.
- Separate model-local metric frame: Z-up. Establish origin from an unambiguous plan grid/corner after inspecting full-res sheet, **never use image sheet size as scale**.
- Room IDs: `WF0028-F01-R###`; wall IDs `WF0028-F01-W###`; entrances `WF0028-F01-D###`; murals `WF0028-MURAL-###`. IDs reserved by convention, not yet instantiated.
- Preserve 1939 and 1940 states as independent evidence decisions.

## Modeling gates
A. Download or request full-scale plan image from NYSL and NYPL with revision/date/rights.
B. Extract written dimensions or graphic scale and independent measurement controls; cross-check both sheets.
C. Trace **exterior boundaries first**, then courtyards, rooms, column/grid locations, entrances and stairs without adding imaginary partitions.
D. Check photo sightlines and Meière murals to locate the correct faces and correct constituent building.
E. Produce source-qualified shell and rooms in separate objects; keep artistically inspired placeholders in an **interpretive** layer only.
F. Join entrance nodes to dated fairground paths after site registration and run physics/collision and visitor traversal in Unreal.

**Current:** Stage A catalog locations identified only. B–F blocked on readable originals, no new GLB or Unreal import. Existing building ID WF0028; Science and Education identity remains unassigned in neighborhood register.

## Additional interior source priority and trace contract

NYPL construction records include C1.0110 Box 142 Folder 7 (Medicine and Public
Health charts, maps and plans), Folder 11 (1939 proposed plan), Folder 6 (N-5
building 1939), and Folder 5 (N-5 building 1940). Cross-check with the
1939 book `Man and His Health`, particularly reported plan pages 30-31; these
pages have not been inspected and are not yet accepted geometry evidence.
The NYPL digital record for a polio/iron lung exhibit is also an exhibit subject
lead, but not a room assignment:
https://digitalcollections.nypl.org/items/5e66b3e9-1b3e-d471-e040-e00a180654d7

[Blank plan trace intake](WF0028_PLAN_TRACE_INTAKE_v001.json) now enumerates
source-sheet IDs, metadata, verification fields, empty room/wall/opening/route
sets, and deliberately unverified registration. It has no invented geometric
coordinates. Populate only after reviewing an original sheet at useful resolution.

No new geometry generated; no source image acquired; source and trace validation
remain to be completed.
