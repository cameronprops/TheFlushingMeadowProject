# Point of truth and query database

Editable text catalogs live in \`catalog/*.csv\` and \`archive/releases.csv\`. Build a fresh SQLite index via:

\`\`\`bash
python tools/validate_catalog.py
python tools/build_db.py --output out/flushing_meadows.sqlite
\`\`\`

The SQL schema supports eras, places, research sources, source-backed claims, surveys, vertical/horizontal georeferencing, archive files, transit and era-specific geometry. The seed import currently fills only eras, places, sources and releases. Other tables are ready for data entry after acquisition and verification.

Do not treat the 20 seed catalog records as an exhaustive fair-wide inventory; more than 50 targets existed in the working research draft, and hundreds of site structures may ultimately need individual records. The master workbook and initial SQLite research snapshot exist as separate research artifacts; they must be reconciled rather than silently bulk-labeled verified.

Do not commit generated \`*.sqlite\` files; commit reviewed source data and migrations.
