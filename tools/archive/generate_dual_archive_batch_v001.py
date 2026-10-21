"""Generate a deterministic FMP backfill manifest from archived local ZIP packages.

URLs/Drive IDs below were verified via Drive metadata, not SHA-authenticated by
this generator. Historical/source rights must be assessed before public Git mirroring.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import zipfile

FOLDER = '11aRetkT2qaA69j8jnRyqxCJu2sR7DAPk'
PROVEN = [
    ('FMP_ThemeCenter_Wolfram_GameDev_EngineeringGate_v001.zip','1PwBZnZ2oDG24TLnF8tQhxWZhhqK2POF_','user-created-code'),
    ('FMP_ThemeCenter_RuntimeMesh_Audit_v001.zip','15b2j_-anBktrh5OKAKYOeVMtHdjqVkCv','user-created-code'),
    ('FMP_ThemeCenter_ReturnRoute_Continuity_v001.zip','1vNaxcSn4SbtOJvH-rTbEmFqdFqGz93UR','user-created-code'),
    ('FMP_Trylon_Actual_GLB_Passage_Evidence_v001.zip','1o8OZlu-q0IOiZbpr90lobYrRql2T6bZ0','rights-review-pending'),
    ('FMP_1939_Bridge_Entrance_Archival_Model_Audit_v001.zip','1LJYXE5P1_tQiUts20qocl2HgGcpMEWih','rights-review-pending'),
    ('FMP_ThemeCenter_Photo_Control_v001.zip','1fMraAZ0QP5oNaaYTtlLG44qOfa-HidbY','user-created-code-and-geometry'),
    ('FMP_ThemeCenter_Shared_Portals_v004.zip','1Z01QmV6EfgElqiBhVUIg7nIvd_pucZdi','rights-review-pending'),
    ('FMP_ThemeCenter_Assembled_Runtime_v005.zip','1OzFZRkHCxN3jMBGwH3Lwdbx0pFJIJhM0','rights-review-pending'),
]


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def generate(directory: Path) -> dict:
    result = {'schema':'fmp.dual-archive-batch.v001',
              'batch_id':'theme-center-chat-retroactive-2026-10-20-batch01',
              'drive_folder_id':FOLDER,
              'source_attestation':'Original conversation attachments present locally; separate Google Drive metadata confirmed matching filename, size and parent folder. Remote ZIP-byte equality still requires authenticated redownload and hash check.',
              'artifacts':[]}
    for filename, fid, rights in PROVEN:
        f = directory / filename
        content = f.read_bytes()
        with zipfile.ZipFile(f) as z:
            members = []
            for member in z.infolist():
                if member.is_dir():
                    continue
                b=z.read(member)
                members.append({'path':member.filename,'sha256':digest(b),'size_bytes':len(b)})
        result['artifacts'].append({'id':filename.removesuffix('.zip'),
                 'filename':filename, 'origin_chat':'2026-10-20 Theme Center Game Development Studio and Wolfram FMP work thread',
                 'component':'Theme Center / WF0001-WF0004',
                 'rights_review':rights,'public_git_rights':'review_pending' if rights=='rights-review-pending' else 'allowed',
                 'drive_file_id':fid,'drive_url':f'https://drive.google.com/file/d/{fid}/view',
                 'drive_relpath':filename,'git_binary_path':f'archive/chat_backfill/2026-10-20/{filename}',
                 'git_binary_path_status':'proposed_only_not_committed',
                 'sha256':digest(content),'size_bytes':len(content),
                 'members':members})
    return result


def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(generate(a.directory),indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()