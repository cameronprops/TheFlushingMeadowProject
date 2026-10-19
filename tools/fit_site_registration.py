"""Fit a 2D similarity transform from reviewed paired map/target coordinates.

Input CSV: control_id,source_x,source_y,target_x,target_y,role
role is fit or check. Coordinates must already use consistent axis conventions.
No projection, vertical-datum conversion, or survey certification is performed.
"""
import argparse
import csv
import json
import math
from pathlib import Path


def fit_registration(rows, source_ref, target_crs, target_units, tolerance):
    if not all(str(v).strip() for v in (source_ref, target_crs, target_units)):
        raise ValueError('Source reference, target CRS and units are required')
    if not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError('Tolerance must be positive and finite in target units')
    points, seen = [], set()
    for row in rows:
        key = row['control_id']
        if not key or key in seen:
            raise ValueError('Control IDs must be present and unique')
        seen.add(key)
        if row['role'] not in {'fit', 'check'}:
            raise ValueError('Control role must be fit or check')
        values = [float(row[k]) for k in ('source_x','source_y','target_x','target_y')]
        if not all(math.isfinite(v) for v in values):
            raise ValueError('Coordinates must be finite')
        points.append((key, row['role'], *values))
    fitted = [p for p in points if p[1] == 'fit']
    if len(fitted) < 3:
        raise ValueError('At least three fit controls are required')
    n = len(fitted)
    mx, my, mu, mv = [sum(p[i] for p in fitted) / n for i in range(2,6)]
    centered = [(p[2]-mx,p[3]-my,p[4]-mu,p[5]-mv) for p in fitted]
    xx = sum(x*x for x,y,u,v in centered)
    yy = sum(y*y for x,y,u,v in centered)
    xy = sum(x*y for x,y,u,v in centered)
    denom = xx + yy
    if denom == 0 or (xx*yy-xy*xy) <= 1e-10*denom*denom:
        raise ValueError('Fit controls are coincident or nearly collinear; distribute them across the map')
    a = sum(x*u+y*v for x,y,u,v in centered)/denom
    b = sum(x*v-y*u for x,y,u,v in centered)/denom
    scale = math.hypot(a,b)
    if scale <= 1e-15:
        raise ValueError('Target controls produce a collapsed transform')
    tx, ty = mu-a*mx+b*my, mv-b*mx-a*my
    residuals = []
    for key,role,x,y,u,v in points:
        du, dv = a*x-b*y+tx-u, b*x+a*y+ty-v
        residuals.append(dict(control_id=key,role=role,dx=du,dy=dv,error=math.hypot(du,dv)))
    def stats(role):
        errors=[r['error'] for r in residuals if r['role']==role]
        return dict(count=len(errors),rmse=math.sqrt(sum(e*e for e in errors)/len(errors)) if errors else None,
                    maximum=max(errors) if errors else None)
    fit, check = stats('fit'), stats('check')
    within = all(r['error'] <= tolerance for r in residuals)
    status = 'RESIDUAL_LIMIT_EXCEEDED' if not within else ('WITHIN_LIMIT_WITH_CHECKS' if check['count'] >= 2 else 'INSUFFICIENT_INDEPENDENT_CHECKS')
    return dict(status=status,survey_verified=False,source_ref=source_ref,target_crs=target_crs,
        target_units=target_units,tolerance=tolerance,model='orientation-preserving 2D similarity',
        equation='X=a*x-b*y+tx; Y=b*x+a*y+ty',a=a,b=b,tx=tx,ty=ty,
        scale=scale,rotation_degrees=math.degrees(math.atan2(b,a)),
        inverse_matrix=[[a/(scale*scale),b/(scale*scale)],[-b/(scale*scale),a/(scale*scale)]],
        inverse_note='Subtract tx,ty from target coordinates before applying inverse_matrix.',
        fit=fit,check=check,residuals=residuals,
        limitations='No elevations, CRS conversion, source-date validation or survey certification. '
                     'Check controls must be independent of the fitted controls. No automatic outlier removal.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('controls',type=Path)
    p.add_argument('--source-ref',required=True)
    p.add_argument('--target-crs',required=True)
    p.add_argument('--target-units',required=True)
    p.add_argument('--tolerance',required=True,type=float)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    if args.output.resolve()==args.controls.resolve():
        p.error('Output cannot overwrite controls')
    with args.controls.open(newline='',encoding='utf-8-sig') as f:
        result=fit_registration(list(csv.DictReader(f)),args.source_ref,args.target_crs,args.target_units,args.tolerance)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(result['status'])


if __name__=='__main__':
    main()
