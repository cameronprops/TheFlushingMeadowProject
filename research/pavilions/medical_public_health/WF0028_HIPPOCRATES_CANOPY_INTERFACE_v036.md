# WF0028 v036 — curved Hippocrates entrance canopy connection

Status **IMPLEMENTED / LOCALLY TESTED / INTERPRETIVE ONLY**. v035's 8m-wide rectangular canopy had a straight rear edge, producing variable overlap/gaps against its bowed wall. Replaced that one component with 32 individually editable watertight extruded quadrilateral strips following the existing v035 curve. Unmodified v035 master remains retained.

Local model parameters inherited from v035 (all **unmeasured**): frontage 18m, bow 1.1m, canopy width 8m, projection 1.5m, height 3.9m, thickness 0.22m, facade wall thickness 0.27m. Corrected canopy back edge is 0.20m behind existing mathematical wall centerline, yielding **0.065m nominal overlap beyond assumed inner face** across canopy width. Each segment is watertight; segments only touch at planar seams and are **not boolean-unioned**. Contact QA is mathematical/model-local, not a historical engineering check.

Verification in local scene: 37 unaffected original nodes preserved, 1 old CANOPY removed, 32 new segment nodes, 69 resulting GLB nodes; all components watertight; GLB export/reimport retained 69 nodes; ZIP CRC passed. No real historic drawing scan or camera solve used; no relief, stairs or threshold added.

**Package**: `WF0028_Hippocrates_Canopy_Connection_v036.zip` 261172 bytes, SHA256 `a9bd19ade76d9968bd00fcdce0de86d70b935a22a547901759ca71cc23939d14`. Contains original v035 GLB and source generator, complete local v036 script, corrected GLB, model-derived PNG/PDF and QA JSON. The reproducible standalone correction source is `tools/world_build/wf0028_canopy_fix_v036.py` (extract original GLB beside script). The archived complete script additionally plots and packages outputs.

The corrected model is an isolated study and does **not** modify main WF0028 shell or claim 1939 measurements. Historical source: `WF0028_HIPPOCRATES_FACADE_OBSERVATIONS_v034.md`. GitHub binary mirror for the GLB/ZIP remains pending unless a release or LFS file exists.
