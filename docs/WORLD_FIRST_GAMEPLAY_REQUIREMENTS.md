# FMP: world-first direction and flexible gameplay requirements

Decision record: 2026-10-18, America/Los_Angeles.
Owner: Cameron Stern. Conversation: FMP Work Thread.
Status: accepted direction and capability requirements, not completed features.

## Core decision

Proceed world first. Build the historical environment in Unreal with reusable
objects and stable identities, preserving flexibility in how it eventually plays.
Cameron has not selected a final genre or a single gameplay format. The project
must accommodate one or more of the reference styles below without requiring
the world to be rebuilt for each format.

World first means advancing actual terrain, architecture, circulation and
exploration while accounting for future interaction and persistence. It does not
mean completing every building before testing player scale, access or navigation.
The previously suggested gameplay test milestone does not supersede the user's
latest instruction to continue world development first.

## User-specified references and capabilities

| Reference | Desired capability direction |
|---|---|
| Fortnite and GTA | In-game navigation maps, minimap and full-map interaction; a custom FMP interface rather than a generic engine presentation |
| Myst and The 7th Guest | Environmental and mechanism puzzles, inspection and state-dependent interactions |
| Return to Zork | First-person adventure interaction, contextual actions, inventory and conversations |
| Sierra Online point-and-click adventures | Point-and-click interaction and movement, action verbs, object use and combinations |
| Indiana Jones and the Fate of Atlantis | Adventure dialogue and inventory interactions; support for alternate solutions and branching play |
| Assassin's Creed | Exploration of historical environments; room for additional gameplay systems as the project develops |

These are functional references, not instructions to copy proprietary assets,
stories or interfaces. Combat, climbing, crowds, companions and complex traversal
are not automatically included or implemented by citing a reference game.

## Shared system requirements

- Inventory that holds tickets, documents, objects and tools, with stable item IDs.
- Ticket/access rules configurable by destination and date/era, including optional
  consumption. Exact ticket mechanics remain an authoring decision.
- In-world photography and a persistent photo album; retain capture location,
  active era/branch and camera information alongside image references.
- Reusable interaction actions: inspect, read, take, use, give, talk, operate and
  combine where appropriate. Available verbs are configurable, not compulsory.
- Puzzle state, prerequisites, multiple solutions, consequences and reset rules.
- Dialogue conditions, choices and remembered state; optional companion behavior
  is an extension rather than a commitment to a particular character or story.
- Discoveries, objectives and progress tracking.
- Full map and minimap with player location/facing, pan/zoom, landmarks, waypoints,
  distance and routes. Era-specific paths and access must affect navigation.
- Direct movement, click-to-move, fixed views and close inspection should be
  possible adapters to the same underlying interaction system.
- Save/load covering inventory, photo references, discoveries, puzzle states,
  access changes and player location. Persist state independently of streamed actors.

## Architecture direction

1. World data: geography, buildings, interiors, era-specific physical conditions
   and historical evidence, with stable place/object identifiers.
2. Shared gameplay services: inventory, interaction, photography, navigation,
   dialogue, conditions, objectives and persistence.
3. Experience rules: enable appropriate systems, controls, cameras, actions and
   progression for a selected mode or location.

Separate the action from its input. Using a ticket should invoke the same rule
whether triggered from an inventory click, verb menu or proximity interaction.
Avoid placing all experience logic in a building's level script. Keep historical
claims distinct from authored gameplay conditions and puzzle fiction.

Use location, era and scenario branch in persistent world-state keys where
appropriate. Do not accidentally share an unlocked door between different world
states. Which possessions travel across eras remains an explicit design decision.

## Engine responsibilities versus project work

The engine supplies underlying physics, collision, rendering, audio, animation,
movement, navigation and save-system facilities. Their use requires configuration,
assets, integration and testing. They do not automatically provide FMP's game rules.

Physics parameters include mass, gravity, friction and constraint limits. Each
interactive object should deliberately use simulation, controlled animation or
scripted behavior. Exact-position puzzle mechanisms may need controlled motion
for repeatability. Ticket validity, puzzle solutions, inventory behavior and
persisted consequences require project-specific implementation.

These are architecture notes, not an engine-version compatibility certification.
Validate specific Unreal APIs and plugins when implementing the selected systems.

## Production order after this conversation

1. Continue historical world work: review source material, acquire usable plans,
   establish control, build exteriors and circulation, and label uncertain massing.
2. Give modeled objects stable identities and preserve entry/access locations so
   navigation, interaction and saved state can attach without geometry rework.
3. Test a small explorable area for player scale, movement, collision and access
   before extending the same practices across the site.
4. Add a minimal shared-system test when useful: collect/inspect/use a test ticket,
   capture a photo, operate a neutral test mechanism and save/reload the state.
   This is an engineering test, not an approved narrative or historical scenario.
5. Expand gameplay modes as Cameron determines the final experience.

## Current implementation boundary

This thread has committed research registers, catalog comparison tools, an
exterior queue and a 2D registration solver. Seventeen Python tests passed at the
last implementation checkpoint. No playable Unreal build, inventory UI, camera
album, navigation-map UI or puzzle runtime was delivered in this conversation.
The historical Theme Center has not yet been survey-registered.

## Authorship and preservation

Cameron owns creative direction. Assistant work covers requested technical
implementation, research and organization; do not invent plot, characters,
puzzles or artistic direction. Commit relevant decisions and completed work to
Git and preserve requested notes in the existing Google Drive project folder.

Repository: https://github.com/cameronprops/TheFlushingMeadowProject
