(* Independent photo-frame admission checks for FMP 1939/1940 Theme Center.
   Load theme_center_structural_solver.wl first. No inferred geometry is released. *)
ClearAll[FMPPhotoHoldoutGate, FMPImageSourceProbe];

FMPPhotoHoldoutGate[frame_Association] := Module[
  {required, obs, dims, train, hold, fit, transform, points, errors, ratios, names,
   maxSig = 3., maxPixel = 6., bad, predicted, r},
  required = {"source_id", "frame_id", "source_uri", "annotator",
    "construction_state", "coordinate_contract", "image_size_px", "controls"};
  If[!AllTrue[required, KeyExistsQ[frame, #] &],
    Return[<|"status" -> "MISSING_FRAME_PROVENANCE",
      "missing_fields" -> Select[required, !KeyExistsQ[frame, #] &]|>]];
  If[!AllTrue[{"source_id", "frame_id", "source_uri", "annotator",
      "construction_state", "coordinate_contract"},
      StringQ[Lookup[frame, #]] && StringLength[Lookup[frame, #]] > 0 &],
    Return[<|"status" -> "INVALID_FRAME_PROVENANCE"|>]];
  If[Lookup[frame, "coordinate_contract"] =!=
      "PLAN_XZ_Y_UP_FEET_MODEL_LOCAL_UNREGISTERED",
    Return[<|"status" -> "COORDINATE_FRAME_MISMATCH"|>]];
  dims = Lookup[frame, "image_size_px"];
  If[!MatchQ[dims, {_Integer?Positive, _Integer?Positive}],
    Return[<|"status" -> "INVALID_FRAME_DIMENSIONS"|>]];
  obs = Lookup[frame, "controls"];
  If[!ListQ[obs] || !AllTrue[obs, AssociationQ],
    Return[<|"status" -> "INVALID_CONTROLS"|>]];
  names = Lookup[obs, "landmark_id", Missing["landmark"]];
  If[!AllTrue[names, StringQ[#] && StringLength[#] > 0 &] ||
    Length[DeleteDuplicates[names]] != Length[names],
    Return[<|"status" -> "MISSING_OR_DUPLICATE_LANDMARK_ID"|>]];
  bad = Select[obs,
    !MatchQ[Lookup[#, "model_xy_ft", Null], {_?NumericQ, _?NumericQ}] ||
    !MatchQ[Lookup[#, "image_xy_px", Null], {_?NumericQ, _?NumericQ}] ||
    !TrueQ[NumericQ[Lookup[#, "pixel_uncertainty", Null]] &&
      Lookup[#, "pixel_uncertainty", 0] > 0] ||
    !MemberQ[{"fit", "holdout"}, Lookup[#, "role", Null]] &];
  If[bad =!= {}, Return[<|"status" -> "INVALID_CONTROL_VALUES"|>]];
  If[!AllTrue[obs, With[{p = #["image_xy_px"]},
    0 <= p[[1]] < dims[[1]] && 0 <= p[[2]] < dims[[2]]] &],
    Return[<|"status" -> "IMAGE_POINT_OUT_OF_BOUNDS"|>]];
  train = Select[obs, #["role"] === "fit" &];
  hold = Select[obs, #["role"] === "holdout" &];
  If[Length[train] < 4 || Length[hold] < 2,
    Return[<|"status" -> "INSUFFICIENT_INDEPENDENT_CONTROLS",
      "fit_count" -> Length[train], "holdout_count" -> Length[hold]|>]];
  fit = FMPPhotoPlanFit[train];
  If[fit["status"] =!= "IMAGE_TO_PLAN_FIT_REVIEW_REQUIRED",
    Return[<|"status" -> "FIT_REJECTED",
      "underlying_status" -> fit["status"]|>]];
  transform = fit["plan_to_pixel_homography"];
  predicted = FMPProjectPlanPoint[transform, #["model_xy_ft"]] & /@ hold;
  If[!FreeQ[predicted, _Missing], Return[<|"status" -> "SINGULAR_HOLDOUT_PROJECTION"|>]];
  errors = N[MapThread[EuclideanDistance, {predicted,
      Lookup[hold, "image_xy_px"]}]];
  ratios = N[errors/Lookup[hold, "pixel_uncertainty"]];
  r = <|"fit_count" -> Length[train], "holdout_count" -> Length[hold],
    "fit_rms_px" -> fit["rms_pixels"],
    "holdout_rms_px" -> N[Sqrt[Mean[errors^2]]],
    "holdout_residual_px" -> errors, "holdout_normalized_residual" -> ratios,
    "max_holdout_residual_px" -> Max[errors],
    "max_holdout_sigma" -> Max[ratios],
    "threshold_pixels" -> maxPixel, "threshold_sigma" -> maxSig,
    "camera_pose_3d_solved" -> False,
    "as_built_geometry_certified" -> False,
    "model_update_allowed" -> False,
    "manual_source_review_required" -> True|>;
  Join[<|"status" -> If[Max[errors] <= maxPixel && Max[ratios] <= maxSig,
    "HOLDOUT_PASS_REVIEW_REQUIRED", "HOLDOUT_REJECTED"]|>, r]
];

(* This checks that a referenced image can be read, not its authenticity or
   that any coordinates were recovered. Network availability is optional. *)
FMPImageSourceProbe[url_String] := Module[{im},
  im = Quiet[Check[Import[url, "Image"], $Failed]];
  If[Head[im] =!= Image, Return[<|"status" -> "SOURCE_IMAGE_UNAVAILABLE"|>]];
  <|"status" -> "IMAGE_BYTES_DECODED",
    "image_size_px" -> ImageDimensions[im],
    "channels" -> ImageChannels[im],
    "source_reviewed" -> False,
    "landmarks_measured" -> 0|>
];
