(* Standalone v002 tests. Run from repository root. *)
Get["tools/world_build/theme_center_structural_solver.wl"];
Get["tools/world_build/theme_center_image_quality_gate_v002.wl"];
testsFailed = 0; testsPassed = 0;
verifyCase[label_,ok_] := If[TrueQ[ok], testsPassed++;
  Print["PASS ",label], testsFailed++; Print["FAIL ",label]];
basePts = {{0,0},{40,0},{80,0},{80,50},{0,50},{20,20},{60,20},{50,40}};
framePoints = Table[<|"landmark_id" -> "synthetic-" <> ToString[i],
  "model_xy_ft" -> basePts[[i]],
  "image_xy_px" -> (N[{160 + 2 basePts[[i,1]], 70 + 2 basePts[[i,2]]}]),
  "pixel_uncertainty" -> 1., "role" -> If[i <= 6,"fit","holdout"]|>,
  {i, 1, Length[basePts]}];
frame = <|"source_id" -> "SYNTHETIC_ONLY", "frame_id" -> "SYNTHETIC_0001",
  "source_uri" -> "fixture:synthetic", "annotator" -> "test",
  "construction_state" -> "SYNTHETIC",
  "coordinate_contract" -> "PLAN_XZ_Y_UP_FEET_MODEL_LOCAL_UNREGISTERED",
  "image_size_px" -> {640,480}, "controls" -> framePoints|>;
passed=FMPPhotoHoldoutGate[frame];
verifyCase["clean independent holdout passes review gate",
  passed["status"] == "HOLDOUT_PASS_REVIEW_REQUIRED"];
verifyCase["two truly independent holdouts", passed["holdout_count"] == 2];
verifyCase["synthetic holdout residual negligible", passed["holdout_rms_px"] < 10^-7];
verifyCase["passing photo never certifies geometry", passed["model_update_allowed"] === False];
outlier = Association[frame];
outlier["controls"] = Map[If[#["landmark_id"] == "synthetic-8",
  Join[#,<|"image_xy_px" -> {270.,180.}|>], #] &, framePoints];
verifyCase["conflicting holdout rejected", FMPPhotoHoldoutGate[outlier]["status"] ==
  "HOLDOUT_REJECTED"];
noHoldout=Association[frame];
noHoldout["controls"] = Take[framePoints,6];
verifyCase["fit-only overfitting rejected",
  FMPPhotoHoldoutGate[noHoldout]["status"] ==
    "INSUFFICIENT_INDEPENDENT_CONTROLS"];
badCoords=Association[frame];
badCoords["coordinate_contract"]="PLAN_XY_METRES_UNKNOWN";
verifyCase["coordinate mixup rejected",
  FMPPhotoHoldoutGate[badCoords]["status"] == "COORDINATE_FRAME_MISMATCH"];
duplicates=Association[frame];
duplicates["controls"] = ReplacePart[framePoints,
  8 -> Join[framePoints[[8]], <|"landmark_id"->"synthetic-7"|>]];
verifyCase["duplicate landmark IDs rejected",
  FMPPhotoHoldoutGate[duplicates]["status"] == "MISSING_OR_DUPLICATE_LANDMARK_ID"];
badPixel=Association[frame];
badPixel["controls"]=ReplacePart[framePoints, 8 ->
  Join[framePoints[[8]], <|"image_xy_px" -> {900.,900.}|>]];
verifyCase["off-image landmark rejected",
  FMPPhotoHoldoutGate[badPixel]["status"] == "IMAGE_POINT_OUT_OF_BOUNDS"];
badUncertainty=Association[frame];
badUncertainty["controls"]=ReplacePart[framePoints,8 ->
  Join[framePoints[[8]], <|"pixel_uncertainty" -> 0.|>]];
verifyCase["zero uncertainty rejected",
  FMPPhotoHoldoutGate[badUncertainty]["status"] == "INVALID_CONTROL_VALUES"];
Print["Pass=", testsPassed," Fail=",testsFailed];
If[testsFailed>0,Exit[1]];
