# Reconciling the initial historical database

The archived SQLite snapshot contains 59 place/exhibit targets, 66 research sources, 99 source links, and 184 production tasks, largely focused on 1939/1940. This exceeds the current Git starter catalog. The Git catalog should not silently inherit older guesses as fact.

## Import gates
1. Import all named and unnamed assets with stable IDs; preserve original data and source references.
2. Reconcile 32 M-number placeholder masses with a controlled dated site-plan registration. Keep M IDs as aliases, not pavilion identities.
3. Separate entity types: permanent buildings, temporary pavilions, concessions, stages, attractions, exhibits, scenery, service, infrastructure, subway/rail, street blocks, parking, landscape, signage, monuments and utilities.
4. For each era document built/altered/removed states. Include 1939 versus 1940 and 1964 versus 1965 changes.
5. Retrieve actual scans when permitted; separately record plan catalogs and archive request statuses.
6. Register all survey control, horizontal CRS, vertical datums, and historical grading before loading measured coordinates.
7. Map each place to an Unreal asset root and collision/LOD/interaction state only after evidence review.

**Do not mark inventory exhaustive** until every structure or explicitly unresolved mark on all baseline official dated plans has a documented entry and reconciliation report.
