(* Run with wolframscript from the repository root. Network needed only at last gate. *)
Get["tools/world_build/nypl_exposed_steel_screen_v001.wl"];
rec = Import["research/pavilions/theme_center/NYPL_EXPOSED_STEEL_SCREEN_v001.json", "RawJSON"];
pass = 0; fail = 0;
test[label_, cond_] := If[TrueQ[cond], pass++; Print["PASS ", label],
   fail++; Print["FAIL ", label]];
a = FMPConstructionCircleFit[rec];
test["six real pixel picks accepted for screen-space review",
   a["status"] === "SCREENSPACE_FIT_REVIEW_REQUIRED"];
test["four fit two heldout", a["fit_count"] === 4 && a["holdout_count"] === 2];
test["screen-space center close to reviewed estimate",
   Norm[a["center_xy_px"] - {300.5123375, 549.5695240}] < 0.2];
test["held-out rim residual bounded", Max[Abs[a["holdout_signed_errors_px"]]] < 2];
test["no 3D certification", a["historical_geometry_release_allowed"] === False];
b = Association[rec]; b["observations"] = Take[rec["observations"], 4];
test["no holdouts rejected", FMPConstructionCircleFit[b]["status"] ===
 "INSUFFICIENT_INDEPENDENT_CONTROLS"];
b = Association[rec];
b["observations"] = ReplacePart[rec["observations"], 6 ->
 Join[rec["observations"][[6]], <|"pixel_xy" -> {500, 680}|>]];
test["wrong held-out landmark rejected",
 FMPConstructionCircleFit[b]["status"] === "HOLDOUT_REJECTED"];
b = Association[rec];
b["observations"] = ReplacePart[rec["observations"], 6 ->
 Join[rec["observations"][[6]], <|"pixel_uncertainty_px" -> 0|>]];
test["zero uncertainty rejected",
 FMPConstructionCircleFit[b]["status"] === "INVALID_PIXEL_OBSERVATION"];
b = Association[rec]; b["decoded_pixel_sha256"] = "corrupted";
test["source digest change rejected",
 FMPVerifyNYPLConstructionPhoto[b]["status"] === "SOURCE_PIXEL_DIGEST_CHANGED"];
a = FMPVerifyNYPLConstructionPhoto[rec];
test["NYPL original derivative decoded and hashed", TrueQ[a["source_pixels_checked"]]];
test["image never certifies steel", a["truss_nodes_verified"] === False];
Print["TOTAL_PASS=", pass, " TOTAL_FAIL=", fail];
If[fail > 0, Exit[1]];
