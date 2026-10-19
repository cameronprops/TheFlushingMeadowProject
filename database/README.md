# Point of truth and query database

Editable text catalogs live in `catalog/*.csv` and `archive/releases.csv`. Build a fresh SQLite index via:

```bash
python tools/validate_catalog.py
python tools/build_db.py --output out/flushing_meadows.sqlite
```

The SQL schema supports eras, places, research sources, source-backed claims, surveys, vertical/horizontal georeferencing, archive files, transit and era-specific geometry. The seed import currently fills only eras, places, sources and releases. Other tables are ready for data entry after acquisition and verification.

Do not treat the 20 seed catalog records as an exhaustive fair-wide inventory; more than 50 targets existed in the working research draft, and hundreds of site structures may ultimately need individual records. The master workbook and initial SQLite research snapshot exist as separate research artifacts; they must be reconciled rather than silently bulk-labeled verified.

Do not commit generated `*.sqlite` files; commit reviewed source data and migrations.

## Literary and narrative sources (v1.1.1)
`catalog/narrative_literature.csv` and `catalog/narrative_threads.csv` preserve **25 researched source records** and **20 source-grounded subjects** from guidebooks, archives, contemporary publications, film catalogs, memoirs and fiction. They are imported through `database/migrations/001_narrative_tables.sql`. Source URLs and their availability/rights status are included in every record. Historical fact, recollection and fiction remain distinct.

The [complete research snapshot on Drive](https://drive.google.com/file/d/1u5ppoqDwpmKF4tg_EZPgZOMlYFJnEybL/view?usp=drivesdk) contains the earlier 239-candidate SQLite index extended with literature tables, plus a researcher-friendly spreadsheet. It does not mean the historical source scans or copyrighted books were downloaded or cleared.
