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

