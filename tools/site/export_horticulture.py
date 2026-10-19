#!/usr/bin/env python3
"""FMP horticulture projection: one SQL source, separate sourced/unknown mapping.
Never distribute species or trees by random historical locations.
  python3 tools/site/export_horticulture.py --database out/flushing_meadows.sqlite --out out/horticulture
"""
from __future__ import annotations
import argparse
import csv
import json
import sqlite3
from pathlib import Path

def records(db,statement,values=()):
    return [dict(row) for row in db.execute(statement,values)]

def write_csv(path,data,headers):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=headers,extrasaction="ignore")
        w.writeheader()
        w.writerows(data)

def export_horticulture(db:sqlite3.Connection,output_dir:Path):
    """Source-preserving horticultural inventory; not a procedural tree generator."""
    db.row_factory=sqlite3.Row
    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=True)
    sources=records(db,"SELECT * FROM horticulture_sources ORDER BY era_year,source_id")
    zones=records(db,"SELECT * FROM horticulture_areas ORDER BY era_year,area_id")
    plants=records(db,"""SELECT p.*,a.historical_name AS area_name,
       a.location_status AS area_location_status,
       t.display_name AS botanical_name,t.scientific_name,t.taxonomic_precision
       FROM horticulture_plantings p JOIN horticulture_areas a ON a.area_id=p.area_id
       LEFT JOIN horticulture_taxa t ON p.taxon_id=t.taxon_id
       ORDER BY p.era_year,p.area_id,p.planting_id""")
    events=records(db,"SELECT * FROM horticulture_seasonal_events ORDER BY era_year,date_start,event_id")
    lineage=records(db,"SELECT * FROM horticulture_era_links ORDER BY earlier_area_id,later_area_id")
    plant_instances=records(db,"SELECT * FROM horticulture_mapped_plants ORDER BY era_year,instance_id")
    irrigation_links=records(db,"SELECT * FROM horticulture_irrigation_links ORDER BY area_id,irrigation_link_id")
    queue=records(db,"SELECT * FROM horticulture_research_queue ORDER BY era_year,historical_name")

    # A historical plan's existence is not geometric registration.
    registered=[]
    for z in zones:
        if z['location_status'] not in ('MAP_TRACED','SITE_REGISTERED'):continue
        if not z['local_polygon_geojson']:
            raise ValueError("Mapped horticultural area has no plan polygon: "+z["area_id"])
        outline=json.loads(z['local_polygon_geojson'])
        if outline.get('type') not in ('Polygon','MultiPolygon'):
            raise ValueError("Expected Polygon or MultiPolygon: "+z['area_id'])
        registered.append({
            'area_id':z['area_id'],'era_year':z['era_year'],
            'historical_name':z['historical_name'],
            'source_id':z['source_id'],'geometry':outline,
            'coordinate_frame':z['coordinate_frame'],
            'horizontal_crs':z['horizontal_crs'],
            'vertical_datum':z['vertical_datum'],
            'status':z['location_status']
        })
    contextual=[z for z in zones if z['location_status'] not in ('MAP_TRACED','SITE_REGISTERED')]
    (out/'mapped_gardens_local.json').write_text(
        json.dumps({'schema':'fmp.horticulture.local-polygons.v1',
                    'warning':'Coordinates are model/site-local and NOT automatically WGS84',
                    'areas':registered},indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        encoding='utf-8')
    (out/'mapped_individual_plants.json').write_text(
        json.dumps({'schema':'fmp.horticulture.mapped-plants.v1',
                    'warning':'Only sourced, date-specific positions, never random vegetation',
                    'instances':plant_instances},indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        encoding='utf-8')
    (out/'unlocated_gardens.json').write_text(
        json.dumps({'schema':'fmp.horticulture.research-zones.v1',
                    'warning':'Named zones are NOT surveyed maps or 3D planting locations',
                    'areas':contextual},indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        encoding='utf-8')
    (out/'seasonal_change_log.json').write_text(
        json.dumps({'schema':'fmp.horticulture.season-events.v1',
                    'warning':'Only cited dates are emitted; flowering calendar is not inferred',
                    'events':events},indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        encoding='utf-8')
    (out/'inter_era_planting_links.json').write_text(
        json.dumps({'schema':'fmp.horticulture.era-links.v1',
                    'warning':'Area relationships are not identity-level tree survivorship proof',
                    'links':lineage},indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        encoding='utf-8')
    write_csv(out/'documented_irrigation_links.csv',irrigation_links,
             ['irrigation_link_id','area_id','network_layer_id','segment_id',
              'source_id','linkage_status','equipment_description','notes'])
    write_csv(out/'source_acquisition_queue.csv',sources,
             ['source_id','era_year','title','repository','source_url','archive_locator',
              'document_date','source_class','access_status','historical_status',
              'rights_status','notes'])
    write_csv(out/'planting_schedule.csv',plants,
             ['planting_id','era_year','area_id','area_name','taxon_id','botanical_name',
              'scientific_name','taxonomic_precision','display_label','planting_role',
              'installation_status','quantity','quantity_basis','variety_count',
              'cultivar_name','seasonal_window','growing_pattern','source_id',
              'estimated_height_m','unreal_layer','note'])
    write_csv(out/'zone_completion_queue.csv',queue,
             ['area_id','era_year','historical_name','area_kind','location_status',
              'source_id','planting_records','identified_planting_records',
              'installed_description_count'])
    metrics={'schema':'fmp.horticulture-summary.v1',
             'source_records':len(sources),
             'identified_taxa':db.execute("SELECT COUNT(*) FROM horticulture_taxa").fetchone()[0],
             'dated_garden_areas':len(zones),
             'planting_observations':len(plants),
             'historical_season_events':len(events),
             'era_relationships':len(lineage),
             'site_registered_or_traced_areas':len(registered),
             'unlocated_or_named_areas':len(contextual),
             'usable_historic_plant_centers':len(plant_instances),
             'documented_or_candidate_irrigation_links':len(irrigation_links),
             'historical_accuracy_status':'RESEARCH_STAGE_NOT_GEOREGISTERED',
             'geometry_output_policy':'No species placements without georeferenced dated plans',
             'priority_source':'LIU Myaida Nippon Garden 1939 plans; NYPL 1939 landscape; NYPL 1964 planting files'}
    (out/'horticulture_progress.json').write_text(
        json.dumps(metrics,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return metrics

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    with sqlite3.connect(args.database) as db:
        print(json.dumps(export_horticulture(db,args.out),indent=2))
