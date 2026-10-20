# FMP working instructions

## Mission, historical rigor, and tool orchestration

FMP is a source-backed, explorable reconstruction of the New York World's Fairs at Flushing Meadows, beginning with a historically credible 1939-1940 site. It is also a modular reference world for architecture, engineering, education, fabrication, digital archaeology, and flexible Unreal-based experiences. The world comes first. Preserve the historical master geometry separately from runtime meshes, printable variants, and authored/speculative worlds. Read the [README](README.md) for the current milestones, era scope, and component links.

At the beginning of **every substantive FMP work session**, assess and actively use the relevant connected specialist plugins and local tools, particularly **Wolfram** and **Game Development Studio**, when they can verify or materially improve the work. Do not simply recommend a tool when it can perform a needed calculation, audit, or production step. Do not make irrelevant tool calls merely to satisfy a name-check. Availability varies by agent and environment: use actual accessible capabilities, and state precisely when a specialist was unavailable or a check was not run.

### Default specialist routing

| Capability | Required behavior when applicable |
| --- | --- |
| **Wolfram** | Primary computational and engineering verifier. Use Wolfram Language / Wolfram|Alpha for mathematical solvers, coordinates, truss/structural plausibility, Trylon and Perisphere geometry, Helicline slope/radius/clearance, perspective constraints, dimension inference, uncertainty and error residuals. Request Wolfram context first where its integration requires it. Record exact assumptions, units, equations and outputs. A structural calculation is not a certified engineering design. |
| **Game Development Studio** | Primary specialist workflow for game assets and technical runtime verification. Use its asset-production, asset-vendoring, visual-debugging, and performance-optimization skills as appropriate to validate GLB/other game assets, transforms, topology, materials, package integrity, rendered captures and measurable performance. Use cross-workflow orchestration for multi-stage production. These checks do not substitute for tests inside Unreal. |
| **GitHub** | Inspect existing implementation and current default-branch commits, preserve working code and tests, commit validated changes, and avoid overwriting concurrent work. This repository is the source record for code, decisions, manifests and asset pointers. |
| **Google Drive** | Archive large CAD/mesh/scene/reference releases and research with stable links, version IDs, hashes, licensing/rights metadata, and corresponding Git references. Follow [archive policy](docs/ARCHIVE_POLICY.md). |
| **SciSpace and public archival research** | Find scholarly literature, engineering background, original plans, contemporary technical publications and primary historical material. Follow the repository evidence rules and distinguish leads from actually reviewed records. |
| **Data Analytics / Python** | Examine geospatial/evidence datasets, detect errors and duplicates, calculate uncertainty, create reproducible inspections and evidence-based dashboards or reports when useful. |
| **Product Design / other relevant specialists** | Use for requested interface, accessibility, navigation or interaction audits. Discover and invoke other available connected tools when they produce a tangible benefit. |

### Historical reconstruction acceptance

- Start from authoritative dated plans, surveys, construction records, period photos, film frames and documented dimensions. Internet Archive / Prelinger footage is an important candidate for geometry and feature-placement analysis, but footage is evidence to inspect, not automatic proof of exact dimensions.
- Label each geometric or historical assertion as **verified** (direct documentation), **derived** (auditable inference), **provisional** (unverified working placeholder), **interpretive** (declared approximation), or **simulated** (modern interaction or nonhistorical state). Include citations/source IDs, edition/year, coordinate reference, units, assumptions, residuals and confidence as applicable.
- Solve site registration, circulation and building massing before decorative reconstruction. Do not invent historical coordinates, footprints, facade heights or hidden truss members. Use photographic and numerical constraints to test alternatives; expose remaining ambiguity.
- Design assets for reuse across editable CAD, game-runtime and physical-print representations. Maintain immutable historical source inputs, editable generators, stable object IDs, per-era placement, reproducible exports and tests. Never promote an AI-generated image or mesh into historical evidence.
- Keep historical states **1939, 1940, 1964, 1965 and 2026** separate. Optional **NEW_FAIR** and **DECLINE** branches at **2039 and 2064** remain authored futures, not historical claims.
- Treat Unreal engine import, collision, traversal, navigation and streaming as distinct test gates. A generated model, viewer screenshot, mesh audit, or Wolfram calculation alone does not certify a playable Unreal experience.
- Cameron retains all story, genre, artistic and speculative creative decisions. Provide research, implementation, testing and technical criticism without inventing canon or committing an unsolicited creative direction.

### Working handoff requirements

For each substantive change, leave a traceable **source -> inference / generator -> asset -> verification -> commit / archive** chain. Report the exact created/modified paths, commit IDs and archive links, successful and unsuccessful test scope, unresolved historical uncertainties and the next executable production step. Continue from the latest verified state rather than producing duplicate frameworks.

## Resume from shared state
- Read README.md and recent default-branch commits before choosing work. Then read the affected component dossier and applicable nested instructions.
- Treat docs/FMP_WORK_THREAD.md as history. Later component updates and verified artifacts may supersede its earlier next-step lists.
- Inspect current files and asset manifests before making changes. Other conversations may be working concurrently. Fetch the current file SHA immediately before API updates; preserve unrelated work and never force-push over it.
- Check for existing assets, scripts and source records before creating replacements. Continue the next useful unfinished production gate.

## Accepted project direction
- World first, exteriors and circulation first. Reuse the integrated Theme Center assembly.
- Build a historically grounded world for 1939, 1940, 1964, 1965 and 2026. Keep year-specific terrain, evidence and object presence distinct.
- Preserve flexible maps, inventory/tickets/tools, photography, puzzles and exploration. Separate world data, shared systems and experience rules; keep stable IDs and saveable state.
- Genre, story and artistic decisions belong to Cameron. Do not invent canon or treat gameplay references as a locked design.
- Optional NEW_FAIR and DECLINE branches each have 2039 and 2064 states. Keep authored futures separate from historical claims.

## Evidence and asset safety
- Follow docs/RESEARCH_RULES.md, docs/GEOSPATIAL_STANDARD.md and docs/ARCHIVE_POLICY.md.
- A catalog record or accessible source URL is not a reviewed drawing, measured dimension or completed model.
- Label provisional geometry and record provenance, units, coordinate frame, year, uncertainty and rights.
- Preserve archival inputs and original watertight print shells. Runtime cutouts, display overlays and print cutters require separate versions and acceptance checks.
- Do not claim Unreal import, collision, navigation, streaming or playability from offline mesh/script tests.
- Prefer concrete world progress to additional scaffolding unless a specific dependency requires tooling.

## Finish with a usable handoff
- Validate the change at the appropriate scope and state what was actually tested. Document unavailable engine/source/asset prerequisites.
- Commit relevant code, data and decisions. Preserve large deliverables in the project Drive archive with stable references and hashes, following existing project authorization and tool capabilities.
- Update the relevant component dossier with the result, asset/version references, open blocker and next executable step.
- Update README.md when overall status or priorities change. Keep detailed evidence in component records rather than duplicating it everywhere.
- Report completed work and material limits concisely. Never imply a local-only change was committed or a failed upload was archived.
