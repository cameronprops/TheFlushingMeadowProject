# Footprint-to-massing stage

The next world-construction tool converts explicit local-metre footprint polygons
into closed triangular OBJ masses. IDs, year, source references, evidence status,
area and volume are written to a companion manifest. OBJ itself is unitless;
the manifest declares metres and Z-up. Confirm importer scale/orientation before
using the mesh in Unreal. No Unreal import or collision test was performed here.

Run:

```bash
python tools/build_footprint_massing.py reviewed_footprints.json --output-dir out/massing
```

Input structure, shown with an explicitly synthetic example:

```json
{
  "units": "m",
  "coordinate_status": "UNREGISTERED_LOCAL",
  "objects": [{
    "id": "SYNTHETIC_TEST",
    "year": 1939,
    "footprint": [[0,0],[4,0],[4,3],[0,3]],
    "base_z": 2,
    "height": 5,
    "evidence_status": "PROVISIONAL",
    "source_refs": []
  }]
}
```

There are no default historical dimensions, elevations or placements. A registered
coordinate declaration requires a registration reference; source-backed geometry
requires references. These presence checks do not verify the underlying evidence.

Current scope: simple strictly convex footprints, flat bases and roofs, one height
per mass. Concave shapes, holes and curved roofs are rejected or require a different
modeling workflow. Preserve distinct component IDs when subdividing a complex
building. A closed mass is not an accessible interior or a finished collision mesh.

Validation: four new tests check manifold edge pairing, outward orientation and
signed volume, clockwise/closed input rings, invalid geometry, evidence metadata,
duplicate identities and missing registration references. All 21 tests in this
thread's local test set pass. Other recently added repository test suites were
not downloaded or run in this increment.

Next input: traced and reviewed footprints with explicit height/base evidence or
provisional labels. No historical building model was generated in this increment;
the synthetic example is solely a geometry test, not a representation of the fair.
