# Actual passage renders, scenic winding repair and WF0028 export filtering

2026-10-20. [Complete reproducible package, inputs, outputs and five actual-mesh renders](https://drive.google.com/file/d/1ofasHEQ3b9sQoqWM6rSGoQ7VVKZKqkYc/view).

[Code and reproduction instructions](../../../tools/asset_fixes_234/README.md).

Three Trylon views show the current passage, with retained and provisional parts differentiated. The cutaway explicitly hides the shell; exterior views retain it. The opening exists, but cut brace ends and rail returns remain unfinished. No architectural repairs to the passage are claimed.

Five scenic meshes received 1,898 face orientation reversals and regenerated normals in a separate derivative. Original binary data, positions, IDs, materials and node transforms preserved. Six regression tests pass. No native Unreal testing.

WF0028 v015 runtime export removes 37 diagnostic/reference/zone/proxy mesh records, retaining 46 modeled components. Unknown kinds, wrong hashes and unregistered meshes fail closed. The concurrent v016 reference-only flags are covered synthetically; its actual artifact was not processed. Use this filter explicitly for runtime export; the unfiltered research masters remain unchanged.

```json
{
  "source": "v005 unchanged",
  "repair": "five meshes; 1898 reversed triangle orientations; normals regenerated only on those five meshes",
  "filter": {
    "input_version": "v015",
    "excluded": 37,
    "retained": 46,
    "v016": "reference-only flags tested synthetically; actual v016 artifact not processed"
  },
  "tests": "6 regression tests",
  "renders": "five deterministic EGL/Pyrender actual-mesh views; diagnostic material overrides, local clipping and explicitly labeled shell-hidden cutaway",
  "limits": [
    "Brace ends and rail returns remain architecturally unfinished",
    "No Unreal import or traversal validation",
    "Winding consistency does not establish outward orientation of all disconnected open surfaces",
    "Historical accuracy not inferred from rendering"
  ]
}
```
