# Game Design Document (GDD) — Battle MVP

| Document ID | DOC-GDD-001 | Version | 0.4 | Status | G0 decisions integrated (pending M1 verification) — combat numbers are S-1 experimental starting values, not balanced |
|---|---|---|---|---|---|---|---|

## 1. Pitch
Original online spinning-top battles for up to **5 competitors** per arena on Windows, Android and Linux (macOS/iOS later). Build your Bey from parts, **launch it by rapid-pressing** for 5 seconds (RPS = max(20, 10 × accepted presses), up to 35 presses = 350 RPS), **steer it with a 360° joystick**, fire its **skill** at the right moment, and be the last one spinning — ideally by **Burst Finish**.

## 2. Core loop
Build (parts → attributes, type, Energy) → room by code → ready → **launch window (5 s rapid press)** → battle (steer, collide, skill) → eliminations (Burst / Over / Spin / Xtreme) → spectate if out → result & history → adjust build.

## 3. Pillars (v0.2)
1. **Launch skill matters** — and matters most between equal Bey's (Energy-dependent RPS weight).
2. **Matchups, not stats** — outcomes depend on both opponents (type tendencies, properties, profiles).
3. **Burst is the climax** — staged burst gauge, cumulative damage, no one-shots at full lock.
4. **Readable & fair** — server-authoritative, bounded skills, same caps on every device.

## 4. Specifications
| Topic | Document |
|---|---|
| Statistics, Energy, spin vs Stamina | `beyblade-statistics-spec.md` |
| Types, hybrids, subtypes, matrix | `classification-spec.md` |
| Opponent-relative interactions, RPS–Energy model | `combat-interaction-spec.md` |
| Launch (5-second rapid press) | `launch-mechanics-spec.md` |
| Burst & other finishes | `burst-finish-spec.md` |
| Skills & Magic | `skills-spec.md` |
| Controls (joystick, skill button) | `input-controls-spec.md` |
| Balancing predictions | `balancing-simulation-report.md` |
| Research sources (official vs ours, §3) | `research-references.md` |
| Changes to confirmed decisions | `design-change-proposals.md` |

## 5. Match flow (FFA, ≤ 5 competitors)
WAITING_FOR_PLAYERS → READY (1.5 s, D-02) → LAUNCH_WINDOW (exactly 5 s) → RELEASE (0.5 s) → BATTLE (**120 s** limit, D-16: survivors ranked by current spin, exact ties share placement) → ENDED. Same-tick eliminations share a placement; if the last competitors all go out in the same tick the match is a draw with no unique winner (D-11). State machine: `../02-uml/state-match.puml`; per-Bey states: `../02-uml/state-bey-combat.puml`.

## 6. HUD (battle)
Own: Spin meter (RPS), Burst gauge stage, Skill ring, joystick (left), skill button (right). Opponents: name, type badge, burst stage (OQ-BU-03), spin bar (coarse). Event feed: "X BURST FINISH by Y".

## 7. Scope
In MVP: FFA, one arena (with or without Xtreme zone — OQ-CB-03), ~8–12 parts per slot, 7 skills, friendly matches. Out: exploration, loot chests, team battle, tournaments, voice, stakes, persistent part wear.

## 8. Arena [P]
Bowl with slope toward centre; perimeter with **over pockets**; optional **dash rail** ring that grants a short speed boost when a top rides it (Xtreme Dash inspiration, R-13) and an optional Xtreme exit zone. Arena geometry lives in content data.
