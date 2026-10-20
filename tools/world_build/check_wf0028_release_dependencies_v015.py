#!/usr/bin/env python3
"""Fail closed if a WF0028 v015 source archive lacks required inputs."""
from pathlib import Path
REQUIRED=[
 "build_wf0028.py","build_wf0028_v002.py","build_wf0028_v003.py",
 "build_wf0028_v009.py","build_wf0028_v011.py","build_wf0028_v013.py",
 "build_wf0028_v015.py","audit_threshold_v010.py","audit_threshold_v011.py",
 "audit_fullwidth_v012.py","test_wf0028_v015.py",
 "out_wf0028_v009/WF0028_1939_Interpretive_Complex_v009.glb",
 "out_wf0028_v009/WF0028_1939_Interpretive_Complex_v009.json",
 "out_wf0028_v011/WF0028_1939_Interpretive_Complex_v011.glb",
 "out_wf0028_v011/WF0028_1939_Interpretive_Complex_v011.json",
 "out_wf0028_v013/WF0028_1939_Interpretive_Complex_v013.glb",
 "out_wf0028_v015/WF0028_1939_Interpretive_Complex_v015.glb"]
def audit(root):
 missing=[n for n in REQUIRED if not (Path(root)/n).is_file() or not (Path(root)/n).stat().st_size]
 if missing:raise RuntimeError("Incomplete WF0028 release: "+", ".join(missing))
 return {"status":"PASS","count":len(REQUIRED)}
if __name__=="__main__":
 print(audit(Path(__file__).resolve().parent))
