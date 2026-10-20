# Runtime diagnostic exclusion

2026-10-20. [Implementation and reproduction](../../../tools/asset_fixes_234/README.md). [Complete tested package](https://drive.google.com/file/d/1ofasHEQ3b9sQoqWM6rSGoQ7VVKZKqkYc/view).

Actual v015 GLB export removes 37 diagnostic/reference/zone/proxy mesh records and preserves 46 modeled components. Node identities and retained geometry remain unchanged; diagnostic nodes no longer reference a mesh. The facade height study, artwork scale witnesses, route markers, unlocated proxies and zone overlays cannot render through the active scene. Collision builders must consume active scene meshes.

Six bounded regression tests across this export and Theme Center repair pass. The filter rejects unknown component kinds, wrong source hashes and unregistered mesh nodes. v016 reference-only flags are tested synthetically; actual v016 bytes were not processed. This is an explicit runtime-export command, not an automatic modification of existing builder outputs. Research masters are unchanged; no Unreal collision/nav certification.
