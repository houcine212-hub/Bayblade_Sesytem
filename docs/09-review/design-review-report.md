# Design Review Report — Gate G0 (package v0.2)

| Document ID | DOC-REV-001 | Version | 0.2 | Status | **Gate G0 NOT approved** — awaiting user decisions |
|---|---|---|---|---|---|---|---|

## 1. Acceptance checklist (Brief §O + Master Update)
| # | Criterion | Status | Where |
|---|---|---|---|
| 1 | Confirmed requirements in SRS with stable IDs | ✔ (206 IDs) | SRS v0.2 |
| 2 | Uncertain rules in register | ✔ (+21 v0.2 questions) | register §2.1b |
| 3 | Five-competitor max consistent | ✔ | BR-001, ERD slot CHECK, SQ-02/03, TC-001 |
| 4 | 100 CCU = peak planning target | ✔ | NFR-001 |
| 5 | Client / Backend / Match Server / MySQL separated; general backend vs real-time server distinguished | ✔ | architecture §1, ADR-012 §1 |
| 6 | No client → MySQL; DB private | ✔ | SEC-001, deployment |
| 7 | Server-authoritative combat (launch, steering, collisions, burst, skills) | ✔ | threat model §4b |
| 8 | Joystick, skill button, rapid-press launch specified | ✔ | controls & launch specs |
| 9 | Attributes / Energy / RPS / Stamina-vs-spin distinguished in DB, calc and UI | ✔ | stats spec §1, data dictionary §2b |
| 10 | Classification with hybrids/subtypes and matrix | ✔ | classification spec |
| 11 | Opponent-relative interaction model + RPS–Energy model with numeric scenarios | ✔ | combat spec §3–5 |
| 12 | Burst Finish primary, model options compared | ✔ | burst spec, ADR-014 |
| 13 | Research with source URLs, official vs secondary | ✔ with limitation (official pages seen via search extracts) | research references |
| 14 | Changes to confirmed decisions documented before applying | ✔ | design-change-proposals CHG-01…06 |
| 15 | Theoretical simulations; predictions vs findings vs recommendations labelled | ✔ | balancing report |
| 16 | Backend stack objectively compared, ADR | ✔ | ADR-012 |
| 17 | Diagrams/DB/API/requirements consistent; traceability | ✔ (static checks) | traceability v0.2 |
| 18 | Diagram syntax validated | ◐ static lint only — renderer not available (§2) | below |
| 19 | No implementation code, scenes or scripts; PR not merged; nothing pushed to main | ✔ | — |

## 2. Validation results
| Check | Result |
|---|---|
| PlantUML static lint (21 files) | **21/21 pass** — start/end markers, unique diagram names, all sequence participants declared, all class/ERD/component relation endpoints declared, alt/loop/end, if/endif, while, repeat, notes, braces. The linter was confirmed to flag deliberately broken input. |
| Fixes made by review | use-case stereotypes moved after aliases (`as UC20 <<post>>`); lost-message arrows changed to `->x`; one-line class bodies made multi-line; enums multi-line; member stereotypes replaced by bracket notes. |
| PlantUML render | **Not done.** Two attempts to download the PlantUML renderer into the scratch area were blocked by this session's permission policy. **Action R-1:** render once locally (`java -jar plantuml.jar -checkonly docs/**/*.puml`) or allow the download, then fix any reported error. |
| Mermaid (roadmap) | Node IDs checked manually; not rendered (GitHub renders it on the PR). |
| Cross-references | All relative document references resolve. |
| Traceability | 206 requirement IDs; 0 unmapped. |
| Godot references vs 4.7.x | Latest stable 4.7.2 confirmed (T-01); 4.7.2 multiplayer fix noted (T-02). `InputEvent.is_echo()`, `ENetMultiplayerPeer`, DTLS on `ENetConnection` and the dedicated-server export are cited from the stable docs structure — **re-verify against the 4.7 class reference and migration guide** (R-2). |
| Laravel references | Reverb event-loop/`nofile` limits from official docs index (T-04); Laravel 13 release date from a secondary source (T-05) — verify. |
| Official Beyblade sources | Hosts unreachable from this environment; facts taken from search extracts are marked "Verify" in research references (R-3). |

## 3. Remaining items
| ID | Item |
|---|---|
| R-1 | Render all PlantUML once; fix errors. |
| R-2 | Re-verify Godot 4.7 API names used in specs. |
| R-3 | Open the official Takara Tomy / Hasbro / FURYU pages and confirm the R-xx facts marked Verify. |
| R-4 | Spikes S-1…S-6 after approval (no implementation before). |

## 4. Decisions required from the user (v0.2)
**Blocking:**
1. CHG-01 launch curve (recommended) vs literal ×10 linear — OQ-LN-04.
2. OQ-LN-01 1.5 s READY cue before the 5 s window.
3. CHG-02 component properties beside the four attributes — OQ-ST-01.
4. CHG-03 / OQ-ST-02 Magic scope and its Energy weight (0.8).
5. CHG-04 / OQ-CB-05 elimination set: BURST primary + OVER + SPIN (+ XTREME).
6. ADR-013 advantage model & starting coefficients — OQ-CB-01.
7. ADR-014 hybrid burst model — OQ-BU-01.
8. ADR-012 backend: PHP + Laravel 13 + Reverb (supersedes ADR-003) and CHG-06 heartbeat-pull channel.
9. OQ-GP-18 time limit & sudden death; OQ-GP-04 tie rule (same-tick shared placement proposed).

**Needed before building the feature:** skills catalogue & limits (OQ-SK-01/02), burst stage visibility (OQ-BU-03), arena Xtreme zone/dash rail (OQ-CB-03), accessibility launch (OQ-LN-02), remaining H items.

## 5. Approval statement (to be completed by user)
> I approve design package v0.2 [with changes: …] and authorise Milestone M1 (technical spikes only). — Name, date
