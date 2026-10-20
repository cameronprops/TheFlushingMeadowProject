(* Run from repository root with Wolfram: wolframscript -file tests/theme_center_structural_solver_tests.wl *)
Get["tools/world_build/theme_center_structural_solver.wl"];
doc=Import["research/pavilions/theme_center/THEME_CENTER_ASBUILT_CONSTRAINTS_v001.json","RawJSON"];
fail=0;
check[name_,condition_]:=If[TrueQ[condition],
  Print["PASS ",name], Print["FAIL ",name]; fail++];
audit=FMPStructuralAudit[doc];
check["real source-dimension consistency",
  audit["status"]=="DOCUMENTED_COUNTS_AND_DIMENSIONS_CONSISTENT"];
check["historical geometry not falsely certified",
  audit["as_built_geometry_certified"]===False];
check["trylon section arithmetic",
  Abs[audit["historical_checks"]["trylon_vertical_closure_residual_m"]]<10^-9];
bad=Association[doc];
bad["constraints"]=Map[If[#["id"]=="F001",
  Join[#,<|"si_value"->213.36|>],#]&,doc["constraints"]];
badAudit=FMPStructuralAudit[bad];
check["reject obsolete 700ft tower",badAudit["status"]=="BLOCKED"&&
  MemberQ[badAudit["errors"],"DIMENSION_DRIFT_F001"]];
helix=FMPHeliclineHypothesis[270,52];
check["conditional helical math",helix["status"]=="HYPOTHESIS_ONLY"&&
  Abs[helix["centerline_diameter_ft"]-402.5880624308254]<10^-6];
check["reject impossible ramp descent",
  FMPHeliclineHypothesis[270,951]["status"]=="INVALID_HYPOTHESIS"];
src={{0,0},{100,0},{100,60},{0,60},{40,30}};
dst=({120+2#[[1]],50+2#[[2]]}&/@src);
obs=MapThread[<|"model_xy_ft"->#1,"image_xy_px"->#2|>&,{src,dst}];
fit=FMPPhotoPlanFit[obs];
check["synthetic photo-to-plan fit",fit["status"]=="IMAGE_TO_PLAN_FIT_REVIEW_REQUIRED"&&
  fit["rms_pixels"]<10^-6];
check["no automatic camera/3D certification",fit["camera_pose_3d_solved"]===False];
check["insufficient controls blocked",
  FMPPhotoPlanFit[Take[obs,3]]["status"]=="INSUFFICIENT_PLAN_CONTROLS"];
deg=Table[<|"model_xy_ft"->{i,0},"image_xy_px"->{2i+20,90}|>,{i,1,5}];
check["collinear controls blocked",
  FMPPhotoPlanFit[deg]["status"]=="DEGENERATE_CONTROLS"];
Print["Failures: ",fail];
If[fail>0,Exit[1]];
