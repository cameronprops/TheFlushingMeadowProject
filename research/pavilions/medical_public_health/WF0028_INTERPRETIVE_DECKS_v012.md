# WF0028 v012 simulated walking-deck overlay

Generated 2026-10-20 from v010 GLB and v011 audit. Separate interpretive alternate; no historical master overwritten.

- Preserved 173 existing v010 scene nodes and added 277 independent watertight simulated 2.2 m wide deck strips along six routes that failed the v011 full-body screen. Deck datum assumed local Z=0; this may conflict with other floors.
- New v012 GLB SHA256: `f6812b7b36451d152314d98af9087c08daf0e8b22912cd187c51d8d52f410744`.
- Package SHA256: `4f00340e0cfef4dbcc77becf3247c2196cb2686513eb8872ce5175aef0280641`.
- Prior v011 seven regression tests executed successfully and the v012 generator asserts existing scene-node preservation and watertight added strips. These checks DO NOT represent repaired full-body traversal tests.
- Decks are `SIMULATED`, not physically verified or sourced from the 1939 plans. The mesh contains seams and overlapping or vertically inconsistent authored floors; Unreal NavMesh not run.
- Six affected links: both street approaches, two Medical courtyard approaches, west courtyard crossing and east courtyard-to-Science crossing.
- Binary and generator generated as `WF0028_1939_Interpretive_Decks_v012.zip` in ChatGPT artifacts.

Next gate: oriented floor polygon tests at the pedestrian radius, continuity at grade changes, physical colliders/wall contacts and native Unreal walkthrough, with a conservative fail rather than declaring all 14 links traversable.
