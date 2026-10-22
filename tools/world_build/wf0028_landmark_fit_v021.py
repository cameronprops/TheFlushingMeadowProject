#!/usr/bin/env python3
"""2D similarity fit ONLY for scanned plans or orthorectified images. No photo camera solve."""
import json,math,sys
import numpy as np
def fit(data):
 c=data.get("controls",[]);h=data.get("holdouts",[])
 if len(c)<3 or not h:return {"status":"INSUFFICIENT_INDEPENDENT_CONTROLS","historical_registration_verified":False}
 ids=[p["id"] for p in c+h]
 if len(ids)!=len(set(ids)):raise ValueError("duplicate point ids")
 if any(not p.get("source_id") for p in c+h):raise ValueError("missing provenance")
 xy=np.array([p["pixel"] for p in c],float)
 if np.linalg.matrix_rank(xy-xy.mean(axis=0))<2:return {"status":"DEGENERATE_CONTROLS","historical_registration_verified":False}
 A=[];B=[]
 for r in c:
  x,y=r["pixel"];u,v=r["local_m"]
  A.extend([[x,-y,1,0],[y,x,0,1]]);B.extend([u,v])
 a,b,tx,ty=np.linalg.lstsq(np.array(A),np.array(B),rcond=None)[0]
 def errors(points):
  return [{"id":r["id"],"source_id":r["source_id"],"residual_m":math.dist([a*r["pixel"][0]-b*r["pixel"][1]+tx,b*r["pixel"][0]+a*r["pixel"][1]+ty],r["local_m"])} for r in points]
 ec=errors(c);eh=errors(h)
 def rms(err):return math.sqrt(sum(x["residual_m"]**2 for x in err)/len(err))
 return {"status":"FIT_COMPUTED_NOT_HISTORICALLY_VERIFIED","scale_m_per_pixel":math.hypot(a,b),"rotation_deg":math.degrees(math.atan2(b,a)),"translation_m":[float(tx),float(ty)],"control_rms_m":rms(ec),"holdout_rms_m":rms(eh),"control_residuals":ec,"holdout_residuals":eh,"historical_registration_verified":False,"limitations":["plan or ortho image only","independent metric controls required","oblique postcards need camera calibration"]}
if __name__=="__main__":
 if len(sys.argv)!=3:raise SystemExit("usage: landmark_fit.py controls.json results.json")
 with open(sys.argv[1]) as f:data=json.load(f)
 with open(sys.argv[2],"w") as f:json.dump(fit(data),f,indent=2)
