# Gate G0 — Decision Sheet (v0.3)

| Document ID | DOC-G0-001 | Status | **All rows are PROPOSALS until the user marks a choice.** Confirmed decisions are listed in §1 for reference only. |
|---|---|---|---|

How to use: for each row mark **Approve**, **Reject** or **Change (write the change)**. Approval of the gate authorises **Milestone M1 (technical spikes) only** — no game implementation.

## 1. Already confirmed by the user (reference, not re-decided)
Godot; Windows/Android/Linux first, macOS/iOS later; one shared account (e-mail + password, unique display names); ≤ 5 competitors per match; ~100 peak CCU target; rooms by code; FFA, last top wins; **ring-out eliminates** (Brief §E1); **Burst Finish is the primary elimination**; 360° joystick + Skill button; 5-second rapid-press launch with 5 presses = 50 RPS; attributes ATK/DEF/STA/MAG with Energy derived; RPS separate; RPS influence decreases smoothly with the Energy gap and is never irrelevant; MySQL private; server-authoritative combat; exploration and real-money wagering out of the MVP.

## 2. Blocking decisions
| ID | Decision | Recommendation (proposal) | Main alternative | Evidence | Your choice |
|---|---|---|---|---|---|
| D-01 | Launch curve (CHG-01) | `RPS = 20 + 130·(1 − e^(−n/19.0575))`; 5 → 50.000 | Literal linear 10·n | DOC-LAUNCH-001 §4 | ☐ Approve ☐ Reject ☐ Change |
| D-02 | 1.5 s non-counted READY cue before the 5 s window (OQ-LN-01) | Yes | No cue | DOC-LAUNCH-001 §2 | ☐ ☐ ☐ |
| D-03 | Zero presses result (OQ-LN-07) | 20.00 RPS auto-launch | 0 RPS = immediate Spin Finish | measured: 0.1–3.5% win rate | ☐ ☐ ☐ |
| D-04 | Launch limits & anti-cheat stance (ADR-015) | Max 60 presses (12/s), max 144.42 RPS; accept documented macro/zone limitations; choose final cap after spike S-5 | Lower cap now (10/s or 8/s) | DOC-LAUNCH-001 §5, §7 | ☐ ☐ ☐ |
| D-05 | Component properties beside the four attributes (CHG-02) | Yes (mass, lock strength, mobility, friction, height, contact profile, spin direction) | Attributes only | official: bit determines burst resistance (O-1) | ☐ ☐ ☐ |
| D-06 | Magic acts directly only on skills (CHG-03) | Yes | Magic as a physical stat | DOC-SKILL-001 | ☐ ☐ ☐ |
| D-07 | Energy formula (CHG-07) | **(ATK + DEF + STA + MAG) / 4** | (ATK + DEF + STA + 0.8·MAG) / 3.8 | DOC-STAT-001 §4.5 | ☐ ☐ ☐ |
| D-08 | Headline type rule (CHG-10) | Option C: TIP part's designed type (official: "type is determined by the Bit") + computed profile | Option A: computed only | DOC-CLS-001 §2 | ☐ ☐ ☐ |
| D-09 | Elimination set (CHG-04) | BURST primary [C]; OVER [C]; SPIN required; XTREME optional per arena | — | DOC-BURST-001 §3 | ☐ ☐ ☐ |
| D-10 | Numeric meaning of "Burst is primary" (CHG-09) | ≥ 30% of all eliminations and most frequent finish in Attack/Balance pairings, measured on real telemetry | Keep ≥ 40% over a uniform mix (not reachable in the model with reasonable match lengths) | DOC-BAL-001 §5, §10 | ☐ ☐ ☐ |
| D-11 | Same-tick eliminations (CHG-11) | Shared placement (deviation from official draw + restart) | Restart the match | DOC-BURST-001 §3.3 | ☐ ☐ ☐ |
| D-12 | Combat model structure (ADR-013) | Approve the **equations** (advantage S with defined g and r, impact/resistance, recoil) and the **v0.3 coefficient set as S-1 starting values only** (CHG-08) | Request a different structure | DOC-CMB-001, DOC-BAL-001 | ☐ ☐ ☐ |
| D-13 | Combat acceptance criteria (CHG-12) | AC-1…AC-7 as exit gate of spike S-1 | Other bands | ADR-013 | ☐ ☐ ☐ |
| D-14 | Burst model (ADR-014) | Hybrid Lock Integrity (original design anchored on official facts) | Pure threshold / durability | DOC-BURST-001 §2 | ☐ ☐ ☐ |
| D-15 | Backend stack (ADR-012, CHG-05/06) | PHP 8.3+ + Laravel 13 + Reverb + MySQL 8.4; Godot 4.7 headless Match Server; heartbeat-pull internal channel; accept risks TR-01…TR-10 | TypeScript/Node + Fastify | ADR-012 §3, §7 | ☐ ☐ ☐ |
| D-16 | Time limit (OQ-GP-18) | 120 s; then remaining Beys ranked by current spin (higher = better), ties shared | No limit; sudden death | DOC-BAL-001 §5.2 (longest median 99 s) | ☐ ☐ ☐ |

## 3. Needed before the feature is built (not blocking G0)
OQ-BU-03 opponent burst-stage visibility (proposal: visible) · OQ-CB-03 arena Xtreme zone / dash rail · OQ-CB-08 outcome-level RPS requirement for g ≤ 0.20 + Energy-band matchmaking for ranked · OQ-SK-01/02 skill limits and catalogue · OQ-LN-02 assisted launch in friendly rooms · OQ-LN-06 final press cap (after S-5) · OQ-GP-05/06/07/13/14/17 room and disconnect rules · OQ-AC-03/04/07 social rules · OQ-TO-06/07/08 hosting, domain, operations owner.

## 4. Gate statement
> Gate G0 decision: ☐ Approved as marked above ☐ Approved with changes ☐ Not approved — Name: ____ Date: ____
