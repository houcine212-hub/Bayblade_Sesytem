# Gate G0 — Decision Sheet (v0.4)

| Document ID | DOC-G0-001 | Version | 0.4 (2026-11-22) | Status | **Decisions recorded. The owner confirmed D-01…D-03 individually and delegated D-04…D-18 to the assistant.** Changes integrated into the documents **pending owner verification**. Initial G0 documentation approval is proposed **with changes**. **Technical proof is M1 and has not been conducted.** |
|---|---|---|---|---|---|---|---|

Source: "Beyblade — Gate G0 Decisions (v0.3.1)" decision register supplied by the owner. Authority legend: **Owner** = individually confirmed by the product owner; **Delegated** = selected by the assistant under the owner's express delegation (priorities: fair, playable, maintainable, cross-platform). Delegated choices are decisions to record, **not evidence of technical validation**.

## 1. Previously confirmed by the owner (reference)
Godot; Windows/Android/Linux first, macOS/iOS later; one shared account (e-mail + password, unique display names); ≤ 5 competitors; ~100 peak CCU target; rooms by code; FFA, last top wins; ring-out eliminates; Burst Finish is the primary elimination; 360° joystick + Skill button; 5-second rapid-press launch; ATK/DEF/STA/MAG with Energy derived; RPS separate; RPS influence decreases smoothly with the Energy gap; MySQL private; server-authoritative combat; exploration and real-money wagering out of the MVP.

## 2. G0 decisions
| ID | Decision | Authority | Outcome recorded | Conditions / where applied |
|---|---|---|---|---|
| D-01 | Launch RPS rule | **Owner** | **CHANGE:** `RPS = 10 × accepted presses` for n ≥ 1, strictly linear (5 → 50, 10 → 100, 35 → 350); no exponential, saturating or rescaled formula | DOC-LAUNCH-001 §4; ADR-015; SRS FR-053/182/183; SQ-04; tools/analysis v0.4 |
| D-02 | READY cue | **Owner** | **APPROVE:** 1.5 s, no accepted presses, then exactly 5.0 s window | DOC-LAUNCH-001 §2; FR-052; state-match; activity |
| D-03 | Zero presses | **Owner** | **APPROVE:** 0 accepted presses = 20 RPS automatic launch (deliberate exception); no automatic elimination | DOC-LAUNCH-001 §4; FR-065. ⚠ Creates the zero/one-tap inversion → **OQ-LN-08** (rules unchanged) |
| D-04 | Launch fairness and cap | Delegated | **APPROVE WITH CHANGE:** cap 35 accepted presses (provisional, from a provisional 7/s median), interval floor 142 857 µs, **max 350 RPS**; FC-1 and ranked gate FR-186 kept; spin as authoritative scalar; no automated punishment from regularity alone; re-select cap after S-5 | DOC-LAUNCH-001 §3, §5–8; DOC-CMB-001 §2.4; FR-181/186; NFR-074 |
| D-05 | Component properties | Delegated | APPROVE | DOC-STAT-001 §3; FR-195 |
| D-06 | Magic scope | Delegated | APPROVE: Magic powers skills directly; indirect Energy contribution intentional | DOC-SKILL-001; FR-232 |
| D-07 | Energy formula | Delegated | **APPROVE PROVISIONALLY:** (ATK + DEF + STA + MAG)/4; not balance-certified until skill-inclusive AC-7 | DOC-STAT-001 §4.5; FR-192 |
| D-08 | Headline type | Delegated | APPROVE: TIP `tip_type`; computed profile separate; UNCLASSIFIED and deterministic tie/zero handling | DOC-CLS-001 §2; FR-202; ERD |
| D-09 | Elimination set | Delegated | APPROVE: BURST signature/primary; OVER and SPIN supported; XTREME only where the arena defines the zone; disconnect = outcome reason | DOC-BURST-001 §3; FR-223 |
| D-10 | Burst metrics | Delegated | **APPROVE AS INITIAL TARGET:** M-1 ≥ 30%; M-2 most frequent in A→A, A→S, A→B; "primary" = signature finish, not globally most frequent | DOC-BURST-001 §3.1; NFR-070 |
| D-11 | Same-tick eliminations | Delegated | **APPROVE WITH CLARIFICATION:** shared placement; all last competitors out in the same tick = draw, no unique winner, no rank-affecting result in MVP; no restart | DOC-BURST-001 §3.4; FR-062/067; state-match; SQ-05 |
| D-12 | Combat model | Delegated | **APPROVE STRUCTURE ONLY:** canonical equations adopted; coefficients = S-1 experimental starting values (re-expressed for the 350-RPS scale) | DOC-CMB-001 §4.9; ADR-013 |
| D-13 | Acceptance criteria | Delegated | APPROVE AC-1…AC-9 as M1 exit criteria; failed or unmeasured = not passing; no silent weakening | ADR-013; DOC-BAL-001 §5.3 |
| D-14 | Burst model | Delegated | APPROVE hybrid Lock Integrity (cap 49, critical gate, full-lock impossibility); verify boundaries in S-1 | DOC-BURST-001 §2; ADR-014 |
| D-15 | Stack | Delegated | **APPROVE CONDITIONALLY:** PHP 8.3+ / Laravel 13 / Reverb / MySQL 8.4 + Godot 4.7 headless authoritative UDP; confirm in M1 (S-3, S-6) or revise ADR | ADR-012; CON-07 |
| D-16 | Time limit | Delegated | APPROVE: 120 s; survivors ranked by current spin; exact ties share placement; provisional | FR-069; state-match; activity; SQ-07 |
| D-17 | RPS-principle meaning | Delegated | **APPROVE OPTION (b) PROVISIONALLY.** ⚠ Under the linear launch the 30-RPS outcome test **fails** for g ≳ 0.13–0.17 → **OQ-CB-12** | ADR-013; FR-212; DOC-BAL-001 §6 |
| D-18 | Formula and data corrections | Delegated | APPROVE: dimensionless impact, canonical burst equation, contact aggregation, slot PK, match-server FK, finish vs outcome reason, TIP-only `tip_type` | DOC-CMB-001; DOC-BURST-001; ERD; data dictionary |

## 3. Open owner questions created by these decisions (not changed unilaterally)
| ID | Question | Recommendation |
|---|---|---|
| OQ-LN-08 | Zero/one-tap inversion: 0 presses (20 RPS) beats 1 press (10 RPS) 98.6% / 99.6% | R1: `RPS = max(20, 10 × n)` — changes D-01 for n = 1 only; needs owner approval |
| OQ-LN-09 | Accessibility of linear launch + median cap | friendly-room assisted launch; measure accessibility users in S-5 |
| OQ-CB-12 | D-17 threshold absolute (30 RPS) vs relative | relative (≈ 7 presses / r ≥ 0.2), which passes in the model |

## 4. Gate statement
> **G0 status:** decisions recorded; documentation updated (v0.4); **G0 documentation approval proposed with changes, pending the owner's verification**. Authorises **M1 technical spikes only** once accepted — not M2 features, deployment or merging PR #1. M1 has **not** been conducted.
>
> Owner acceptance: ______________________ (to be completed by the owner; not signed by the assistant)
