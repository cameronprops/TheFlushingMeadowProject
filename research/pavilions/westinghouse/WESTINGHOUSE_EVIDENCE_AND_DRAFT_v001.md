# Flushing Meadows Project — Westinghouse Electric Building (1939) research and preliminary drafting package

**Project ID:** WF0020. **Date:** 2026-10-18. **State:** source-constrained historical impression, **not** as-built documentation. No geometry has been placed on the FMP master site. This source package distinguishes the building's contemporary evidence from the provisional rendering parameters. The 1964–1965 Westinghouse Time Capsule display was a **different architectural installation** and must not be merged with the 1939 horseshoe-building geometry.

## 1. Source-supported exterior reconstruction facts

| Item | Status | Finding | Evidence |
|---|---|---|---|
| Name/exhibitor | High | Westinghouse Electric & Manufacturing Company; often titled Westinghouse Electric Building. | S01,S02,S03 |
| Architect | High | Skidmore & Owings with John Moss. Note that an official postcard credits only Skidmore & Owings, while LOC and CCA explicitly list Moss. | S01,S02,S03,S05 |
| Original silhouette | High (qualitative) | Two large curved/glazed wing-fronts, central entry/cross-hall, tall Singing Tower of Light. Photographs verify the morphology, but not their surveyed section radii. | S01,S02,S03,S05 |
| Tower height | Strong period evidence | **150 feet / 45.72 metres** printed on officially licensed 1939 souvenir postcard. This is the only height used as a period-published input in the generator. | S04 |
| Wing heights | Leads needing confirmation | **55 feet / 16.764 m**, reproduced in a secondary collector transcription of postcard text. Do not confuse roof height with number of occupied floors. | S06 |
| Pavilion reported size | Leads needing confirmation | **25,200 sq ft / 2,341.156608 m²** reported, but unclear if it means ground coverage, gross exhibition floor area, or combined wing floor area. The draft is NOT calibrated to this figure. | S06 |
| Central fountain | Qualitative strong; numeric pending | Historical photography explicitly identifies a fountain at the Singing Tower. A secondary description gives maximum fountain jet **120 ft / 36.576 m**, not a structure dimension. | S03,S06 |
| Time Capsule | High | A first capsule was buried September 23, 1938, 50 feet below ground. LOC displays a contemporary diagram with printed burial coordinates. Its relation to the exact building footprint remains unverified. | S07,S08 |
| Principal halls | High program / incomplete plan | Hall of Power; Hall of Electrical Living; Theater of Tomorrow, plus exhibits including television, junior science, kitchen appliances and Elektro. Their internal partitions and exact adjacency have not been traced. | S09,S10,S11 |
| 1939 vs 1940 | Unknown geometry delta | The 1939 and 1940 fair seasons existed; current sources do not demonstrate unaltered building/exhibit configuration between them. Treat as separate year states until confirmed. | S11 |

## 2. Capsule geographical point — valuable lead, not the pavilion center

The LOC *Inside Adams* article reproduces Westinghouse's contemporary time-capsule graphic with coordinates printed as approx. **40°44′34.089″ N, 73°50′43.842″ W**. Interpreting that as decimal arcseconds produces latitude **40.7428025**, longitude **−73.8455116667**. A provisional conversion from modern WGS84 to EPSG:32118 yields about **E 313,048.25 m; N 63,989.03 m**. These numbers **must not** become an as-built pavilion placement or certified survey station: the original drawing may use a period geographic reference, the printed fractions need careful original-image transcription, the buried capsule is not the hall centroid, and survey datum matching is unverified. Survey the surviving monument / relevant 1964 map and reconcile with the 1939 site plan before creating building translation and rotation. Source: S07.

## 3. Exterior draft assembly shipped here

The `Westinghouse_1939_Exterior_Impression_v001.glb` is a stand-alone **local-metre Z-up** GLB. It includes **329 named, independently editable components**: the twin wings; provisional glazed facade panels and horizontal mullions; connecting hall; tower shaft and stacked open rings; and an indicative basin. The companion manifest tags each component's evidence status. The first-pass plan and elevation are editable **SVG**, supplemented by PNG preview files. `build_westinghouse.py` reproduces the GLB from parameters and is not a genuine digitization of a construction drawing.

**Geometry parameters that are deliberate guesses:** hall width and depth; wing centers and shape; entrance recession; glass-bay spacing and number; tower width, ring diameters and elevations; facade finishes; hall partitioning; basin diameter and position; horizontal location, true north rotation and the site grading. Fountain water height is kept only in metadata (not a 36 m solid column). No capsule location is implied by the model origin. Window mullion rhythm is suggestive, not recovered from plans.

**Dimensions to revise first on receipt of plans:** complete footprint outline; frontage between end walls; distance between tower and hall; tower structural core and ring elevations; true wing roof/overall height; fountain basin footprint; northing/easting and forecourt azimuth.

## 4. Interior reconstruction scope (evidence discovered, no interior model fabricated)

- **Hall of Power:** electric stairway noted in 1939 May 8 photography; machinery and public power exhibits. Need primary floor plan and documented vertical levels. (S10,S11)
- **Hall of Electrical Living:** Elektro robot performance visible through glass; 1939 May 8 AP photograph of crowd viewing the performance; exhibits illustrating electrified household technology. Need exact show platform and sightlines. (S10)
- **Theater of Tomorrow:** listed with the pavilion descriptions; layout / seating / programming remains unmeasured. (S11)
- **Junior Science Hall**, **Playground of Science**, **television display**, **Battle of the Centuries** appliance demonstration: present in Westinghouse's 1939 promotional film. Film cuts are not guaranteed continuous spatial geography. (S09)
- **Time Capsule display:** placement and interpretation documented in corporate publications. 1938 burial is below ground and must not be invented as an interior object floating within an arbitrary room. (S07,S08,S12)

## 5. High-value acquisition requests

1. **Smithsonian, NMAH.AC.0560_ref2919, Box 66 Folders 18–19 and Box 87 Folders 5–6.** Request item inventory, photographs of construction/interiors, exhibits, architectural plans, dated floor plans and rights terms. Distinguish envelope photographs from exhibit memorabilia. (S12)
2. **Smithsonian, NMAH.AC.0560_ref972 / ref4189.** Request annotated photographs of Westinghouse exhibits and the period publication *Westinghouse Fair World*. (S13)
3. **1939 Westinghouse employee handbook** listed on Disney Docs archival-document website. Landing page exists, but the scanned text is not retrieved in this batch. Request complete scan, table of contents, show flow and section list. (S14)
4. **Westinghouse company publications 1938 and 1939** listed in secondary research, including *Westinghouse at the World's Fair* and *Westinghouse Fair World*. Public links encountered at `1939nyworldsfair.com` were unavailable/502 at retrieval time; **not acquired or read**. (S15)
5. **LOC Gottscho-Schleisner negatives/slides and CCA photographs.** Identify precise camera positions, front/back facades, night-lighting scheme and structural details. CCA's photo rights need separate permission before republishing. (S01,S02,S03)
6. **1939 survey/map registration.** Retrieve high-resolution 1939 Fair general plan XM-250 and period site drawings. Only then fit the building footprint relative to the Time Capsule anchor and its neighbors. (S16)

## 6. Drafting next-pass order

A. Build a **site-space** plan from a dated 1939 map showing Westinghouse parcel outline/roads/adjacent buildings; do not arbitrarily place this preliminary model on Constitution Mall.

B. Match known source views: frontal LOC/CCA photos for twin wings, tower and fountain; oblique CCA images for profile; aerial period photographs for horse-shoe depth and roofline. Use at least two independent camera views when inferring each curvature/dimension.

C. Replace generator's interpretive dimension parameters with measurements and **per-parameter citations**. Maintain source IDs and stable part IDs for Rhino/Worldwright/Unreal exchange.

D. Separate **1939** and **1940** display states; no assumption that the 1940 Elektro/Sparko programming or exhibition layout was unchanged.

E. Draft interior zoning only after handbook and floor plan; avoid designing a new storyline or speculative circulation.

## 7. Primary and other evidence links

- **S01 LOC** Gottscho photograph, Singing Tower and Westinghouse, architects listed: https://www.loc.gov/pictures/item/2018750438/
- **S02 CCA** night building/photo of pool: https://www.cca.qc.ca/en/search/details/collection/object/346638
- **S03 CCA** ground-level Singing Tower and fountain: https://www.cca.qc.ca/en/search/details/collection/object/3706
- **S04 licensed 1939 postcard** transcribed by seller, 150 ft tower: https://www.cardcow.com/152381/westinghouse-electric-building-exposition-1939-ny-worlds-fair/
- **S05 SOM** firm's own 1939 Fair project portfolio: https://www.som.com/projects/new-york-worlds-fair-1939/
- **S06 collector transcription** 55 ft wings / 25,200 sq ft / 120 ft fountain: https://postcardmuseum.wordpress.com/2012/01/31/1939-new-york-worlds-fair-westinghouse-electric-building/
- **S07 LOC blog** capsule original coordinates and burial details: https://blogs.loc.gov/inside_adams/2023/07/time-capsule/
- **S08 academic historical analysis** time capsule and exhibit: https://cjh.uchicago.edu/issues/fall15/5.2.pdf
- **S09 San Jose State Univ.** analysis of Westinghouse's period film and exhibit stops: https://www.sjsu.edu/faculty/wooda/middleton/middletonfilm.html
- **S10 Associated Press** contemporaneous Hall of Electrical Living/Elektro photo May 8, 1939: https://apimagesblog.com/historical/2019/4/26/1939-worlds-fair-80-years-since-a-world-of-tomorrow
- **S11 Pavilion architectural summary** plan description / exhibit group: https://en.wikipedia.org/wiki/1939_New_York_World%27s_Fair_pavilions_and_attractions (secondary cross-reference only)
- **S12 Smithsonian archived Westinghouse company materials**: https://www.si.edu/object/archives/components/sova-nmah-ac-0560-ref2919
- **S13 Smithsonian exhibit photos / publication inventory**: https://www.americanhistory.si.edu/ne/collections/archival-collection/sova-nmah-ac-0560
- **S14 Disney Docs** 1939 employee handbook landing page: https://www.disneydocs.net/westinghouse-emp-handbook
- **S15 Secondary bibliography** pointers to 1938/1939 period magazines, unverified digital copies: https://minystories.wordpress.com/2013/04/29/worlds-of-tomorrow/
- **S16 NYPL site planning/drawings**: https://archives.nypl.org/mss/2233

**CAUTION: 1964 Westinghouse** described at https://www.worldsfairphotos.com/nywf64/westinghouse.htm is three open-sided discs near the capsule. It is **not** a source for the geometry of the 1939 winged pavilion.