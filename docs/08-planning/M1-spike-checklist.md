# M1 Technical Spike Checklist (executable)

| Document ID | DOC-M1-001 | Version | 0.4.1 | Status | **Authorised by the owner's G0 acceptance (2026-11-22) — not started; no step has been run.** Spikes are throw-away prototypes, not game features. |
|---|---|---|---|---|---|---|---|

Rules: every spike produces a short report in `docs/11-spikes/S-x-report.md` (to be created when run) with environment, steps, raw data location, and a pass/fail line per criterion. **Failed or unmeasured criteria are not passing (D-13).** If a criterion proves unrealistic, raise an explicit change decision — never weaken it silently. Nothing here is implemented yet.

## S-5 — Launch input study (run first; feeds D-04, FC-1, AC-9)
| # | Step | Output | Pass criterion |
|---|---|---|---|
| 5.1 | Build a throw-away input-capture prototype (Godot 4.7) recording edge-triggered presses with timestamps for touch (Android, ≥ 3 phones: low/mid/high), keyboard, mouse, gamepad | CSV per participant/device | data from ≥ 30 participants per input type (target) incl. accessibility participants (OQ-LN-09) |
| 5.2 | Apply DOC-LAUNCH-001 §3 counting (interval ≥ 142 857 µs, cap 35, half-open window) | accepted-press counts | — |
| 5.3 | Compute median and spread of sustained presses per input type | table | NFR-073: median launch RPS per input type within 5% — pass/fail |
| 5.4 | Re-select the cap = measured median (D-04) | proposed cap value | owner informed before adoption |
| 5.5 | Re-run `tools/analysis` with measured distributions; compute FC-1 | e5 results | **AC-9 / FC-1 ≤ 60%** |
| 5.6 | Measure regularity (CV) of humans vs a scripted macro | distributions | document false-positive rate; no auto-punishment |
| 5.7 | Verify the launch rule `max(20, 10 × n)` end-to-end (TC-016, TC-038: 0, 1, 2 → 20 RPS) | test log | all cases match (OQ-LN-08 decided) |
| 5.8 | Accessibility sample: participants with reduced press rate / one-handed play | distribution | informs OQ-LN-09 (assisted launch in friendly rooms) |

## S-1 — Combat simulation in Godot headless (feeds D-12, D-14, D-16, D-17, AC-1…AC-8)
| # | Step | Output | Pass criterion |
|---|---|---|---|
| 1.1 | Implement the canonical equations (DOC-CMB-001 §2–4, DOC-BURST-001 §2.2) in a throw-away headless prototype with spin as an authoritative scalar up to 350 RPS (§2.4) | prototype | TC-041 (no overflow/rescaling) |
| 1.2 | Burst boundary tests (D-14) | test log | TC-033 / TC-023: full lock never bursts in one contact; gate at L_start ≤ 50 |
| 1.3 | Bot policies (seek, evade, hold), S-5 launch distributions, real arena geometry | bot framework | — |
| 1.4 | 1-v-1 matrices, ≥ 4,000 matches per cell, fixed seeds | CSV | AC-1, AC-2, AC-4, AC-5 |
| 1.5 | Five-competitor FFA bots with random type composition | CSV | **AC-8** |
| 1.6 | Implement the 7 MVP skills; equal-budget Magic test | CSV | **AC-7** (D-07 provisional until then) |
| 1.7 | D-17 test: 7-press (70-RPS) difference at g = 0, 0.10, 0.20 for every type mirror | CSV | **AC-6** (owner-amended, OQ-CB-12): ≥ 10 points for |g| ≤ 0.20; model warns Stamina 9.9 at g = 0.20 |
| 1.8 | Time-limit ranking share and spin-ranking effects in FFA (D-16) | CSV | report; no criterion yet |
| 1.9 | Burst metrics M-1 / M-2 (D-10) | CSV | **AC-3** |
| 1.10 | Compare with `tools/analysis` predictions | diff report | explain divergences |

## S-2 — Netcode (feeds ADR-005/007, NFR-006/007/011)
| # | Step | Pass criterion |
|---|---|---|
| 2.1 | ENet UDP client ↔ headless server; 30 Hz snapshots with u16 spin; 30 Hz inputs | stable at 5 competitors + 2 spectators |
| 2.2 | Own-top prediction + reconciliation under 50/150/250 ms RTT, 0/2/5% loss | **NFR-011** ≤ 100 ms own-input response; corrections < 100 ms |
| 2.3 | Launch press batches under latency | **TC-L07**: no valid press lost at 300 ms RTT |
| 2.4 | DTLS option (`ENetConnection.dtls_*`) cost | report |

## S-3 — Server resources (feeds ADR-006/010, TR-05/TR-06)
| # | Step | Pass criterion |
|---|---|---|
| 3.1 | 20 concurrent headless match processes on the candidate VPS size | CPU < 70% sustained, RAM < 80%, tick p99 < 8.3 ms |
| 3.2 | Same host also running PHP-FPM, Reverb, queue, MySQL | no OOM; systemd limits respected |

## S-4 — Mobile rendering (feeds NFR-020/021/022)
| # | Step | Pass criterion |
|---|---|---|
| 4.1 | Arena + 5 tops + VFX on low/mid Android | frame-rate targets defined per device, 15-min thermal run documented |
| 4.2 | Visual spin at 350 RPS (capped/blurred) readability | playtester comprehension check |

## S-6 — Laravel / Reverb / Godot integration (feeds D-15, TR-01…TR-04)
| # | Step | Pass criterion |
|---|---|---|
| 6.1 | Laravel 13 on PHP 8.3+ with MySQL 8.4; dependency compatibility | runs; versions recorded |
| 6.2 | Custom GDScript Pusher-protocol client ↔ Reverb private channels (`/broadcasting/auth`) | subscribe, receive, reconnect |
| 6.3 | Sanctum short-lived tokens + custom refresh rotation | reuse detection works |
| 6.4 | Heartbeat-pull: commands idempotent, acknowledged, retried; stale instances reclaimed | allocation ≤ 1 s added; NFR-009 ≤ 5 s |
| 6.5 | Build-preview golden-file parity PHP ↔ GDScript | **TC-029** |
| 6.6 | Reconnect/rollback flows (SQ-08) | reconnect within grace |
If S-6 fails a criterion: propose a focused ADR-012 revision (D-15) instead of forcing the stack.

## M1 exit
All AC-1…AC-9 evaluated with S-1/S-5 data; spike reports reviewed by the owner; ADRs moved to Accepted/Superseded with evidence; ranked gate (FR-186) re-assessed. Only then may M2 planning start.
