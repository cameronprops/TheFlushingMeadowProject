# Theme Center conversation backfill: eight ZIP packages, 52 member files

**Recorded:** 2026-10-20. **Scope:** retrospective FMP Theme Center Wolfram + Game Development Studio research, numerical audits, image-based architectural review and photo-registration work. **Status: partially recovered, not dual-certified.**

The canonical requirements are [`AGENTS.md`](../AGENTS.md), [`ARCHIVE_POLICY.md`](ARCHIVE_POLICY.md) and [`FMP_RETROACTIVE_DUAL_ARCHIVE_REGISTER.md`](FMP_RETROACTIVE_DUAL_ARCHIVE_REGISTER.md).

## Exact batch evidence

- [`FMP_DUAL_ARCHIVE_BATCH_20261020_01.json`](FMP_DUAL_ARCHIVE_BATCH_20261020_01.json) records **eight** original conversation ZIPs, their locally measured byte sizes and SHA-256 digests, **52** members, per-member hashes, exact Drive file IDs/URLs, origins, preliminary rights flags, and **proposed only** Git binary mirror paths.
- `audit_dual_archive_v001.py` is a read-only, standard-library implementation with **11 passing synthetic tests**. It checks the actual ZIP bytes and each member digest, and it refuses unsafe archive entries and missing or mismatching Git copies. Matching local files alone are **not** a verified GitHub+Drive remote backup: they receive `BOTH_LOCAL_COPIES_MATCH` until independently attested by each provider.
- A local run on existing conversation attachments produced `FMP_DUAL_ARCHIVE_AUDIT_BATCH_20261020_01.json` (stored in `docs/` in the repository): eight locally valid ZIP archives, all statuses `GIT_BINARY_PENDING`. Drive connector separately confirmed matching names, sizes and parent folder IDs for the batch. To certify *remote bytes*, explicitly re-fetch the Drive ZIP, compare SHA-256, and confirm a GitHub blob/commit or release with identical byte digest.
- The original binaries were **not** modified. A native GitHub binary blob write was blocked by the connector's safety checks, so no blocked upload is being represented as success.

## User-generated file versus restricted historical source

The three small Python/JSON audit packages are user-created source outputs that may be eligible for a true Git binary/LFS/release copy. Larger Trylon models, reference-media bundles and model bundles still require rights and licensing review before they are publicly published. A metadata pointer is a necessary cross-reference but **not** an actual second copy.

Reject invented 1939 AI art as historical evidence. If storing a verbatim conversation archive with that output, label it *rejected synthetic* and do not include it in archival picture references or measured CAD.

## Reproduction from repository root

```bash
python3 -m unittest -v tools.archive.test_audit_dual_archive_v001
python3 -m tools.archive.audit_dual_archive_v001 \
  --manifest docs/FMP_DUAL_ARCHIVE_BATCH_20261020_01.json \
  --drive-dir /path/to/verified-authenticated-drive-downloads \
  --git-root /path/to/verified-git-checkout \
  --out /path/to/new_audit.json
```

**Independent provider checks are required** after local matching hashes. Consult the associated Drive IDs from the JSON and authenticated GitHub commit IDs; verify the SHA-256 of the bytes retrieved from each. Do not treat a local unpushed commit, a source-file match inside a ZIP, or a GitHub README pointer as `DUAL_VERIFIED`.

## Outstanding blockers

1. Mirror the actual binary packages to a GitHub LFS/release mechanism with verified bytes and appropriate rights, and record real path/commit/release IDs. The working proposed paths in the manifest do **not** exist merely because they are listed.
2. Re-fetch from the Drive provider, check exact ZIP hashes against this batch and update `DUAL_VERIFIED` only after GitHub actual byte validation.
3. Continue past this eight-item batch through earlier FMP chat attachments, research originals and verbatim transcript export. A copied decision summary does not preserve the original conversation.
4. Keep each originating chat's component dossier and the retroactive project register current. Other threads may be producing parallel revisions; never overwrite them without SHA-based reconcile.

**Completion:** 8 inventories checked, 52 ZIP members hashed, 11/11 regression tests passed. **0/8 binary packages are dual-certified.**
