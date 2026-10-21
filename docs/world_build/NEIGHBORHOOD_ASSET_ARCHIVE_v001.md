# FMP 1939 neighborhood partition v001

Neighborhood grouping is for **asset organization and production**, not a verified geographic polygon subdivision. Names and membership should be checked against period fair plans. Do not read row order as distance or location. Site transforms and footprint registration remain unverified.

## Index
- `catalog/1939_neighborhoods_v001.csv`: the four organizational districts.
- `catalog/1939_neighborhood_buildings_v001.csv`: building memberships and stable IDs where already assigned.
- `catalog/1939_neighborhood_asset_manifest_v001.csv`: catalog of local floorplan images, renders and archived model packages with SHA256 digests.
- Existing catalogs `places.csv`, `site_network_*.csv`, `theme_center_neighbor_*.csv` remain authoritative for identities and source evidence.

## File arrangement
Each building keeps its own research sources in `research/pavilions/<building>/`, with the neighborhood index pointing to them. Git stores human-readable maps, catalogs, architecture notes, reproducible source scripts; binary floorplan PNGs, GLBs, and ZIP packages are mirrored to Drive when upload succeeds. Keep each iteration and distinguish historical source scans from conjectural 3D model screenshots. Never overwrite a dated state with a different era.

## Current archive
The current local archive comprises **17 local assets**: 3 RCA schematic images, 1 WF0028 model-derived floorplan PNG, and 13 WF0028 versioned ZIP packages. Note: archive coverage is limited to assets accessible in the conversation container; it is **not** a complete inventory of all the project Drive's master assets, nor does it include the physically held original blueprint scans. RCA floorplan is a fresh interpretive schematic, **not the original RCA GLB**.

The recent Git records for WF0028 go beyond v014, through v019 facade/material work; this archive intentionally retains only binary files available locally today. Incorporate higher revisions after verifying corresponding files and checksum.

No georeferenced placement, Unreal collision qualification, or historical architectural accuracy is implied by archiving.
