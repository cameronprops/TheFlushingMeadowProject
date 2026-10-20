# WF0028 v006: executable alternate-route planning stage

2026-10-20. The v005 geometry report recorded 9 blocked / 5 no-hit route links
(14 total) for a 0.45 m-radius, 1.8 m-tall pedestrian proxy.
That report remains authoritative until a new geometry run is completed.

New source:
- `tools/world_build/plan_wf0028_alternate_routes.py`: 8-connected
  metric-grid A* candidate route finder with a default 0.25 m cell and
  configurable 0.45 m radial clearance around axis-aligned obstacles.
  It forbids corner-cutting around diagonally adjacent wall corners and
  reports endpoint blockage versus no available candidate.
- `tools/world_build/test_plan_wf0028_alternate_routes.py`:
  four tests for open space, blocked endpoint, impassable cross-wall and
  detour around a finite obstacle. **Not executed in this session**.

Input is a JSON object with `bounds`, `obstacles` and `routes` arrays.
An obstacle must have `id` and local XY `bounds=[xmin,ymin,xmax,ymax]`.
A route must have `id`, `start=[x,y]` and `goal=[x,y]`.
To use against WF0028, extract all collidable AABBs from v004 geometry
that vertically intersect the walker interval. Do not feed visual route
markers, vegetation art or non-collidable guides into the obstacle set;
include sidewalls, partition walls and physical exhibits.

No corridor, doorway, exhibit or wall coordinates were changed here.
The planner creates **possible rerouting candidates**, not architecture.
A proposed route cannot be certified until continuous world collision,
floor/threshold elevation and Unreal NavMesh all pass.
If there is no candidate, preserve failure and record which speculative
barriers would need repositioning in a separate variant. Do not alter
verified historic objects to force a test pass.

Run from project root:
`python3 tools/world_build/plan_wf0028_alternate_routes.py INPUT.json OUTPUT.json`
`python3 -m unittest discover -s tools/world_build -p test_plan_wf0028_alternate_routes.py`

Blocker: local v005 ZIP/runtime not accessible in this execution, so the
previous 14 edges were not rerun against new candidate routes and no v006
GLB was produced. This is a committed planning-tool increment rather
than a completed geometry correction.
