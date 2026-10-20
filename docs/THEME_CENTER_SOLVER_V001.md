# Theme Center mathematical truth solver v0.1

Runtime assembled model is **v005**, not replaced by this audit. Solver applies to the existing scene as a numerical/provenance overlay.

- Complete source/model references, frozen BIM-ready workbook, source builder and optional analytic comparison GLB: [solver package on project Drive](https://drive.google.com/file/d/1lVtPOlNAyZWt-IEnroNxEqAk-QmPi_IT/view).
- Bundle SHA-256: `e32a683127e2dc248832ba1065402d5224d0089a63e6471577b7e8b34963e0f2`.
- Source workbook SHA-256: `ae7a3f3443e0966e9d1acbb7fc4e8c406328eab80b99976a18f9b1d036c54acb`.
- 68 fact source records (no provisional final code drives); 60 unique registry-backed element records; 12 local regression tests PASS.
- Existing v005 assembled runtime SHA-256: `de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439`.
- Helix centerline and bridge elevations remain genuinely underdetermined. No automatic 270° sweep and no 52/64-ft entrance elevation promotion.
- Wolfram independent results: height partition 610 - 480 = 130 ft, sphere radius 90 ft, conditional center Z 107 ft relative to pool; ring-circle possible shell intersections only a geometric thought experiment, not accepted ring Z.
- Game Development Studio CLI unavailable in this runtime. No game-dev validation receipt, canonical asset package, native Unreal import, or runtime collision proof.

Run from the repo's `tools/theme_center_constraints` directory:

```bash
python3 -m unittest discover -s tests -v
python3 src/fmp_theme_solver.py --out output
```

Requires Python 3.9+ standard library. Only optional analytic GLB uses `trimesh`. The archive's source workbook is available as read-only original; repository contains the frozen fact JSON plus pinned hash, not a duplicated binary workbook.

**Next production gate:** compare v005 assembled mesh against constraint overlay, retaining Y-up/metres source basis; evaluate 1939 openings and visitor clearance in actual Unreal when available. Verify historical source plan and control coordinates before georeferencing.
