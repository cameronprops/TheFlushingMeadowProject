"""Read-only hash-and-content audit for FMP's dual GitHub/Drive archive.

The operator must download original Drive files into --drive-dir and obtain a
local checkout with actual Git binary/release files in --git-root. Merely
having a provider URL, Git source pointer, or an index entry is never PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

SCHEMA = 'fmp.dual-archive-batch.v001'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def safe_relpath(raw: str) -> Path:
    if not isinstance(raw, str) or not raw or '\\' in raw:
        raise ValueError('unsafe or empty path')
    p = PurePosixPath(raw)
    if p.is_absolute() or any(seg in ('..', '', '.') for seg in p.parts) or ':' in p.parts[0]:
        raise ValueError('unsafe relative path: ' + raw)
    return Path(*p.parts)


def verify_zip(path: Path, members: list) -> list[str]:
    errors = []
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                errors.append('ZIP_DUPLICATE_NAMES')
            for name in names:
                try:
                    safe_relpath(name.rstrip('/'))
                except ValueError:
                    errors.append('ZIP_UNSAFE_NAME')
                    break
            expected = {m['path']: m for m in members}
            if set(expected) != {n for n in names if not n.endswith('/')}:
                errors.append('ZIP_MEMBERS_MISMATCH')
            for name, member in expected.items():
                if name not in names:
                    continue
                with archive.open(name) as stream:
                    content = stream.read()
                if len(content) != member['size_bytes']:
                    errors.append('ZIP_MEMBER_SIZE_MISMATCH:' + name)
                if hashlib.sha256(content).hexdigest() != member['sha256']:
                    errors.append('ZIP_MEMBER_SHA256_MISMATCH:' + name)
    except (zipfile.BadZipFile, OSError, RuntimeError) as error:
        errors.append('ZIP_INVALID:' + type(error).__name__)
    return errors


def inspect_artifact(a: dict, drive_dir: Path, git_root: Path) -> dict:
    name = a['filename']
    local_drive = drive_dir / safe_relpath(a['drive_relpath'])
    git_ref = a.get('git_binary_path')
    local_git = git_root / safe_relpath(git_ref) if git_ref else None
    row = {'id': a['id'], 'filename': name, 'sha256': a['sha256'],
           'size_bytes': a['size_bytes'], 'drive_file_id': a['drive_file_id'],
           'git_binary_path': git_ref, 'errors': [], 'drive_local_bytes_verified': False,
           'git_local_bytes_verified': False}
    if local_drive.is_file():
        if local_drive.stat().st_size != a['size_bytes'] or sha256(local_drive) != a['sha256']:
            row['errors'].append('DRIVE_COPY_HASH_MISMATCH')
        else:
            row['drive_local_bytes_verified'] = True
            if a.get('members') is not None:
                row['errors'].extend(verify_zip(local_drive, a['members']))
    else:
        row['errors'].append('DRIVE_BYTES_NOT_AVAILABLE')
    if local_git and local_git.is_file():
        if local_git.stat().st_size != a['size_bytes'] or sha256(local_git) != a['sha256']:
            row['errors'].append('GIT_BINARY_HASH_MISMATCH')
        else:
            row['git_local_bytes_verified'] = True
    else:
        row['errors'].append('GIT_BINARY_NOT_AVAILABLE')
    if a.get('public_git_rights') == 'blocked':
        row['status'] = 'BLOCKED_RIGHTS'
    elif row['errors'] and any('MISMATCH' in e or 'INVALID' in e or 'UNSAFE' in e or 'DUPLICATE' in e for e in row['errors']):
        row['status'] = 'INTEGRITY_FAILURE'
    elif row['drive_local_bytes_verified'] and row['git_local_bytes_verified'] and not row['errors']:
        row['status'] = 'BOTH_LOCAL_COPIES_MATCH'  # Requires independent provider API checks before DUAL_VERIFIED
    elif row['drive_local_bytes_verified'] and not row['git_local_bytes_verified']:
        row['status'] = 'GIT_BINARY_PENDING'
    elif row['git_local_bytes_verified'] and not row['drive_local_bytes_verified']:
        row['status'] = 'DRIVE_COPY_PENDING'
    else:
        row['status'] = 'UNRECOVERED'
    return row


def audit(manifest: dict, drive_dir: Path, git_root: Path) -> dict:
    if manifest.get('schema') != SCHEMA:
        raise ValueError('Unsupported manifest schema')
    rows = [inspect_artifact(a, drive_dir, git_root) for a in manifest['artifacts']]
    return {'schema': 'fmp.dual-archive-audit-report.v001',
            'batch_id': manifest['batch_id'],
            'status_counts': {s: sum(row['status'] == s for row in rows) for s in sorted({r['status'] for r in rows})},
            'results': rows,
            'limits': ['Provider folder membership and download authenticity must be independently checked before using local bytes as Drive evidence.',
                       'GitHub pointers and source member copies do not constitute a GitHub binary ZIP mirror.',
                       'Matching local bytes are only BOTH_LOCAL_COPIES_MATCH; verify actual remote GitHub SHA/release and authenticated Drive bytes before declaring DUAL_VERIFIED.']}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--drive-dir', type=Path, required=True)
    ap.add_argument('--git-root', type=Path, required=True)
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    report = audit(json.loads(args.manifest.read_text()), args.drive_dir, args.git_root)
    output = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()