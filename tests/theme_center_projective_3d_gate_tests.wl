(* wolframscript -file tests/theme_center_projective_3d_gate_tests.wl *)
Get["tools/world_build/theme_center_projective_3d_gate_v003.wl"];
fail3=0;pass3=0;
gate3Test[title_,ok_]:=If[TrueQ[ok],pass3++;Print["PASS ",title],
 fail3++;Print["FAIL ",title]];
pts3={{-20,10,-30},{15,20,18},{-12,60,-20},{30,70,10},
 {-25,100,28},{18,110,-18},{10,30,30},{-5,90,-38},{25,55,-25},{-30,30,10}};
camera3={{700.,0.,360.,72000.},{0.,-700.,260.,90000.},{0.,0.,1.,200.}};
obs3=Table[<|"landmark_id"->("synthetic_"<>ToString[i]),
 "model_xyz_m"->pts3[[i]],
 "image_xy_px"->FMPProject3D[camera3,pts3[[i]]],
 "pixel_uncertainty"->1.,"role"->If[i<=8,"fit","holdout"]|>,{i,10}];
base3=<|"source_id"->"SYNTHETIC","frame_id"->"SYNTH_1",
 "source_uri"->"fixture://synthetic","construction_state"->"SYNTHETIC",
 "annotator"->"unit-test","coordinate_contract"->"GLTF_Y_UP_METRES_UNREGISTERED",
 "image_size_px"->{800,600},"controls"->obs3|>;
a3=FMPFrameProjective3DGate[base3];
gate3Test["3D fit synthetic fixture",a3["status"]=="3D_PROJECTIVE_FIT_REVIEW_REQUIRED"];
gate3Test["independent holdout error",a3["holdout_rms_px"]<10^-6];
gate3Test["correct counts",a3["fit_count"]==8&&a3["holdout_count"]==2];
gate3Test["geometry never auto-accepted",a3["historical_geometry_release_allowed"]===False];
mut3=Association[base3];
mut3["controls"]=Map[If[#["landmark_id"]=="synthetic_10",
 Join[#,<|"image_xy_px"->{600.,450.}|>],#]&,obs3];
gate3Test["held-out outlier rejected",FMPFrameProjective3DGate[mut3]["status"]=="HOLDOUT_REJECTED"];
mut3=Association[base3];mut3["controls"]=Take[obs3,8];
gate3Test["missing holdouts rejected",FMPFrameProjective3DGate[mut3]["status"]=="INSUFFICIENT_3D_CONTROLS"];
mut3=Association[base3];mut3["coordinate_contract"]="Z_UP_METRES";
gate3Test["wrong axes rejected",FMPFrameProjective3DGate[mut3]["status"]=="COORDINATE_FRAME_MISMATCH"];
mut3=Association[base3];
mut3["controls"]=Map[Join[#,<|"model_xyz_m"->ReplacePart[#["model_xyz_m"],2->0]|>]&,obs3];
gate3Test["coplanar 3D rejected",FMPFrameProjective3DGate[mut3]["status"]=="COPLANAR_3D_CONTROLS"];
mut3=Association[base3];
mut3["controls"]=ReplacePart[obs3,10->Join[obs3[[10]],<|"landmark_id"->"synthetic_9"|>]];
gate3Test["duplicate IDs rejected",FMPFrameProjective3DGate[mut3]["status"]=="INVALID_LANDMARK_IDS"];
mut3=Association[base3];
mut3["controls"]=ReplacePart[obs3,10->Join[obs3[[10]],<|"pixel_uncertainty"->0.|>]];
gate3Test["zero uncertainty rejected",FMPFrameProjective3DGate[mut3]["status"]=="INVALID_OBSERVATION_FIELDS"];
mut3=Association[base3];
mut3["controls"]=ReplacePart[obs3,10->Join[obs3[[10]],<|"image_xy_px"->{1000.,1000.}|>]];
gate3Test["outside pixel rejected",FMPFrameProjective3DGate[mut3]["status"]=="IMAGE_POINT_OUTSIDE"];
mut3=KeyDrop[base3,"source_uri"];
gate3Test["missing frame provenance rejected",FMPFrameProjective3DGate[mut3]["status"]=="MISSING_PROVENANCE"];
Print["TOTAL_PASS=",pass3," TOTAL_FAIL=",fail3];
If[fail3>0,Exit[1]];