# Optional future timelines: 2039 and 2064

**Status:** User-authored concept options, NOT locked canon or historical predictions.

The Flushing Meadows Project maintains a source-grounded baseline:
**1939, 1940, 1964, 1965, 2026**.

It may later support two **alternative** branches for **2039** and **2064**:

| Branch | 2039 | 2064 |
|---|---|---|
| `NEW_FAIR` | A utopian-feeling new World's Fair | A utopian-feeling World's Fair in a later generation |
| `DECLINE` | Post-apocalyptic Flushing Meadows | Conditions much worse than the 2039 decline |

These rows are **proposals for playable scene states**, not mandates to build both. Either branch may be revised, rejected or merged into a user-directed design. No architecture, characters, dialogue, or plot are implied by the labels.

## Data and geography
- Keep `catalog/eras.csv` at the five source-grounded eras.
- Store proposed years separately in `catalog/future_scenarios.csv`, indexed by `branch_id + year`.
- Both branches reference the **same stable site/place IDs** and coordinate frame as the historical world; each branch may replace topology, grading, objects, or landmarks later.
- Never use speculative future geometry or history as a historical source.
- The 2026 baseline is a research reconstruction in progress, not a validated elevation point of truth.
- Existing place and survey rows should not be overwritten for speculative content.

## Unreal architecture
A temporal travel destination can be either:
1. `HistoricalEra(year)`, where year is one of the five researched years; or
2. `FutureScenario(scenario_id)`, where ID resolves to branch plus year.

Use `scenario_id`, not year alone, to select speculative layers. The same year may have two completely different authored futures. A destination needs source-controlled location identity and an era-specific or scenario-specific playable arrival anchor. Verify collision and terrain before allowing traversal.

**No UE build or future landscape has been created by this metadata checkpoint.** Creative authorship remains with the project owner.
