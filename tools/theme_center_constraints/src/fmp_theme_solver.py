#!/usr/bin/env python3
"""1939 NY World's Fair Theme Center fact-gated constraint solver.

Pure Python 3.9+ standard library. No historic geometry is inferred from
unverified or blocked source facts. JSON data is a frozen, SHA-bound export
of the BIM-ready master; conversion script is separate from the runtime.
"""
import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

FT_TO_MM = 304.8
FT_TO_CM = 30.48
FT_TO_M = 0.3048
SOLVER_ID = "FMP_THEME_CENTER_CONSTRAINT_SOLVER_V0_1"
WORKBOOK_SHA256 = "ae7a3f3443e0966e9d1acbb7fc4e8c406328eab80b99976a18f9b1d036c54acb"
AUTHORIZED = {"VERIFIED_AS_BUILT", "DERIVED_FROM_VERIFIED_AS_BUILT"}
VALID_STATUSES = AUTHORIZED | {"PROVISIONAL", "HOLD", "UNKNOWN", "RESEARCH_PREVIEW"}
SCHEMA = "fmp.theme-center.solver/0.1"


class TruthError(ValueError):
    """A factual inconsistency or an inadmissible source value."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(actual: float, expected: float, tolerance=1e-8) -> bool:
    return math.isclose(float(actual), float(expected), abs_tol=tolerance, rel_tol=0)


class Catalog:
    def __init__(self, facts: List[Dict[str, Any]]):
        self.facts = {}
        for fact in facts:
            fid = fact.get("Fact_ID")
            if not re.fullmatch(r"F\d{3}", str(fid)) or fid in self.facts:
                raise TruthError("invalid/duplicate Fact_ID: %r" % fid)
            status = fact.get("Status")
            if status not in VALID_STATUSES:
                raise TruthError("unsupported status on %s: %r" % (fid, status))
            if fact.get("Code_Drive") not in ("YES", "NO"):
                raise TruthError("invalid Code_Drive on %s" % fid)
            if fact.get("Code_Drive") == "YES" and status not in AUTHORIZED:
                raise TruthError("unsafe auto-drive flag on %s" % fid)
            self.facts[fid] = fact
        if len(self.facts) != 68:
            raise TruthError("expected 68 reference facts, found %d" % len(self.facts))

    def fact(self, fid: str) -> Dict[str, Any]:
        if fid not in self.facts:
            raise TruthError("missing required fact %s" % fid)
        return self.facts[fid]

    def approved(self, fid: str) -> Dict[str, Any]:
        fact = self.fact(fid)
        if fact["Status"] not in AUTHORIZED or fact["Code_Drive"] != "YES":
            raise TruthError("fact %s not approved for final geometry" % fid)
        if not fact.get("Source_IDs"):
            raise TruthError("fact %s missing source provenance" % fid)
        return fact

    def numeric(self, fid: str) -> float:
        fact = self.approved(fid)
        value = fact["Value"]
        if isinstance(value, bool):
            raise TruthError("boolean numeric fact %s" % fid)
        if isinstance(value, (int, float)) and math.isfinite(value):
            return float(value)
        if fid == "F012" and isinstance(value, str):
            match = re.fullmatch(r"\s*(\d+)\s*ft\s*(\d+)\s*in\s*", value)
            if match:
                return int(match[1]) + int(match[2]) / 12.0
        raise TruthError("fact %s is not an exact numeric value: %r" % (fid, value))

    def exact(self, fid: str, expected: float):
        actual = self.numeric(fid)
        if not close(actual, expected):
            raise TruthError("locked %s drifted: %.10g != %.10g" % (fid, actual, expected))

    def count(self, fid: str) -> int:
        n = self.numeric(fid)
        if n < 0 or int(n) != n:
            raise TruthError("fact %s must be nonnegative integer" % fid)
        return int(n)

    def source(self, ids: List[str]):
        return [{"fact_id": fid, "status": self.fact(fid)["Status"],
                 "code_drive": self.fact(fid)["Code_Drive"],
                 "sources": self.fact(fid).get("Source_IDs"),
                 "open_issue": self.fact(fid).get("Open_Issue")}
                for fid in ids]


def load_catalog(path: Path) -> Catalog:
    facts = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(facts, list):
        raise TruthError("master facts snapshot must be a list")
    return Catalog(facts)


def record(element_id: str, kind: str, facts: List[str], geometry: Dict[str, Any],
           geometry_status: str, notes: str, renderable: bool, catalog: Catalog):
    return {"element_id": element_id,
            "kind": kind,
            "geometry_status": geometry_status,
            "renderable": renderable,
            "geometry": geometry,
            "source_facts": catalog.source(facts),
            "notes": notes}


def solve(catalog: Catalog, scale: float = 120) -> Dict[str, Any]:
    if not math.isfinite(scale) or scale <= 0:
        raise TruthError("scale denominator must be finite and positive")
    # Do not quietly accept changes to the audited primary source.
    for fid, num in {"F001":610, "F002":3, "F009":480, "F010":130,
                     "F012":2 + 7/12, "F021":180, "F022":17, "F023":8,
                     "F025":528, "F027":72, "F028":32, "F029":15,
                     "F034":2, "F045":2, "F058":950, "F059":18}.items():
        catalog.exact(fid, num)
    h = catalog.numeric("F001")
    transition = catalog.numeric("F009")
    plate_h = catalog.numeric("F010")
    if not close(h - transition, plate_h):
        raise TruthError("F001-F009 != F010")
    r = catalog.numeric("F021") / 2
    pool_clearance = catalog.numeric("F022")
    ring_r = catalog.numeric("F027") / 2
    if ring_r >= r:
        raise TruthError("ring girder radius must be smaller than shell radius")
    tip_width = catalog.numeric("F012")
    if tip_width <= 0:
        raise TruthError("nonphysical tip width")
    z_center = pool_clearance + r  # Conditional on reflecting pool datum interpretation
    ring_delta_z = math.sqrt(r*r - ring_r*ring_r)
    meridians = catalog.count("F028")
    helicline_length = catalog.numeric("F058")
    helicline_width = catalog.numeric("F059")
    if helicline_width >= helicline_length:
        raise TruthError("implausible helicline dimensions")

    # Source IDs are copied from the actual BIM element registry, not new inferred UUIDs.
    elements = [
        record("TP-PERI", "exterior_sphere", ["F021", "F022"], {
            "diameter_ft":2*r, "radius_ft":r, "center_relative_pool_ft":[0,0,z_center],
            "shell_thickness_ft":None,
            "coordinate_frame":"THEME_CENTER_LOCAL_POOL_DATUM_UNPLACED",
            "placement_certainty":"CONDITIONAL_DATUM; SITE_XY_UNKNOWN"},
            "VERIFIED_RADIUS_CONDITIONAL_Z", "Full sphere envelope only, not as-built shell thickness or interior structure. F022 pool datum remains an open issue.", True, catalog),
        record("TP-TRYLON", "triangular_tower", ["F001", "F002", "F009", "F010", "F012"], {
            "total_height_ft":h, "sides":catalog.count("F002"),
            "frame_to_plate_transition_ft":transition, "plate_height_ft":plate_h,
            "tip_width_ft":tip_width, "base_footprint_ft":None,
            "plate_base_width_ft":None, "site_xy_ft":None},
            "PARTIAL_VERIFIED_UNDERDETERMINED", "No closed Trylon envelope without base dimensions. F011 is an inequality (<15 ft), not an exact width.", False, catalog),
        record("TP-PERI", "ring_girder", ["F027"], {
            "diameter_ft":2*ring_r, "elevation_ft":None,
            "possible_shell_intersection_z_ft":[z_center-ring_delta_z,z_center+ring_delta_z]},
            "UNDERDETERMINED", "Intersection elevations are conditional mathematical candidates, NOT the historical ring elevation.", False, catalog),
        record("TP-PERI", "meridian_truss_array", ["F028"], {
            "count":meridians, "azimuths_deg":None,
            "uniform_spacing_preview_deg":360/meridians},
            "COUNT_VERIFIED_POSITIONS_UNKNOWN", "11.25 deg assumes uniform spacing; not certified from source.", False, catalog),
        record("TP-PERI", "horizontal_truss_array", ["F029"], {
            "count":catalog.count("F029"), "latitudes_deg":None},
            "COUNT_VERIFIED_POSITIONS_UNKNOWN", "No arbitrary truss-latitude grid in final geometry.", False, catalog),
        record("TP-PERI", "tubular_supports", ["F023", "F024"], {
            "count":catalog.count("F023"), "section":"TUBULAR_STEEL",
            "diameter_ft":None,"xyz_positions_ft":None},
            "COUNT_FAMILY_VERIFIED_POSITIONS_UNKNOWN", "No evenly spaced support columns until footprint is sourced.", False, catalog),
        record("TP-HELI", "ramp", ["F058", "F059", "F060"], {
            "path_length_ft":helicline_length, "width_ft":helicline_width,
            "centerline_points_ft":None,"sweep_deg":None,"slope":None},
            "MEASUREMENTS_VERIFIED_PATH_UNDERDETERMINED", "950 ft and 18 ft do not determine path, gradient, endpoint, or 270 degree sweep.", False, catalog),
        record("TP-BRIDGE-001", "connecting_bridge", ["F048", "F049"], {
            "exists":True, "expansion_joints":"AT_BOTH_STRUCTURAL_INTERFACES",
            "span_ft":None, "width_ft":None, "entry_elevations_ft":None},
            "EXISTENCE_VERIFIED_GEOMETRY_UNKNOWN", "Provisional F047 52/64-ft entrance heights are NOT geometric driving inputs.", False, catalog),
    ]
    # Expand grouped truss/column constraints onto their ACTUAL registered BIM
    # member IDs. Reusing the TP-PERI assembly ID would lose identity on export.
    expanded = []
    for element in elements:
        if element["kind"] == "ring_girder":
            element["element_id"] = "TP-PERI-RING-001"
            expanded.append(element)
        elif element["kind"] == "meridian_truss_array":
            for index in range(1, meridians + 1):
                member = dict(element)
                member["element_id"] = "TP-PERI-MER-%03d" % index
                member["kind"] = "meridian_truss"
                member["geometry"] = {"azimuth_deg":None, "member_index":index,
                                      "member_count":meridians,
                                      "uniform_spacing_preview_deg":360/meridians}
                expanded.append(member)
        elif element["kind"] == "horizontal_truss_array":
            for index in range(1, catalog.count("F029") + 1):
                member = dict(element)
                member["element_id"] = "TP-PERI-HRING-%03d" % index
                member["kind"] = "horizontal_truss"
                member["geometry"] = {"latitude_deg":None, "elevation_ft":None,
                                      "member_index":index, "member_count":catalog.count("F029")}
                expanded.append(member)
        elif element["kind"] == "tubular_supports":
            for index in range(1, catalog.count("F023") + 1):
                member = dict(element)
                member["element_id"] = "TP-PERI-COL-%03d" % index
                member["kind"] = "tubular_support"
                member["geometry"] = {"column_index":index, "count":catalog.count("F023"),
                                      "material_family":"TUBULAR_STEEL", "diameter_ft":None,
                                      "xyz_position_ft":None}
                expanded.append(member)
        else:
            expanded.append(element)
    elements = expanded
    if len({obj["element_id"] for obj in elements}) != len(elements):
        raise TruthError("duplicate element IDs in exported geometry")
    counts = Counter(f["Status"] for f in catalog.facts.values())
    blocked = [f["Fact_ID"] for f in catalog.facts.values()
               if f["Status"] not in AUTHORIZED or f["Code_Drive"] != "YES"]
    missing = [
        {"id":"GAP-TRYLON-BASE", "priority":"P0", "blocked_elements":["TP-TRYLON"], "needed":"as-built base triangular vertex locations/profile and site XY", "facts":["F011"]},
        {"id":"GAP-BRIDGE-SECTION", "priority":"P0", "blocked_elements":["TP-BRIDGE-001"], "needed":"as-built bridge endpoints, width, cross-section and floor elevations", "facts":["F047","F048","F049"]},
        {"id":"GAP-HELICLINE-PATH", "priority":"P0", "blocked_elements":["TP-HELI"], "needed":"georeferenced ramp route/control points, endpoint elevation, grade, sweep", "facts":["F058","F059"]},
        {"id":"GAP-PERI-TRUSS-STATIONS", "priority":"P1", "blocked_elements":["TP-PERI"], "needed":"meridian azimuths, 15 horizontal truss elevations, ring girder Z", "facts":["F027","F028","F029"]},
        {"id":"GAP-POOL-DATUM", "priority":"P1", "blocked_elements":["TP-PERI"], "needed":"confirm 17-ft clearance referenced to modeled water level", "facts":["F022"]},
        {"id":"GAP-PERI-SHELL-DEPTH", "priority":"P1", "blocked_elements":["TP-PERI"], "needed":"historical skin thickness and truss sectional dimensions", "facts":["F031","F032","F033"]},
        {"id":"GAP-SITE-TRANSFORM", "priority":"P0", "blocked_elements":["TP-PERI","TP-TRYLON","TP-HELI","TP-BRIDGE-001"], "needed":"site control points to transform Theme Center coordinates into fairground coordinates", "facts":[]},
    ]
    calculations = {
        "trylon_height_ft":h, "trylon_frame_height_ft":transition,
        "trylon_plate_height_ft":plate_h,"trylon_tip_width_ft":tip_width,
        "perisphere_radius_ft":r,
        "perisphere_sphere_center_z_from_pool_ft_conditional":z_center,
        "perisphere_lower_elevation_from_pool_ft_conditional":pool_clearance,
        "perisphere_ring_shell_intersection_z_ft_hypothetical":[z_center-ring_delta_z,z_center+ring_delta_z],
        "uniform_meridian_pitch_deg_preview":360/meridians,
        "helicline_path_length_ft":helicline_length,
        "helicline_width_ft":helicline_width,
        "print_scale_denominator":scale,
        "print_perisphere_diameter_mm":2*r*FT_TO_MM/scale,
        "print_trylon_height_mm":h*FT_TO_MM/scale,
        "print_helicline_developed_length_mm":helicline_length*FT_TO_MM/scale,
        "print_ring_girder_diameter_mm":2*ring_r*FT_TO_MM/scale
    }
    return {"schema":SCHEMA,"solver_id":SOLVER_ID,
            "truth_workbook_sha256":WORKBOOK_SHA256,
            "input_fact_count":len(catalog.facts),
            "fact_status_counts":dict(counts),
            "quarantined_or_non_driving_fact_ids":blocked,
            "checks":{"locked_facts":"PASS", "trylon_height_partition":"PASS",
                      "perisphere_radius_ring_feasibility":"PASS",
                      "unverified_geometry_auto_drive":"BLOCKED"},
            "units":{"historical":"feet", "print":"millimeters", "game_engine":"centimeters", "glb":"meters"},
            "coordinate_frame":"THEME_CENTER_LOCAL_POOL_DATUM_UNPLACED",
            "calculations":calculations,
            "elements":elements,
            "open_constraints":missing}


def game_manifest(result: Dict[str, Any]) -> Dict[str, Any]:
    c = result["calculations"]
    # The current project's v005 *assembled* asset is the scene to extend.
    # Our analytic sphere is ONLY a dimension cross-check, not replacement art.
    return {
        "schema":"fmp.game.asset-handoff/0.1",
        "target_engine":"Unreal Engine; engine-neutral metadata overlay",
        "source_solver":result["solver_id"],
        "historical_truth_sha256":result["truth_workbook_sha256"],
        "period_year":1939,
        "policy":"PRESERVE_EXISTING_ASSEMBLY__NOT_GAME_DEV_VENDOR_APPROVED",
        "current_assembled_scene":{
            "asset":"FMP_ThemeCenter_Assembled_Runtime_v005.glb",
            "sha256":"de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439",
            "manifest_repo_path":"research/pavilions/theme_center/ASSEMBLED_RUNTIME_v005.json",
            "drive_download":"https://drive.google.com/file/d/1OzFZRkHCxN3jMBGwH3Lwdbx0pFJIJhM0/view",
            "historical_pavilion_place_ids":["WF0001","WF0002","WF0003","WF0004","WF0005"],
            "nodes":573,"visible_mesh_nodes":558,
            "input_units":"metres",
            "input_axes":"right-handed Y-up; local coordinates; NOT site registered",
            "must_preserve_meshes_materials_source_node_ids":True,
            "do_not_replace_with_analytic_sphere":True
        },
        "geometry_validation_overlay":{
            "element_id":"TP-PERI",
            "tested_constraint":"F021: Perisphere outside diameter",
            "sphere_radius_uu_cm":round(c["perisphere_radius_ft"]*FT_TO_CM,9),
            "conditional_center_z_uu_cm":round(c["perisphere_sphere_center_z_from_pool_ft_conditional"]*FT_TO_CM,9),
            "comparison_glb_optional":"perisphere_exterior_preview.glb",
            "comparison_only":True,
            "must_not_override_existing_scene":True,
            "final_site_transform":None,
            "collision_policy":"ENGINE_VALIDATION_REQUIRED",
            "navigation_policy":"ENGINE_VALIDATION_REQUIRED"
        },
        "coordinate_warning":"Solver uses conceptual Z-up mathematics and cm. Scene v005 uses Y-up metres. The coordinate transform and site registration are NOT solved here.",
        "unresolved_elements":[{"element_id":obj["element_id"],"kind":obj["kind"],
                                "reason":obj["geometry_status"]}
                               for obj in result["elements"] if not obj["renderable"]],
        "game_development_studio_next_gate":["CLI capabilities/doctor", "asset inspection of existing v005", "provenance/license validation", "canonical package integrity verification", "dry-run project admission"],
        "game_dev_receipts":None,
        "engine_import_tested":False,
        "gpu_render_tested":False,
        "performance_tested":False
    }


def preview_mesh(result: Dict[str, Any], out_path: Path):
    """Export one non-canonical, full-scale Perisphere-envelope GLB in meters.

    Requires trimesh. No ring, trusses, openings, walkable interior, Trylon,
    bridge or guessed ramp can enter this mesh.
    """
    try:
        import trimesh
    except ImportError as exc:
        raise TruthError("optional --preview-glb requires trimesh") from exc
    c = result["calculations"]
    sphere = trimesh.creation.icosphere(subdivisions=3,
                                       radius=c["perisphere_radius_ft"]*FT_TO_M)
    sphere.apply_translation([0,0,c["perisphere_sphere_center_z_from_pool_ft_conditional"]*FT_TO_M])
    if not sphere.is_watertight or not sphere.is_winding_consistent:
        raise TruthError("preview sphere mesh failed manifold/winding gate")
    scene = trimesh.Scene()
    scene.add_geometry(sphere, geom_name="TP-PERI-EXTERIOR-ENVELOPE", node_name="TP-PERI")
    scene.export(str(out_path),file_type="glb")
    return {"path":out_path.name,"watertight":bool(sphere.is_watertight),
            "triangle_count":len(sphere.faces),"vertices":len(sphere.vertices),
            "preview_only":True,"unit":"meters","sha256":sha256(out_path)}


def run():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--facts",type=Path,default=Path(__file__).resolve().parents[1]/"data"/"master_facts.json")
    ap.add_argument("--source-workbook",type=Path,default=None,help="optional SHA256 verification against audited original bytes")
    ap.add_argument("--out",type=Path,default=Path(__file__).resolve().parents[1]/"output")
    ap.add_argument("--scale",type=float,default=120)
    ap.add_argument("--preview-glb",action="store_true",help="generate Perisphere-only GLB preview; not a canonical game-dev asset")
    args=ap.parse_args()
    try:
        if args.source_workbook and sha256(args.source_workbook)!=WORKBOOK_SHA256:
            raise TruthError("source workbook hash mismatch; stop and re-audit the source")
        catalog=load_catalog(args.facts)
        result=solve(catalog,args.scale)
        args.out.mkdir(parents=True,exist_ok=True)
        (args.out/"constraint_report.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
        manifest=game_manifest(result)
        (args.out/"game_handoff.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
        if args.preview_glb:
            mesh_receipt=preview_mesh(result,args.out/"perisphere_exterior_preview.glb")
            (args.out/"preview_mesh_receipt.json").write_text(json.dumps(mesh_receipt,indent=2)+"\n")
        print("PASS: verified facts + derived constraints; %d source facts; %d open research constraints" % (result["input_fact_count"],len(result["open_constraints"])))
        print("Output: %s" % args.out)
        print("Missing data is explicitly withheld from final geometry.")
    except (TruthError, OSError, ValueError) as exc:
        print("FAIL: %s" % exc,file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(run())
