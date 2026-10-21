# Archival preservation and licensing

## Storage roles
**Google Drive**: canonical original scans, plans, survey datasets, aerials, citations, high-resolution references, large versioned exports. Do not silently resave, crop or overwrite originals.

**GitHub**: metadata, code, small text catalogs, schema and database build code, release manifests, research notes, selected Git LFS working assets.

**SQLite**: generated indexed query copy of historical data; regenerate from reviewed records.

## Mandatory dual-copy archive and retroactive recovery

**Project-wide mandate, including all earlier FMP chat sessions:** Every new **and previously created** FMP deliverable or source-derived file used for ongoing work requires both:
- A validated GitHub file, Git LFS object, or GitHub release asset in `cameronprops/TheFlushingMeadowProject`, with an appropriate tracked manifest and exact commit/release identity.
- The same file or an original-byte-preserving ZIP in [The Flushing Meadows Project Google Drive archive](https://drive.google.com/drive/folders/11aRetkT2qaA69j8jnRyqxCJu2sR7DAPk), with verified Drive ID and folder membership.

**Source copies and metadata are different things:** A GitHub README pointing to a Drive-only ZIP is not a physical second copy. A Drive copy of a source script without the GitHub script is not a Git commit. A screenshot or a ChatGPT sandbox link is not a durable backup. Never mark an artifact fully archived when one destination only has a pointer. Large assets should use Git LFS or an authorized repository release where possible, without breaking size limits; if these facilities are unavailable, record a pending Git binary mirror, **not a fabricated success**.

Every work thread must backfill **all its own prior project artifacts** before calling its archive complete. Inspect prior attachments, created artifacts, connected GitHub paths and Drive folders; use exact versioned filenames and hashes. This covers research scans, stills/film frames, render sequences, CAD meshes and masters, generators, tests, drawings, spreadsheets, documentation, sample/experimental assets, verification reports and packaged releases. Avoid duplicating an identical verified hash under a new identity. Keep original masters intact. Preserve the difference between `historical source`, `evidence-based derived asset`, `provisional derivative`, `runtime derivative`, `print derivative` and `rejected synthetic non-evidence`.

**Archive completion state** (per file/revision, never generalized to an entire conversation):
- `DUAL_VERIFIED`: both actual copies are retrievable, Git commit/release and Drive file confirmed, SHA-256/size compared.
- `GIT_BINARY_PENDING`: Drive bytes exist, but GitHub contains only code/manifest/pointers or lacks the large asset.
- `DRIVE_COPY_PENDING`: GitHub file is present, but no verified same-content Drive copy.
- `UNRECOVERED`: source or generated chat attachment is known but not presently accessible to recover.
- `SOURCE_ACQUISITION_PENDING`: citation/catalog reference exists but licensed original source bytes have not been acquired.
- `BLOCKED_RIGHTS`: copying to public GitHub would violate rights, confidentiality or licensing; retain only authorized/private bytes plus a public-safe descriptive pointer, and mark exception.
- `TRANSCRIPT_PENDING`: complete verbatim conversation export, attachment inventory or message sequence has not been archived.
- `NOT_CREATED`: expected downstream artifact/test was never actually produced; do not treat it as a lost file.

Every created/recovered file must include or link to **originating chat/workstream, historical/provisional classification, actual filename, version, SHA-256, size, source and creator/rights, Git path + commit or release, Drive link + ID, verification scope and next action**. A ZIP must expose a member list and internal hashes. Track the status in the [retroactive backfill register](FMP_RETROACTIVE_DUAL_ARCHIVE_REGISTER.md) and component dossier. Verify both endpoints after upload; avoid rewriting existing identifiers or overwriting another thread's newer work.

**Chat transcript boundary:** A research summary does not preserve an exact ChatGPT transcript or all embedded media. If native transcript export is not available through the active tools, leave `TRANSCRIPT_PENDING` with the originating thread, and recover it by user export or direct attachment access when possible. Do not claim background synchronization.

**Safety:** The user's instruction to archive to GitHub never licenses public posting of restricted archival scans, private correspondence or personal information. Preserve locally/privately only when permitted, and record `BLOCKED_RIGHTS` rather than exposing it publicly. Archive rejected AI-generated graphics only in a clearly labeled non-evidence area if conversation-completeness demands, never in the historical-photo reference corpus.

## Required archival metadata
Each item should have a stable `source_id`, title, issuing institution, catalog permalink, original filename, source document date, acquisition timestamp, SHA-256, media/scan quality, archival Drive URI, download/access state, copyright/licensing assessment, and association to buildings/claims.

Mark records as **catalog lead**, **metadata retrieved**, **source downloaded**, **rights review pending**, **plan registered**, or **survey/control verified**. A catalog link is NOT proof a drawing was downloaded or fully inspected. Preserve low-value and unresolved leads too.

Do not redistribute scans where rights are uncertain. Drive folders and file links must be verified after upload, and any Git-hosted artifact must have an independently verified commit.

Known Democracity releases:
- v0.9.0 grounds: https://drive.google.com/drive/folders/1jsOrwquvw2OlEjolYfPzBDkO6EXupOWO
- v0.9.1 expanded walkthrough: https://drive.google.com/drive/folders/1HnGr2tsgES3kcTIRC_OwWzFc9TvY5yNz
- v0.9.2 visitor route repairs: https://drive.google.com/drive/folders/1mrHhpIy-ps5PJCF4GGw0LlsHrIa13fVx
- v0.9.3 architectural context study: https://drive.google.com/drive/folders/10aBO7aqyzeY5B6WvaenR7eisX-7ePFWZ

These folders hold prototypes/research; they do not establish historically as-built geometry.

## Verified project research snapshot
- Drive research snapshot: https://drive.google.com/file/d/1t5XpdiUC27QTL0928cQloJdRUSkGeAHj/view?usp=drivesdk
- SHA-256: `3c50e5b88fa79be8a17fb972ee0df41e573355a58ff98efa480d22257a79e5b0`
- ZIP integrity passed, 385 archived files.
- Historical-source URLs are acquisition leads unless their individual file download and rights status is independently documented.

Master research snapshot folder: https://drive.google.com/drive/folders/1zxrj-HFmhDQOQSH3f8zVCGtm0MDNMZcA
