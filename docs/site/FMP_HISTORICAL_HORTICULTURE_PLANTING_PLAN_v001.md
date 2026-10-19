# Flushing Meadows Project — historic horticulture and planting plan, v0.1

**Objective:** Reconstruct the exact gardens, tree rows, shrub masses, bulb displays, lawn areas, planting beds, greenhouse gardens and seasonal changes as supported by original 1939, 1940, 1964 and 1965 documentation. Share site coordinates with the pedestrian, fountain, irrigation and utility layers. Do not place random period-looking trees and call them authentic.

**Status 2026-10-19:** Source acquisition/indexing complete for initial references; the geometry of individual beds/trees is NOT yet traced or registered. All imported plantings are reports or construction contracts, not measured individual polygons.

## Best archival sources — start here

1. [Long Island University — Shogo Myaida Map Drawer](https://liu.cwp.libguides.com/archives_and_special_collections/shogo_myaida_mapdrawer). **Folder 15.3**: 42 × 22 in **Nippon Garden planting plan**; **15.4**: two 22 × 11 in garden planting plans; **15.2**: Japanese Pavilion garden detail dated December 9, 1939. That last plan may be a subsequent/1940 design; do not apply it to the 1939 opening without review.
2. [NYPL 1939–40 collection container list](https://worldsfair.nypl.org/containerlist.pdf), MssCol 2233: **Box 191, folders 9–10**: 1939 landscape; **Box 191 folder 8**: 1940 landscape; **Box 192 folder 2**: Administration Building planting program; Box 192 **6 / 7 / 9**: Communications Building / Court N-5 / Federal Building landscaping; **Box 1698 folders 1–10**: Bulbs, lawns, maintenance, roses, soil analysis and trees. These are original archive subject files and leads, not fully acquired plans.
3. [Cornell University Helen Bullard papers](https://rmc.library.cornell.edu/EAD/htmldocs/RMM06501.html): **Box 3 folder 31 and Box 4 folders 1–4**, original 1937–38 World's Fair tree and bedding specifications.
4. [Queens Botanical Garden — Lost Flowers of the Fair](https://queensbotanical.org/lost-flowers-of-the-fair/): historical research on *Gardens on Parade* based on original Hortus guides, Harriet Pratt papers and photographs. Distinguishes the 1939 and 1940 seasons. The 1939 100-page souvenir guide reportedly contains a **keyed exhibit garden map**; locate and scan that original before drawing dozens of garden beds.
5. [NYPL 1964–65 fair corporate archive](https://archives.nypl.org/mss/2234) and [1964–65 finding aid](https://nyplorg-data-archives.s3.amazonaws.com/uploads/collection/pdf_finding_aid/nywf64.pdf): **C3.7 Planting Program**, C3.70 Trees, C3.71 Topsoil, C3.72 Meadow Mat, C3.73 Shrubbery, C3.74 Bedding Plants, C3.75 Sodding, C3.76 Spraying. These are classifications, NOT already recovered geodetic plant points.
6. [Cornell Clarke & Rapuano records 3047](https://rmc.library.cornell.edu/EAD/htmldocs/RMM03047.html): planning and Fair drawings, with 1964 landscaping by Clarke & Rapuano. [NYC Parks 1962 press record](https://www.nyc.gov/html/records/pdf/govpub/42521962_press_releases.pdf) references a **400-tree contract** along central roads from the Unisphere through the Industrial Area, naming red maples and honey locusts among the plants; **400 is NOT a per-species count, nor proof of installation**.
7. [NPS/Cornell 3D GIS and landscape study](https://www.nps.gov/subjects/ncptt/upload/2017-23.pdf), pp 72–78: uses **1965 demolition grading plan** and NYPL planting maps for historic-tree reconstruction. References 1964 site-preparation advice to **retain 1939-40 trees in rows**; some estimated positions and contemporary species IDs are research approximations, not a certified tree-by-tree continuity map.

## Seed planting schedule — only names and attributes supported by the cited historical accounts

| Era | Named location | Plants / feature | Evidence status | Counts |
|---|---|---|---|---|
| 1939 | Gardens on Parade — Jackson & Perkins Parade of Modern Roses | **Rosa** genus, specific cultivars to acquire | Historical exhibit description | **8,000 rose bushes in 250 varieties** |
| 1939 | Havemeyer Tribute Garden | **Weeping Japanese cherries**, botanical species/cultivars unresolved | Historical museum description | Unknown |
| 1939 | Havemeyer Tribute Garden | Central grass bowl | Historical museum description | Area/grass mix unknown |
| 1939 | Garden of Tomorrow | Lawn and display beds | Historical museum description | Species and exact geometry unknown |
| 1939 | Wayside Wild Flower Shrine | Native roadside flowering plants | Historical museum description | Species unknown |
| 1939 | Japanese Pavilion Nippon Garden | Detailed original 42×22-in planting plan identified | **Plan not acquired** | **No invented taxa, numbers or beds** |
| 1940 | Gardens on Parade — Pony Express **living stamp** | Alternanthera + Sedum, genus level only | Based on **1940** Hortus guide cited by QBG | Unknown |
| 1964 preparations | Central fair roads / Unisphere–Industrial Area | Red maples, honey locusts and other trees | **400-tree contract**, not installed census | **400 contract total, not 400 of each species** |
| 1964 | Mature formal tree rows in earlier Fair alignment | Surviving plantings from 1939–40 | NPS/Cornell citing period site-preparation report | Identity-level tree matches still unverified |

**Important source caveat:** The current Queens Botanical Garden contains some descendants/survivors of the earlier fair's horticultural collection, but it moved to a **different site** for the 1964 fair. Do not paste its modern beds into either historic fair plan.

## Master DB tables added

- `horticulture_sources`: 19 dated source records; original planting sheet versus finding aid versus later study.
- `horticulture_taxa`: 10 botanical taxa or explicitly unnamed/uncertain planting groups.
- `horticulture_areas`: 20 named garden/landscape units with nested beds, landscaping context and optional geometry.
- `horticulture_plantings`: 11 planted or contracted botanical descriptions; quantity basis, evidence class, variety and optional time window are distinct.
- `horticulture_seasonal_events`: 5 historical changes, including the 1938 storm/recovery, the 1940 living stamp and the 1962 contract.
- `horticulture_era_links`: 2 area-level cross-fair relationships, with a research-supported but NOT identity-level link between retained 1939 trees and 1964 rows.
- `horticulture_plant_instances`: **0** individual tree/shrub centers until traced.
- `horticulture_irrigation_links`: **0** supposed historic pipes until supported by an irrigation plan and existing site utility layer.
- `horticulture_mapped_areas`, `horticulture_mapped_plants`, `horticulture_research_queue`: validation-oriented views.

### Provenance requirements

Taxa must not be promoted from genus to species/cultivar without evidence. A detailed landscape original could be a **proposal**, a **construction contract**, a **1939 opening scheme**, or a **1940 revision**. Its document date and state must remain separate. Installations are not proven merely because contracted.

No tree, garden bed or lawn gets coordinates without sheet identification, map/control-point registration and uncertainty. All vegetation is absent from the current mapped-position feed until that work succeeds. Source sheet coordinates and true GPS/park coordinates must never be equated without an approved transform.

Historic individual-tree sizes (canopy and height) can eventually be inferred from dated species, original stock size, passage of years and period photographs, with inference separately flagged. Do not assign an idealized fully grown height by default.

## Procedural use: Unreal, print and eventual projection mapping

- Preserve the **same 1939/1940/1964/1965 coordinate and year system** already used for pavilions and site utilities.
- Each mapped planting/bed has a stable ID, species/precision, quantity, original plan symbol, evidence, planting density and installation status.
- Unreal: source-driven foliage instancing/HISM, seasonal material and bloom-state variations, outdoor shadow/collision budgets, distance LODs and possible nighttime illumination. Photos and original color descriptions are the source for foliage appearance.
- Physical model: print individual landmark trees where scale allows; at smaller scales derive simplified tree crowns and vegetation masses from registered points/beds, while retaining surface IDs to allow projection-mapped seasonal lighting.
- Irrigation: any discovered supply connection may link to `FMP_UTIL_SERVICE_WATER` and other existing site infrastructure, only with period evidence. Do NOT extend water/sewer centerlines automatically from a garden's existence.
- No generic randomized vegetation scatters in historically certified world layers. Optional interpretive filler must be separately named and able to be disabled.

## Reproduce / QA

```bash
python3 tools/sync_master_database.py --once
python3 -m unittest -v tests.test_horticulture

# Or with a previously built master database:
python3 tools/site/export_horticulture.py \
  --database out/flushing_meadows.sqlite --out out/horticulture
```

Outputs: `horticulture_progress.json`, `source_acquisition_queue.csv`, `planting_schedule.csv`, `zone_completion_queue.csv`, `unlocated_gardens.json`, `mapped_gardens_local.json`, `mapped_individual_plants.json`, `seasonal_change_log.json`, `inter_era_planting_links.json`, `documented_irrigation_links.csv`.

All outputs derive from one SQLite source, itself generated from the Git-controlled catalogs. No separate handwritten horticulture DB. Full rebuild and native Unreal/print host QA are still pending.

## Next research-to-geometry operation

**Begin with the original LIU Nippon Garden planting plan (15.3 and 15.4)** and the *Hortus* Gardens on Parade 1939 and 1940 keyed maps. Acquire permission/scan; digitize beds + exact legend labels at plan coordinates; align against named neighboring pavilions/paths and a dated, independently controlled base map; populate traced polygons and individual trees only after registration; then proceed to 1964 NYPL planting plans and 1965 tree survey source.

The reconstruction should show what was **actually planted**, not just what was feasible in the 1930s or 1960s.
