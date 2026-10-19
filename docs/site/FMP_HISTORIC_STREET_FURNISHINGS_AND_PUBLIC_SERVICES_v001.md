# FMP | The lived-in fair — street furniture, art and services (2026-10-19)

**Owner:** FMP master data program. **Status:** SOURCE INDEX / SPATIAL TRACING QUEUE, not a surveyed site furniture map.

## Purpose

Record all modest but essential objects that help the 1939–1940 and 1964–1965 fairs feel inhabited: street refuse cans, drinking fountains, benches, movable chairs, lampposts and tree lights, post boxes, public telephones, lockers, information booths, newspaper/news stands, street clocks, directional signage, floral planters, flagpoles, entrance fixtures, historic sculpture, water fountains and pools, comfort stations, first aid and maintenance/service facilities.

The same source-backed records can later drive Unreal prefabs, CAD components, a physical-model print schedule, nighttime lighting and projector/AV cues. Architecture **is not** automatically replaced with a decorative guessed street scene.

## Existing data source and current work

Use the existing `database/migrations/015_dated_site_networks.sql` for streets, walkways, service lanes, electricity, utility mains, sewer, storm and fountain pump routing. The *new* `database/migrations/016_dated_site_amenities.sql` associates physical small objects with those networks without conflating a drinking fountain with a main water line or a show fountain's recirculation piping.

New catalog tables (all indexed through `tools/build_db.py`):
- `site_amenity_categories`: 23 visual / functional families and potential scene layers.
- `site_amenity_types`: 32 period-specific designs or documented asset classes. Unmeasured physical height/width/depth and counts remain NULL.
- `site_amenity_evidence`: 56 source observations, with sheet/file locators, media/rights status and approval class.
- `site_amenity_instances`: only **six** identifiable objects/groups currently have named-area contexts. All are geospatially unregistered. This is not a census of known objects.
- `site_amenity_service_links`: two NON-CERTIFIED fountain water-system needs. No invented plumbing alignments.
- `site_amenity_era_relations`: empty until a specific installation is proved to have moved, survived, or been replaced.
- `site_amenity_map_points` and `site_amenity_research_queue`: current map candidates / research status.

### Particularly valuable 1964–65 drawing series

[1964–65 Operations Drawing Manual master index](https://www.worldsfairphotos.com/nywf64/operations-drawings-manual/index.htm):

- **8, 9, 10**: three separate location sheets for benches, drinking fountains, information booths, newsstands, public lockers, telephone booths, mailboxes, Swiss clocks, and time-sales booths.
- **7**: entrance structures, turnstiles, toll booths and flagpoles.
- **16–20**: street lighting locations and precise luminaire variants; **21**: tree/open-space light fixtures.
- **28–30**: potable distribution; **31–33**: storm drains; **34–36**: sanitary sewers; **37**: fountain pumps; **38–39**: gas lines.
- **51–53**: service building, maintenance/paint-shop and maintenance annex plans.
- **57**: comfort station and typical first aid plans.

Sheet names/links are directly from the index. Their *individual symbol coordinates are not digitized yet*; fetching a PDF index is not georeferencing a plan. This is a copyrighted re-scan: DO NOT upload or republish the actual drawing scans without rights assessment.

### Particularly valuable 1939–1940 NYPL primary material

[1939–1940 NYPL original central files/maintenance finding aid](https://worldsfair.nypl.org/containerlist.pdf), archives [MssCol 2233](https://archives.nypl.org/mss/2233):
- **Box 238 Folder 26**: *Waste Cans (1939)*.
- **Box 238 Folder 8 / 7**: *Waste Disposal (1939 / 1940)*.
- **Box 238 Folder 10 / 9**: *Comfort Stations (1939 / 1940)*.
- **Box 275 Folder 11 / 10**: *Benches (1939 / 1940)*.
- **Box 275 Folder 18 / 17**: *Drinking Fountains (1939 / 1940)*.
- **Box 275 Folder 14**: *Bulletin Boards (1939)*.
- **Box 275 Folder 21**: *Flags and Banners (1939)*.

These are strong source *leads*, not physical-object placement plans until their contents are examined.

For outdoor site art, [NYC Parks historical guide](https://www.nycgovparks.org/pagefiles/73/tomorrows-world-publication.pdf), [Hofstra George Washington statue archive](https://omeka.hofstra.edu/exhibits/show/new-york-worlds-fairs/the-george-washington-statue-a), and [Minnesota Museum of American Art Manship history](https://mmaa.org/portfolio-item/paul-manship/) support:
- **James Earle Fraser's George Washington statue**, about 65 feet high, Washington Square/Constitution Mall (1939).
- **Paul Manship's Time and the Fates of Man sundial** and **Moods of Time** in Constitution Mall (1939), with period photographs available. Period proposal drawings and installed physical specifications need separate review.
- **Constitution Mall fountains**, documented by the NYC Parks period photograph.

For 1964, the [Fountain of the Planets / Pool of Industry](https://www.worldsfairphotos.com/nywf64/pool-industry.htm) is a historically documented complex; source pump sheets 37 etc can later enable a detailed operating-show scene.

## Spatial certainty ladder

1. **CATALOG_LEAD**: item or class named in a list; location and form unknown.
2. **NAMED_AREA_ONLY**: one historical item is contextually located (e.g., Constitution Mall). Never place a GPS pin or projected 3D prop automatically.
3. **PHOTO_ESTIMATE**: multiple matched camera landmarks and image source recorded; projected uncertainties/alternate interpretations retained.
4. **MAP_TRACED**: a dated sheet is traced, coordinate frame recorded, and the per-object source observation linked.
5. **SITE_REGISTERED**: actual control points and geodetic transforms documented; host coordinate/elevation and uncertainty measured.

Only steps 4 or 5 enter local-scene coordinate exports; only step 5 with actual WGS84 lon/lat enters `verified_points_wgs84.geojson`. This avoids corrupting a physical scale model with approximated bench/garbage can locations.

All 1939, 1940, 1964, 1965 and present-day data remain separately dated. Do not assume a 1964 luminaire or restroom remained in place in 1965 or after redevelopment.

## How the output is consumed

```bash
python3 tools/sync_master_database.py --once
# OR standalone after master build:
python3 tools/site/export_site_amenities.py \
  --database out/flushing_meadows.sqlite --out out/site_amenities
```

Deliverables automatically regenerated by the master refresh:
- `out/site_amenities/research_queue.csv` — work queue for types without locations.
- `out/site_amenities/evidence_and_photo_leads.csv` — exact primary document links/box numbers.
- `out/site_amenities/source_sheet_priority.csv` — sheets to acquire/georeference.
- `out/site_amenities/named_area_landmarks.json` — confirmed neighborhood/site associations; no fictitious coordinates.
- `out/site_amenities/local_scene_points.json` — model-local XYZ with recorded source and confidence, once traced.
- `out/site_amenities/verified_points_wgs84.geojson` — map pins only for calibrated coordinates.
- `out/site_amenities/network_service_links.csv` — plumbing/electrical link candidates, with evidence levels.
- `out/site_amenities/site_amenity_summary.json` — live completeness counts.

### Priority production work

1. **Acquisition/registration:** sheets 8/9/10 for every type of recurring 1964 street furnishing. Trace every indexed location **by symbol type** using a control-point-registered fairground plan and preserve source sheet and symbol coordinates.
2. **Lighting:** trace sheets 16–21 into pole/light fixture positions + verified luminaire families; match evening photos to installed luminaire arrangements. Light/show cues future.
3. **1939 objects:** obtain NYPL boxes 238 & 275, reconstruct exact bin/bench/drinking-fountain appearance from originals/period photos, then catalog instances one by one.
4. **Major landmarks:** register George Washington statue, Manship sundial/Moods of Time, fountains, pool edges, and their materials/lighting by historical plan and distinct photo viewpoints.
5. **Facilities & operations:** toilets/first-aid, phone/news booths, refuse pickup and access routes; utilities tied to the existing dated network where independently documented.
6. **Time transition:** only when a specific fixture persists, is moved, is removed or replaced, add cross-year relations with contemporaneous supporting evidence.
7. **Digital/physical fabrication:** use a shared asset/scene identity with separate Unreal meshes, print-friendly solids, correct historical material/look, and optional projection-mapping cue objects. Neither printability nor native Unreal runtime has been certified.

**Current validation:** The CSV/source references passed an independent consistency check; schema/run-time integration tests are in `tests/test_site_amenities.py` and still require execution against a complete local FMP checkout.
