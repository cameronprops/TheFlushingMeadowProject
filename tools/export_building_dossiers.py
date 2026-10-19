"""Export a detailed, queryable FMP building construction pack from the SQLite point of truth.

One JSON file per building candidate, links to its source records, a master
building inventory CSV, a four-building public-access alpha shortlist and
a completeness report. Does NOT certify a candidate as a separate building.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import sqlite3
from pathlib import Path

SQL_BUILDINGS = """
SELECT d.*, s.display_name, s.year_candidates, s.candidate_category,
       s.subject_status, s.parent_building_id
FROM building_dossiers d JOIN reconstruction_subjects s
  ON d.building_id=s.subject_id
ORDER BY CASE d.production_priority WHEN 'P1' THEN 1
      WHEN 'P2' THEN 2 ELSE 3 END,
      s.year_candidates, s.display_name
"""
EXPORT_FIELDS = ("building_id","display_name","year_candidates","classification",
                 "production_priority","site_position_status","footprint_status",
                 "baseline_model_status","public_access_status","evidence_count",
                 "interior_space_count","model_release_count","next_action")

def records(conn, query, params=()):
    return [dict(x) for x in conn.execute(query, params).fetchall()]

def next_action(dossier):
    if dossier["classification"] not in ("ARCHITECTURE_LISTED", "CONFIRMED_BUILDING"):
        return "Classify: independent building, exhibit tenant, venue or other subject"
    if not dossier["source_evidence"]:
        return "Locate period primary sources and date/version the building"
    if dossier["site_position_status"] == "UNREGISTERED":
        return "Trace a period site map and record a defensible local placement"
    if dossier["footprint_status"] in ("NOT_TRACED", "DRAWING_LEAD_UNTRACED"):
        return "Trace footprint from a dated plan; record interpretation and tolerance"
    if dossier["public_access_status"] == "INTERIOR_ALPHA_TARGET":
        return "Develop separate walkable interior proxy and collision/nav tests"
    return "Review evidence and advance exterior/entrance modeling"

def export_pack(connection, output_dir: Path):
    connection.row_factory = sqlite3.Row
    target = Path(output_dir)
    target.mkdir(parents=True,exist_ok=True)
    source_rows = records(connection, "SELECT * FROM reconstruction_subjects ORDER BY subject_id")
    buildings = records(connection, SQL_BUILDINGS)
    if not source_rows or not buildings:
        raise ValueError("No imported archive subjects or building candidates")
    if len({r["subject_id"] for r in source_rows}) != len(source_rows):
        raise ValueError("Duplicate subject IDs")
    building_dir = target / "buildings"
    building_dir.mkdir(parents=True, exist_ok=True)
    queue, access = [], []
    for b in buildings:
        building_id = b["building_id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+",building_id):
            raise ValueError("Unsafe archive inventory ID")
        detail = records(connection,"SELECT * FROM building_details WHERE building_id=?",(building_id,))
        evid = records(connection,"SELECT * FROM building_evidence WHERE building_id=? ORDER BY evidence_id",(building_id,))
        rooms = records(connection,"SELECT * FROM building_spaces WHERE building_id=? ORDER BY year,space_id",(building_id,))
        skins = records(connection,"SELECT * FROM building_appearance WHERE building_id=? ORDER BY variant",(building_id,))
        releases = records(connection,"SELECT * FROM building_worklog WHERE building_id=? ORDER BY changed_utc",(building_id,))
        parameters = records(connection,"SELECT * FROM building_geometry_parameters WHERE building_id=? ORDER BY period_year,component_id,parameter_key",(building_id,))
        surfaces = records(connection,"SELECT * FROM building_surface_research WHERE building_id=? ORDER BY period_year,component_selector",(building_id,))
        photographs = records(connection,"SELECT * FROM building_view_observations WHERE building_id=? ORDER BY period_year,view_id",(building_id,))
        if {r["variant"] for r in skins} != {"REALISTIC","STYLIZED"}:
            raise ValueError("Missing shared-geometry appearance variants: "+building_id)
        packet = dict(b)
        packet.update(schema="fmp.building-dossier.v1",
                      is_historically_certified=False,
                      architect_details=detail[0] if detail else None,
                      source_evidence=evid, interior_spaces=rooms,
                      appearances=skins, model_release_history=releases,
                      procedural_parameters=parameters, surface_research=surfaces,
                      photographic_observations=photographs,
                      geometry_format_policy="SHARED_CORE_WITH_REALISTIC_AND_STYLIZED_MATERIALS",
                      alternate_build_targets=["UNREAL","WORLDWRIGHT","RHINO","MINECRAFT_PLANNED"])
        packet["next_action"]=next_action(packet)
        (building_dir/(building_id+".json")).write_text(
            json.dumps(packet,indent=2,ensure_ascii=False,allow_nan=False)+"\n",
            encoding="utf-8")
        row={k:packet.get(k) for k in EXPORT_FIELDS}
        row["evidence_count"]=len(evid)
        row["interior_space_count"]=len(rooms)
        row["model_release_count"]=len(releases)
        row["next_action"]=packet["next_action"]
        queue.append(row)
        if b["public_access_status"]=="INTERIOR_ALPHA_TARGET":
            access.append(packet)
    with (target/"master_building_queue.csv").open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=EXPORT_FIELDS)
        writer.writeheader()
        writer.writerows(queue)
    with (target/"all_research_subjects.csv").open("w",encoding="utf-8",newline="") as f:
        cols=("subject_id","display_name","candidate_category","year_candidates","subject_status","parent_building_id")
        writer=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore")
        writer.writeheader()
        writer.writerows(source_rows)
    by_class={}
    for b in buildings:
        by_class[b["classification"]]=by_class.get(b["classification"],0)+1
    summary=dict(schema="fmp.building-build-report.v1",
                 research_subjects=len(source_rows),building_candidates=len(buildings),
                 candidate_types=by_class,
                 detailed_dossiers=sum(bool(records(connection,"SELECT 1 FROM building_details WHERE building_id=?",
                                                      (b["building_id"],))) for b in buildings),
                 attached_source_references=sum(row["evidence_count"] for row in queue),
                 indexed_interior_spaces=sum(row["interior_space_count"] for row in queue),
                 researched_geometry_parameters=connection.execute("SELECT count(*) FROM building_geometry_parameters").fetchone()[0],
                 researched_surface_records=connection.execute("SELECT count(*) FROM building_surface_research").fetchone()[0],
                 photographic_reference_records=connection.execute("SELECT count(*) FROM building_view_observations").fetchone()[0],
                 unresolved_visual_identification_leads=connection.execute("SELECT count(*) FROM unidentified_visual_leads WHERE status='UNIDENTIFIED'").fetchone()[0],
                 accessible_alpha_targets=[b["building_id"] for b in access],
                 source_caveat="Archive candidate names are not certified separate buildings; many are exhibits or venues.",
                 acceptance_gate="No building ready for visitors until local scale, collision, exit and navigation are engine-tested")
    (target/"building_program_summary.json").write_text(
        json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    unresolved=records(connection,"SELECT * FROM unidentified_visual_leads ORDER BY lead_id")
    (target/"unidentified_landmarks.json").write_text(
        json.dumps(unresolved,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (target/"accessibility_pilots.json").write_text(
        json.dumps([dict(building_id=b["building_id"],name=b["display_name"],
                         source_count=len(b["source_evidence"]),
                         spaces=b["interior_spaces"],appearance_variants=b["appearances"],
                         collision_tested=False,unreal_host_tested=False,
                         next_action=b["next_action"]) for b in access],
                  indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return summary

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database",type=Path,default=Path("out/flushing_meadows.sqlite"))
    parser.add_argument("--output-dir",type=Path,default=Path("out/building_program"))
    args=parser.parse_args()
    with sqlite3.connect(args.database) as connection:
        summary=export_pack(connection,args.output_dir)
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
