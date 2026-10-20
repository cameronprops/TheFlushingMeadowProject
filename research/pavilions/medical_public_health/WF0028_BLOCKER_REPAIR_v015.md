# WF0028 v015: block repair + facade reference alternative

2026-10-20. **Release blocker remediation first, incremental artwork study second.**

## Found and repaired
The v013 distribution contained builder scripts and newer GLBs but omitted the **v009 GLB/JSON pair**, despite the v010 and v011 audit scripts importing that pair from `out_wf0028_v009/`. Running all contained tests before repair produced five FileNotFoundError failures. These are **reproducibility/dependency packaging defects**, not proof that the physical courtyard has failed.

Restored both exact v009 archived upstream files into the working package. A rerun of the 50 preexisting tests reported **50 passing**. Added `check_release_dependencies_v015.py` which fails on any missing/empty required file (17 mandatory paths); the checker passed. The v015 release ZIP **contains** these upstream assets and scripts, not merely links to them.

## Facade incremental change
A separate v015 GLB adds exactly one off-building `VISUAL_ONLY_HYPOTHETICAL_FACADE` scale witness to v013's 82 components. New total **83**. Witness height is mural height (36 ft = 10.9728 m) plus an explicitly **assumed** 1 m margin: **11.9728 m**. This is neither a measured wall elevation nor approved as-built structure, and is non-colliding. The original 82 model components remain. GLB SHA-256 `7b18fcf22833e7a77c33aa73f3cbe6b5ccd052881cafab906eaac474dde2efa3`.

Five new unit tests check original component retention, count, minimum height, nonhistorical classification and exclusion from collision category. Total full regression: **55 passed**.

## Remaining gates and issues
- Architectural floor/roof dimensions and exact curved courtyard geometry unmeasured: **HISTORICAL_SOURCE_BLOCKER**, not a software bug; no source-qualified facade substitution permitted.
- Full triangle-mesh swept capsule and Unreal native nav check: **VALIDATION_PENDING**. Existing AABB/sampling passes are screening only.
- Visual witnesses must remain outside operational collision and export layers: test proxy label is explicit; check runtime export filtering when implemented.
- No real 1939 doorway positions, site registration, artwork placement, or structural roofline should be promoted.

Self-contained ZIP SHA256 `858c8cdacb5ea1174d7507b4197767216eaf89ec0061d9978faad11e7df0b0eb`. To rerun from the ZIP:
`python check_release_dependencies_v015.py`
`python -m unittest discover -p 'test*.py'`

The release artifact is an interpretive study, not the historical master scene.
