# Ford Exposition 1939–40: architectural drafting + computational reconstruction v0.1

**Database ID:** WF0014 • **Exhibit ID:** FORD39_CYCLE_OF_PRODUCTION • **CAD axes:** provisional local X/Y (not world-aligned) • **Building status:** neither site-registered nor as-built verified. Dates 1939 and 1940 will be modeled separately.

## Evidence-grade dimensional ledger

| Property | Historical value | Metric | Evidence | Use in CAD |
|---|---:|---:|---|---|
| Industrial Hall revolving turntable diameter | 100 ft | 30.480 m | 1938 *Architectural Record*, Design Trends, p. 85, FMP-EV-FORD-AR1938-01 | LOCKED period-published diameter |
| Road of Tomorrow visitor ride length | 0.5 mile | 804.672 m | Ford original souvenir brochure FMP-EV-FORD-SOUV1939-01; guidebook quote; exact brochure text still needs inspection | Period-reported, not footprint or spiral length |
| Road of Tomorrow spiral | Three-tier cantilever reinforced-concrete ramp, inner column ring | Three tiers | 1938 *Architectural Record* | LOCKED topology; radius, run, rise, structural sections not known |
| Mercury entrance figure | 25 ft reported | 7.620 m | Secondary accounts, primary brochure text to verify | PROVISIONAL dimension |
| Ford Cycle industrial display models | 87 | 87 | The Henry Ford, THF225380 (FMP-EV-FORD-CYCLE-01) | Sourced object count, positions undetermined |
| Animated exhibit figures | 142 | 142 | The Henry Ford | Sourced count, animated states undetermined |
| Raw material topics | 27 | 27 | The Henry Ford | Sourced subject count, exact scene list incomplete |
| Hall outside walls, roof elevations, entrances, ramp curvature, roadway width, moat depth, pontoon count | unknown | unknown | No usable original measured drawing transcribed | Hypotheses only |

**Important:** The 1938 article provides a scaled *plan image* along with prose, but its relevant drawing has NOT been transcribed from a high-resolution original in this pass. The schematic issued now is an illustration of the program and dimensions, not a traced period floorplan.

## Implemented local CAD preview (separate from registered FMP park)

- Four facility sectors: entrance, Industrial Hall, Garden Court and Road of Tomorrow. Sector locations and dimensions in the present drawing are deliberately **hypothetical**; their general visitor sequence is documented.
- Ford Cycle tier model: 4 **interpretive** radii [15.24, 12.5, 9.0, 5.2] m, 4 **interpretive** stage elevations [0.9, 3.4, 6.25, 9.25] m. The first radius is derived from the sourced 100-ft diameter; other tier radii are NOT historical measurements.
- Industrial moat outer radius example: 19.1 m, water depth example 0.55 m, not sourced measurements.
- Road spiral schematic radius 26 m with 2.8 illustrative turns (NOT three historical turns). Representational road width 4.7 m, bottom/top nominal elevation 1.6/10.0 m; all are adjustable assumptions.
- The glTF preview includes 87 named working-model proxies and 142 unlocated/undetailed figure placeholders to reserve the full source-backed show component counts.
- Solids are separate material/object slots; the non-watertight road preview surface is not printable or suitable as collision without closing/rebuilding the roadway.

## Mechanics and equations

Using D=30.48 m:
- R = D/2 = 15.24 m.
- Turntable plan A = pi*(15.24)^2 ≈ 729.66 m^2 (describes projected circle, NOT hall area).
- Circumference C = pi*30.48 ≈ 95.76 m.
- Animated phase: theta(t)=theta0+(2*pi*rpm/60)*t; actual rpm UNKNOWN.
- Tangential rim speed: 15.24*(2*pi*rpm/60) m/s, hypothetical until rpm obtained.
- Pontoon float buoyancy idealization: displaced water volume V=m/(rho_water); actual masses/hulls/guidance/bearings UNKNOWN.
- Illustrative spiral plan run if mean radius 26 m and 2.8 turns: ~457.4 m. Remaining ~347.3 m of a half-mile route is NOT a measured geometry and should not be used to constrain the as-built map.
- Three-tier denotes structural levels, NOT evidence of three complete revolutions.

## Primary photographic plates and geometry inferences

- THF225380 Cycle of Production frontal interior: https://www.thehenryford.org/collections/explore/artifact/47282 (public exhibit edge, tier silhouettes and vehicle model at apex)
- THF217081 Road of Tomorrow: https://www.thehenryford.org/collections/explore/artifact/373201 (multi-level concentric automobile roadway, railing and inner supports)
- THF216101 Garden Court: https://www.thehenryford.org/collections/explore/artifact/372195 (visitor queues and elevated circulation facing water)
- THF216259 nighttime Ford exposition: https://www.thehenryford.org/collections/explore/artifact/372510 (outline and period lighting)
- CCA PH2000:0572 original night view: https://www.cca.qc.ca/en/search/details/collection/object/348846
- CCA PH2000:0571 main entrance photograph: https://www.cca.qc.ca/en/search/details/collection/object/348845
- Hugh Ferriss concept rendering THF153317: https://www.thehenryford.org/collections/explore/artifact/31119 (proposed design **NOT** verified as built)
- Ford Exposition brochure **with map** THF223276: https://www.thehenryford.org/collections/explore/artifact/373551 (high-value next plan source)
- *Architectural Record*, November 1938, page 85 and facing plan: https://usmodernist.org/AR/AR-1938-11.pdf (50 MB digitization; acquire sheet crop at original res)
- 1940 changed-building negatives: The Henry Ford catalogue https://askus.thehenryford.org/bibs/faq/445890 (14584–14586, 14647–14653).

Archival images are linked by source URI, not redistributed. Their displayed images remain owned by their institutions; verify rights before texturing or public-release use.

## Plans and deliverables (local generated artifacts)

Sheet A001: evidence-marked facility hierarchy.
Sheet A101: **schematic** ground plan with documented turntable dimension and invented surrounding room boxes.
Sheet A301: 100-ft turntable/industrial moat sectional hypothesis.
Sheet A302: three-tier Road of Tomorrow sectional hypothesis.
Page 6: mechanical formulas, Page 8: linked source plate catalogue.
A401: 3D tier illustration; 3D GLB with explicit exhibit scene IDs.

All deliverables were generated in the session and exported as a single ZIP alongside a full Python/ReportLab/SVG/trimesh generator. This GitHub file is a durable index and data basis, not a claim that the binary GLB or PDF is committed in Git.

## Next drafting corrections after full-size primary sheet acquisition

1. Scan/digitize Ford floor plan in *Architectural Record* (visible printed scale) and THF223276; preserve map source hash/issue year.
2. Register building footprint into NY State Plane EPSG:32118 with independent holdout checks; keep provisional local axes until verified.
3. Trace Industrial Hall perimeters and the actual turntable *placement in room* and pedestrian semi-ring. Replace current arbitrary center offsets.
4. Solve spiral center, inner support-circle radius, level elevations, vehicle lanes, canopy clearances using plan photo matches. Do not overconstrain by half-mile total route alone.
5. Use construction photographs to model loading platform, Mercury entrance, garden fountain, orchestra platform, broadcaster studio, door and glazing details.
6. Separate 1939 built revision from photographed 1940 remodel; establish material/lighting PBR color using available period color records, not grayscale intensity.
7. Test avatars/vehicle collisions and roof access in Unreal. Offer realistic and stylized presentation without changing architectural identity IDs.
