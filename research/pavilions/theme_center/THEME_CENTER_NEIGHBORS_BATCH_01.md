# 1939 Theme Center neighbors: batch 01 acquisition and construction ledger

Date: 2026-10-19. This is a **source triage**, not a verified plan or completed model.

## Linked data

- `catalog/theme_center_neighbor_buildings_1939_v001.csv`: seven candidate structures with existing IDs where assigned; `UNASSIGNED` does not authorize creating an arbitrary new `WF` ID.
- `catalog/theme_center_neighbor_sources_1939_v001.csv`: sixteen external archive references and evidence leads keyed to those candidates.
- `tools/validate_theme_center_neighbors.py`: checks referential integrity and that unregistered research is not represented as certified geometry.

The existing `catalog/places.csv` already contains WF0009 RCA, WF0010 AT&T, and WF0028 Medical and Public Health. Do not duplicate those entries. Reconcile other building keys to the master inventory before assigning persistent IDs. Neither site adjacency nor footprint location is accurately surveyed.

## Prioritize reconstruction by usable evidence

1. **WF0028 Medical and Public Health**: New York State Library Expositions collection Box 5 Folder 11 has a specifically titled **Plan of the Medical and Public Health Buildings** (physical sheet 50.5 x 39.5 cm). Library of Congress Gottscho photograph `2018750371` can check massing and exterior finish. Obtain the plan image and sheet metadata, establish whether it shows built state, trace exterior and rooms, compare photograph, then model separate 1939 assembly. Until the plan is readable there are **zero source-measured dimensions** accepted in this batch.
2. **WF0009 RCA**: prior provisional 29-part shell and Athenaeum April 11 1938 CRE351 plan/section set. Existing shell is not a substitute for the final 1st and 2nd floor plans. Trace CRE351-001/002/005 then build independent room/wall/door objects and experience positions only when supported.
3. **Business Systems and Insurance**: Smithsonian model photograph (ref775), Underwood exhibit (ref778), Great Discoveries mural (ref777), dated Rose Court postcard. Recover architect's site and floor plans, check with model and facade views, avoid dimensions from an illustration.
4. **Communications Building**: Smithsonian Cooper Hewitt Donald Deskey 1938 focal exhibit rendering n-d-8093; Art Institute of Chicago 1939 exterior photographic archive record (Box.FF 1.28). The exhibit design is not a building floorplan. Verify which exhibit spaces it occupied.
5. **Hall of Pharmacy**: Smithsonian photographic holdings (ref960) and NYPL mural construction file C1.6 Folder 11. Confirm independent building envelope, archival site relation and entrance before modeling.
6. **Science and Education**: Smithsonian photographic holdings ref835 and historical information Box 50 Folder 22 (ref2765). Find plan/section references; photographic record alone cannot support floor subdivisions.
7. **WF0010 AT&T**: Library of Congress photo `2018750314` specifically looks from the Theme Center toward the building, useful for view-direction registration but not distance or surveyed coordinates. Search first/second floor plan and machinery exhibits separately.

## Each building's acceptance gates

- A: at least one dated image or plan record linked by stable source ID.
- B: acquire drawable plan and record scale, revision, rights, coordinate frame, trace controls and uncertainty. No drawing = B blocked.
- C: independent local source-derived envelope, openings and structure; photograph and section cross-check.
- D: floors, rooms, exhibits and public/service path graph independently located and evidence tagged.
- E: world registration with dated plans and independent check residuals.
- F: export source mesh and native Unreal collision/path validation; separate print-safe shell as needed.

Present state: **A partially or fully achieved for all seven after this batch; B-F not achieved here**. RCA has earlier provisional shell work, not a newly certified B/C pass. Keep historical year 1939 distinct from 1940.

## Next focus: WF0028

Ask New York State Library for a high-resolution reproduction of Box 5 Folder 11, including scan or photography rights and any plan reverse/legend. Use the LOC photograph to cross-check envelope details. Then compare with the existing `WF0028` live catalog record and trace the floorplan. There is no permission to promote guesses into a surveyed fairground coordinate.

No model generated or new world GLB exported in this batch; no Unreal tests performed.
