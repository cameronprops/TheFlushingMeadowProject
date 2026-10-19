# Unreal open world architecture

Target is a large, geographically coherent world covering the park, both fairs, relevant adjoining street blocks and all connected transportation access.

## Game state
- Persistent subway-station hub containing a time-travel gate.
- Five states: **1939, 1940, 1964, 1965, 2026**.
- First-person walking and third-person character camera; same collision capsule and actual navigable surfaces.
- Interactable exhibit controllers that can load local show scenes, live actors/animatronic simulations and ride systems.
- Multiple detail levels: overhead fair panorama, walkable streets, pavilion exterior, interior exhibits.

## Streaming
- World Partition and spatial streaming for geography.
- Period-specific Data Layers or separately loaded levels for buildings, grading, transit and vegetation.
- Shared source catalog but **not** shared geometry when an era's physical structure changed.
- Avoid loading the five full parks or immersive 100× Democracity simultaneously.
- Use HLOD/instancing/occlusion and collision LODs at distance.

## Prototype acceptance
1. 1st/3rd person toggle works in a real PIE build.
2. Subway portal switches eras while preserving a source-controlled world-space reference.
3. All year changes including Sparko (1940) respond to verified era metadata.
4. Stairs, ramps, Trylon entrance, bridge, Helicline and ride paths pass capsule/camera collision checks, including steep grades.
5. Real landscape and waterline provenance recorded; no visible seams.
6. Source-backed pavilion geometry can replace interpretive shells without losing location or version lineage.
7. Automated catalog QA and manual Unreal frame-time/streaming and reproducibility logs.

Previous \`WorldFair1939\` C++ prototype is an **uncompiled reference scaffold**; it is not a verified Unreal Engine build. The web walkthrough is a separate earlier play test.
