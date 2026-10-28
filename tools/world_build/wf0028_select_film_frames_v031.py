#!/usr/bin/env python3
"""Rank candidate video frames; does not establish calibrated camera views."""
import argparse,cv2,numpy as np,csv,json,hashlib
from pathlib import Path
def select_frames(path,out,step_seconds=1.,max_frames=20,min_motion=0.015):
 path=Path(path);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 cap=cv2.VideoCapture(str(path))
 if not cap.isOpened():raise ValueError('Unreadable video')
 fps=cap.get(cv2.CAP_PROP_FPS);total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
 if fps<=0:raise ValueError('Invalid fps')
 frames=[];prev=None;stride=max(1,round(fps*step_seconds))
 for i in range(0,total,stride):
  cap.set(cv2.CAP_PROP_POS_FRAMES,i);ok,bgr=cap.read()
  if not ok:continue
  g=cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
  sharp=float(cv2.Laplacian(g,cv2.CV_64F).var())
  small=cv2.resize(g,(160,90))
  motion=float(np.mean(np.abs(small.astype(np.float32)-prev.astype(np.float32)))/255) if prev is not None else 1.
  prev=small;frames.append((i,i/fps,sharp,motion,bgr))
 cap.release()
 valid=[f for f in frames if f[3]>=min_motion];valid.sort(key=lambda f:f[2],reverse=True)
 chosen=sorted(valid[:max_frames],key=lambda f:f[0]);outrows=[];thumbs=[]
 for i,t,sharp,motion,im in chosen:
  name=f'frame_{i:06d}.png';cv2.imwrite(str(out/name),im)
  outrows.append([name,i,round(t,5),round(sharp,3),round(motion,6),'UNVERIFIED_ARCHITECTURAL_CONTENT'])
  th=cv2.resize(im,(320,180));cv2.putText(th,f'frame {i} | {t:.2f}s',(8,22),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),2);thumbs.append(th)
 with (out/'frames.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['file','frame_index','time_s','laplacian_variance','frame_difference','architectural_content_status']);w.writerows(outrows)
 if thumbs:
  w=3;h=(len(thumbs)+w-1)//w;sheet=np.full((h*180,w*320,3),240,np.uint8)
  for j,th in enumerate(thumbs):sheet[(j//w)*180:(j//w+1)*180,(j%w)*320:(j%w+1)*320]=th
  cv2.imwrite(str(out/'contact_sheet.png'),sheet)
 manifest={'video_name':path.name,'video_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'fps':fps,'frame_count':total,'candidate_count':len(chosen),'calibration_performed':False,'accuracy_verified':False}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2));return manifest
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('video');a.add_argument('output');a.add_argument('--step-seconds',type=float,default=.4);a.add_argument('--max-frames',type=int,default=20);opts=a.parse_args();print(select_frames(opts.video,opts.output,opts.step_seconds,opts.max_frames))
