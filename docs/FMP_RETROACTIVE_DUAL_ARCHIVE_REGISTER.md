# Flushing Meadows Project: retroactive dual-archive register

**Established:** October 20, 2026. **Mandate:** [AGENTS.md](../AGENTS.md) and [ARCHIVE_POLICY.md](ARCHIVE_POLICY.md). **Scope:** all prior, current and future Flushing Meadows Project chats and created/revised artifacts. **Owner:** each conversation/work thread audits and backfills its own output; other threads must not overwrite newer assets.

**Canonical destinations**
- GitHub: https://github.com/cameronprops/TheFlushingMeadowProject
- Drive: https://drive.google.com/drive/folders/11aRetkT2qaA69j8jnRyqxCJu2sR7DAPk

> **Important:** This register is a *worklist*, not a declaration that the project's historical artifacts are fully archived. A GitHub link to a Drive file is only a **pointer**, not the bytes of the same artifact. Do not claim `DUAL_VERIFIED` without comparing actual retrievable copies. These entries summarize verified Drive/Git findings from the Theme Center work thread; they do not cover every file in every other conversation.

## Universal backfill task for EVERY prior FMP conversation

1. **Re-read the latest** [AGENTS.md](../AGENTS.md), [archive policy](ARCHIVE_POLICY.md), this register and latest GitHub commits. These instructions apply **retroactively**, including all files created in that same chat before the policy date.
2. Inventory *every meaningful file created or modified in that chat*, not just the last release: originals and references, ZIPs, renders, print/CAD/runtime outputs, image/film frames, calculators, code, tests, spreadsheets, PDFs, QA reports, working source generators and revisions. Check all previous upload/attachment links and Libraries accessible to that conversation; include alternate derivative versions where useful. Do not conflate a source reference URL with downloaded bytes.
3. Match actual filenames and cryptographic hashes against what exists in both GitHub (direct Git, LFS or release binaries) and project Drive (actual files or indexed package members). Check every ZIP's member list and SHA-256; retain original byte identity, rights metadata and master/derivative classification. Reuse already-archived matching files rather than uploading duplicate copies.
4. Recover missing copies in the appropriate destination, verify Git commit/release IDs and Drive file IDs with readback. **Never force-push or overwrite existing historical masters.** Coordinate simultaneous chats by rereading current SHA immediately before file changes.
5. If Git LFS or GitHub releases are unavailable, record `GIT_BINARY_PENDING` for a Drive-only binary. If the underlying reference is copyright-restricted, use `BLOCKED_RIGHTS` with a public-safe pointer instead of illegal public redistribution. Lack of access becomes `UNRECOVERED`, not a fabricated file.
6. Append/reconcile a manifest entry (or component-specific subregister) containing **originating thread, component, file/version, provenance and class, SHA-256, byte size, GitHub path+commit or release, Drive link+ID, license, exact status, verification date and outstanding fix**. Mirror this manifest to both systems. Report gaps explicitly.
7. Where possible export the **complete verbatim ChatGPT conversation** and attachment inventory to Drive, with a GitHub-safe manifest/export pointer. If the transcript cannot be accessed through tools, keep `TRANSCRIPT_PENDING`; a short work log is not a replacement.

## Initial known items from the Theme Center conversation

*These are not automatically representative of other FMP chats. Explicit status refers to the file or ZIP **itself**, not every script or manifest inside it.*

| Artifact/workstream | Verified Drive copy | GitHub situation | Initial status / required recovery |
| --- | --- | --- | --- |
| Theme Center original 510-node source `FMP_ThemeCenter_Staging_v001.glb` | [Drive](https://drive.google.com/file/d/197H4eTaLAFYEyfPSFFh8wp7_2B5IflIl/view) | [Dossier/manifest pointers](../research/pavilions/theme_center/README.md), binary Git mirror unverified | `GIT_BINARY_PENDING`. Check permitted Git LFS/release byte copy before upgrading. |
| Theme Center assembled `FMP_ThemeCenter_Assembled_Runtime_v005.zip` | [Drive](https://drive.google.com/file/d/1OzFZRkHCxN3jMBGwH3Lwdbx0pFJIJhM0/view) | [Manifest](../research/pavilions/theme_center/ASSEMBLED_RUNTIME_v005.json), binary ZIP Git mirror unverified | `GIT_BINARY_PENDING`. Preserve source and exact hash. |
| Framed portal v007 ZIP | [Drive](https://drive.google.com/file/d/1nR8_305Dx3t6yEbcRdMPhm1Owi-vqS6Y/view) | GitHub binary mirror not checked | `GIT_BINARY_PENDING`. Check contents, version and component dossier before a new upload. |
| Photo-control registration ZIP | [Drive](https://drive.google.com/file/d/1fMraAZ0QP5oNaaYTtlLG44qOfa-HidbY/view) | [Evidence record](../research/pavilions/theme_center/BRIDGE_PHOTO_CONTROLS_v001.md), ZIP binary Git copy not confirmed | `GIT_BINARY_PENDING`; register exact package members and hashes. |
| Wolfram + Game Development Studio engineering gate ZIP | [Drive](https://drive.google.com/file/d/1PwBZnZ2oDG24TLnF8tQhxWZhhqK2POF_/view) | [GitHub source handoff](THEME_CENTER_ENGINE_HANDOFF_v001.md), packaged ZIP itself not confirmed in Git | `GIT_BINARY_PENDING` at package level; some text/source files already tracked. |
| Runtime mesh audit ZIP | [Drive](https://drive.google.com/file/d/15b2j_-anBktrh5OKAKYOeVMtHdjqVkCv/view) | [GitHub audit](../research/pavilions/theme_center/RUNTIME_MESH_AUDIT_v001.md), ZIP itself not confirmed in Git | `GIT_BINARY_PENDING` at package level. |
| Return-route continuity ZIP | [Drive](https://drive.google.com/file/d/1vNaxcSn4SbtOJvH-rTbEmFqdFqGz93UR/view) | [GitHub audit](../research/pavilions/theme_center/RETURN_ROUTE_CONTINUITY_v001.md), ZIP itself not confirmed in Git | `GIT_BINARY_PENDING` at package level. |
| Real v005 Trylon passage rendering evidence ZIP | [Drive](https://drive.google.com/file/d/1o8OZlu-q0IOiZbpr90lobYrRql2T6bZ0/view) | [GitHub review](../research/pavilions/theme_center/TRYLON_PASSAGE_VISUAL_REVIEW_v001.md), actual rendered PNGs/code require individual manifest reconciliation | `GIT_BINARY_PENDING`; inspect ZIP members; avoid confusing archival/reference photos with rendered model views. |
| Bridge entrance archival/model audit ZIP | [Drive](https://drive.google.com/file/d/1LJYXE5P1_tQiUts20qocl2HgGcpMEWih/view) | [GitHub evidence](../research/pavilions/theme_center/BRIDGE_ENTRY_PRIMARY_EVIDENCE_v001.md), binary release in Git not confirmed | `GIT_BINARY_PENDING` and rights review on originals if included. |
| Period photographs/film frames and engineering sheets linked during this work | [Research source list](../research/pavilions/theme_center/BRIDGE_ENTRY_PRIMARY_EVIDENCE_v001.md); individual high-resolution source files not exhaustively verified | Citation links are not downloaded bytes | `SOURCE_ACQUISITION_PENDING` per source; check owner, rights and original scan; never expose restricted scans via public Git. |
| Entire word-for-word Theme Center ChatGPT transcript and attached-file inventory | No confirmed exact ChatGPT transcript export | [Curated backup summary](FMP_2026-10-20_CONVERSATION_BACKUP_INVENTORY_v001.md), not a verbatim transcript | `TRANSCRIPT_PENDING`. Export and verify when accessible. |
| Other FMP conversations' historical output (including Worldwright/other pavilion developments in other threads) | Not audited by this register | Not audited by this register | **Open project-wide retroactive audit.** Each resumed thread discovers and registers its own files. |

## Additional archive safeguards

- **Rejected AI-generated illustrations** remain `REJECTED_NON_EVIDENCE` if retained as part of an exact transcript. Never copy into primary photographic evidence, architectural masters or photo-fit datasets.
- Existing source, printable and runtime objects stay separate, with distinct hashes and dated histories. A processed derivative does not replace the source master.
- Work interrupted by missing connector/CLI access is **PENDING**, not verified. Do not promise background sync.
- For large original rights-cleared binaries, prefer an authorized Git LFS or release workflow over polluting Git history. Until a GitHub *binary* is actually retrievable, dual verification remains open.
- This register is append-only in intent; reconcile duplicate hashes/records and update statuses **only after validating the evidence**.

## Proof of completion for an artifact

`DUAL_VERIFIED` is permitted only when all are true: **GitHub actual bytes verified** (path+commit / LFS / release), **Drive actual bytes verified** (file ID + folder), **SHA-256/byte-size correspondence verified**, appropriate license/rights clearance recorded, ZIP members accounted for, and originating chat/component documented. Otherwise state the exact pending condition.

**Initial status:** retroactive policy active; historical backfill remains **IN PROGRESS**.

## Portal finishing thread: bounded recovery batch

The unfinished-ends/returns workstream recovered v007 source, validation hardening, model, four original renders, section PNG/SVG, measurement JSON and original release ZIP into [Drive archive 1yF-mgJDTLaksGkV231E65VvXvVxSAZwr](https://drive.google.com/file/d/1yF-mgJDTLaksGkV231E65VvXvVxSAZwr/view). Folder and size were verified. [Inventory and hashes](../tools/portal_finish_v007/SECTION_ARCHIVE_INVENTORY.json), [current receipt](../tools/portal_finish_v007/SECTION_ARCHIVE_RECEIPT.json), and [ten earlier accessible files](../tools/portal_finish_v007/LEGACY_WORKSPACE_INVENTORY.json).

SVG, code and JSON are directly tracked under `tools/portal_finish_v007`; current register/dossier/receipt are mirrored in a supplemental Drive ZIP named `FMP_Portal_Archive_Records_v007_v2.zip`. PNG, GLB and ZIP binary Git copies remain `GIT_BINARY_PENDING`; direct push failed for missing write credentials and no release/LFS connector is exposed. The earlier records ZIP is superseded because it was assembled before the failed push returned. Earlier file origins and byte copies remain `LEGACY_COPY_VERIFICATION_PENDING`. Do not infer project-wide dual completion. Verbatim conversation: `TRANSCRIPT_PENDING`.

## 2026-10-20 Backfill batch 01: Theme Center files and hash checks

- **Reproducible batch manifest:** [8 archives / 52 members with SHA-256 per member](FMP_DUAL_ARCHIVE_BATCH_20261020_01.json). [Read-only audit report](FMP_DUAL_ARCHIVE_AUDIT_BATCH_20261020_01.json). [Interpretation and recovery steps](FMP_DUAL_ARCHIVE_BATCH_20261020_01.md).
- **Local test result:** 11 of 11 synthetic unit tests passed for [hash and ZIP verification](../tools/archive/audit_dual_archive_v001.py), with [test script](../tools/archive/test_audit_dual_archive_v001.py) and [batch manifest generator](../tools/archive/generate_dual_archive_batch_v001.py). The eight source ZIPs and their 52 internal files passed local integrity checks.
- **Original ZIP package backfill:** eight selected archives remain **`GIT_BINARY_PENDING`**, not `DUAL_VERIFIED`. Drive metadata confirms file names, matching sizes and canonical FMP parent. GitHub has some source members but **no independently retrieved identical GitHub ZIP binary**. A proposed path or code-only commit cannot count as a second physical ZIP copy. Binary upload was blocked, no release was fabricated.
- **Six newly created audit source files:** all are committed in GitHub and their actual bytes are preserved in Google Drive. After a raw Drive download, SHA-256 equality with the local originals was confirmed for five, and exact Drive-vs-GitHub text equality was confirmed for the sixth Markdown file. Independently retrieved GitHub Git-blob SHA-1s matched the local original files. These files are **`DRIVE_FOLDER_PENDING`** for project-archive completeness because their verified Drive copies currently remain in **My Drive root**, rather than inside the FMP Drive parent folder: moves were blocked by connector safety checks. **Do not mark the six as `DUAL_VERIFIED` until location is corrected.**
  - GitHub audit tool: [`audit_dual_archive_v001.py`](../tools/archive/audit_dual_archive_v001.py) / Drive file `13FgnLDctd2QTnNRibn-nY7VNEeyvPFzX`.
  - GitHub tests: [`test_audit_dual_archive_v001.py`](../tools/archive/test_audit_dual_archive_v001.py) / Drive file `1qNOCoxkW6CrjFZN9cgQjyj9cEplJdIRu`.
  - GitHub generator: [`generate_dual_archive_batch_v001.py`](../tools/archive/generate_dual_archive_batch_v001.py) / Drive file `1fQhFv3YPIFGRXZsz9pM6NshevUDvSusW`.
  - GitHub [batch manifest](FMP_DUAL_ARCHIVE_BATCH_20261020_01.json) / Drive `1MfXXLr0pXqpIyz0Phma3XEkeUWvhubbQ`.
  - GitHub [batch audit report](FMP_DUAL_ARCHIVE_AUDIT_BATCH_20261020_01.json) / Drive `1v_sLEdPYC2IfwJU-90EWD5PDyUXHMfOO`.
  - GitHub [instructions](FMP_DUAL_ARCHIVE_BATCH_20261020_01.md) / Drive `1GRY1aD-gMPV9PSGP1W9N8MerbmjvIhNN`.
- **Critical boundary:** A matched local source tree is not proof of a remote GitHub release/commit; archived original scans need rights review. A successfully uploaded Drive root file is not yet in the designated FMP archive. Future chats should reconcile missing moves and exact Git binary copies rather than creating more manifests that falsely close these gaps.

## 2026-10-21 Backfill batch 02: 18 source copies reconciled

**Supersedes the `DRIVE_FOLDER_PENDING` state for the six audit files in the 2026-10-20 batch-01 section above; the older section remains as an audit trail.** Authenticated Google Drive API copied each file into [Backfill Audit Batches](https://drive.google.com/drive/folders/1T5tEnKN9qCcDr24oewLizJ2nQ2SmLMy_), verified this folder is a child of the canonical FMP Drive project folder, then downloaded the stored raw bytes. Independently retrieved current GitHub file bytes and Git blob SHA-1 identities. **Six of six are exact byte-for-byte matches, original sizes preserved, and both remote endpoints readable: `DUAL_VERIFIED` for these exact versions.** Earlier Drive-root copies were left untouched for provenance/cleanup later.

| Exact GitHub source | Git blob SHA-1 | New Drive project-folder copy | Bytes | Status |
| --- | --- | --- | ---: | --- |
| [audit_dual_archive_v001.py](../tools/archive/audit_dual_archive_v001.py) | `049993a39417721e0b55a93e38ebbbeafc987e56` | [Drive](https://drive.google.com/file/d/1u6TnPxmCHz824hwZuU876f5l0Y6iOoun/view) | 6068 | `DUAL_VERIFIED` |
| [test_audit_dual_archive_v001.py](../tools/archive/test_audit_dual_archive_v001.py) | `b1f2cdb1bca5125de9e40d50abcd3555170ae162` | [Drive](https://drive.google.com/file/d/1SgOKfkH82gvW0iGbDu5osoq1yckjRuiQ/view) | 3953 | `DUAL_VERIFIED` |
| [generate_dual_archive_batch_v001.py](../tools/archive/generate_dual_archive_batch_v001.py) | `b688fa12f3dbbbda368427a3f64dfac94d43f143` | [Drive](https://drive.google.com/file/d/1dTHQGHweT0YWr0RYCrP7f9F6rSiCLQDV/view) | 3434 | `DUAL_VERIFIED` |
| [FMP_DUAL_ARCHIVE_BATCH_20261020_01.json](FMP_DUAL_ARCHIVE_BATCH_20261020_01.json) | `e2234c4ff94856a030f5d422cfcf1dd04b977d7f` | [Drive](https://drive.google.com/file/d/1pm-4P1A7f2HqCCGay8Cqb346HiJpD0yX/view) | 18127 | `DUAL_VERIFIED` |
| [FMP_DUAL_ARCHIVE_AUDIT_BATCH_20261020_01.json](FMP_DUAL_ARCHIVE_AUDIT_BATCH_20261020_01.json) | `2381e7326d7c073a756f5e0de04a523f671a3d86` | [Drive](https://drive.google.com/file/d/1PeskYVUYIKDGVPh2MBnn4gCtAzl6Ynas/view) | 5401 | `DUAL_VERIFIED` |
| [FMP_DUAL_ARCHIVE_BATCH_20261020_01.md](FMP_DUAL_ARCHIVE_BATCH_20261020_01.md) | `d431f3d1ee2a3dd2c44560c502da2d96b65964a6` | [Drive](https://drive.google.com/file/d/1A8wfs81uS6wyqJTIMGJz3yrnHQUiM-oN/view) | 4223 | `DUAL_VERIFIED` |

### Repaired exact source-member preservation for the first three Theme Center ZIPs

Compared 12 local original ZIP member bytes against the **Git blob SHA-1** of each current canonical source file, revealing that the GitHub copy of each previously lacked **only its terminating LF (`\\n`) byte**. We verified this was the *sole* difference by hashing both the complete member and member minus one byte. Restored those 12 original trailing LF bytes with guarded SHA Git updates, without changing any code or historical content. All 12 current Git blobs were then independently fetched and verified **exactly equal** to the corresponding archived ZIP member bytes. These 12 member files are therefore backed by Git and are also present within existing verified Drive ZIP packages:

- `FMP_ThemeCenter_Wolfram_GameDev_EngineeringGate_v001.zip`: four exact source members under `tools/world_build/`, `research/pavilions/theme_center/`, and `docs/`.
- `FMP_ThemeCenter_RuntimeMesh_Audit_v001.zip`: four exact source members under `tools/world_build/` and `research/pavilions/theme_center/`.
- `FMP_ThemeCenter_ReturnRoute_Continuity_v001.zip`: four exact source members under `tools/world_build/` and `research/pavilions/theme_center/`.

The original ZIP member manifest and SHA-256 digests remain [machine-readable](FMP_DUAL_ARCHIVE_BATCH_20261020_01.json); Git SHA-1 identities match their members' exact bytes. A fresh local execution of all three synthetic test modules from the preserved source ZIPs ran **24/24 passing tests**, return code 0 (separate unrelated environment spreadsheet-warmup warning printed at startup). This does not certify Unreal native collision or the Game Development Studio CLI.

**Important remaining boundary:** The complete eight original ZIP packages are **still `GIT_BINARY_PENDING`**. Individual member files being in Git does NOT mean the exact archived ZIP container is in GitHub. Five other ZIPs in batch 01 remain to be reconciled per member. Full verbatim chat transcript is still `TRANSCRIPT_PENDING`. Do not conflate successful read-only tests with full engine acceptance. No historical masters or source ZIP bytes were altered.


## 2026-10-21: Portal finishing thread v008 landing repair

[Component evidence](../research/pavilions/theme_center/UPPER_LANDING_v008.md), [18-member inventory](../tools/portal_approach_v008/ARCHIVE_INVENTORY.json), [Drive package 14X-Jp_tt8PfbNNy0F3TpBFkuKbJM5eGO](https://drive.google.com/file/d/14X-Jp_tt8PfbNNy0F3TpBFkuKbJM5eGO/view). Code, SVG and JSON committed through 0d4a6db42de08b3a5347c34d18e2a41207ea3792; complete source and binaries are in project Drive with metadata readback. PNG/GLB/ZIP remain GIT_BINARY_PENDING. Source/dossier/register snapshots mirrored in FMP_UpperLanding_v008_Record_Snapshot.zip. Older workstream backfill and TRANSCRIPT_PENDING remain open.
