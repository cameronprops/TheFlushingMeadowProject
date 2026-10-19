# Theme Center working assembly v0.0.1

Recovered the existing v0.9.2 integrated model from Drive and prepared a metadata-only
working copy. This preserves the earlier geometry rather than rebuilding a blockout.

- 510 scene nodes, including 501 mesh-bearing nodes.
- Persistent UUIDs assigned to all nodes, recorded in a companion manifest.
- Component labels cover grounds/fixtures, Perisphere, Trylon, circulation,
  Helicline, Democracity, provisional exit stair, concept approach and viewing decks.
- Links to catalog place IDs are assigned only at the component-group level.
- No coordinates, vertex buffers, topology, materials, animations or transforms changed.

Files:
- [Working GLB](https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view)
- [Object manifest](https://drive.google.com/file/d/1oPWka59qenBOSiPEE3VLxgqXMjsyRBTh/view)
- [Original v0.9.2 GLB](https://drive.google.com/file/d/1S-fMjZlzHSAo_H-8bp4YT9Iqw8nS2vlI/view)
- [Original release notes](https://drive.google.com/file/d/1HzqV9lQQjOGY8YyJujWMC0DopYnGQJzl/view)

Reproduce with Python 3:

```bash
python tools/prepare_theme_center_v092.py source.glb out/theme_center
```

The migration requires the exact inspected source SHA-256. It refuses other
versions because the reviewed component mapping is specific to this scene layout.
Once assigned, IDs must be retained through subsequent revisions; do not rerun a
node-index identity scheme against reordered geometry. The manifest provides a
fallback if an engine importer drops glTF extras. Importer support is not assumed.

Validation performed on the actual file: header length and format; unique IDs;
exact equality of all non-FMP JSON after stripping the added metadata; byte-for-byte
equality of every binary chunk. Repeated migration produced the same output hash.
This is preservation QA, not geometric correctness or collision certification.

Source SHA-256: 2b82e39f388cdae1e182472b337b554df80baddfd1c3b61d8ed1876c2da56aac

Output SHA-256: a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5

Inherited limitations: the west Trylon opening is a provisional clearance cut;
the stair, circulation and site placement need further validation. The scene is
not survey-registered. Historical year presence remains review-required. glTF's
metre/Y-up convention is retained without an engine axis or scale conversion.
No Unreal import, gameplay implementation or body-volume collision test occurred.

Next: import this preserved assembly into the Unreal test level and verify scale,
orientation, node identity retention and player-sized passage along the existing
route. Keep changes to historical geometry separate from clearance experiments.
