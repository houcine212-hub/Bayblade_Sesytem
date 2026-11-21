# UML & system models

All diagrams are **PlantUML** sources (`.puml`). Labels: [C] confirmed, [P] proposed, [TBD] open.

| File | Diagram | Key requirements |
|---|---|---|
| `context.puml` | System context | SEC-001, FR-150, CON-03 |
| `use-case.puml` | Use cases UC-01…UC-23 | all FR groups |
| `domain-model.puml` | Domain / class model | FR-020…FR-133 |
| `sequence/SQ-01-register-login.puml` | Registration & login | FR-002, FR-003, FR-006 |
| `sequence/SQ-02-create-join-room.puml` | Create / join room | FR-030…FR-035, BR-001 |
| `sequence/SQ-03-match-authorization.puml` | Allocation + match tickets | FR-050, FR-051, SEC-006 |
| `sequence/SQ-04-launch-start.puml` | READY, 5 s rapid-press launch, battle start | FR-052, FR-053, FR-180–FR-185 |
| `sequence/SQ-05-elimination.puml` | Contact resolution & elimination (BURST primary) | FR-056, FR-060, FR-210–FR-224 |
| `sequence/SQ-06-spectator-transition.puml` | Spectator transition / join | FR-058, FR-090, FR-091 |
| `sequence/SQ-07-match-completion.puml` | Result persistence | FR-070, FR-071, FR-100 |
| `sequence/SQ-08-disconnect-reconnect.puml` | Disconnect / reconnect / server failure | FR-063, FR-064, FR-068 |
| `sequence/SQ-09-steering-prediction.puml` | Joystick steering, prediction & reconciliation (v0.2) | FR-170–FR-175, NFR-011 |
| `sequence/SQ-10-skill-activation.puml` | Skill activation & validation (v0.2) | FR-230–FR-234 |
| `combat-model-class.puml` | Combat model class diagram (v0.2) | FR-190–FR-241 |
| `state-bey-combat.puml` | Per-Bey combat state machine (v0.2) | FR-220–FR-233 |
| `activity-room-to-match.puml` | Room-to-match activity | FR-030…FR-070 |
| `state-room.puml` | Room state machine | FR-030…FR-039 |
| `state-match.puml` | Match state machine | FR-050…FR-069 |
| `component.puml` | Components | NFR-040 |
| `deployment.puml` | Initial deployment | CON-03, OPS-005, SEC-001 |
| `../03-data/erd.puml` | ERD | data dictionary |

## Viewing / editing
- **VS Code:** "PlantUML" extension (jebbs.plantuml) + Java; preview with Alt+D.
- **CLI:** `java -jar plantuml.jar -tsvg docs/**/*.puml` (render output is not committed; sources are the truth).
- **JetBrains IDEs:** PlantUML Integration plugin.
- Avoid pasting diagrams into public online renderers if they ever contain non-public information.

## Validation status (v0.3, 2026-11-21)
| Check | Tool | Result |
|---|---|---|
| **PlantUML syntax check** | `plantuml -checkonly` — PlantUML **1.2020.02** (Ubuntu package) + Graphviz | **21/21 files pass** |
| **PlantUML rendering** | `plantuml -tsvg` (same version) | **21/21 render to SVG**; no embedded error text in any SVG; 4 diagrams inspected visually as PNG (state-bey-combat, SQ-05, combat-model-class, use-case) |
| **Mermaid rendering** (`../08-planning/roadmap.md`) | `@mermaid-js/mermaid-cli` 11.x with headless Chromium | renders, no parse error |
| Static lint (participants, endpoints, block balance) | custom script | 21/21 pass — this is a structural check only and is **not** a substitute for rendering |
Caveat: PlantUML 1.2020.02 is older than current releases; syntax accepted by it is expected to be accepted by newer versions, but newer-only features are not used. Rendered images are not committed (sources are the truth); render locally with `plantuml -tsvg docs/**/*.puml`.

## Consistency rules
State names, message names and endpoint paths in diagrams must match
`../04-interfaces/*.md`. Change them in both places in the same commit.
