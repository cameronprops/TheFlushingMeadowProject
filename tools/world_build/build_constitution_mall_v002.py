#!/usr/bin/env python3
"""FMP Constitution Mall position-controlled impression v0.2.
Append independent, fully labeled interpretive geometry to preserved existing GLB.
Do NOT overwrite original nodes, mesh data, extras, or binary chunk.
"""
import argparse, hashlib, json, math, struct, uuid
from pathlib import Path
import numpy as np

NS = uuid.uuid5(uuid.NAMESPACE_URL,'https://github.com/cameronprops/TheFlushingMeadowProject#mall-impression')
MAT={
 'warm_paving':([0.70,0.65,0.57,1],0.9),
 'path_inlay':([0.85,0.82,0.74,1],0.85),
 'water':([0.15,0.38,0.52,0.88],0.23),
 'basin_stone':([0.72,0.72,0.67,1],0.86),
 'turf':([0.25,0.38,0.23,1],0.96),
 'evergreen':([0.16,0.31,0.22,1],0.91),
 'light_foliage':([0.32,0.48,0.30,1],0.91),
 'trunk':([0.32,0.28,0.23,1],1),
 'cream_facade':([0.79,0.78,0.69,1],0.92),
 'bright_facade':([0.90,0.87,0.79,1],0.90),
 'shadow_recess':([0.39,0.41,0.39,1],0.95),
 'lighting_metal':([0.31,0.35,0.34,1],0.47),
 'glow':([1.0,0.89,0.66,1],0.4),
 'spray':([0.55,0.81,0.90,0.69],0.15),
}

class Geometry:
 def __init__(self):self.items=[]
 def add(self,name,v,f,material,kind,notes='',data_status='INTERPRETIVE',group='mall'):
  v=np.asarray(v,dtype=np.float32);f=np.asarray(f,dtype=np.uint32)
  if len(v)<3 or len(f)<1 or v.ndim!=2 or v.shape[1]!=3 or f.ndim!=2 or f.shape[1]!=3:
   raise ValueError('mesh has invalid shape '+name)
  if not np.isfinite(v).all() or int(f.max())>=len(v):raise ValueError('invalid mesh '+name)
  self.items.append(dict(name=name,vertices=v,faces=f,material=material,kind=kind,notes=notes,
                         data_status=data_status,group=group,id=str(uuid.uuid5(NS,name))))
 def box(self,name,x0,x1,y0,y1,z0,z1,material,kind,**k):
  if x1<=x0 or y1<=y0 or z1<=z0:raise ValueError(name)
  v=[[x0,y0,z0],[x1,y0,z0],[x1,y0,z1],[x0,y0,z1],
     [x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]]
  f=[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],
     [2,3,7],[2,7,6],[3,0,4],[3,4,7]]
  self.add(name,v,f,material,kind,**k)
 def ellipse(self,name,cx,cy,cz,rx,rz,thickness,material,kind,segments=64,**k):
  a=np.linspace(0,2*math.pi,segments,endpoint=False)
  v=[[cx+rx*math.cos(t),cy,cz+rz*math.sin(t)] for t in a]
  v+=[[p[0],cy+thickness,p[2]] for p in v]
  f=[]
  for i in range(1,segments-1):f.extend([[0,i+1,i],[segments,segments+i,segments+i+1]])
  for i in range(segments):j=(i+1)%segments;f.extend([[i,j,segments+j],[i,segments+j,segments+i]])
  self.add(name,v,f,material,kind,**k)
 def cylinder(self,name,x,y,z,rad,height,material,kind,segments=10,**k):
  a=np.linspace(0,2*math.pi,segments,endpoint=False)
  v=[[x+rad*math.cos(t),y,z+rad*math.sin(t)] for t in a]
  v+=[[p[0],y+height,p[2]] for p in v]
  f=[]
  for i in range(1,segments-1):f.extend([[0,i+1,i],[segments,segments+i,segments+i+1]])
  for i in range(segments):j=(i+1)%segments;f.extend([[i,j,segments+j],[i,segments+j,segments+i]])
  self.add(name,v,f,material,kind,**k)
 def ellipsoid(self,name,x,y,z,r,h,material,kind,rows=7,segs=14,**k):
  v=[];f=[]
  for i in range(rows+1):
   phi=math.pi*i/rows
   for j in range(segs):
    t=2*math.pi*j/segs
    v.append([x+r*math.sin(phi)*math.cos(t),y+h*math.cos(phi),z+r*math.sin(phi)*math.sin(t)])
  for i in range(rows):
   for j in range(segs):
    n=i*segs+j;nn=i*segs+(j+1)%segs
    f.extend([[n,n+segs,nn],[nn,n+segs,nn+segs]])
  self.add(name,v,f,material,kind,**k)
 def spray(self,name,x,y,z,direction,reach,height,material='spray'):
  # Continuous parabola tube with a real 3D arc; no simulation, show-effect proxy.
  v=[];f=[];segments=13;sides=5;rad=0.045
  dx,dz=direction
  for i in range(segments+1):
   u=i/segments
   px=x+dx*reach*u;py=y+4*height*u*(1-u)+0.14; pz=z+dz*reach*u
   for a in range(sides):
    theta=2*math.pi*a/sides
    v.append([px+rad*math.cos(theta),py,pz+rad*math.sin(theta)])
  for i in range(segments):
   for j in range(sides):
    a=i*sides+j;b=i*sides+(j+1)%sides
    f.extend([[a,b,a+sides],[b,b+sides,a+sides]])
  self.add(name,v,f,material,'FOUNTAIN_ARC_PROXY',notes='Non-simulated proposed water effect.',group='water')

def generate():
 g=Geometry()
 def b(name,x0,x1,z0,z1,y0,y1,mat,kind='GROUND_ELEMENT',notes='',group='mall'):
  g.box(name,x0,x1,y0,y1,z0,z1,mat,kind,notes=notes,group=group)
 # These coordinates are PREVIEW local (metres), Y is up, existing Perisphere centered X=0/Z=0.
 # East-looking long-axis guess, not an as-built survey. The ground platform overlaps
 # the source model at X=158..172 so that a visitor has continuous visible ground.
 b('FMP_MALL_v001_RETAINED_BASE_CONNECTION',157,188,-111,111,-0.22,-0.105,'warm_paving',notes='Connection overlay onto source grounds; do not infer survey level.')
 b('FMP_MALL_v001_NEW_GROUND',185,566,-119,119,-0.21,-0.12,'warm_paving',notes='Interpretive site extension; footprint proportions are provisional.')
 b('FMP_MALL_v001_MAIN_APPROACH',88,145,-13,13,-0.095,0.012,'path_inlay',kind='PEDESTRIAN_PATH')
 b('FMP_MALL_v001_AXIAL_ENTRY',125,163,-32,32,-0.085,0.014,'path_inlay',kind='PEDESTRIAN_PATH')
 # north/south pedestrian promenade paths including walkable visual connectivity.
 for sign,key in [(-1,'S'),(1,'N')]:
  def band(zlo,zhi,mat,part):
   if sign<0:zlo,zhi=-zhi,-zlo
   b('FMP_MALL_v001_'+key+'_'+part,156,545,zlo,zhi,-0.083,0.02,mat,kind='PEDESTRIAN_PATH' if mat=='path_inlay' else 'LANDSCAPE')
  band(26,43,'path_inlay','PROMENADE')
  band(45,69,'turf','PLANTING')
  band(71,85,'path_inlay','OUTER_PATH')
  band(86,112,'turf','PAVILION_MARGIN')
  for i,x in enumerate(np.linspace(168,525,24)):
   z=52.7*sign
   g.cylinder('FMP_MALL_v001_TREE_'+key+f'_{i:02d}_TRUNK',float(x),0.03,z,0.23,4.6,'trunk','TREE_TRUNK',group='trees')
   g.ellipsoid('FMP_MALL_v001_TREE_'+key+f'_{i:02d}_CROWN',float(x),5.5,z,3.3,3.3,'evergreen' if i%3 else 'light_foliage','TREE_CROWN',group='trees')
  for i,x in enumerate(np.linspace(160,530,19)):
   z=36.4*sign
   g.cylinder('FMP_MALL_v001_LIGHT_'+key+f'_{i:02d}_SHAFT',float(x),0.028,z,0.105,4.1,'lighting_metal','LIGHTING_POST',group='lighting')
   g.ellipsoid('FMP_MALL_v001_LIGHT_'+key+f'_{i:02d}_LAMP',float(x),4.55,z,0.34,0.49,'glow','LIGHTING_HEAD',group='lighting')
 # Three water terraces and deliberate cross bridges to maintain walkability.
 terrace=[(152,228),(240,316),(328,423)]
 for i,(a,b_) in enumerate(terrace):
  b(f'FMP_MALL_v001_POOL_{i}_FOUNDATION',a,b_,-25.1,25.1,-0.065,0.05,'basin_stone',kind='BASIN_EDGE',group='water')
  b(f'FMP_MALL_v001_POOL_{i}_WATER',a+1.3,b_-1.3,-23.7,23.7,0.051,0.082,'water',kind='REFLECTING_POOL',group='water')
  # visible edge above water without interfering with the surface
  for key,z0,z1 in [('N',24.0,25.7),('S',-25.7,-24.0)]:
   b(f'FMP_MALL_v001_POOL_{i}_RIM_{key}',a,b_,z0,z1,0.065,0.18,'basin_stone',kind='BASIN_EDGE',group='water')
  for key,xa,xb in [('W',a-0.7,a+0.8),('E',b_-0.8,b_+0.7)]:
   b(f'FMP_MALL_v001_POOL_{i}_RIM_{key}',xa,xb,-25.8,25.8,0.075,0.18,'basin_stone',kind='BASIN_EDGE',group='water')
  for j,x in enumerate(np.arange(a+8,b_-5,13)):
   for sign,key in [(-1,'S'),(1,'N')]:
    z=sign*18.5
    g.cylinder(f'FMP_MALL_v001_POOL_{i}_JET_{j}_{key}_BASE',float(x),0.1,float(z),0.32,0.23,'basin_stone','FOUNTAIN_NOZZLE',group='water')
    g.spray(f'FMP_MALL_v001_POOL_{i}_JET_{j}_{key}_ARC',float(x),0.27,float(z),(0,-sign),reach=4.8,height=2.2+(j%3)*0.34)
 for i,(a,b_) in enumerate([(228,240),(316,328)]):
  b(f'FMP_MALL_v001_CROSSWALK_{i}',a,b_,-35,35,-0.075,0.037,'path_inlay',kind='PEDESTRIAN_CROSSING')
  for z in (-24.9,24.9):
   b(f'FMP_MALL_v001_BRIDGE_PARAPET_{i}_{z}',a,b_,z-.25,z+.25,0.05,0.5,'basin_stone',kind='PEDESTRIAN_PARAPET')
 # a transitional formal ellipse beyond the axial water terraces.
 g.ellipse('FMP_MALL_v001_TERMINAL_LAGOON_PAVING',479,-.10,0,71,53,0.10,'basin_stone','LAGOON_EDGE',segments=84,group='water')
 g.ellipse('FMP_MALL_v001_TERMINAL_LAGOON_WATER',479,0.005,0,66,48,0.04,'water','LAGOON_WATER',segments=84,group='water')
 # concentric jets at ellipse focus rings.
 for ring,(rad,n) in enumerate([(17,12),(38,20)]):
  for i in range(n):
   t=2*math.pi*i/n
   x=479+rad*math.cos(t);z=.72*rad*math.sin(t)
   g.cylinder(f'FMP_MALL_v001_LAGOON_NOZZLE_{ring}_{i:02d}',x,.055,z,.22,.18,'basin_stone','FOUNTAIN_NOZZLE',group='water')
   g.spray(f'FMP_MALL_v001_LAGOON_SPRAY_{ring}_{i:02d}',x,.14,z,(-math.cos(t),-math.sin(t)),reach=4.2 if ring==0 else 7.6,height=3.1 if ring==0 else 2.3)
 # Intentionally no pavilion volumes. The v0.1 symmetric pavilion blocks
 # were not based on a dated fairground plan and are EXCLUDED from v0.2.
 # Authentic footprints and placement require a 1939/1940 source-map trace,
 # documented image revision and site registration before adding architecture.
 # A clearly unassigned plinth, for later evidence-checked sculptural location.
 b('FMP_MALL_v001_MONUMENT_PLAZA',117,140,-19,19,-0.05,0.025,'warm_paving',kind='PLAZA')
 g.cylinder('FMP_MALL_v001_SCULPTURE_UNASSIGNED_PEDESTAL',130,0.03,0,3.5,1.4,'basin_stone',kind='SCULPTURE_PLACEHOLDER',segments=18,notes='Empty base only; no statue or historical identity asserted.')
 # Two sunken lawn texture bands.
 for key,za,zb in [('N',57,66),('S',-66,-57)]:
  for i in range(3):
   x=166+i*127
   b(f'FMP_MALL_v001_PLANTING_{key}{i}',x,x+95,za,zb,0.005,0.021,'turf',kind='PLANTED_MEDIAN')
 return g

def parse_glb(blob):
 if len(blob)<20 or blob[:4]!=b'glTF': raise ValueError('Not GLB')
 _,version,length=struct.unpack_from('<III',blob)
 if version!=2 or length!=len(blob):raise ValueError('Malformed GLB header')
 pieces=[];pos=12
 while pos<len(blob):
  ln,kind=struct.unpack_from('<II',blob,pos);pos+=8
  pieces.append((kind,blob[pos:pos+ln]));pos+=ln
 if len(pieces)!=2 or pieces[0][0]!=0x4e4f534a or pieces[1][0]!=0x004e4942:
  raise ValueError('Expected exactly JSON and BIN chunks')
 data=json.loads(pieces[0][1].decode('utf8'));return data,pieces[1][1]

def build(source):
 base=Path(source).read_bytes();data,rawbin=parse_glb(base)
 # Important: original buffer view byte offsets must not change.
 old_meshes=len(data.get('meshes',[]));old_nodes=len(data.get('nodes',[]));old_materials=len(data.get('materials',[]))
 old_json_hash=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 old_bin_hash=hashlib.sha256(rawbin).hexdigest()
 items=generate().items
 if not data.get('buffers') or len(data['buffers'])!=1:raise ValueError('Expected one embedded GLB buffer')
 data.setdefault('accessors',[]);data.setdefault('bufferViews',[]);data.setdefault('meshes',[]);data.setdefault('materials',[])
 data.setdefault('nodes',[])
 mats={}
 for name,(rgb,roughness) in MAT.items():
  mats[name]=len(data['materials'])
  pbr={'baseColorFactor':rgb,'metallicFactor':0.05 if name=='lighting_metal' else 0.0,'roughnessFactor':roughness}
  mat={'name':'FMP_IMPRESSION_'+name,'pbrMetallicRoughness':pbr,'doubleSided':True}
  if rgb[3]<1:mat['alphaMode']='BLEND'
  data['materials'].append(mat)
 # append each attribute aligned to 4bytes; indices U32; ensure no mutation of original binary.
 binbytes=bytearray(rawbin)
 def view(payload,target):
  pad=(-len(binbytes))%4
  if pad:binbytes.extend(b'\0'*pad)
  offset=len(binbytes);binbytes.extend(payload)
  i=len(data['bufferViews'])
  data['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(payload),'target':target})
  return i
 records=[]
 for item in items:
  v=item['vertices'];f=item['faces'];vview=view(v.astype('<f4').tobytes(),34962)
  vi=len(data['accessors']);data['accessors'].append({'bufferView':vview,'componentType':5126,'count':len(v),'type':'VEC3','min':v.min(axis=0).tolist(),'max':v.max(axis=0).tolist()})
  fview=view(f.astype('<u4').tobytes(),34963)
  fi=len(data['accessors']);data['accessors'].append({'bufferView':fview,'componentType':5125,'count':int(f.size),'type':'SCALAR'})
  mi=len(data['meshes']);data['meshes'].append({'name':item['name'],'primitives':[{'attributes':{'POSITION':vi},'indices':fi,'material':mats[item['material']],'mode':4}]})
  ni=len(data['nodes']); metadata={'object_id':item['id'],'component_group':item['group'],'component_type':item['kind'],
                    'evidence_status':item['data_status'],'construction_phase':'FMP_CONSTITUTION_MALL_IMPRESSION_v002',
                    'interpretive':True,'year_presence':'1939_IMPRESSION_NOT_CERTIFIED',
                    'survey_status':'UNREGISTERED_LOCAL','collisions':'NOT_TESTED','notes':item['notes']}
  data['nodes'].append({'name':item['name'],'mesh':mi,'extras':{'fmp':metadata}})
  data['scenes'][data.get('scene',0)]['nodes'].append(ni)
  records.append({'object_id':item['id'],'node_index':ni,'name':item['name'],'type':item['kind'],'group':item['group'],'material':item['material'],'vertices':len(v),'triangles':len(f),'evidence_status':item['data_status']})
 data['buffers'][0]['byteLength']=len(binbytes)
 encoded=json.dumps(data,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf8')
 encoded+=b' '*((-len(encoded))%4)
 binbytes.extend(b'\0'*(-len(binbytes)%4))
 out=struct.pack('<III',0x46546c67,2,12+8+len(encoded)+8+len(binbytes))+struct.pack('<II',len(encoded),0x4e4f534a)+encoded+struct.pack('<II',len(binbytes),0x004e4942)+bytes(binbytes)
 # Complete immutability assertions on source core.
 reread,newbin=parse_glb(out)
 for key in ('meshes','nodes','materials','accessors','bufferViews'):
  if reread[key][:len(json.loads(base[20:20+struct.unpack_from('<I',base,12)[0]]) .get(key,[]))]!=json.loads(base[20:20+struct.unpack_from('<I',base,12)[0]]).get(key,[]):
   raise AssertionError('Original '+key+' modified')
 if newbin[:len(rawbin)]!=rawbin:raise AssertionError('Original BIN bytes modified')
 if old_nodes!=510:raise AssertionError('Unexpected Theme Center source nodes')
 if len({r['object_id'] for r in records})!=len(records):raise AssertionError('duplicate identifiers')
 manifest={'release':'FMP_Constitution_Mall_Impression_v002','world_state':'1939_INTERPRETIVE_PREVIEW',
           'units':'metres','up_axis':'Y','local_axis':'positive-X extension from Theme Center is an IMPRESSION, not georeferenced east',
           'source_sha256':hashlib.sha256(base).hexdigest(),'source_original_nodes':old_nodes,
           'source_original_meshes':old_meshes,'source_original_materials':old_materials,
           'source_original_binary_sha256':old_bin_hash,'source_original_json_sha256':old_json_hash,
           'output_sha256':hashlib.sha256(out).hexdigest(),'source_bin_preserved':True,'named_pavilions_created':0,
           'old_node_mesh_material_and_accessor_records_preserved':True,
           'added_nodes':len(records),'new_total_nodes':len(reread['nodes']),
           'new_total_meshes':len(reread['meshes']),
           'site_registration':'UNREGISTERED_LOCAL','historical_certification':False,'pavilion_placement_policy':'NO_UNVERIFIED_PAVILION_GEOMETRY','excluded_from_prior_release':'six symmetric speculative pavilion assemblies',
           'unreal_host_tested':False,'worldwright_host_tested':False,
           'note':'Constitution Mall planting/fountain geometry remains provisional. Six invented symmetric pavilion blocks from v0.1 are excluded; add historical pavilion volumes only after period map footprint review.',
           'references':[
            'https://www.tclf.org/landscapes/new-york-worlds-fair',
            'https://www.worldsfairphotos.com/nywf39/book-sample-pages.pdf',
            'https://s-media.nyc.gov/agencies/lpc/lp/1925.pdf'],
           'objects':records}
 return out,manifest

def main():
 ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--output',required=True)
 args=ap.parse_args()
 out,manifest=build(args.source);p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(out);p.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 print('Created',p,'new nodes',manifest['added_nodes'],'total nodes',manifest['new_total_nodes'], 'size',len(out))

if __name__=='__main__':main()
