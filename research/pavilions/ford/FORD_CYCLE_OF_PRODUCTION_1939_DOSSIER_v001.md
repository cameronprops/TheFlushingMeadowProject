# FMP — Ford Exposition / Ford Cycle of Production (1939–1940)

**Parent physical building:** WF0014 (1939–1940 Ford Motor Company Pavilion / Ford Exposition). **Feature:** `FORD39_CYCLE_OF_PRODUCTION`, a *nested exhibit*, NOT a separate building.  
**Identification:** confirmed from user correction "ford exposition pavilion" plus the museum's 1939–1940 contemporary photographic catalog.  
**Geometry status:** RESEARCH ONLY; no measured floorplan, vertical dimensions, mechanical speed, or registered site transform yet.

## Confirmed architectural / exhibit facts

- Inside the 1939–40 Ford Exposition stood the **Ford Cycle of Production**, a very large revolving, layered "wedding-cake" turntable in a surrounding water moat.
- The tiered display floated **on pontoons**. The rotational mechanism requires further engineering investigation; do not assume the entire structure was freestanding or that it rotated about a fixed tower in a pond.
- The Henry Ford Museum's Ford Motor Company photographic record specifies **87 working models**, **142 animated figures** and **27 raw materials** progressing through manufacture from lower to higher tiers. This is an excellent source for distinct procedural scene units, but does not mean their exact positions are known.
- Historical photo THF225380 / object **64.167.232.1793**, made 1939–40, shows the entire rotating layered exhibit in an interior public viewing space: https://www.thehenryford.org/collections/explore/artifact/47282
- Additional **1939-dated detail photographs** at The Henry Ford: **rubber display** THF217071 (object 64.167.232.1714): https://www.thehenryford.org/collections/explore/artifact/373196 and **leather display** THF217059 (object 64.167.232.1709): https://www.thehenryford.org/collections/explore/artifact/373191
- Separate Ford archive documentation shows a **soybean food display** THF216399 / object 64.167.232.1380, and **cellulose acetate plastics display** THF216401 / object 64.167.232.1381: https://www.thehenryford.org/collections/explore/artifact/372309 and https://www.thehenryford.org/collections/explore/artifact/372310 . The catalog dates these photos January 8, 1940; establish whether they show post-season modifications.
- The Henry Ford holds a **1939–1940 souvenir brochure** describing the architectural design, exhibits, and Road of Tomorrow; museum expert set: https://www.thehenryford.org/collections/explore/sets/detail/henry-ford-worlds-fair?AssetId=THF222343 .
- Hofstra special collections includes a Ford Exposition brochure: https://omeka.hofstra.edu/exhibits/show/new-york-worlds-fairs/the-ford-exposition-at-the-194
- Ford's broader pavilion included a distinctive **Road of Tomorrow** elevated car roadway that loops and enters/exits the building, plus garden court. Do not mistake the spiral road for the rotating exhibition platform.
- A *secondary reconstruction account* estimates the rotating display at **100 ft diameter (30.48 m)**: https://bygonelife.com/worldsfair39/transportation.php . This is a parametric starting value **PHOTO/SOURCE-INFERRED**, not a certified architectural diameter or water-basin size.

## Proposed CAD hierarchy

- `WF0014_1939/FORD39_PAVILION`: independent exterior massing; correct period site placement required
- `WF0014_1939/INDUSTRIAL_HALL`: enclosing exhibition hall and accessible visitor route
- `WF0014_1939/FORD39_CYCLE_OF_PRODUCTION`
  - `WATER_MOAT`: outer basin geometry / visible water surface, footprint TBD
  - `PONTOONS`: concealed buoyant supports; count and layout unknown
  - `ROTATING_PLATFORM`: rigid-body pivot animation; speed and support mechanism unknown
  - `TIER_00`: extraction and raw-material scenes
  - `TIER_01..`: industrial transformation and fabrication, layer count still unconfirmed
  - `MODEL_UNITS`: 87 identified working models as an overall sourced count; per-scene assignment TBD
  - `FIGURES`: 142 animated figures as an overall sourced count; per-scene assignment TBD
  - `VIEWER_PERIMETER`: public walkable viewing and crowd-clearance envelope (interpretive until floorplan)
- `WF0014_1939/ROAD_OF_TOMORROW`: car roadway and guest boarding circulation are separate pavilion subsystems.

## Research / engineering gates

1. Obtain full-resolution original Ford Cycle images THF225380, THF217071, THF217059, THF216399, THF216401, licensed for permitted project use. Retain image rights and original resolution.
2. Collect Ford Exposition souvenir brochures and company exhibition/construction drawing holdings. Check archived architect **Albert Kahn** and exhibition designer **Walter Dorwin Teague** roles against original approvals.
3. Determine year-specific plan, hall bounds, tier count, water geometry, stage rotation and pontoon arrangement. Do not confuse 1939 Ford with Chicago (1934), San Diego (1935), or NYWF 1964 Ford pavilion.
4. Photomatch multiple views using known guests/guardrails as rough scale only. Record uncertainty. If the 100-ft estimate is used, mark the base circle as a hypothesis.
5. Prototype an Unreal animated rotating exhibit and separate walkable spectator perimeter. Preserve realistic/stylized material overrides and shared collisions.
6. Sequence the industrial miniature scenes by evidence; do not invent source claims for specific figures, dioramas or processes.

**Validation:** sourced identity/content, but building footprint, motor details, part placement, and exact dimensions are NOT verified. Historical architecture and show content are different source classes.
