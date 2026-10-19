# The Flushing Meadows Project

A source-backed reconstruction of Flushing Meadows–Corona Park across **1939, 1940, 1964, 1965 and 2026**, built toward an explorable Unreal Engine world with flexible adventure, puzzle and exploration systems.

**World first.** Build and validate the place, beginning with exteriors and circulation. Preserve the ability to choose how it is played later. Cameron owns the creative direction; the final genre and story remain open.

## Start here in every work conversation

1. Read [repository working instructions](AGENTS.md), this overview and the latest commits on the default branch.
2. Read the relevant component dossier and its latest asset/version references. The [FMP Work Thread](docs/FMP_WORK_THREAD.md) is a chronological record, not a complete current task list.
3. Continue an unfinished production gate using existing assets and tools. Record what changed, what was checked, and the next actionable step.

**Status reviewed: 2026-10-19**, including infrastructure research commit `df51c682105d9147126991a912a8b75e60f3942e`. This is a snapshot; check newer commits before acting.

## Where the project is

| Area | Available now | Remaining gate |
| --- | --- | --- |
| Theme Center | Existing integrated Trylon, Perisphere, Democracity and Helicline model; stable-ID staging copy; guest-flow v002 circulation preview | Historical opening dimensions, site registration, actual Unreal clearance/collision/navigation |
| Research inventory | 239 archived candidates recovered and compared with the 20-place starter catalog; separate source and availability records | Evidence review, classification and promotion into the live catalog; neither inventory is exhaustive |
| World construction tools | Exterior work queue, footprint massing, registration and map-digitizing tooling | Apply reviewed source measurements to actual world geometry |
| Site networks | Dated pedestrian/service-route/utility schema and source-sheet register | Acquire/review sheets, trace alignments and register them; a source lead is not a modeled pipe or road |
| Gameplay | Accepted requirements for maps, inventory, photography and reusable adventure systems | Implement and test these systems in Unreal |
| Unreal experience | Implementation direction and reference work | No validated playable five-era build, streaming, era transitions or visitor collision established by this overview |

The older Democracity web tours are proof-of-concept releases. Local mesh checks and script tests do not establish native Unreal traversal or historical accuracy.

## Current production priorities

1. Continue the [Theme Center master dossier](research/pavilions/theme_center/README.md) and [guest-flow v002](research/pavilions/theme_center/THEME_CENTER_GUEST_FLOW_V002.md). Preserve original source/print shells; keep runtime openings and optional cutter guides separate.
2. Obtain and review dated plans and control measurements. Resolve architectural openings and site registration with recorded uncertainty and residuals. Do not invent coordinates or substitute modern terrain for historical grading.
3. Import the appropriate working assembly into Unreal when the engine environment is available; check scale, player clearance, collision and the full visitor route. Record the build and actual results.
4. Advance source-supported exterior work, including the RCA pavilion evidence register, while blocked source acquisitions remain explicit. Extend dated paths, landscape and infrastructure from reviewed evidence.

Priorities are dependency-aware: do useful unblocked world work rather than repeatedly creating new planning frameworks.

## Gameplay flexibility

Keep **world data**, **reusable gameplay systems** and **experience-specific rules** separate. Preserve stable object IDs, era/branch identity, interaction points and saveable state as the world develops.

- Custom full map and minimap inspired by Fortnite/GTA: player position/facing, landmarks, zoom/pan, waypoints and routes.
- Inventory for tickets, tools and documents; camera capture and a photo album.
- Reusable inspect, use, collect and puzzle interactions, independent of click, verb-menu or proximity controls.
- Support for approaches inspired by Myst, The 7th Guest, Return to Zork, Sierra adventures, Indiana Jones and the Fate of Atlantis, and Assassin's Creed historical exploration.

These are capabilities to preserve and implement, not a decision to combine every reference into one game. Engine physics and navigation supply foundations that still need configuration and project-specific rules. See [accepted world-first requirements](docs/WORLD_FIRST_GAMEPLAY_REQUIREMENTS.md) and [Unreal implementation](docs/UNREAL_IMPLEMENTATION.md).

## Scope and evidence

Inventory documented buildings, exhibits, landscape, entrances, plazas, roads, transit, parking and adjoining context. Distinguish verified, inferred, proposed, provisional and interpretive work. Record source, date/revision, rights and uncertainty for measurements and claims.

Historical baseline: **1939 / 1940 / 1964 / 1965 / 2026**, with distinct terrain and year-specific presence. Optional futures are **two proposed branches**, NEW_FAIR and DECLINE, each at 2039 and 2064: four scene states, not four branches. They are not historical evidence or locked canon. See [future timelines](docs/FUTURE_TIMELINES.md).

Potential later expansion beyond Flushing Meadows is outside the current proof-of-concept scope.

## Working references

- [Catalog/database](database/README.md) and [inventory reconciliation](docs/INVENTORY_RECONCILIATION.md)
- [Historical research rules](docs/RESEARCH_RULES.md) and [geospatial standard](docs/GEOSPATIAL_STANDARD.md)
- [Theme Center staging](docs/THEME_CENTER_STAGING.md) and [registration](docs/THEME_CENTER_REGISTRATION.md)
- [Footprint massing](docs/FOOTPRINT_MASSING.md)
- [Site network source sheets](catalog/site_network_sheets.csv) and [dated network schema](database/migrations/015_dated_site_networks.sql)
- [Building evidence register](catalog/building_evidence.csv)
- [Milestones](docs/MILESTONES.md) and [archive policy](docs/ARCHIVE_POLICY.md)

## Local catalog checks

The catalog tools require Python 3.10+ with no third-party packages. Other tools have their own dependencies and asset requirements; consult their documentation.

```bash
python tools/validate_catalog.py
python tools/build_db.py --output out/flushing_meadows.sqlite
```

SQLite and generated queues are derived working indexes. Maintain authoritative text inputs, SQL migrations and manifests. Run checks relevant to the actual change; report the exact scope rather than presenting a partial test run as repository-wide validation.

## Preservation and continuity

Git holds decisions, source records, code and asset references. [Google Drive project archive](https://drive.google.com/drive/folders/11aRetkT2qaA69j8jnRyqxCJu2sR7DAPk) holds large models, releases, scans and GIS datasets. Preserve stable links, versions, SHA-256 hashes and rights notes. Use Git LFS for selected binary assets; omit transient Unreal caches and generated databases.

[Research Snapshot v1.0.0](https://drive.google.com/file/d/1t5XpdiUC27QTL0928cQloJdRUSkGeAHj/view) contains the older 59-target / 66-source 1939–1940 research database, 45-row plan register and uncompiled Unreal reference code. It remains an archived seed, not an exhaustive five-era authority. See [snapshot manifest](archive/research_snapshots.csv).

Repository: https://github.com/cameronprops/TheFlushingMeadowProject  
The URL uses **Meadow** singular; the public project name uses **Meadows**.
