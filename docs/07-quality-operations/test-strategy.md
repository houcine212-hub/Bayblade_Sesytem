# Test Strategy

| Document ID | DOC-QA-001 | Status | [P] |
|---|---|---|---|

## 1. Test levels
| Level | Scope | Tools [P] | Examples |
|---|---|---|---|
| Unit | Pure logic: launch formula, elimination rules, placement calc, permission checks, validation | GDScript: GUT or gdUnit4; Backend: Vitest/Jest | Two ring-outs in the same tick → placement per decided rule |
| Integration | Backend + real MySQL (container); migrations | Testcontainers / Compose | Join room under concurrency never exceeds 5 competitors |
| Contract | Client↔Backend JSON schemas; Backend↔Match Server internal messages; protocol message catalogue | JSON Schema / OpenAPI checks in CI on both sides | Backend rejects result missing placements |
| Multiplayer simulation | Headless Match Server + bot clients, no rendering; network impairment (latency/loss via `tc netem` on Linux) | Godot headless + bots | 5 bots launch, battle ends, result reported once |
| End-to-end | Real client builds on devices against staging | Manual scripts + automated smoke | Register → room → match → history visible |
| Load | 10/25/50/100 CCU; concurrent matches | Bot fleet | See load-test-plan.md |
| Security | Auth, authZ matrix, rate limits, port scan | Automated API tests, nmap | MySQL port closed externally |
| Platform | Cross-platform matrix | Device lab | See below |

## 1b. Combat balancing test levels (v0.2)
| Level | What | Labels |
|---|---|---|
| Analytic model | Spreadsheet/script duel predictions (done) | [PRED] |
| Headless bot simulation | Thousands of bot matches per build pair with randomised launch distributions and steering policies | [PRED] at scale |
| Internal playtest | Humans, telemetry, surveys (feel, fairness, burst randomness) | [PLAY] |
| Closed beta telemetry | Win rate per type pair, finish shares, match length, launch RPS per device | [PLAY] |

## 2. Determinism for tests
Simulation accepts a seed and fixed tick; tests replay recorded launch inputs and assert outcomes (golden tests). Balance changes update golden files intentionally.

## 3. Cross-platform test matrix (devices TBD, OQ-PL-01)
| Platform | Device tiers to test | Focus |
|---|---|---|
| Windows | Low iGPU laptop, mid desktop | Input, FPS, window modes |
| Linux | One distro (Ubuntu LTS) | Build runs, input |
| macOS | Apple Silicon (post-MVP) | Signing, Metal |
| Android | Low (~3–4 GB RAM), mid, tablet | Touch, FPS/thermal 15-min session, backgrounding, Wi-Fi↔cell switch |
| iOS | One older + one current iPhone (post-MVP) | Safe areas, App Review flows |

## 4. Traceability
Every test case ID `TC-xxx` references requirement IDs; see `../08-planning/traceability-matrix.md`.

## 5. Key test cases (initial)
| TC | Requirement | Case |
|---|---|---|
| TC-001 | FR-033/BR-001 | 6th competitor join → 409, concurrent joins race test |
| TC-002 | FR-051/SEC-006 | Expired / reused / wrong-match / wrong-protocol ticket rejected |
| TC-003 | FR-056/057 | Ring-out ordering → correct placements & winner |
| TC-004 | FR-058/FR-090 | Eliminated peer becomes spectator; inputs dropped |
| TC-005 | FR-070 | Duplicate result report persisted once |
| TC-006 | FR-071 | Forged client result RPC ignored |
| TC-007 | FR-064 | Reconnect within grace restores control/view |
| TC-008 | FR-068/BR-013 | Kill Match Server mid-battle → ABORTED, no record change |
| TC-009 | NFR-031 | Stop Backend mid-battle → match completes, result delivered after restart |
| TC-010 | SEC-001 | External scan: 3306 closed |
| TC-011 | FR-122/BR-006 | Non-admin approval attempt → 403; admin approval audited |
| TC-012 | FR-006 | Old client → 426 |
| TC-013 | FR-130/131 | Block & report flows; rate limit |
| TC-014 | FR-024 | Edit loadout after match → history unchanged |
| TC-015 | SEC-008/011 | Room-code brute force throttled |
| TC-016 | FR-182/183 | Linear launch (D-01/D-03): 0 → 20, 1 → 10, 5 → 50, 15 → 150, 25 → 250, 35 → 350; no rescaling between server and display |
| TC-017 | FR-181 | Key repeat, held key, presses < 83 ms apart, presses outside zone not counted |
| TC-018 | FR-184/SEC-013 | Back-dated / future / late batches rejected; 300 ms RTT player loses no valid presses |
| TC-019 | FR-191/192 | Energy recomputed from attributes; API rejects Energy as input |
| TC-020 | FR-194 | Schema & UI lint: no ambiguous `stamina` field for current spin |
| TC-021 | FR-202/203 | Classification golden tests (examples in CLS spec), threshold changes via config only |
| TC-022 | FR-211/212 | Advantage S table (DOC-BAL-001 §4, S1–S9) reproduced to 4 decimals; w ≥ 0.15 for all g in (−2, 2) |
| TC-023 | FR-221 | L=100 never bursts in one contact; critical burst only at L ≤ 50; seeded variance within ±10% |
| TC-024 | FR-231/233 | Skill rejected for gauge/cooldown/limit/opening/spin; 4th use rejected |
| TC-025 | FR-172/NFR-011 | Prediction: own-input visual response ≤ 100 ms at 150 ms RTT; correction < 100 ms |
| TC-026 | SEC-015 | |u| > 1 clamped; > 60 inputs/s dropped then kicked |
| TC-027 | FR-222 | Burst at tick T → all clients receive Eliminated(BURST) and role change; remaining fight continues |
| TC-028 | NFR-045 | Same seed + recorded inputs → identical result (replay) |
| TC-029 | API-23 | Backend build preview equals Match Server snapshot for golden builds (contract test) |
| TC-030 | NFR-070..073 | Balance telemetry dashboards populated from bot matches |
| TC-031 | ADR-013 AC-1…AC-9 | Bot-simulation report (≥ 4,000 duels per pairing, fixed seeds) evaluated against every acceptance criterion |
| TC-032 | FR-181 | 36th press rejected; interval 142 856 µs rejected, 142 857 µs accepted; press at exactly W0+5000 ms rejected; 35 presses → 350 RPS |
| TC-033 | FR-225 | Boundary/extreme: L = 100 with N = 1, 10, 10³, 10⁶ → L ≥ 51, no burst; L_start = 51 → no critical burst; L_start = 50 → critical allowed; 3 attackers in one tick → summed damage ≤ 49 |
| TC-034 | NFR-074 / FR-186 | FC-1 computed from S-5 press data + S-1 physics; ranked endpoints return 403 RANKED_DISABLED until FC-1 passes |
| TC-035 | FR-226 | Same pair contact reported on 6 consecutive ticks → one contact event; v_n ≤ v_min → no effects |
| TC-036 | FR-202 | Classification guard: P = 0 / 29 → UNCLASSIFIED; P = 30 classified; threshold equalities; tie order |
| TC-038 | FR-065/OQ-LN-08 | Regression test documenting the confirmed rule: 0 presses → 20 RPS and 1 press → 10 RPS (update only if the owner resolves OQ-LN-08) |
| TC-039 | FR-069 (D-16) | At 120 s survivors ranked by current spin; exact equal spin → shared placement |
| TC-040 | FR-062/067 (D-11) | Last competitors eliminated in the same tick → draw, no unique winner, no rank-affecting result, no restart |
| TC-041 | DOC-CMB-001 §2.4 | spin_rps up to 350 handled as scalar; snapshot u16 carries 350.0 without overflow; visual spin capped |
| TC-037 | DOC-BAL-001 | `python3 tools/analysis/run_all.py` reproduces `results/` byte-for-byte on the documented numpy version |
