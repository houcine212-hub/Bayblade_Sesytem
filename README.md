# Multiplayer Spinning-Top Battle Game — Design Package

> **Current phase: DESIGN (Milestone M0), package v0.4.1 — G0 decisions integrated (owner-confirmed D-01…D-03, delegated D-04…D-18) and owner decisions OQ-LN-08 / OQ-CB-12 applied. The owner accepted Gate G0 with changes on 2026-11-22 for M1 technical spikes only (`docs/09-review/G0-approval-review.md`). M1 is authorised but has not started; no M1 spike has been run.**
> This package contains no game code, scenes, scripts, migrations or infrastructure. G0 authorises M1 spikes only — not M2 features, deployment, ranked play or merging PR #1.

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
| `docs/02-uml/` | PlantUML: context, use case, domain model, combat class model, 10 sequences (SQ-01…SQ-10), activity, 3 state machines (room, match, per-Bey), component, deployment — 20 diagrams; the ERD is the 21st (`docs/03-data/erd.puml`) |
| `docs/03-data/` | `erd.puml`, `data-dictionary.md` (entities, integrity, indexes, retention, memory vs DB) |
| `docs/04-interfaces/` | `backend-api.md`, `multiplayer-protocol.md`, `interaction-boundaries.md` |
| `docs/05-architecture/` | `architecture.md` + `adr/` (ADR-001…015; ADR-003 superseded by ADR-012; index and sources in `adr/README.md`) |
| `docs/06-security/` | threat model, auth & permissions, moderation, secrets & backups |
| `docs/07-quality-operations/` | test strategy, load-test plan, operations, MVP readiness |
| `docs/08-planning/` | roadmap + dependency map, traceability matrix, risk register |
| `docs/09-review/` | **G0 approval review** (accepted, M1 only), G0 decision sheet, v0.4 G0 decision changelog, v0.4.1 owner-decisions changelog, v0.3.1 audit correction log, design review report |
| `tools/analysis/` | **design-analysis bundle (not game code)**: reproducible 1-v-1 combat model, configs, fixed seeds, CSV/JSON results |
| `docs/10-game-design/` | **GDD**, statistics, classification, combat interaction, launch, burst, skills, controls specs; balancing report; research references; change proposals |

## Status labels
**[C]** confirmed by owner · **[D]** decided under owner delegation at G0 (pending M1 verification) · **[P]** proposed recommendation · **[A]** assumption · **[TBD]** open question.
[C] and [D] items are the recorded decisions ([D] pending M1 technical verification); [P]/[A]/[TBD] are not. See `docs/01-requirements/assumptions-and-open-questions.md`.

## Decisions at a glance (v0.4.1)
| Owner-confirmed [C] | Decided under delegation at G0 [D] (pending M1) | Open owner questions |
|---|---|---|
| Godot; Windows/Android/Linux first; one account (e-mail + password, unique names) | Stack: PHP 8.3+ / Laravel 13 / Reverb / MySQL 8.4 + Godot 4.7 headless UDP server — **conditional on M1** (D-15) | OQ-LN-09 accessibility of linear launch |
| ≤ 5 competitors; ~100 peak CCU target; FFA; ring-out; Burst primary | Burst = signature finish; M-1/M-2 targets (D-09/D-10); hybrid Lock Integrity (D-14) | — (OQ-LN-08 and OQ-CB-12 decided by owner, 2026-11-22) |
| 360° joystick + Skill button | Same-tick: shared placement, all-out = draw (D-11); 120 s limit ranked by spin (D-16) | — |
| **Launch: RPS = max(20, 10 × accepted presses) (D-01/D-03 amended by OQ-LN-08); READY 1.5 s + 5 s window (D-02)** | Cap 35 presses → max 350 RPS, FC-1, ranked gate (D-04) | — |
| ATK/DEF/STA/MAG; Energy derived; RPS separate | Energy plain mean, provisional (D-07); Magic → skills (D-06); component properties (D-05); TIP headline type (D-08) | — |
| MySQL private; server-authoritative combat | Equation structure (D-12, values experimental); AC-1…AC-9 (D-13); D-17 option (b) with owner-amended 7-press (70-RPS) threshold (OQ-CB-12); formula/data corrections (D-18) | — |

## Reproducing the balance numbers
```bash
cd tools/analysis && python3 run_all.py
```
Requires Python ≥ 3.10 and numpy ≥ 2.0. Scope: 1-v-1 analytic model only — not gameplay validation (see `tools/analysis/README.md`).

## Viewing / editing diagrams
Sources are `.puml` (PlantUML) and one Mermaid block (`docs/08-planning/roadmap.md`).
VS Code: install the *PlantUML* extension (needs Java) and preview; or `java -jar plantuml.jar -tsvg docs/**/*.puml`.
GitHub renders Mermaid natively. Do not commit rendered images as the source of truth.

## Next milestone & approval gate
**G0:** owner accepts the approval-with-changes review (`docs/09-review/G0-approval-review.md`) →
**M1:** throw-away technical spikes per `docs/08-planning/M1-spike-checklist.md` (S-5 launch input study first) → AC-1…AC-9 evaluated → ADRs moved to Accepted/Superseded with evidence → M2 planning.
