(* Read-only 1939 Theme Center structural and planar-photo solver.
   Source: research/pavilions/theme_center/THEME_CENTER_ASBUILT_CONSTRAINTS_v001.json.
   No inferred geometry is automatically promoted to historical evidence. *)
ClearAll[FMPStructuralAudit, FMPHeliclineHypothesis, FMPProjectPlanPoint, FMPPhotoPlanFit];

FMPStructuralAudit[doc_Association] := Module[
  {records, facts, locked, errors = {}, r, v, ev, diameter, n, ring, sphereR, clearance},
  records = Lookup[doc, "constraints", {}];
  If[!ListQ[records], Return[<|"status" -> "INVALID_SCHEMA"|>]];
  facts = Association[Map[#["id"] -> # &, records]];
  locked = <|"F001" -> 185.928, "F009" -> 146.304, "F010" -> 39.624,
    "F012" -> 0.7874, "F021" -> 54.864, "F022" -> 5.1816,
    "F023" -> 8, "F025" -> 528, "F027" -> 21.9456,
    "F028" -> 32, "F029" -> 15, "F058" -> 289.56, "F059" -> 5.4864|>;
  Do[
    r = Lookup[facts, id, Missing["Absent"]];
    If[MissingQ[r], AppendTo[errors, "MISSING_" <> id],
      v = Lookup[r, "si_value", Null];
      ev = Lookup[r, "evidence_status", ""];
      If[!MemberQ[{"BUILT_PERIOD_DOCUMENTED", "WORKBOOK_REVIEWED"}, ev],
        AppendTo[errors, "NOT_VERIFIED_" <> id]];
      If[!NumericQ[v] || Abs[N[v] - N[locked[id]]] > 0.00001,
        AppendTo[errors, "DIMENSION_DRIFT_" <> id]]
    ],
    {id, Keys[locked]}
  ];
  If[Lookup[doc, "period_year", Missing[]] =!= 1939,
    AppendTo[errors, "ERA_MISMATCH"]];
  If[Lookup[doc, "assembly_id", ""] =!= "FMP_THEME_CENTER_1939",
    AppendTo[errors, "ASSET_ID_MISMATCH"]];
  If[errors =!= {},
    Return[<|"status" -> "BLOCKED", "errors" -> DeleteDuplicates[errors],
      "as_built_geometry_certified" -> False|>]];
  diameter = locked["F021"]; n = locked["F028"]; ring = locked["F027"];
  sphereR = diameter/2; clearance = locked["F022"];
  <|"status" -> "DOCUMENTED_COUNTS_AND_DIMENSIONS_CONSISTENT",
    "as_built_geometry_certified" -> False,
    "historical_checks" -> <|
      "trylon_vertical_closure_residual_m" ->
        N[locked["F009"] + locked["F010"] - locked["F001"]],
      "perisphere_meridian_count" -> n,
      "perisphere_horizontal_truss_count" -> locked["F029"],
      "perisphere_support_column_count" -> locked["F023"],
      "helicline_length_m" -> locked["F058"],
      "helicline_width_m" -> locked["F059"]|>,
    "idealized_not_as_built" -> <|
      "uniform_meridian_pitch_deg" -> N[360/n],
      "uniform_meridian_equator_arc_m" -> N[Pi diameter/n],
      "sphere_surface_lower_intersection_ring_height_m" ->
        N[clearance + sphereR - Sqrt[sphereR^2 - (ring/2)^2]]|>,
    "unresolved" -> {
      "Trylon bay elevations and bracing connectivity",
      "Trylon base steel footprint and plate-section transition width",
      "Perisphere horizontal truss stations and connections",
      "Ring girder real position and structural depth",
      "Helicline plan, slope, supports and site registration"}|>
];

FMPHeliclineHypothesis[sweepDeg_?NumericQ, totalDropFt_?NumericQ] := Module[
  {lengthFt = 950., theta, horizontalFt, radiusFt},
  If[sweepDeg <= 0 || sweepDeg > 720 || Abs[totalDropFt] >= lengthFt,
    Return[<|"status" -> "INVALID_HYPOTHESIS"|>]];
  theta = N[sweepDeg Degree];
  horizontalFt = Sqrt[lengthFt^2 - N[totalDropFt]^2];
  radiusFt = horizontalFt/theta;
  <|"status" -> "HYPOTHESIS_ONLY",
    "centerline_radius_ft" -> N[radiusFt],
    "centerline_diameter_ft" -> N[2 radiusFt],
    "grade_percent_if_constant_grade" -> N[100 Abs[totalDropFt]/horizontalFt],
    "sweep_degrees_assumed" -> N[sweepDeg],
    "total_drop_ft_assumed" -> N[totalDropFt],
    "built_support_locations_verified" -> False|>
];

FMPProjectPlanPoint[h_?MatrixQ, p_List] := Module[{q},
  If[Length[p] != 2, Return[Missing["InvalidPoint"]]];
  q = N[h].Append[N[p], 1.];
  If[Abs[q[[3]]] < 10^-12, Return[Missing["ProjectiveInfinity"]]];
  Take[q, 2]/q[[3]]
];

FMPPhotoPlanFit[obs_List] := Module[
  {src, dst, a, b, coeff, homography, preds, residual, rms},
  If[Length[obs] < 4,
    Return[<|"status" -> "INSUFFICIENT_PLAN_CONTROLS", "minimum" -> 4|>]];
  src = Lookup[obs, "model_xy_ft", Missing["MissingXY"]];
  dst = Lookup[obs, "image_xy_px", Missing["MissingPixel"]];
  If[!AllTrue[Join[src, dst], MatchQ[#, {_?NumericQ, _?NumericQ}] &],
    Return[<|"status" -> "INVALID_CONTROL_POINTS"|>]];
  a = Flatten[MapThread[
    Function[{s, t}, With[{x = s[[1]], y = s[[2]], u = t[[1]], v = t[[2]]},
      {{x, y, 1, 0, 0, 0, -u x, -u y},
       {0, 0, 0, x, y, 1, -v x, -v y}}]], {src, dst}], 1];
  If[MatrixRank[N[a]] < 8,
    Return[<|"status" -> "DEGENERATE_CONTROLS"|>]];
  b = Flatten[dst];
  coeff = LeastSquares[N[a], N[b]];
  homography = Partition[Append[coeff, 1.], 3];
  preds = FMPProjectPlanPoint[homography, #] & /@ src;
  If[!FreeQ[preds, _Missing],
    Return[<|"status" -> "SINGULAR_PROJECTION"|>]];
  residual = MapThread[EuclideanDistance, {preds, dst}];
  rms = N[Sqrt[Mean[residual^2]]];
  <|"status" -> "IMAGE_TO_PLAN_FIT_REVIEW_REQUIRED",
    "plan_to_pixel_homography" -> homography,
    "rms_pixels" -> rms,
    "per_control_residual_px" -> N[residual],
    "controls_used" -> Length[obs],
    "camera_pose_3d_solved" -> False,
    "site_georeferencing_solved" -> False,
    "structural_evidence_promoted" -> False|>
];
