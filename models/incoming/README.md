# FMP incoming model folder

GLB source files can be copied or synced here from local work or Google Drive. They are not required to be committed to GitHub.

A model is **not** silently assigned to a pavilion. Register it by copying the relevant `.fmp-model.json.template` to the same filename without `.template`, and point its `glb` at the actual GLB file.

You may register multiple buildings in the same source model—for example, Trylon and Perisphere—using distinct manifest files and explicit `nodes` lists. The importer only measures selected source nodes for each building.

### Trylon example
1. Put `FMP_ThemeCenter_Staging_v001.glb` in this folder (or edit `glb` to a local relative path).
2. Rename `trylon.fmp-model.json.template` → `trylon.fmp-model.json`.
3. Optional: similarly register Perisphere against the same original GLB using the Perisphere template.
4. From the repository root, run `python3 tools/sync_master_database.py --once`.

For continuous development, run `python3 tools/sync_master_database.py --watch --interval 4` and leave that command active. Saving the registered GLB with new bytes will cause a new asset revision, updated mesh component records, then a full SQLite/dossier refresh. Source GLBs remain untouched.

**Not automatic:** Google Drive folder changes outside this local directory, Rhino or Unreal exports that never reach the registered file, historical site registration, mesh repair, Unreal collision, print-wall thickness, and uploads to remote storage.

Use an `asset_uri` only if it really points to that exact model revision. The default is blank so the database does not claim that a local GLB is already on Google Drive. Do not use the same `role` more than once for a building and year: each building/year/role has only one active revision.

Installing Python dependencies: `pip install numpy trimesh` (other database tools are Python standard library). See `docs/buildings/AUTOMATIC_MODEL_REFRESH_v002.md`.
