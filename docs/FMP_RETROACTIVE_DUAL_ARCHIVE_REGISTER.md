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
