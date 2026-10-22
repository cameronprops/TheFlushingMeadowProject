# Theme Center v004: shared runtime openings

This revision fixes the preview passage, not the historical structural design.

The master workbook's K031/K032 rules require one aperture definition to control
structure and skin separately. E003/P011 also require the portal to interrupt
bracing. The September truth/math audits leave exact bay elevations, portal
sizes, bridge placement and rail geometry unresolved. The previous workflow
incorrectly treated the uninterrupted preview frame as an immutable obstruction.

## What changed

Two shared, explicitly provisional opening volumes are applied to derivative
copies of Trylon_Face_3_Frame, Trylon_Hollow_Exterior and Helicline_Rail_-1.
Two brace components and four rail components are locally cut with closed Boolean
results. The shell loses no meaningful volume because its openings already clear
these envelopes. No primary leg is modified. Original GLB/print bytes are preserved.
Each opening is 2.4 m wide by 2.4 m high, with 3.4 m cutter depth. These are
runtime topology-test parameters, NOT dimensions recovered from historic drawings.
The remaining disconnected brace ends are NOT an engineered portal transfer frame.
The rail gap still needs proper return/edge-protection design.

## Use

Load ThemeCenter_1939_GuestFlow_Trim_v004.glb instead of the v003 overlay.
In the visitor view only, hide the five source nodes listed in Shared_Portals_v004.json.
The corresponding three new replacement meshes are in the overlay. Never apply
this visibility recipe to print/export originals. The model remains Y-up metres,
local and not site-registered. Native Unreal validation has not been run.

## Verification

The identical four-segment return route now has zero sampled surface contacts
across 435 body poses. Body assumption: radius 0.3 m, height 1.8 m, feet raised
0.05 m. The new meshes participate in collision screening; this is not merely
hiding the obstacles. Eight focused tests pass. Sampled clearance does not establish
continuous motion, solid containment, complete visitor-route traversal or safety.

Reproduce from repository root (Python, numpy, trimesh and manifold3d):

```bash
python -m tools.world_build.build_shared_portals_v004 SOURCE.glb V003.glb OUT
```

Run the existing clearance audit from Python with the new overlay SHA recorded in
the manifest and extra_hidden set to the builder's REPLACED tuple. Retain source
hash verification. Audit report records the exact visibility set. Run the artifact
checks with FMP_V004_DIR=OUT and python -m unittest -v
 tools.world_build.test_shared_portals_v004 tools.world_build.test_transition_clearance.

## Source reconciliation

Master workbook: https://drive.google.com/file/d/1YnjHL9NIw7_jGvLc7Cs4-AUXcLnWKEgN/view
Truth audit: https://drive.google.com/file/d/1IWHAdUS_prVnM71ErlFOcSrdSAaYAIuc/view
Math audit: https://drive.google.com/file/d/1LC5vECuII2wUCV9L5xcXDqHon96bwBr3/view
Read 2026-10-19 local date. These establish project modeling rules and unknowns;
they do not verify the new aperture dimensions. Period drawing acquisition remains
open. Do not relabel this revision historically verified.

Next: import the integrated visitor assembly into Unreal and test full-route
movement with the actual character. Separately reconcile portal transfer framing
and guard details from architectural evidence. Do not repeat the completed local
reroute search as if it could repair missing portal topology.
