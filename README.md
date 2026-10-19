# The Flushing Meadows Project

An open research and reconstruction effort for the Flushing Meadows–Corona Park site across **1939, 1940, 1964, 1965, and 2026**, with a geographically grounded, explorable Unreal Engine world.

**Repository:** https://github.com/cameronprops/TheFlushingMeadowProject

## Goals
- Inventory **every documented structure**, landscape feature, entrance, plaza, road, transit line, parking area, and adjoining city-block context, rather than assuming the current starter catalog is exhaustive.
- Track original plans, surveys, photographs, archival sources, dimensional facts, uncertainty, and licensing through a searchable point of truth.
- Reconstruct source-backed buildings and exhibits, including Trylon, Perisphere, Democracity, Aquacade, Westinghouse's Elektro and Sparko, and both World's Fairs.
- Build an Unreal Engine open-world walkthrough with **first-person and third-person modes**, interactions, and a subway-station time-travel hub.
- Reconstruct **distinct terrain and grading states** for each era. Modern elevation data must never be presented as 1939 terrain.

## Project state
**Foundation/bootstrap only.** The starter catalog is NOT a complete list of buildings. Historical footprint matching, survey control, the Unreal build, character collision, world streaming, and the five-era transition are not yet validated. The existing Democracity v0.9.x web tours are separate proof-of-concept releases.

## Working areas
- [Catalog and database](database/README.md): structured records, evidence claims, archived-source references, and SQLite generation.
- [Historical accuracy standard](docs/RESEARCH_RULES.md): distinguish verified, inferred, proposed, provisional, and interpretive data.
- [Geospatial rules](docs/GEOSPATIAL_STANDARD.md): provenance, horizontal CRS, vertical datums, epoch-specific topography.
- [World and gameplay design](docs/UNREAL_IMPLEMENTATION.md): Unreal World Partition, eras, time portal, interaction and navigation.
- [Archive policy](docs/ARCHIVE_POLICY.md): file hashes, rights, Drive archival storage and stable release references.
- [Milestones](docs/MILESTONES.md): ongoing production and research gates.

## Verify the catalog locally
Requires Python 3.10+ and no third-party Python packages.

```bash
python tools/validate_catalog.py
python tools/build_db.py --output out/flushing_meadows.sqlite
```

The SQLite file is a **generated working index**, not the sole historical authority. Check in text CSVs, SQL migrations, and source manifests; do not commit multi-GB scans, terrain rasters, or transient Unreal cache directories.

## Preservation and collaboration
Git records decisions, source data, code and asset references. The archival originals, large releases, scans and GIS datasets belong in the Google Drive research archive, with stable links, SHA-256 hashes and rights notes kept here. Binary 3D/Unreal assets selected for Git are tracked through Git LFS (see `.gitattributes`).

**Important:** The repo name uses **Meadow** (singular) in the URL, as originally created; the project's public name remains **The Flushing Meadows Project**.

## Initial research archive
[Research Snapshot v1.0.0 on Google Drive](https://drive.google.com/file/d/1t5XpdiUC27QTL0928cQloJdRUSkGeAHj/view?usp=drivesdk) includes the older **59-target / 66-source** 1939–1940 research database, a 45-row plan register, per-target CSV records and uncompiled Unreal reference code. The ZIP is **an archived seed**, not a reconciled or exhaustive five-era point of truth. See [snapshot manifest](archive/research_snapshots.csv).
