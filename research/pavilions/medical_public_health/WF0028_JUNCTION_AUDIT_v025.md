# WF0028 v025 — actual scene junction audit

Date: 2026-10-22. Read 187-node v024 GLB using trimesh; geometry-derived model-local bounds and orthographic plan. No geometry modified. Not historical survey, merely a test of internal consistency.

## Results
- v024 courtyard hypothetical chord y=20.0 m, connector south wall starts y=22.5 m: 2.5 m separation.
- v024 nominal left return tip reaches y=21.4 m: 1.1 m gap to connector. The result is an axis-aligned measurement, **not** a complete 3D wall-clearance certification.
- Science entrance curve is centered around y=-1.0 m, while existing south facade sits at y=-12.0 m: 11.0 m inward offset in the model.
- Entrance curve x extent is 23..35 m; current Science south doorway x=40.2..43.8m, leaving 5.2m horizontal mismatch.
- Five curve families are retained only as reference/no-collision studies. No wall intersection, doorway, roof or interior partition alteration justified.
- Model node count: 187. v024 architectural origin v004 is interpretive.

Outputs: `WF0028_Junction_Audit_v025.zip`, SHA256 `9b3dde15fd0ddaa387b005c0382b83b8cdc683a7eecbcbf3d04a65edc5899016` with `junction_audit_plan.png`, `junction_audit_plan.pdf`, `component_bounds.csv`, `junction_audit.json`, and `README.md`. ZIP CRC checked. The CSV lists actual scene node AABBs as extracted.

**Next:** do not fabricate arbitrary end returns to bridge gaps. Obtain usable historical plan and facade photographic controls and only then solve for location, orientation, height and a curved vs. sculptural-feature distinction. Add residual metrics and original evidence coordinates. No historical dimensions verified, and no Unreal runtime tests.
