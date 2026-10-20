# FMP WF0009 — RCA Building shell/source gate (1939)

## Status, 2026-10-19
**The first provisional exterior/interior shell preview has been built and tested locally (29 closed mesh components, 9/9 local tests). It is NOT an as-built RCA building.** The building's final footprint, room division, door locations, elevations, roof dimensions, skylight type, and height cannot be qualified until the original plan set is read at architectural drawing resolution.

Production focus: exterior and public interior shells for Unreal and 3D printing. Do **not** spend project time reconstructing steel unless archival evidence and a particular optional construction-animation require it.

## The source corpus / original drawings to request
Holding: Cret Collection, [Athenaeum of Philadelphia work 351 (CRE351)](https://www.americanbuildings.org/pab/app/ho_display.cfm/56239). Paul Philippe Cret with Skidmore, Owings & Merrill; records dated 1937–1938; 12 sheets listed (13 digital gallery images).

Priority originals, newest known versions first:
- CRE351-001 — 1st Floor Plan & Details, April 11 1938. **Required for footprint/entrances/room outline.**
- CRE351-002 — 2nd Floor Plan & Details, April 11 1938.
- CRE351-003 — Roof Plan, April 11 1938. **Required for projecting roof mass/central circular feature.**
- CRE351-004 — Elevations, April 11 1938.
- CRE351-005 — Sections, April 11 1938. **Required for height and walkable volumes.**
- CRE351-006 — Details, April 11 1938.
- CRE351-007 — Wall Sections, April 11 1938.
- CRE351-008 — Grading & Layout Plan, March 3 1938. **Source for future fair-wide path graph entrance connections.**
- CRE351-SK1 — Ground Floor Plan / West Elevation, February 11 1938.
- CRE351-001.02 / 002.02 / 003.02 / 004.02 — preliminary 1937 plans/elevations and revised plan evolution. The 1937 alternative dimensions must never drive the assumed final 1939 shell without checking revision.
- Source photo: [Smithsonian Sarnoff at pavilion April 1939](https://www.si.edu/object/david-sarnoff-1891-1971-front-tv-cameras-1939-worlds-fair%3Asiris_arc_367592) and [period postcard](https://www.cardcow.com/601230/radio-corporation-america-exhibit-building-exposition-1939-ny-worlds-fair/) for silhouette only. The postcard is an artistic rendering, not a dimensional plan.

High-resolution drawing scans through the PAB/AAB website are subscriber/reproduction-gated. Metadata and thumbnails do not establish the measured outline. The source request should include permission to use dimension transcription in a research/portfolio model.

## Current provisional model package
Built by a separate source script under FMP archive release **RCA_1939_Research_Preview_v001**:
- 29 named watertight GLB objects, explicit Z-up metres.
- Basic outer hall shell with a traversable-looking front door void and undivided exhibition interior.
- Projecting cap/roof feature and central round roof-feature markers inspired by visual references.
- Separate public floor and exhibit guide markers.
- DXF local schematic first-floor envelope; CSV part register; JSON manifest; diagram and nine local tests.
- **Everything with a numeric length is an authored adjustable hypothesis, NOT a CRE351 measure.** Current quick-preview envelope 55 m wide x 28.06 m long x 12.38 m high is a *source mesh bound*, not a building fact or surveyed dimension.
- No historical/site registration. No Unreal collision certification; no wall-thickness/minimum-print-area test; skylight is currently an overlay, not a roof penetration.

## What counts as RCA "done"
1. Full-res final 1938 period sheet(s) or defensible scaled tracing obtained and archived with sheet date and rights; 1937 alternative retained separately.
2. Reconstruct independent shell/room/canopy/entry/roof height parameters with source evidence record, uncertainty and photograph cross-checks.
3. Match exterior facade and door openings in at least two period images.
4. Import native Unreal and check traversal, room transitions and lighting; prepare separate printable watertight shell variants.
5. Register dated visitor entry/exit endpoints and local meter positions to building structure; no invented global street coordinates.
6. Publish versioned source GLB, DXF, documented dimension schedule and tests into FMP master database.

RCA source-gate blocking item: **CRE351 high-resolution drawings**, not steel. After that, move the project's main modeling focus to all fairground paths, named roads, service routes, dated water/storm/sanitary utilities and temporal alignment analysis.

## Interior experience and plan reconstruction track (2026-10-19)

Interior artifacts must be tied to *rooms* only after the period plan and section
have been inspected. The present 29-part preview is an **undivided provisional
hall**, not evidence that the completed pavilion had no internal partitions.

New evidence register:
[`RCA_1939_INTERIOR_EXHIBIT_REGISTER_v001.csv`](RCA_1939_INTERIOR_EXHIBIT_REGISTER_v001.csv).
Its records document possible exhibit-modeling targets but deliberately leave
`room_id` blank and `location_status=ROOM_UNLOCATED`. Exhibit presence is not
proof of the room used, exact exhibit installation dates, or visitor sequence.

### Trace and model sequence

1. Acquire CRE351-001, April 11 1938: digitize external wall perimeter,
   partition centerlines, openings, door swings, stair locations, dimension
   strings and labeled spaces. Keep sheet scale, scan crop, grid and drawing
   revision in the trace metadata.
2. Acquire CRE351-002: digitize the second floor separately. Do not carry an
   inferred first-floor footprint upward without evaluating setbacks and voids.
3. Cross-check CRE351-005 sections with both plans for actual floor-to-floor
   elevations, opening heights, stair/ramp connections, ceiling clearances and
   any mezzanine or overlook.
4. Compare CRE351-003 roof plan and CRE351-004 elevations to the traced wall
   envelope. Treat the present round roof features as hypotheses until checked.
5. Define persistent `WF0009-F01-R###` room IDs and `WF0009-F01-D###`
   opening IDs *after tracing*, with polygon coordinates in local metres, evidence
   references, uncertainty and public/staff access. Use separate objects for
   walls, floors, doors, exhibits, lighting and roof.
6. Associate documented exhibits with rooms only when plan legends, labels,
   photographic sightlines or other source evidence support the assignment.
   Preserve alternatives and unresolved positions without guessed placements.
7. Build separate public visitor path graph and service graph, recording entrances,
   stair endpoints, queue areas and obstacles. Screen with test-agent profiles,
   then perform actual collision and traversal validation in Unreal.

Prioritized exhibit references: the transparent Lucite Phantom Teleceiver
(https://spectrum.ieee.org/rca-tv), period live television camera demonstration
records and the *Radio Living-Room of Tomorrow*
(https://www.earlytelevision.org/worlds_fair.html).
These are **objects and activities to study**, not a verified tour itinerary.

High-resolution CRE351 scans remain the architectural blocker. Subscription
and reproduction access must follow the holding institution's policies. The
metadata catalog and thumbnails alone cannot resolve wall positions. No interior
floorplan geometry was modified, no Unreal simulation was run, and no new room
coordinates were asserted in this update.

Next executable modeling gate: obtain a usable CRE351-001 image with reproduction
rights, create a measured trace with independent control checks, and register its
local origin to the existing provisional shell without adjusting the shell to
force a fit. Once CRE351-002 and CRE351-005 are traced, generate qualified room
volumes and navigation endpoints.
