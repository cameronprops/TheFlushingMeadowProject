#!/usr/bin/env python3
"""Validate Theme Center neighbor research records without promoting evidence to geometry."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDINGS = ROOT / "catalog/theme_center_neighbor_buildings_1939_v001.csv"
SOURCES = ROOT / "catalog/theme_center_neighbor_sources_1939_v001.csv"
VALID_PLANS = {"NOT_LOCATED", "NOT_VERIFIED", "PLAN_HOLDING_CONFIRMED", "EXHIBIT_DESIGN_DRAWING_ONLY", "ARCHITECTURAL_SHEETS_LISTED"}
VALID_GEO = {"NOT_BUILT", "PROVISIONAL_SHELL"}

def validate(building_path=BUILDINGS, source_path=SOURCES):
    with open(building_path, encoding="utf-8", newline="") as f:
        buildings=list(csv.DictReader(f))
    with open(source_path, encoding="utf-8", newline="") as f:
        sources=list(csv.DictReader(f))
    assert buildings and sources, "Empty research register"
    keys=[b["building_key"] for b in buildings]
    assert len(keys)==len(set(keys)), "Duplicate building keys"
    ids=[b["existing_place_id"] for b in buildings if b["existing_place_id"]!="UNASSIGNED"]
    assert len(ids)==len(set(ids)), "Duplicate assigned place IDs"
    for b in buildings:
        assert b["plans_status"] in VALID_PLANS, b
        assert b["model_status"] in VALID_GEO, b
        assert b["site_registration"]=="UNREGISTERED", b
        assert b["next_model_gate"].strip(), b
    source_ids=[s["source_id"] for s in sources]
    assert len(source_ids)==len(set(source_ids)), "Duplicate sources"
    for s in sources:
        assert s["building_key"] in set(keys)|{"ALL"}, s
        assert s["source_url"].startswith("https://"), s
        assert s["role"].strip() and s["access_status"].strip(), s
    return {"building_count":len(buildings),"source_count":len(sources),
            "unassigned_identity_count":sum(b["existing_place_id"]=="UNASSIGNED" for b in buildings),
            "geometry_certified_count":0}

if __name__=="__main__":
    import json
    print(json.dumps(validate(), indent=2))
