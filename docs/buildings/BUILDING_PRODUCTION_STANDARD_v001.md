# FMP building-by-building production standard (2026-10-18)

Decision: **construct the world systematically by building**, with researched and
educated-guess reconstruction allowed. Historically plausible visual impressions
are a legitimate milestone. **Realistic and stylized skins share the same physical
architectural geometry.** Invite external explorers only when several building
interiors are genuinely navigable in the target engine.

## One source of truth, not competing spreadsheets

- catalog/archive_inventory_candidates.csv: original 239 historical leads; NOT
  a census of 239 actual physical buildings.
- catalog/building_master_inventory_v001.csv: immediately readable list of 195
  possible buildings/venues/pavilions/concessions. Of these, 38 older entries are
  explicitly architecture-classified and 157 are still ambiguous classifications.
- database/migrations/005_building_program.sql: automatically preserves all 239
  research subjects in reconstruction_subjects and opens individual dossiers
  for the 195 candidate physical-building subjects. No candidate is silently
  promoted to verified built architecture.
- catalog/building_details.csv: researched author, form, dimensions/materials,
  configuration, rooms and uncertainty, initially 13 populated records.
- catalog/building_evidence.csv: individual period sources with actual archive
  call numbers, URLs, source/rights type, extracted claim and review status.
- catalog/building_spaces.csv: candidate walkable interior spaces, initially 8.
- building_appearance in SQLite: every candidate has REALISTIC and STYLIZED
  appearance records with the same footprint, collision, entrance and route IDs.
- building_worklog in SQLite: source geometry / export / engine test, linked to
  existing assets, each with review status and archival URI.
- tools/export_building_dossiers.py: produces 195 stand-alone JSON dossier files,
  searchable CSV master queue and alpha-interiors manifest from the SQLite DB.

## Reproducible DB and dossier generation

    python3 tools/validate_catalog.py
    python3 tools/build_db.py --output out/flushing_meadows.sqlite
    python3 tools/export_building_dossiers.py --database out/flushing_meadows.sqlite --output-dir out/building_program
    python3 -m unittest discover -s tests -v

The generated SQLite and JSON should be treated as derived outputs; edit
version-controlled CSVs and SQL migrations, then rebuild. Do not manually edit
out/building_program/buildings/*.json as source data.

## Archive reality
The 1939 Fair had design reviews, planning and construction records, but it is
not safe to assume every filed drawing is preserved or that every historic
tenant had a separate architectural filing. NYPL says many architectural
drawings were destroyed or dispersed after the fair. Seek site plans, dated
approved construction sets, board design records, architects' private archives,
corporate archives, photos, guidebooks and period films in parallel.

High-value currently traceable holdings:
- RCA: 1938 CRE351 (Athenaeum/Cret) first and second floors, elevations,
  sections, roof, grading and layout. The actual scans/measurements remain to acquire.
- Westinghouse: LOC Gottscho views; Skidmore and Owings/John Moss credited;
  150-ft tower period published; Smithsonian corporate exhibit records.
  329-component provisional exterior; now visitor-access proxy separately.
- New York City Building: original pavilion is the Queens Museum building,
  attributed by museum to Aymar Embury II; historic colonnade, glass brick,
  limestone and granite details.
- Consumer Interests: NYPL ps_mss_490 tenant/renting plan.
- Medical & Public Health: NYSL Box 5 Folder 11.
- Applied Arts: LOC Winold Reiss design studies; **proposed** not automatically built.
- Shelter Building: NYPL ps_mss_491 renting plan.

## Building stages: all must be independently gated

| Stage | Deliverable | Evidence bar |
|---|---|---|
| 00 Classify | physical structure / venue / exhibit / tenant / infrastructure / program | candidate; no geometry entitlement |
| 01 Source | per-claim citation with exact period/revision, scan, source URL, rights and file hash | catalog or period source |
| 02 Place | correct period site zone, orientation, footprint and local coordinate system | drawn plan or evidence-based map registration |
| 03 Envelope | roof, facade, overall massing, bay rhythm, dominant heights | dimensions where available; inferred otherwise |
| 04 Openings | entrance thresholds, exits, level transitions, door/frame clearances | measured or clearly labeled prototype |
| 05 Interior | separately loaded walkable public zones; exhibit details as source allows | access test planned, no fake as-built floor plan |
| 06 Skins | realistic + stylized materials/lighting | shared core wall/floor/door IDs, same collision meshes |
| 07 QA | human-scale walkthrough, nav paths, collider/door checks, performance | tested in Unreal/Worldwright, not inferred from GLB |
| 08 Release | archive geometry, generator, source snapshot hashes, revision and changelog | reproducible, backed up to Git+Drive |

For Stage 02-05, attribute each datum: DOCUMENTED_BUILT, PROPOSED,
PHOTO_INFERRED, HISTORICAL_MAP_TRACED, INTERPRETIVE or UNKNOWN. An accurate
building **placement** does not make guessed facade heights proven.

## First external-explorer alpha

1. Perisphere/Democracity: use existing model, establish walkable arrival,
   spectator area and return route. Verify entrances and floors in native Unreal.
2. Westinghouse: use photographed twin-wing exterior and a *separate*
   provisional hollow public-access proxy; add documented exhibits and actual
   hall boundaries as original plans become available.
3. RCA: architectural plan set CRE351 gives the best initial source
   for an interior after scans are acquired.
4. New York City Building: additional strong early target thanks to surviving
   architecture; keep the 1939 layout distinct from the modern museum.

Before inviting external testers, require at least **three** contiguous
accessible building visits, stable map transitions, collision-enabled floors,
doors wide enough for the chosen game avatar, no fall-through or trapped points,
correct scene origin, reproducible launch package and basic performance smoke
tests. No released FMP build meets that acceptance gate yet.

### The stylized skin policy

Geometry is **not rebuilt** for skins. Each piece has a stable component ID,
material slot, period, provenance and physical/visual role. Realistic and
stylized appearances can change textures, palette, materials, edge treatment,
render lighting and non-colliding graphic overlays. Entrance geometry, floors,
stairs/ramps, door openings, LOD collision, walkable navmesh and world transform
must remain identical unless the project owner separately authorizes topology
changes. Stylization is a visual option, not invented narrative.

## What should be worked on next

Trace RCA CRE351-001/-002 and CRE351-008 accurately, then model a registered
RCA footprint and an uncluttered accessible ground-floor prototype. In parallel,
test Perisphere/Westinghouse access geometry in Unreal on the target avatar and
collision profile. Continue identity/classification work through the 1964/65
candidate list rather than blindly placing 122 index topics as separate pavilions.

## Direct references
- NYPL fair corporation records: https://archives.nypl.org/mss/2233
- Athenaeum RCA drawings: https://www.americanbuildings.org/pab/app/ho_display.cfm/56239
- LOC Westinghouse architectural photo: https://www.loc.gov/pictures/item/2018750438/
- Queens Museum: https://queensmuseum.org/history/
- NYSL public health: https://nysl.nysed.gov/msscfa/qc16514
- NYPL Consumer Interests: https://old-digitalcollections.nypl.org/items/932609db-b85a-ffde-e040-e00a18067b32
- LOC Applied Arts: https://www.loc.gov/pictures/item/2019647967/

This file is a BUILD STANDARD and QA contract, not evidence of a playable
Unreal game or surveyed pavilion layout.

## 2026-10-18 procedural and cinematic data extension
See [the source-driven procedural, cinematic PBR, and Minecraft pipeline](PROCEDURAL_CINEMATIC_AND_VOXEL_PIPELINE_v001.md).

New tables: building_geometry_parameters, building_surface_research,
building_view_observations, unidentified_visual_leads. These feed the *same*
per-building JSON export; no parallel manual model list. Geometry parameters
store era, units, source ID, uncertainty and component identifier. Surface
records distinguish lookdev numbers from historical measurements.

Priority additions: 1939-1940 GM (WF0012; Albert Kahn building drawings,
Norman Bel Geddes Futurama) and 1964-1965 GM (FMP64SUBJ0064; period canopy,
roof indicator and pavilion dimensions). These are **different pavilions**.
The owner-described rotating floating pyramid is an UNIDENTIFIED research
lead, not yet a named historical building.

Minecraft export is architecturally feasible as a derived voxel/structure
build from the same core site/building assets and distinct block palette,
but is **not implemented**. Unreal cinematic surface lookdev, native host
inspection, and photo camera matching are also future implementation gates.
