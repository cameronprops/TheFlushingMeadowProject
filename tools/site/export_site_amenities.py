#!/usr/bin/env python3
"""FMP: source-gated site-furniture, art, fountains and public-service map export.
Does not create historical street furniture at guessed positions.
Run: python3 tools/site/export_site_amenities.py --database out/flushing_meadows.sqlite --out out/site_amenities
"""
from __future__ import annotations
import argparse
import csv
import json
import sqlite3
from pathlib import Path

def rows(db, statement, args=()):
    return [dict(r) for r in db.execute(statement, args)]

def write_csv(path, records, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

def export_site_amenities(db: sqlite3.Connection, out: Path):
    """One canonical SQLite database; no second authoritative source catalog."""
    db.row_factory=sqlite3.Row
    out=Path(out)
    out.mkdir(parents=True,exist_ok=True)
    types=rows(db, """SELECT t.*,c.category_family,c.display_name AS category_name,
     c.suggested_layer FROM site_amenity_types t
     JOIN site_amenity_categories c ON t.category_id=c.category_id
     ORDER BY t.era_year,c.category_family,t.historical_label""")
    evidence=rows(db, """SELECT * FROM site_amenity_evidence
                         ORDER BY era_year,type_id,observation_id""")
    instances=rows(db, """SELECT i.*,t.historical_label,t.category_id,
       c.category_family,c.suggested_layer
       FROM site_amenity_instances i
       JOIN site_amenity_types t ON i.type_id=t.type_id
       JOIN site_amenity_categories c ON t.category_id=c.category_id
       ORDER BY i.era_year,i.instance_id""")
    research=rows(db,"SELECT * FROM site_amenity_research_queue ORDER BY era_year,category_family,historical_label")
    services=rows(db,"SELECT * FROM site_amenity_service_links ORDER BY instance_id")
    sheets=rows(db, """SELECT s.* FROM site_network_sheets s
      WHERE s.sheet_id IN (SELECT DISTINCT source_sheet_id FROM site_amenity_evidence
        WHERE source_sheet_id IS NOT NULL)
      ORDER BY era_year,sheet_id""")
    relations=rows(db,"SELECT * FROM site_amenity_era_relations ORDER BY relation_id")

    # Objects with only a named site district belong in the RESEARCH backlog,
    # not in a made-up Unreal coordinate or GPS map.
    contextual=[r for r in instances if r["position_status"] in
                ("UNLOCATED","NAMED_AREA_ONLY","PHOTO_ESTIMATE")]
    traced=[r for r in instances if r["position_status"] in ("MAP_TRACED","SITE_REGISTERED")]
    if any(any(p is None for p in (r["x_m"],r["y_m"],r["z_m"])) for r in traced):
        raise ValueError("Traced model point missing coordinates")
    local_points=[{
      "id":r["instance_id"], "building_id":r["nearby_building_id"],
      "type_id":r["type_id"], "category_id":r["category_id"],
      "layer":r["suggested_layer"],"year":r["era_year"],
      "position_m":[r["x_m"],r["y_m"],r["z_m"]],
      "coordinate_frame":r["coordinate_frame"],
      "placement_status":r["position_status"],
      "evidence_id":r["source_observation_id"],
      "uncertainty_m":r["placement_uncertainty_m"],
      "model_asset_uri":r["model_asset_uri"],"unreal_id":r["unreal_scene_object_id"]
    } for r in traced]
    # Standard GeoJSON is WGS84 longitude/latitude, never projected metres.
    # Never turn unregistered model-local X,Y into GPS by assumption.
    geo_features=[]
    for r in instances:
        if r["position_status"]!="SITE_REGISTERED":
            continue
        if r["longitude"] is None or r["latitude"] is None:
            continue
        if not r["horizontal_crs"] or not r["vertical_datum"]:
            continue
        geo_features.append({
          "type":"Feature","id":r["instance_id"],
          "geometry":{"type":"Point","coordinates":[r["longitude"],r["latitude"]]},
          "properties":{"era_year":r["era_year"],"type_id":r["type_id"],
            "category_id":r["category_id"],"name":r["historical_label"],
            "evidence_id":r["source_observation_id"],"registered":True,
            "uncertainty_m":r["placement_uncertainty_m"]}
        })

    (out/"verified_points_wgs84.geojson").write_text(
      json.dumps({"type":"FeatureCollection","features":geo_features},
        indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    (out/"local_scene_points.json").write_text(
      json.dumps({"schema":"fmp.site-amenity-local.v1","points":local_points,
                  "units":"metres","coordinate_system":"AS_RECORDED_PER_POINT"},
         indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    (out/"named_area_landmarks.json").write_text(
      json.dumps({"schema":"fmp.site-amenity-unregistered.v1",
          "warning":"These are researched names, NOT fixed map points.",
          "features":contextual},
          indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")

    write_csv(out/"research_queue.csv",research,
              ["type_id","era_year","historical_label","category_family",
               "type_status","source_sheet_id","evidence_records",
               "located_or_unlocated_instances","spatially_traced_instances"])
    write_csv(out/"evidence_and_photo_leads.csv",evidence,
              ["observation_id","type_id","era_year","source_sheet_id","source_url",
               "source_locator","observation_kind","observation_status","claim",
               "approximate_named_context","observed_quantity","rights_status","notes"])
    write_csv(out/"source_sheet_priority.csv",sheets,
              ["sheet_id","era_year","sheet_title","sheet_number","archive_collection",
               "archive_url","primary_layer","availability","status_note"])
    write_csv(out/"network_service_links.csv",services,
              ["service_link_id","instance_id","network_layer_id","segment_id",
               "service_kind","linkage_status","source_observation_id","notes"])
    # A lighting pole may link back to its circuit; this export keeps that
    # connection separate until period conduit sheets actually support it.
    summary={"schema":"fmp.site-amenities-report.v1","typologies":len(types),
      "source_observations":len(evidence),"sheets_with_observations":len(sheets),
      "identified_instances":len(instances),
      "named_area_only_instances":len(contextual),
      "traced_local_site_points":len(local_points),
      "geodetically_registered_wgs84_points":len(geo_features),
      "service_link_records":len(services),
      "cross_era_object_relations":len(relations),
      "complete_spatial_map":False,
      "time_separation":"1939,1940,1964,1965,2026; no automatic reuse",
      "requirement":"Do not distribute, instantiate, or project imagery from unlocated source types",
      "next":("Acquire and georeference Operations Manual sheets 8-10 and 16-21,"
              " then read 1939 NYPL boxes 238/275; register individual confirmed symbols.")}
    (out/"site_amenity_summary.json").write_text(
        json.dumps(summary,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    return summary

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--database",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    with sqlite3.connect(a.database) as db:
        print(json.dumps(export_site_amenities(db,a.out),indent=2))

if __name__=="__main__":
    main()
