# FMP — historical horticulture and planting plan register

**Objective:** Reconstruct what was planted **where and when**, not simply scatter generic tree assets around the fairground.

The canonical FMP database now includes `site_plant_sources`, `site_plant_taxa`, `site_planting_beds`, `site_planting_schedules`, `site_individual_plants`, and `site_plant_era_relations`. Each is year-specific and retains provenance and location certainty. Bed boundaries are empty until historically sourced drawings are aligned to site control. Plant taxon names need confirmation from planting schedules rather than image-based guesswork.

## Strong archival leads

1. **Long Island University, Shogo Myaida archive:** 1939 Nippon Garden planting plan in Map Drawer Folder 15.3 (42 x 22 in), copies Folder 15.4; Japanese Pavilion garden detail plans Folder 15.2, dated December 9, 1939. This is the first candidate for a truly plant-by-plant reconstruction. [Archive inventory](https://liu.cwp.libguides.com/archives_and_special_collections/shogo_myaida_mapdrawer).
2. **Cornell, Helen Bullard papers:** 1937 NY World's Fair tree-planting contracts in Box 4 Folders 1–2 and 1938 bedding/landscaping and tree-planting specifications in Box 4 Folders 3–4. These should tell us actual specified species, stock size, spacing, materials and methods if the pages survive. [Collection inventory](https://rmc.library.cornell.edu/EAD/htmldocs/RMM06501.html).
3. **NYPL 1939/1940 fair corporation records:** Board of Design drawings, construction and maintenance files covering landscaping, public gardens, and site plans, not necessarily complete as-built individual tree maps. [Archive guide](https://archives.nypl.org/mss/2233).
4. **1964–65:** source-specific garden and landscape plans must still be obtained. The published Operations Drawing Manual is valuable for site infrastructure and ground plans but should not be mistaken for a species-by-species planting schedule. [Manual index](https://www.worldsfairphotos.com/nywf64/operations-drawings-manual/index.htm).

## Required detail for every reconstructed planting
- Era and season: 1939 vs 1940 vs 1964 vs 1965, opening season and any replanting, blooming state or removal.
- Named landscape zone/garden and associated pavilion, garden bed ID or tree ID.
- Species/genus/cultivar (with uncertainty), stock height/caliper or spread when specified, quantity, spacing and arrangement.
- Bed outlines or individual planting centerlines, date of drawing and source callout, dimension provenance and uncertainty.
- Irrigation/water-system interface (do not infer pipe routing), soil/topography, hardscape borders and maintenance paths.
- Unreal plant model identity, LOD and canopy growth state; optional scaled print geometry or proxy for small plants.
- Preserve relationship across eras only with evidence; a 1964 tree near the same place as a 1939 tree is not automatically the same tree.

## Current starting state
Six archival leads; five botanical/common-name research placeholders; three named-area garden records (Nippon Garden, Japanese Pavilion garden and Constitution Mall beds). **Zero traced bed polygons, zero confirmed species-to-bed schedules, and zero placed individual plants.** Counts cited in secondary historic summaries are not per-bed inventories.

Next: obtain LIU 15.3/15.4, trace bed geometry and transcribe species symbols and legend; investigate Cornell planting specifications; independently build 1964/1965 landscape drawing list. Only then generate exact planting positions and seasonal Unreal variants.

Run `python3 tools/sync_master_database.py --once` to rebuild master SQLite from all committed catalogs. Runtime rebuild and native Unreal acceptance remain pending.
