"""Build closed OBJ masses from explicit convex local-metre footprints.

Input JSON: units='m', coordinate_status, objects=[{id,year,footprint:[[x,y],...],
base_z,height,evidence_status,source_refs:[...]}]. No default dimensions or location.
Concave footprints, holes and geographic coordinates need a separate mesh workflow.
"""
import argparse
import json
import math
import re
from pathlib import Path


def build(data):
    if data.get('units') != 'm':
        raise ValueError('Explicit local metre coordinates required')
    if data.get('coordinate_status') not in {'UNREGISTERED_LOCAL','REGISTERED_LOCAL'}:
        raise ValueError('Declare coordinate_status')
    if data['coordinate_status']=='REGISTERED_LOCAL' and not data.get('registration_ref'):
        raise ValueError('Registered input needs registration_ref')
    lines=['# FMP footprint masses; metres; Z up; see manifest for evidence.']
    manifest={'units':'m','up_axis':'Z','coordinate_status':data['coordinate_status'],
              'registration_ref':data.get('registration_ref'), 'objects':[]}
    offset=0;seen=set()
    for obj in data['objects']:
        key=obj['id'];year=obj['year']
        if not isinstance(key,str) or not re.fullmatch(r'[A-Za-z0-9_-]+',key):
            raise ValueError('Use a stable alphanumeric object ID')
        if type(year) is not int or year not in {1939,1940,1964,1965,2026}:
            raise ValueError('Historical year required')
        if (key,year) in seen:raise ValueError('Duplicate object/year')
        seen.add((key,year))
        if obj['evidence_status'] not in {'PROVISIONAL','SOURCE_BACKED'}:
            raise ValueError('Explicit evidence status required')
        refs=obj.get('source_refs')
        if not isinstance(refs,list) or any(not isinstance(v,str) or not v.strip() for v in refs):
            raise ValueError('source_refs must be a list of nonempty references')
        if obj['evidence_status']=='SOURCE_BACKED' and not refs:
            raise ValueError('Source-backed geometry needs references')
        pts=[tuple(map(float,p)) for p in obj['footprint']]
        if len(pts)>1 and pts[0]==pts[-1]:pts.pop()
        if len(pts)<3 or len(set(pts))!=len(pts) or any(len(p)!=2 for p in pts):
            raise ValueError('Footprint needs at least three distinct 2D points')
        z,h=float(obj['base_z']),float(obj['height'])
        if not all(math.isfinite(v) for p in pts for v in p) or not all(map(math.isfinite,[z,h])) or h<=0:
            raise ValueError('Coordinates and dimensions must be finite; height must be positive')
        area=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))/2
        if abs(area)<1e-9:raise ValueError('Degenerate footprint')
        if area<0:pts.reverse();area=-area
        # Every other point must lie strictly left of each edge. This also
        # rejects self-intersecting stars that local turn tests can miss.
        for i,(x,y) in enumerate(pts):
            q=pts[(i+1)%len(pts)];dx,dy=q[0]-x,q[1]-y
            for j,p in enumerate(pts):
                if j not in {i,(i+1)%len(pts)} and dx*(p[1]-y)-dy*(p[0]-x)<=1e-9:
                    raise ValueError('Only simple strictly convex footprints supported; split or triangulate upstream')
        n=len(pts);faces=[]
        vertices=[(x,y,level) for level in (z,z+h) for x,y in pts]
        for i in range(1,n-1):
            faces.extend([(0,i+1,i),(n,n+i,n+i+1)])
        for i in range(n):
            j=(i+1)%n;faces.extend([(i,j,n+j),(i,n+j,n+i)])
        lines.append(f'o {key}_{year}')
        lines.extend('v '+' '.join(format(v,'.12g') for v in p) for p in vertices)
        lines.extend('f '+' '.join(str(offset+v+1) for v in face) for face in faces)
        manifest['objects'].append(dict(id=key,year=year,evidence_status=obj['evidence_status'],
            source_refs=refs,base_z=z,height=h,footprint_area_m2=area,volume_m3=area*h,
            vertex_count=len(vertices),triangle_count=len(faces),
            geometry_scope='EXTERIOR_MASS_ONLY',collision_status='NOT_ENGINE_TESTED',
            first_vertex_index=offset+1))
        offset+=len(vertices)
    if not seen:raise ValueError('No objects supplied')
    return '\n'.join(lines)+'\n',manifest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('--output-dir',required=True,type=Path)
    args=p.parse_args();outputs=[args.output_dir/'massing.obj',args.output_dir/'manifest.json']
    if args.input.resolve() in [v.resolve() for v in outputs]:p.error('Cannot overwrite input')
    obj,manifest=build(json.loads(args.input.read_text()))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    outputs[0].write_text(obj);outputs[1].write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')
    print(f"Built {len(manifest['objects'])} exterior masses; collision and historical review remain separate.")


if __name__=='__main__':main()
