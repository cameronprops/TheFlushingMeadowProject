# WF0028 v010: actual model-space threshold and clearance audit

Date: 2026-10-20. Executed against the archived **v009 GLB**, not inferred from plan sketches.

## What was tested

Six successive access links (Medical interior, Medical side opening, courtyard west, courtyard center, courtyard east, Science side opening/interior), sampled every **0.10 metres**. The original GLB scene nodes were transformed into world-space bounding boxes. At each pedestrian-center point, the audit checks:
- the presence and top elevation of underlying floor, public walk or provisional threshold deck;
- intersection between an upright **0.45m-radius, 1.8m-tall** pedestrian body and mesh-component axis-aligned bounds;
- abrupt changes exceeding **20mm** between adjacent sampled floor top levels.

## Executed results

- **0 unsupported floor samples** along any of the six candidate links;
- **0 body-bounds intersection samples**;
- **4/6** links clear this sampled static proxy;
- **2/6** links flagged for abrupt **0.055m (55mm)** support elevation changes: Medical portal to courtyard west, and courtyard east to Science portal.
- Source v009 geometry unchanged; no new GLB produced.
- **6/6 local regression tests passed.**

## Qualification

This is a sampled, conservative **AABB-based 3D body and floor screen**, not a true continuous triangle-mesh swept capsule, physics step-up simulation, formal accessibility review or Unreal NavMesh validation. All hall locations, walls and doors are interpretive guesses, not historically traced. Floor surfaces and existing 55mm lips need architectural treatment in a subsequent reversible runtime variant, not unverified alterations to the historical master.

Archived executable package including the preserved v009 builders and GLB, v010 Python 3D audit, JSON data and six tests: [WF0028_1939_Threshold_Audit_v010.zip](https://drive.google.com/file/d/11sppI6tCvikXQkn5Ocw00_y5B2D8HprS/view?usp=drivesdk).
ZIP SHA256: `5d9b34927eac82e77ebea636d00855b84d148aaabdd364921a045df88f831a12`.

Next: design separate adjustable, speculative threshold transition surfaces (without modifying original floors), rerun support, head-clearance and continuous-collision checks; cross-check original entrance plans when available.
