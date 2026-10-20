"""Preserving GLB edits: winding repair and fail-closed WF0028 runtime filtering."""
import copy,hashlib,json,struct
from pathlib import Path
import numpy as np
import trimesh

def read_glb(path):
 b=Path(path).read_bytes(); n=struct.unpack_from('<I',b,12)[0]
 d=json.loads(b[20:20+n]); off=20+n
 return d,bytearray(b[off+8:off+8+struct.unpack_from('<I',b,off)[0]])

def write_glb(path,d,b):
 d['buffers'][0]['byteLength']=len(b)
 j=json.dumps(d,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
 b=bytes(b)+b'\0'*((-len(b))%4)
 Path(path).write_bytes(struct.pack('<III',0x46546c67,2,28+len(j)+len(b))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(b),0x004e4942)+b)

def array(d,b,i):
 a=d['accessors'][i];v=d['bufferViews'][a['bufferView']]
 dt={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']];width={'SCALAR':1,'VEC3':3,'VEC4':4,'VEC2':2}[a['type']]
 assert 'sparse' not in a and 'byteStride' not in v
 return np.frombuffer(b,dtype=dt,count=a['count']*width,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,width).copy()

def append(d,b,a,typ,ctype):
 b.extend(b'\0'*((-len(b))%4));off=len(b);b.extend(a.tobytes())
 d['bufferViews'].append({'buffer':0,'byteOffset':off,'byteLength':a.nbytes})
 d['accessors'].append({'bufferView':len(d['bufferViews'])-1,'componentType':ctype,'count':len(a),'type':typ})
 return len(d['accessors'])-1

def repair(src,dst):
 if Path(src).resolve()==Path(dst).resolve():raise ValueError('Cannot overwrite source')
 if hashlib.sha256(Path(src).read_bytes()).hexdigest()!='de38fdd5294285afd92dbb6be0a9d4e564c52bacd588a9fd116c9e1e35f06439':raise ValueError('Source hash mismatch')
 d,b=read_glb(src);report=[]
 for mi in [354,355,356,357,358]:
  p=d['meshes'][mi]['primitives'][0];v=array(d,b,p['attributes']['POSITION']);f=array(d,b,p['indices']).reshape(-1,3)
  m=trimesh.Trimesh(v,f,process=False);assert not m.is_winding_consistent
  trimesh.repair.fix_winding(m); assert m.is_winding_consistent
  p['indices']=append(d,b,np.asarray(m.faces,dtype='<u4').reshape(-1,1),'SCALAR',5125)
  p['attributes']['NORMAL']=append(d,b,np.asarray(m.vertex_normals,dtype='<f4'),'VEC3',5126)
  report.append({'mesh':d['meshes'][mi]['name'],'flipped_faces':int(np.any(f!=m.faces,axis=1).sum()),'consistent':True,'orientation_scope':'shared-edge consistency, not closed-solid outward certification'})
 write_glb(dst,d,b);return report

DIAGNOSTIC_PREFIXES=('VISUAL_ONLY','REFERENCE_','ARTWORK_UNPLACED','ROUTE_WAYPOINT','VISITOR_ROUTE_MARKER')
ALLOWED={'ENTRY_LINTEL','EXHIBIT_ZONE','FLOOR','INTERPRETIVE_SLOPED_THRESHOLD','LANDSCAPE','PERIMETER_WALL','PROVISIONAL_DISPLAY_PLINTH','PROVISIONAL_ENTRY_APPROACH','PUBLIC_ENTRY','PUBLIC_WALK_PROVISIONAL','ROOF','SPECULATIVE_FLOOR_CONNECTOR','SPECULATIVE_PARTITION','SPECULATIVE_SIDEWALL_LINTEL','SPECULATIVE_SIDEWALL_REPLACEMENT'}
def excluded(c):
 k=c.get('kind','')
 if c.get('excluded_from_runtime_collisions') is True or k.startswith(DIAGNOSTIC_PREFIXES) or k in {'UNLOCATED_EXHIBIT_PROXY','EXHIBIT_ZONE'} or c.get('id','').startswith('V002_ZONE_'):return True
 if k not in ALLOWED:raise ValueError('Unclassified component kind: '+k)
 return False

def export_runtime(src,manifest,dst):
 if Path(src).resolve()==Path(dst).resolve():raise ValueError('Cannot overwrite source')
 m=json.loads(Path(manifest).read_text());raw=Path(src).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=m['glb_sha256']:raise ValueError('Source hash mismatch')
 cs=m['components']
 if len({c['id'] for c in cs})!=len(cs):raise ValueError('Duplicate component IDs')
 d,b=read_glb(src);nodes={n.get('name'):n for n in d['nodes'] if 'mesh' in n}
 if set(nodes)!={c['id'] for c in cs}:raise ValueError('Unregistered mesh or missing component')
 removed=[];kept=[]
 for c in cs:
  if excluded(c):
   nodes[c['id']].pop('mesh');removed.append(c['id'])
  else:kept.append(c['id'])
 used=sorted({n['mesh'] for n in d['nodes'] if 'mesh' in n}); remap={old:new for new,old in enumerate(used)}
 d['meshes']=[d['meshes'][i] for i in used]
 for n in d['nodes']:
  if 'mesh' in n:n['mesh']=remap[n['mesh']]
 write_glb(dst,d,b)
 return {'source_sha256':hashlib.sha256(raw).hexdigest(),'excluded':removed,'runtime_render_and_collision_candidates':kept,'policy':'Diagnostic nodes have no mesh binding and their mesh records are removed; unused raw buffer bytes are retained for preservation. Collision generation must use active scene nodes only. No Unreal certification.'}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['repair','filter']);p.add_argument('source');p.add_argument('output');p.add_argument('--manifest');a=p.parse_args()
 r=repair(a.source,a.output) if a.mode=='repair' else export_runtime(a.source,a.manifest,a.output)
 Path(a.output+'.receipt.json').write_text(json.dumps(r,indent=2))
 print(json.dumps(r,indent=2))
