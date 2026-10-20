# WF0028 v016: curved courtyard facade study, integrity gated

2026-10-20. Generated actual reversible interpretive GLB (99 parts) from restored v015 archive.

- Preserved all **83 existing v015 components**, including vertices/transforms. 16 new individually editable tangent-segment facade witness meshes.
- Curvature: hypothetical 19 m radius, 110° arc, 16 panels, 6 m high. **No historical source calibration for these dimensions or position**; not merged into historical wall geometry.
- All 16 source-independent witness meshes are watertight and flagged `REFERENCE_ONLY_NO_COLLISION` / `excluded_from_runtime_collisions: true`. Importers MUST exclude these from collision and navigation. These are visual studies, not operational walls.
- **62/62 local Python unittest cases passed**, including 7 new ones. Upstream release integrity guard **17/17 required files** passed. GLB SHA256: `51150c7f02385ae77af226c1e325ab5d36f956d7417c5b675dedcc3d80d3521a`.
- Release ZIP SHA256: `4a528d58e0a6191bafc296a576cee1f9f1b83447803bda9ac4c51b10d3558f9d`.
- No source-qualified curved elevation, comparison to calibrated historical camera, as-built facade height, or Unreal NavMesh certification. Known archival and engine validation gates remain open.

Full package contains all dependencies, `build_wf0028_v016.py`, `test_wf0028_v016.py`, v016 GLB/JSON and preceding builder/audit/test chain. Run `python build_wf0028_v016.py`, `python check_release_dependencies_v015.py`, `python -m unittest discover -p 'test*.py'` from extracted `wf0028` folder.

**Next:** perform calibrated facade silhouette comparison from source photos, then revise radius/arc and height as warranted. Do not mark current arbitrary 19 m radius as measured.
