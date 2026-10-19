#!/usr/bin/env python3
"""Fit historical drawing pixels to projected metres. No invented control points."""
import argparse,csv,json,math

def solve3(m,v):
 a=[list(map(float,r))+[float(z)] for r,z in zip(m,v)]
 for i in range(3):
  p=max(range(i,3),key=lambda k:abs(a[k][i]))
  if abs(a[p][i])<1e-10: raise ValueError("Singular or collinear controls")
  a[i],a[p]=a[p],a[i]
  d=a[i][i]; a[i]=[x/d for x in a[i]]
  for j in range(3):
   if j!=i:
    t=a[j][i]; a[j]=[x-t*y for x,y in zip(a[j],a[i])]
 return [a[i][3] for i in range(3)]

def fit(rows):
 controls=[r for r in rows if r["role"]=="control"]
 checks=[r for r in rows if r["role"]=="check"]
 if len(controls)<3 or len(checks)<2: raise ValueError("Need >=3 controls and >=2 independent checks")
 crs={r["crs"].strip() for r in rows}
 if len(crs)!=1 or not next(iter(crs)): raise ValueError("Use one explicit projected CRS")
 m=[[0.]*3 for _ in range(3)]; bx=[0.]*3; by=[0.]*3
 for r in controls:
  v=[float(r["pixel_x"]),float(r["pixel_y"]),1.]
  x,y=float(r["world_x_m"]),float(r["world_y_m"])
  for i in range(3):
   bx[i]+=v[i]*x;by[i]+=v[i]*y
   for j in range(3):m[i][j]+=v[i]*v[j]
 tx,ty=solve3(m,bx),solve3(m,by)
 residuals=[]
 for r in rows:
  v=[float(r["pixel_x"]),float(r["pixel_y"]),1.]
  dx=sum(a*b for a,b in zip(tx,v))-float(r["world_x_m"])
  dy=sum(a*b for a,b in zip(ty,v))-float(r["world_y_m"])
  residuals.append({"id":r["id"],"role":r["role"],"error_m":math.hypot(dx,dy)})
 def rms(role):
  z=[r["error_m"]**2 for r in residuals if r["role"]==role]
  return math.sqrt(sum(z)/len(z))
 return {"crs":next(iter(crs)),"affine_x":tx,"affine_y":ty,"control_rmse_m":rms("control"),
         "check_rmse_m":rms("check"),"residuals":residuals,"certified":False,
         "note":"Numeric fit only; archival provenance and survey validation required."}

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("csv");p.add_argument("--output")
 a=p.parse_args()
 with open(a.csv,encoding="utf-8-sig",newline="") as f:rows=list(csv.DictReader(f))
 required={"id","role","pixel_x","pixel_y","world_x_m","world_y_m","crs"}
 if not rows or not required.issubset(rows[0]):p.error("Missing required CSV columns")
 if any(r["role"] not in ("control","check") for r in rows):p.error("Invalid role")
 result=json.dumps(fit(rows),indent=2)+"\n"
 if a.output:
  with open(a.output,"w",encoding="utf-8") as f:f.write(result)
 else:print(result,end="")
