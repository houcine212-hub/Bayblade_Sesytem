# Multiplayer Spinning-Top Battle Game — Design Package

> **Current phase: DESIGN (Milestone M0).** This repository contains **documentation only**:
> no game code, scenes, scripts, migrations or infrastructure. Implementation starts only after the
> owner approves the design at **Gate G0** (`docs/09-review/design-review-report.md`).

## Product overview
A 3D online spinning-top battle game built with Godot for Windows, Linux, macOS, Android and iOS,
sharing one account, backend and multiplayer ecosystem. Rooms are joined by code; each match has
**at most 5 competitors**; FFA = ring-out eliminates, last top wins; the server decides results.
The initial deployment is planned for **~100 concurrent connected players at peak** (planning target, not proven).

## Documentation map
| Folder | Contents |
|---|---|
| `docs/00-overview/` | `gap-analysis.md` (start here), `product-vision.md`, `product-scope.md` |
| `docs/01-requirements/` | `SRS.md`, `MVP-scope.md`, `assumptions-and-open-questions.md`, `glossary.md` |
| `docs/02-uml/` | PlantUML: context, use case, domain, 8 sequences, activity, 2 state machines, component, deployment |
| `docs/03-data/` | `erd.puml`, `data-dictionary.md` (entities, integrity, indexes, retention, memory vs DB) |
| `docs/04-interfaces/` | `backend-api.md`, `multiplayer-protocol.md`, `interaction-boundaries.md` |
| `docs/05-architecture/` | `architecture.md` + `adr/` (ADR-001…011 and cited sources) |
| `docs/06-security/` | threat model, auth & permissions, moderation, secrets & backups |
| `docs/07-quality-operations/` | test strategy, load-test plan, operations, MVP readiness |
| `docs/08-planning/` | roadmap + dependency map, traceability matrix, risk register |
| `docs/09-review/` | design review report and approval gate |

## Status labels
**[C]** confirmed by owner · **[P]** proposed recommendation · **[A]** assumption · **[TBD]** open question.
Only [C] items are binding. See `docs/01-requirements/assumptions-and-open-questions.md`.

## Approved decisions vs TBD (summary)
| Confirmed | Proposed (needs approval) | Open (blocking) |
|---|---|---|
| Godot; desktop + mobile; shared ecosystem | Godot 4.7.x, GDScript, one project | In-battle control? |
| Max 5 competitors; 100 = peak CCU target | ENet/UDP; 1 match per process | Spin-out / burst / time limit? |
| FFA ring-out, last top wins, eliminated spectate | Custom server-side top simulation | Five-second launch semantics & formula |
| MySQL, never exposed to clients | MySQL 8.4 LTS; TypeScript/Node backend | First platforms |
| Server-side official results | Rooms in Backend + WSS events | Registration method |
| Organizers need admin approval | Single VPS with systemd limits | Exploration timing |
| No real-money wagering / voice control in MVP | MVP = battle + small social layer | Backend language |

## Viewing / editing diagrams
Sources are `.puml` (PlantUML) and one Mermaid block (`docs/08-planning/roadmap.md`).
VS Code: install the *PlantUML* extension (needs Java) and preview; or `java -jar plantuml.jar -tsvg docs/**/*.puml`.
GitHub renders Mermaid natively. Do not commit rendered images as the source of truth.

## Next milestone & approval gate
**G0:** owner answers the blocking questions and approves (or amends) ADRs and MVP scope →
**M1:** throw-away technical spikes (physics feel, network, server benchmark, mobile rendering) → ADRs accepted → M2 Battle MVP.
