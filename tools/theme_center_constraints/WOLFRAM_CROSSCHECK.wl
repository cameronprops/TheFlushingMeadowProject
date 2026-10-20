(* Independent Wolfram constraint check for master truth snapshot. *)
ClearAll[trylonHeight, frameTransition, plateHeight, sphereDiameter, poolClearance, ringDiameter, meridians, heliclineLength, heliclineWidth];
trylonHeight = 610;
frameTransition = 480;
plateHeight = 130;
sphereDiameter = 180;
poolClearance = 17;
ringDiameter = 72;
meridians = 32;
heliclineLength = 950;
heliclineWidth = 18;
centerHeight = poolClearance + sphereDiameter/2;
ringCandidateZ = centerHeight + {-1, 1} Sqrt[(sphereDiameter/2)^2 - (ringDiameter/2)^2];
checks = <|
  "TrylonTransition" -> (trylonHeight - frameTransition == plateHeight),
  "SphereCenterRelativePool_ft_Conditional" -> centerHeight,
  "RingGirderPossibleSphereIntersectionZ_ft_NotHistorical" -> N[ringCandidateZ, 10],
  "UniformMeridianPitchDegrees_NotVerifiedAsBuilt" -> 360/meridians,
  "HeliclinePathUniquelyConstrainedByLengthAndWidth" -> False,
  "Scale120PerisphereDiameter_mm" -> sphereDiameter * (3048/10)/120,
  "Scale120TrylonHeight_mm" -> trylonHeight * (3048/10)/120,
  "Scale120HeliclineDevelopedLength_mm" -> heliclineLength * (3048/10)/120
|>;
checks
