# NYPL exposed-steel image screening v001

Evidence: NYPL [Trylon and Perisphere skeleton](https://old-digitalcollections.nypl.org/items/917bd448-7f64-b36d-e040-e00a180609bd), image ID `ps_mss_cd23_351`, 605 x 760 standard derivative. Catalog date range 1935–1945; exact exposure date unresolved. Rights status undetermined, so **archival photograph bytes are not included or publicly republished**.

The Wolfram screen fits a circle to four approximate points on the Perisphere steel-skeleton silhouette and independently checks two held-out points. This is a **2D pixel-space photographic validation**, not camera calibration, truss node derivation, footing measurement, registered BREP, 1939 as-built acceptance, or an engineered structure. Extra visible lines may be temporary scaffold and erection hardware. The nonmetrical fit **cannot** certify scale by itself.

Run from the repository root:

```sh
wolframscript -file tests/test_nypl_exposed_steel_screen_v001.wl
```

Files: `tools/world_build/nypl_exposed_steel_screen_v001.wl`, `research/pavilions/theme_center/NYPL_EXPOSED_STEEL_SCREEN_v001.json`, and `tests/test_nypl_exposed_steel_screen_v001.wl`. All historical source and runtime meshes remain unchanged.

Game Development Studio: this is historical source validation only, not an authorized asset-production, normalizing, vendoring, Unreal import or renderer test. Preserve the master GLB and portal/circulation exports separately.

**Next:** establish the frame date, acquire verified engineering truss stations and a second exposed-structure photograph with known camera/landmark controls. Only then use the existing projective 3D solver to test candidate structural node placement.
