# WF0028 v012: width-aware courtyard route screening

Date: 2026-10-20. Tested against v011 interpretive model without changing geometry.

- Six of six route segments passed 13 lateral floor samples across a 0.9 m wide corridor at 0.05 m longitudinal spacing.
- Unsupported support samples: **zero**. Conservative 2.5D obstacle hits: **zero**.
- Collision method: continuous XY swept 0.45m-radius pedestrian footprint versus transformed mesh AABBs; Z elevation range filtered using full 1.8m body height. The sloped ramps use interpolated surface elevations, not ramp upper bounding boxes.
- Five executable local regression tests passed, including explicit non-certification checks.
- The technique is *not* an exact 3D swept-capsule triangle mesh collision test, continuous full-width floor polygon proof, Unreal NavMesh, site registration, or historical drawing verification. No as-built qualification.
- Package: `WF0028_1939_FullWidth_Audit_v012.zip` SHA256 `5c89bf67e12e799c4ffdfb9b750910c294d353d6dcf6d97865471ba1aa6572db`; includes prior generators, GLB, manifest, audit script and test evidence.

Next: source-based facade and interior reconstruction. Route is ready **for native Unreal validation**, not certified until that test.
