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
