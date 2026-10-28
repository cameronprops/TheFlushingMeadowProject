#!/usr/bin/env python3
"""Candidate frame correspondences; never a certified metric camera solve."""
import argparse,csv,json,hashlib
from pathlib import Path
import cv2,numpy as np
def match_pair(a,b):
 orb=cv2.ORB_create(nfeatures=3000)
 ka,da=orb.detectAndCompute(cv2.cvtColor(a,cv2.COLOR_BGR2GRAY),None)
 kb,db=orb.detectAndCompute(cv2.cvtColor(b,cv2.COLOR_BGR2GRAY),None)
 if da is None or db is None:return {'matches':0,'inliers':0,'status':'INSUFFICIENT_FEATURES'}
 groups=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da,db,k=2)
 ms=[m for g in groups if len(g)==2 for m,n in [g] if m.distance<.75*n.distance]
 if len(ms)<8:return {'matches':len(ms),'inliers':0,'status':'INSUFFICIENT_MATCHES'}
 pa=np.float32([ka[m.queryIdx].pt for m in ms]).reshape(-1,1,2)
 pb=np.float32([kb[m.trainIdx].pt for m in ms]).reshape(-1,1,2)
 H,mask=cv2.findHomography(pa,pb,cv2.RANSAC,3.)
 if H is None or mask is None:return {'matches':len(ms),'inliers':0,'status':'NO_STABLE_HOMOGRAPHY'}
 count=int(mask.sum());fraction=count/len(ms)
 err=np.linalg.norm((cv2.perspectiveTransform(pa,H)-pb).reshape(-1,2),axis=1)
 med=float(np.median(err[mask.ravel().astype(bool)])) if count else None
 return {'matches':len(ms),'inliers':count,'homography_inlier_fraction':round(fraction,4),'median_reprojection_px':round(med,3) if med is not None else None,'status':'PLANAR_OR_ROTATIONAL_AMBIGUITY' if fraction>=.7 else 'NONPLANAR_CANDIDATE_REQUIRES_MANUAL_REVIEW'}
def inspect(folder,out,spacing=1):
 frames=sorted(Path(folder).glob('frame_*.png'))
 if len(frames)<spacing+1:raise ValueError('Not enough frames')
 out=Path(out);out.mkdir(parents=True,exist_ok=True);rows=[]
 for i in range(len(frames)-spacing):
  a,b=frames[i],frames[i+spacing];im1=cv2.imread(str(a));im2=cv2.imread(str(b))
  if im1 is None or im2 is None:raise ValueError('Unreadable frame')
  rows.append({'frame_a':a.name,'frame_b':b.name,**match_pair(im1,im2)})
 with (out/'pair_diagnostics.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (out/'pair_gate.json').write_text(json.dumps({'status':'CANDIDATE_ONLY','historical_depth_solved':False,'camera_baseline_verified':False,'source_checksums':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in frames}},indent=2))
 return rows
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('frames');p.add_argument('output');p.add_argument('--spacing',type=int,default=1);a=p.parse_args();print(inspect(a.frames,a.output,a.spacing))
