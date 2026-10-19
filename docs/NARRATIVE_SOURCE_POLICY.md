# Literature as research material for potential gameplay
This is an **evidence source catalog, not an authored quest list**. All source-derived observations use fresh, concise summaries rather than reproducing copyrighted literature. Fiction may guide historical atmosphere; it is never proof of a real structure, character, or event.

## Research and rights gates
- Treat period **guidebooks and timetables** as leads for show operation, opening and closing times, and spatial sequencing, but verify individual issue/date.
- Treat **firsthand oral histories** as attributed recollections, cross-checked against production records.
- Treat **novels and children's books** as fictional perspectives only. Adaptation of protected characters, plots or wording requires permission.
- Preserve source permalink, access status, rights status, and physical-asset checksum when legitimately obtained.
- Never assign a narrative to a pavilion or era without primary evidence and historical coordinates.
- Separate 1939, 1940, 1964, and 1965 content explicitly. A 2026 visitor may examine archival evidence about previous periods; this does not license use of a copyrighted story.

## Data
- [Research source CSV](../catalog/narrative_literature.csv)
- [Grounded subject CSV](../catalog/narrative_threads.csv)
- [SQLite migration](../database/migrations/001_narrative_tables.sql)
- [Drive archive](https://drive.google.com/file/d/1u5ppoqDwpmKF4tg_EZPgZOMlYFJnEybL/view?usp=drivesdk)

To test: `python tools/validate_catalog.py` and `python -m unittest discover -s tests -v` followed by `python tools/build_db.py`.
