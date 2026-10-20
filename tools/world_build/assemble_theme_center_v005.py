"""Preserve source glTF data and append the provisional v004 runtime overlay."""
import copy, hashlib, json, pathlib, struct, uuid
SOURCE_SHA = 'a35661fd1eef633b8ae4767c0db1f953ed986c8555814361c0824700c6080cf5'
OVERLAY_SHA = 'b1467273bf674c7fbf081bb7ec64800ae61ecf88942e42678ed8948c452c5e01'
HIDDEN = ['Perisphere_Lower_Removable_Shell', 'Helicline_Bridge_Transition_Hypothesis', 'Trylon_Face_3_Frame', 'Trylon_Hollow_Exterior', 'Helicline_Rail_-1']
def read(path, expected):
    b=pathlib.Path(path).read_bytes()
    assert hashlib.sha256(b).hexdigest()==expected, 'Input checksum mismatch'
    magic,version,total=struct.unpack_from('<III',b)
    assert (magic,version,total)==(0x46546c67,2,len(b))
    n,t=struct.unpack_from('<II',b,12); assert t==0x4e4f534a
    d=json.loads(b[20:20+n]); size,kind=struct.unpack_from('<II',b,20+n)
    assert kind==0x004e4942 and len(d['buffers'])==1
    return d,b[28+n:28+n+size]
def build(source,overlay,out):
    s,sbin=read(source,SOURCE_SHA); o,obin=read(overlay,OVERLAY_SHA)
    # This assembler explicitly supports the observed static, embedded-buffer inputs.
    for d in (s,o):
        assert not any(d.get(k) for k in ('skins','animations','extensionsUsed','extensionsRequired'))
        assert all('uri' not in x for x in d['buffers'])
    assert not any(o.get(k) for k in ('materials','textures','images','cameras','samplers'))
    d=copy.deepcopy(s); offsets={k:len(s.get(k,[])) for k in ('nodes','meshes','accessors','bufferViews')}
    disabled=[]
    for i,node in enumerate(d['nodes']):
        if node.get('name') in HIDDEN:
            mesh=node.pop('mesh'); disabled.append({'name':node['name'],'node':i,'source_mesh':mesh})
            node.setdefault('extras',{})['runtime_assembly']={'disabled_source_mesh':mesh,'reason':'Superseded by provisional v004 circulation'}
    assert sorted(x['name'] for x in disabled)==sorted(HIDDEN)
    shift=len(sbin)
    for view in o['bufferViews']:
        v=copy.deepcopy(view); assert v.get('buffer',0)==0
        v['byteOffset']=v.get('byteOffset',0)+shift; d['bufferViews'].append(v)
    for acc in o['accessors']:
        a=copy.deepcopy(acc); assert 'sparse' not in a
        if 'bufferView' in a:a['bufferView']+=offsets['bufferViews']
        d['accessors'].append(a)
    for mesh in o['meshes']:
        m=copy.deepcopy(mesh)
        for p in m['primitives']:
            assert not any(k in p for k in ('material','extensions','targets'))
            if 'indices' in p:p['indices']+=offsets['accessors']
            p['attributes']={k:v+offsets['accessors'] for k,v in p['attributes'].items()}
        d['meshes'].append(m)
    for i,node in enumerate(o['nodes']):
        n=copy.deepcopy(node)
        if 'mesh' in n:n['mesh']+=offsets['meshes']
        if 'children' in n:n['children']=[x+offsets['nodes'] for x in n['children']]
        n.setdefault('extras',{})['fmp']={'object_id':str(uuid.uuid5(uuid.NAMESPACE_URL,'fmp:theme-center:v004:'+str(i)+':'+n.get('name',''))),'evidence_status':'PROVISIONAL_RUNTIME_DERIVATIVE','source_release':'guest-flow-v004','site_registration':'UNREGISTERED','collision_status':'NOT_ENGINE_TESTED'}
        d['nodes'].append(n)
    root=len(d['nodes']);d['nodes'].append({'name':'FMP_Provisional_Runtime_v004','children':[n+offsets['nodes'] for n in o['scenes'][o.get('scene',0)]['nodes']]})
    d['scenes'][d.get('scene',0)]['nodes'].append(root)
    binary=sbin+obin;d['buffers']=[{'byteLength':len(binary)}]
    raw=json.dumps(d,separators=(',',':')).encode();raw+=b' '*((-len(raw))%4)
    result=struct.pack('<III',0x46546c67,2,28+len(raw)+len(binary))+struct.pack('<II',len(raw),0x4e4f534a)+raw+struct.pack('<II',len(binary),0x004e4942)+binary
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
    filename='FMP_ThemeCenter_Assembled_Runtime_v005.glb';(out/filename).write_bytes(result)
    # Verify preservation and indexing against both input documents.
    assert binary[:len(sbin)]==sbin
    for k in ('meshes','accessors','bufferViews','materials','images','textures'):
        assert d[k][:len(s[k])]==s[k]
    for before,after in zip(s['nodes'],d['nodes']):
        assert before.get('extras')=={k:v for k,v in after.get('extras',{}).items() if k!='runtime_assembly'}
        for k in ('matrix','translation','rotation','scale','children'):assert before.get(k)==after.get(k)
    manifest={'asset':filename,'sha256':hashlib.sha256(result).hexdigest(),'source_sha256':SOURCE_SHA,'overlay_sha256':OVERLAY_SHA,'disabled_source_meshes':disabled,'units':'metres','coordinate_frame':'right-handed Y-up local, unregistered','source_binary_preserved':True,'source_materials_and_ids_preserved':True,'source_nodes':len(s['nodes']),'overlay_nodes':len(o['nodes']),'assembled_nodes':len(d['nodes']),'visible_mesh_nodes':sum('mesh' in n for n in d['nodes']),'limitations':['Provisional runtime geometry, not a print master','No Unreal import, collision, navigation or play test','Shared aperture dimensions and structural reframing remain unresolved','1939 working asset; year presence remains subject to evidence review']}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
if __name__=='__main__':
    import sys
    build(*sys.argv[1:])
