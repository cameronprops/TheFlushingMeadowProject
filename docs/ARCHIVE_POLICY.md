# Archival preservation and licensing

## Storage roles
**Google Drive**: canonical original scans, plans, survey datasets, aerials, citations, high-resolution references, large versioned exports. Do not silently resave, crop or overwrite originals.

**GitHub**: metadata, code, small text catalogs, schema and database build code, release manifests, research notes, selected Git LFS working assets.

**SQLite**: generated indexed query copy of historical data; regenerate from reviewed records.

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
