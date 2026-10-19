# Ford Exposition / WF0014 / v0.3

Procedural, provisional 1939 architectural impression. Real building location, hall footprint, ramp curve, elevation and orientation are NOT surveyed or certified.

## Model
- Ford_1939_Exterior_Road_Production_v003.glb: 310 named objects, separate PBR material slots.
- A103_Ford_1939_Exterior_Structure_Plan_v003.dxf: 32 CAD entities, metric units.
- Ford_1939_Exterior_Road_Production_Sheets_v003.pdf: plan, ramp elevation and evidence/QA.
- Road_of_Tomorrow_Centerlines_v003.csv: 1,121 model-local samples including proposed two links.
- Road_and_Animation_Contract_v003.json: inferred pitch, grade, exhibit rotating rig identity.
- Source scripts build_ford_exterior_v002.py and build_ford_exterior_v003.py.
- Nine unit tests in test_ford_v003.py.

Build: python3 build_ford_exterior_v003.py --output-dir .
Test: python3 -m unittest -v test_ford_v003
Dependencies: numpy, trimesh, ezdxf, matplotlib, reportlab, Pillow.

## Evidence hierarchy
PERIOD DOCUMENTED: Architectural Record Nov 1938 states 100-foot exhibit diameter and 3-tier reinforced-concrete cantilevered spiral supported by inner column ring. Ford brochure advertises ~half-mile automobile route. The Henry Ford catalogs Ford Cycle 87 models, 142 figures, 27 materials, and a photo titled '150-Ton Turntable' dated June 2 1939.
INTERPRETIVE: 24 column grid, inner radius, entire site relationship, 2.8 turns, 1.83% modeled grade, 2.54m vertical deck clearance, outer building ellipse, water radius, curbs, and other structural sizes.
Road finish is modeled with period-researched Monocork as a provisional cinematic shader (not sampled historic material).
Only unregistered preview files; no Unreal or native Worldwright/Rhino host test yet.

Research: https://usmodernist.org/AR/AR-1938-11.pdf
Ford Cycle: https://www.thehenryford.org/collections/explore/artifact/47282
Turntable catalog: https://www.thehenryford.org/collections/explore/artifact/77707
