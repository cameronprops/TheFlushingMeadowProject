"""Attach FMP identities to the reviewed v0.9.2 GLB without changing geometry.
Run with source.glb and an output directory. IDs in this manifest must be carried
forward by future revisions, not regenerated from reordered node indices.
"""
import argparse
import copy
import hashlib
import json
import struct
import uuid
from pathlib import Path

SOURCE_ID='1S-fMjZlzHSAo_H-8bp4YT9Iqw8nS2vlI'


def prepare(source,output):
    raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!='2b82e39f388cdae1e182472b337b554df80baddfd1c3b61d8ed1876c2da56aac':
        raise ValueError('Source hash differs from inspected v0.9.2; review mapping before migrating')
    magic,version,total=struct.unpack_from('<III',raw)
    if (magic,version,total)!=(0x46546c67,2,len(raw)):
        raise ValueError('Invalid GLB header')
    length,kind=struct.unpack_from('<II',raw,12)
    if kind!=0x4e4f534a:raise ValueError('Expected JSON chunk')
    original=json.loads(raw[20:20+length]);data=copy.deepcopy(original)
    nodes=data['nodes']
    if len(nodes)!=510 or nodes[185].get('name')!='Trylon_Hollow_Exterior' or nodes[204].get('name','').split(' / ')[0]!='DEMOCRACITY_0_6_3':
        raise ValueError('This migration only accepts the reviewed v0.9.2 node layout')
    source_hash=hashlib.sha256(raw).hexdigest()
    records=[]
    for i,node in enumerate(nodes):
        group='scene_root';place=None
        if 1<=i<=125:group='grounds_and_fixtures';place='WF0005'
        elif 126<=i<=184:group='perisphere';place='WF0002'
        elif 185<=i<=188 or i==196:group='trylon';place='WF0001'
        elif 189<=i<=195:group='internal_circulation'
        elif 197<=i<=203:group='helicline';place='WF0004'
        elif 204<=i<=496:group='democracity';place='WF0003'
        elif 497<=i<=498:group='provisional_exit_stair'
        elif 499<=i<=501:group='concept_approach'
        elif 502<=i<=509:group='moving_viewing_decks';place='WF0002'
        oid=str(uuid.uuid5(uuid.NAMESPACE_URL,f'https://drive.google.com/file/d/{SOURCE_ID}#node-{i}'))
        tag=dict(object_id=oid,component_group=group,place_id=place,
                 source_release='v0.9.2',source_node_index=i,
                 evidence_status='PROVISIONAL_INHERITED',site_registration='UNREGISTERED',
                 collision_status='NOT_ENGINE_TESTED',year_presence='REVIEW_REQUIRED')
        if i==185:tag['review_note']='West entrance cut is a provisional clearance modification, not verified historical geometry.'
        if 'fmp' in node.get('extras',{}):raise ValueError('Existing FMP identity must not be overwritten')
        node.setdefault('extras',{})['fmp']=tag
        records.append(dict(tag,name=node.get('name',''),mesh_index=node.get('mesh')))
    encoded=json.dumps(data,separators=(',',':'),ensure_ascii=False).encode()
    encoded+=b' '*((-len(encoded))%4)
    remainder=raw[20+length:]
    out=struct.pack('<III',magic,version,20+len(encoded)+len(remainder))+struct.pack('<II',len(encoded),kind)+encoded+remainder
    # Prove all non-FMP JSON values and every remaining binary chunk unchanged.
    stripped=copy.deepcopy(data)
    for i,node in enumerate(stripped['nodes']):
        del node['extras']['fmp']
        if 'extras' not in original['nodes'][i]:del node['extras']
    if stripped!=original:raise AssertionError('Non-metadata JSON changed')
    assert out[20+len(encoded):]==remainder
    assert len({r['object_id'] for r in records})==len(records)
    manifest=dict(source_drive_id=SOURCE_ID,source_sha256=source_hash,
                  output_sha256=hashlib.sha256(out).hexdigest(),nodes=len(nodes),
                  mesh_nodes=sum('mesh' in n for n in nodes),
                  binary_chunks_unchanged=True,non_fmp_json_unchanged=True,
                  units='glTF metres',axis_convention='glTF Y-up; no conversion applied',
                  engine_import_tested=False,objects=records)
    output.mkdir(parents=True,exist_ok=True)
    (output/'FMP_ThemeCenter_Staging_v001.glb').write_bytes(out)
    (output/'FMP_ThemeCenter_Object_Manifest_v001.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='objects'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    args=p.parse_args();prepare(args.source,args.output)
