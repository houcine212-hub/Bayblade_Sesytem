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
| `sequence/SQ-04-launch-start.puml` | Pre-launch & launch | FR-052…FR-055 |
| `sequence/SQ-05-elimination.puml` | Ring-out elimination | FR-056, FR-057, BR-002 |
| `sequence/SQ-06-spectator-transition.puml` | Spectator transition / join | FR-058, FR-090, FR-091 |
| `sequence/SQ-07-match-completion.puml` | Result persistence | FR-070, FR-071, FR-100 |
| `sequence/SQ-08-disconnect-reconnect.puml` | Disconnect / reconnect / server failure | FR-063, FR-064, FR-068 |
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

## Consistency rules
State names, message names and endpoint paths in diagrams must match
`../04-interfaces/*.md`. Change them in both places in the same commit.
