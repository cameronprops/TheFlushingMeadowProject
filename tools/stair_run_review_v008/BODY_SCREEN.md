# v008 stair body surface inspection

Status: no nonwalking contacts at sampled poses; stair contacts require engine testing. No geometry changed.

Input: `ThemeCenter_UpperLanding_v008.glb`, SHA-256 `aefc8b0a83c5e8264b936151a13cb5f7190e69d9e55c28a5141ce84c0fced867`.

The checker samples 23 tread centres on three lateral tracks and 17 positions on each straight landing-turn segment: 103 poses, 1,339 sphere centres. Nominal body diameter is 0.6 m and height 1.8 m, lifted 0.05 m above each reference tread. Sphere centres span 0.35 through 1.55 m above the reference surface at 0.1 m spacing. Radius sqrt(0.3^2 + 0.05^2) = 0.304138126514911 m conservatively covers the capsule between centres. Wolfram Language independently evaluated this formula as 0.30413812651491098444998421226010335311 (18-digit precision).

Results: zero nonwalking surface contacts and 69 walking surface contacts, all at the lowest sphere centre (0.35 m). Walking labels classify contacts; they do not suppress them. The reported head-sphere margin is 0.33238 m to INTERPRETIVE_UPPER_EXIT_HANDRAIL_R among broad-phase candidate meshes. This is a surface-distance diagnostic, not vertical overhead clearance or a global nearest-surface measurement.

Reproduce with Python, NumPy, trimesh (run used 5.1.1), scipy and rtree:

```sh
python check_body.py ThemeCenter_UpperLanding_v008.glb body_screen.json
```

The script exits normally after producing an inspection report; exit status is not traversal acceptance. This is discrete surface testing, without continuous sweeps, solid containment, native Unreal collision, navigation or step handling. Landing paths are sampled straight segments, not validated curved movement. Historical geometry remains provisional/interpretive. The game-dev executable was unavailable in this environment.

Next production gate: import v008 into Unreal, configure the actual pawn capsule and stair step handling, and traverse both directions through both turns while recording collisions. Resolve the retained stair contacts there before accepting movement. Full verbatim conversation export remains unavailable. Prior GLB/binary Git archive gaps remain GIT_BINARY_PENDING.
