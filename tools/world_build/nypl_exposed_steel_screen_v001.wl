(* FMP NYPL source-constrained construction-photo screen, v001.
   Only a 2D visible Perisphere silhouette is estimated. No 3D as-built release.
   The source image remains at NYPL; no image bytes are redistributed. *)
ClearAll[FMPConstructionCircleFit, FMPVerifyNYPLConstructionPhoto];

FMPConstructionCircleFit[record_Association] := Module[
  {obs, fit, hold, pts, mat, coeff, center, radius, trainErr, holdErr, holdSigma},
  If[!KeyExistsQ[record, "observations"] ||
     !KeyExistsQ[record, "pixel_size"],
    Return[<|"status" -> "MISSING_SOURCE_FIELDS"|>]];
  obs = record["observations"];
  If[!ListQ[obs] || !AllTrue[obs, AssociationQ],
    Return[<|"status" -> "INVALID_OBSERVATIONS"|>]];
  If[Length[Union[Lookup[obs, "id", Missing["ID"]]]] != Length[obs] ||
     !AllTrue[Lookup[obs, "id", Missing["ID"]], StringQ],
    Return[<|"status" -> "DUPLICATE_OR_MISSING_ID"|>]];
  If[!AllTrue[obs,
      MatchQ[Lookup[#, "pixel_xy", Null], {_?NumericQ, _?NumericQ}] &&
      NumericQ[Lookup[#, "pixel_uncertainty_px", Null]] &&
      TrueQ[Lookup[#, "pixel_uncertainty_px", 0] > 0] &&
      MemberQ[{"fit", "holdout"}, Lookup[#, "role", Null]] &],
    Return[<|"status" -> "INVALID_PIXEL_OBSERVATION"|>]];
  If[!AllTrue[obs, With[{q = #["pixel_xy"]},
      0 <= q[[1]] < record["pixel_size"][[1]] &&
      0 <= q[[2]] < record["pixel_size"][[2]]] &],
    Return[<|"status" -> "OUT_OF_IMAGE_BOUNDS"|>]];
  fit = Select[obs, #["role"] === "fit" &];
  hold = Select[obs, #["role"] === "holdout" &];
  If[Length[fit] < 4 || Length[hold] < 2,
    Return[<|"status" -> "INSUFFICIENT_INDEPENDENT_CONTROLS"|>]];
  pts = N[Lookup[fit, "pixel_xy"]];
  mat = Append[#, 1.] & /@ pts;
  If[MatrixRank[mat] < 3,
    Return[<|"status" -> "DEGENERATE_SILHOUETTE"|>]];
  coeff = LeastSquares[mat, -Total[#^2] & /@ pts];
  center = -Take[coeff, 2]/2.;
  radius = Sqrt[Total[center^2] - coeff[[3]]];
  trainErr = (Norm[# - center] - radius) & /@ pts;
  holdErr = (Norm[#["pixel_xy"] - center] - radius) & /@ hold;
  holdSigma = N[Abs[holdErr]/Lookup[hold, "pixel_uncertainty_px"]];
  <|"status" -> If[Max[Abs[holdErr]] <= 8. && Max[holdSigma] <= 2.,
       "SCREENSPACE_FIT_REVIEW_REQUIRED", "HOLDOUT_REJECTED"],
    "center_xy_px" -> N[center], "radius_px" -> N[radius],
    "diameter_px" -> N[2 radius],
    "fit_rms_px" -> N[Sqrt[Mean[trainErr^2]]],
    "holdout_signed_errors_px" -> N[holdErr],
    "holdout_errors_in_sigma" -> holdSigma,
    "fit_count" -> Length[fit], "holdout_count" -> Length[hold],
    "model_3d_position_verified" -> False,
    "truss_nodes_verified" -> False,
    "helicline_supports_verified" -> False,
    "historical_geometry_release_allowed" -> False|>
];

FMPVerifyNYPLConstructionPhoto[record_Association] := Module[
  {url = "https://images.nypl.org/index.php?id=ps_mss_cd23_351&t=w",
   image, pixelDigest, result},
  If[Lookup[record, "source_id", ""] =!= "NYPL_PS_MSS_CD23_351" ||
     Lookup[record, "source_image_uri", ""] =!= url,
    Return[<|"status" -> "SOURCE_ID_MISMATCH"|>]];
  image = Quiet[Check[Import[url, "Image"], $Failed]];
  If[Head[image] =!= Image,
    Return[<|"status" -> "NYPL_IMAGE_UNAVAILABLE"|>]];
  If[ImageDimensions[image] =!= Lookup[record, "pixel_size", {}],
    Return[<|"status" -> "SOURCE_IMAGE_SIZE_CHANGED"|>]];
  pixelDigest = Hash[ImageData[image, "Byte"], "SHA256", "HexString"];
  If[pixelDigest =!= Lookup[record, "decoded_pixel_sha256", ""],
    Return[<|"status" -> "SOURCE_PIXEL_DIGEST_CHANGED"|>]];
  result = FMPConstructionCircleFit[record];
  Join[result, <|"source_pixels_checked" -> True,
    "pixel_digest" -> pixelDigest,
    "archival_photo_date_verified" -> False,
    "source_image_rights_cleared_for_public_republication" -> False,
    "historical_geometry_release_allowed" -> False|>]
];
