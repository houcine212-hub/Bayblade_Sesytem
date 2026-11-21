# Multiplayer Spinning-Top Battle Game — Design Package

> **Current phase: DESIGN (Milestone M0), package v0.3 — awaiting Gate G0 decisions (`docs/09-review/G0-decision-sheet.md`).** This repository contains **documentation only**:
> no game code, scenes, scripts, migrations or infrastructure. Implementation starts only after the
> owner approves the design at **Gate G0** (`docs/09-review/design-review-report.md`).

## Product overview
A 3D online spinning-top battle game built with Godot for Windows, Linux, macOS, Android and iOS,
sharing one account, backend and multiplayer ecosystem. Rooms are joined by code; each match has
**at most 5 competitors**; players launch by rapid-pressing for 5 s, steer with a 360° joystick, use skills; **Burst Finish** is the primary elimination (ring-out and spin-out also eliminate, proposed); last top wins; the server decides everything.
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
| `docs/09-review/` | design review report and **G0 decision sheet** |
| `docs/10-game-design/` | **GDD**, statistics, classification, combat interaction, launch, burst, skills, controls specs; balancing report; research references; change proposals |

## Status labels
**[C]** confirmed by owner · **[P]** proposed recommendation · **[A]** assumption · **[TBD]** open question.
Only [C] items are binding. See `docs/01-requirements/assumptions-and-open-questions.md`.

## Approved decisions vs TBD (summary)
| Confirmed | Proposed (needs approval) | Open (blocking) |
|---|---|---|
| Godot; desktop + mobile; Windows/Android/Linux first, macOS/iOS later | Godot 4.7.x, GDScript, one project | Launch curve vs literal ×10 (CHG-01) |
| Max 5 competitors; 100 = peak CCU target | ENet/UDP; 1 match per process; local prediction | Component properties (CHG-02) |
| 360° joystick + Skill button; 5 s rapid-press launch (5 presses = 50 RPS) | Backend PHP + Laravel 13 + Reverb (ADR-012) | Magic scope & Energy weight (CHG-03, OQ-ST-02) |
| ATK/DEF/STA/MAG; Energy derived; RPS separate | Energy = plain mean (CHG-07), advantage S, v0.3 coefficients as spike start (ADR-013) | Burst-primary metric (CHG-09) |
| Burst Finish primary elimination; ring-out; last top wins | Hybrid burst model (ADR-014) | Time limit / tie rules |
| E-mail + password; unique display names | Skills catalogue & limits | Skill limits & catalogue |
| MySQL private; server-authoritative combat | Rooms in Backend + Reverb push | Backend stack approval (ADR-012) |
| Exploration postponed; no real-money wagering | MVP = battle + small social layer | — |

## Viewing / editing diagrams
Sources are `.puml` (PlantUML) and one Mermaid block (`docs/08-planning/roadmap.md`).
VS Code: install the *PlantUML* extension (needs Java) and preview; or `java -jar plantuml.jar -tsvg docs/**/*.puml`.
GitHub renders Mermaid natively. Do not commit rendered images as the source of truth.

## Next milestone & approval gate
**G0:** owner answers the blocking questions and approves (or amends) ADRs and MVP scope →
**M1:** throw-away technical spikes (physics feel, network, server benchmark, mobile rendering) → ADRs accepted → M2 Battle MVP.
