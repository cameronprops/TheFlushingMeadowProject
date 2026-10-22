"""Evidence-first archival camera pose solver: refuses missing 2D/3D image correspondences.

Mathematically aligns an authenticated photograph to known v005 model-space positions.
This is NOT a solved reconstruction; no control points are supplied by default.
Requires a measured or externally calibrated camera intrinsic matrix in pixels.
"""
from __future__ import annotations
import argparse, json,hashlib
from pathlib import Path
import cv2
import numpy as np

SOURCE_SHA='de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439'

class PhotoCalibrationError(ValueError):pass

def solve(data):
    if data.get('model_sha256')!=SOURCE_SHA:raise PhotoCalibrationError('Model GLB identity mismatch')
    if data.get('camera_intrinsics_status')!='MEASURED_OR_CALIBRATED':
        raise PhotoCalibrationError('Measured/calibrated camera intrinsics required')
    provenance=data.get('photo',{})
    if not provenance.get('source_url') or not provenance.get('credit'):
        raise PhotoCalibrationError('Archival photo provenance required')
    if not provenance.get('local_image_sha256'):
        raise PhotoCalibrationError('Hash of actual acquired photograph required')
    if len(provenance['local_image_sha256'])!=64:
        raise PhotoCalibrationError('Invalid image hash')
    rows=data.get('correspondences',[])
    if len(rows)<6:raise PhotoCalibrationError('At least 6 identified 2D/3D correspondences required')
    if len({x.get('feature_id') for x in rows})!=len(rows):
        raise PhotoCalibrationError('Duplicate feature IDs')
    try:
        world=np.asarray([x['world_xyz_m'] for x in rows],dtype=np.float64)
        pixels=np.asarray([x['image_uv_px'] for x in rows],dtype=np.float64)
        matrix=np.asarray(data['camera_matrix_px'],dtype=np.float64)
    except (KeyError,TypeError,ValueError) as ex:
        raise PhotoCalibrationError('Missing or invalid calibration inputs') from ex
    if world.shape!=(len(rows),3) or pixels.shape!=(len(rows),2) or matrix.shape!=(3,3):
        raise PhotoCalibrationError('Expected points Nx3/Nx2 and intrinsic 3x3 matrix')
    if not (np.isfinite(world).all() and np.isfinite(pixels).all() and np.isfinite(matrix).all()):
        raise PhotoCalibrationError('Nonfinite points or camera intrinsics')
    if np.linalg.matrix_rank(world-world.mean(axis=0),tol=1e-6)<3:
        raise PhotoCalibrationError('Control points must be non-coplanar for this conservative solver')
    if abs(np.linalg.det(matrix))<1e-6 or matrix[0,0]<=0 or matrix[1,1]<=0:
        raise PhotoCalibrationError('Degenerate camera calibration')
    imgsize=data.get('image_dimensions_px')
    if not (isinstance(imgsize,list) and len(imgsize)==2 and all(isinstance(v,int) and v>0 for v in imgsize)):
        raise PhotoCalibrationError('Positive source image dimensions required')
    if np.any(pixels<0) or np.any(pixels[:,0]>=imgsize[0]) or np.any(pixels[:,1]>=imgsize[1]):
        raise PhotoCalibrationError('Control points exceed image bounds')
    distortion=np.asarray(data.get('distortion_coefficients',[0,0,0,0,0]),dtype=np.float64).reshape(-1,1)
    if len(distortion) not in (4,5,8) or not np.isfinite(distortion).all():
        raise PhotoCalibrationError('Invalid camera distortion coefficients')
    cv2.setRNGSeed(1939)
    ok,rvec,tvec,inliers=cv2.solvePnPRansac(world,pixels,matrix,distortion,
        flags=cv2.SOLVEPNP_EPNP,iterationsCount=1200,reprojectionError=2.5,confidence=.999)
    if not ok or inliers is None or len(inliers)<6:
        raise PhotoCalibrationError('Photo pose RANSAC unable to fit 6 reliable points')
    inliers=inliers.reshape(-1)
    rvec,tvec=cv2.solvePnPRefineLM(world[inliers],pixels[inliers],matrix,distortion,rvec,tvec)
    rot=cv2.Rodrigues(rvec)[0]
    if np.linalg.det(rot)<.999999 or np.linalg.det(rot)>1.000001:
        raise PhotoCalibrationError('Camera rotation not proper')
    z=(world@rot.T+tvec.reshape(1,3))[:,2]
    if not np.all(z>0):raise PhotoCalibrationError('Some model control points lie behind the fitted camera')
    projected=cv2.projectPoints(world,rvec,tvec,matrix,distortion)[0].reshape(-1,2)
    err=np.linalg.norm(pixels-projected,axis=1)
    if np.max(err[inliers])>3.0:
        raise PhotoCalibrationError('Reprojection error exceeded 3 pixels on inliers')
    if np.quantile(err,.75)>4.0:
        raise PhotoCalibrationError('Most control points do not fit the pose')
    return {'schema':'fmp.photo-camera-pose.v001',
        'status':'PROVISIONAL_CAMERA_POSE_NOT_ARCHITECTURAL_VERIFICATION',
        'source_glb_sha256':SOURCE_SHA,
        'source_image_sha256':provenance['local_image_sha256'],
        'source_url':provenance['source_url'],'credit':provenance['credit'],
        'rotation_world_to_camera':rot.round(12).tolist(),
        'translation_world_to_camera_m':tvec.reshape(3).round(12).tolist(),
        'inliers':len(inliers),'correspondence_count':len(rows),
        'reprojection_rmse_px':float(np.sqrt(np.mean(err[inliers]**2))),
        'reprojection_max_inlier_px':float(max(err[inliers])),
        'world_frame':'right-handed Y-up model-local UNREGISTERED',
        'camera_frame':'OpenCV x-right y-down z-forward',
        'measured_historic_architecture':False,
        'limitations':['Camera pose is provisional; verify image lens and 3D control point identification.',
            'Historical 1939 location and exact bridge soffit remain unmeasured. No geometry is created.']}

def run_file(src,dest):
    obj=json.loads(Path(src).read_text())
    info=obj.get('photo',{}).get('local_image_path')
    if not info or not Path(info).is_file():raise PhotoCalibrationError('Original archival image must be acquired locally')
    digest=hashlib.sha256(Path(info).read_bytes()).hexdigest()
    if digest!=obj.get('photo',{}).get('local_image_sha256'):
        raise PhotoCalibrationError('Original image hash mismatch')
    result=solve(obj)
    Path(dest).write_text(json.dumps(result,indent=2)+'\n')
    return result
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('input_json');a.add_argument('output_json');v=a.parse_args()
    print(json.dumps(run_file(v.input_json,v.output_json),indent=2))
