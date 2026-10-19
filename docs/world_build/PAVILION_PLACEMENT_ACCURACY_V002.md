# FMP historical pavilion placement standard, v0.2

## User directive (2026-10-18)
The world can be a historical *impression*, with vegetation, ambience, fountain animation and incomplete facades provisionally modeled. **Pavilion identity, placement, footprint and rotation must be as faithful to contemporary fair maps as available evidence permits.** Do not make invented pavilion buildings part of the historical scene just to fill open space.

## Corrective world release
The Constitution Mall v0.1 model used six anonymous mirrored pavilion masses, each with plinth, main shell, crown, seven piers and fascia (66 mesh nodes). They had no measured period plan basis, and must NOT be treated as actual pavilion placement. The v0.2 generator, built directly on the unchanged 510-node Theme Center, omits these 66 objects. The combined v0.2 world has 350 added nodes (860 total). All original source nodes and original BIN bytes remain unchanged. The retained reflecting pools, lagoon, paths, landscape, fountain effects and local +X mall orientation are still interpretive and NOT georeferenced.

## Historical orientation references
The period descriptions place the central Constitution Mall axis from the Trylon/Perisphere toward the Lagoon of Nations and Court of Peace. The Court of Communications and Court of Power are distinct neighboring sections, not a symmetrical six-pavilion row. These descriptions establish organization and adjacency, **not precise footprints**.

Historical source priorities:
1. NYPL 1939 General Plan, drawing XM-250: https://old-digitalcollections.nypl.org/items/926ff6bc-5ff8-0931-e040-e00a180628c4 (public preview only; original high-resolution scan may need ordering)
2. NYPL Blum's 1939 Travel and Guide Map: https://old-digitalcollections.nypl.org/items/a907fab0-35d3-0131-dc50-58d385a7bbd0 (original scan download listed, map's planimetric accuracy must be evaluated)
3. Historical 1939 fair description published by Alton Railroad: https://www.rgusrail.com/fairs/nywf1939_alton/nywf1939_alton.pdf
4. Historic fair photographs and visual massing: https://www.worldsfairphotos.com/nywf39/book-sample-pages.pdf
5. NYPL Board of Design / grading and survey plans: https://archives.nypl.org/mss/2233

## Geometry evidence levels
- **A, DRAWING_REGISTERED**: selected final/as-built, era-specific scaled footprint + control registration + documented residuals + direction/rotation.
- **B, PERIOD_MAP_TRACED**: period map image, dated/versioned image hash, pixel-traced polygon transformed to the FMP local model frame, review record and uncertainty estimate. Suitable for approximate but evidence-backed pavilion shell placement.
- **C, ZONE_LOCATED**: identity and fairgrounds zone known, outline/center unknown. **No visible historical pavilion mesh should be created yet.**
- **D, INVENTED**: interpretive placeholders separate from historical architecture, not placed by default.

Required before placing each named 1939/1940 pavilion: stable place ID, year/season, map source URI, map image hash/edition, polygon pixel vertices, registration reference, transform/accuracy classification, derived local footprint, facade orientation, evidence links. Dimensions, roof, materials and facade have independent confidence values; do not infer accurate height from an accurate center coordinate.

Every 1939, 1940, 1964, 1965 and 2026 world state requires separate verification. No automatic 1939-to-1940 or 1939-to-1964 unchanged footprints. Future 2039/2064 asset layers are fictional and must not enter historical-source registries.

## Current known facts, not false placements
The accompanying FMP_1939_Pavilion_Placement_Register_v001.csv contains candidates whose names/zones are known in the working catalog. Their XY, rotation and footprints are intentionally blank. They are **not** necessarily the actual pavilions directly lining Constitution Mall.

## World QA
Verify v0.2 against 510-node base: original nodes and binary unchanged, 860-node result, 350 new interpretive nodes, no FMP_MALL_v001_PAVILION_* objects reachable in active scene, no invented pavilion row, no claimed pavilion coordinates. Original 1939 ground axis itself remains unregistered pending map control.
