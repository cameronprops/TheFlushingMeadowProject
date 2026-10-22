# v008 stair-run support inspection

Read-only inspection of the exact v008 GLB (SHA256 aefc8b0a83c5e8264b936151a13cb5f7190e69d9e55c28a5141ce84c0fced867). No model changes.

375/375 vertical support probes reach the expected surface height: 15 points on each of 23 treads, plus 15 points at each of 0.10 m and 0.50 m beyond the final tread. Tread samples span lateral offsets -0.75 to +0.75 m and longitudinal offsets -0.10, 0, +0.10 m from each tread centre. Bridge samples span -0.875 to +0.875 m. Actual mesh going is 0.296622 m. Wolfram independently calculates nominal rise 0.159026 m, going 0.296622 m and slope 28.196819 degrees. These values describe the provisional model, not historical or regulatory compliance.

The script hashes its input, evaluates active world-transformed scene triangles and records hit node, hit elevation and error for every probe. Origins are 50 mm above expected surfaces; it does not detect obstacles above those origins. This is discrete floor support, not headroom, swept body collision, edge/riser continuity, structural engineering or native Unreal movement. Do not call this complete traversal. Game Development Studio CLI is unavailable; local Trimesh performed the inspection. The next unresolved production check is body/head clearance along the stair and its turns, followed by native engine movement.

Reproduce with Python, numpy, trimesh, scipy and rtree:
`python check_stair_run.py /path/to/ThemeCenter_UpperLanding_v008.glb stair_support.json`

The input is available in [v008 complete scene](https://drive.google.com/file/d/14X-Jp_tt8PfbNNy0F3TpBFkuKbJM5eGO/view). The script exits nonzero if a sampled support check fails. Current code, report, Wolfram receipt and this note are archived as individual text files in GitHub and project Drive. The prior mesh/ZIP binary Git-copy blockers and verbatim transcript backfill remain open.
