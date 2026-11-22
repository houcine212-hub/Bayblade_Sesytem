# Risk Register

| Document ID | DOC-RSK-001 | Status | Living document |
|---|---|---|---|

Likelihood/Impact: L/M/H.

| ID | Risk | L | I | Mitigation | Owner | Trigger |
|---|---|---|---|---|---|---|
| RK-01 | Server-authoritative battle feels laggy/unresponsive on mobile | M | H | Launch-centric design hides latency; interpolation; spike S-1/S-2; prediction if in-battle control | Tech lead | S-2 results |
| RK-02 | Physics model not fun / hard to balance | M | H | Data-driven parameters; early playtests in M1/M2 | Game design | Playtest feedback |
| RK-03 | UDP blocked on some networks | M | M | Measure in beta; WebSocket fallback possible (ADR-007) | Tech lead | >2% failures |
| RK-04 | 100 CCU / 20 matches not achievable on affordable VPS | M | M | S-3 early; optimise snapshots; GDExtension hot path; second VPS | Tech lead | S-3/L-100 |
| RK-05 | Single VPS failure = full outage | M | H | Backups, restore rehearsal, documented rebuild; accept for MVP | Ops owner | — |
| RK-06 | Core gameplay rules remain undecided, blocking implementation | H | H | Blocking questions list; default proposals offered | User | G0 date |
| RK-07 | iOS/macOS release cost & review delays | H | M | Release Windows/Android/Linux first; keep exports building in CI | Product | OQ-PL-02 |
| RK-08 | Cheating via launch macros (**re-rated v0.3.1**) | H | H | Count-based rapid press with counted-press cap at the measured median touch rate (CHG-13), FC-1, **ranked gate FR-186**; v0.2 wording "timing-based design" was wrong — the mechanic is count-based | Game design | FC-1 fails in S-5 |
| RK-09 | Scope creep (exploration, voice, tournaments) | H | H | Strict MVP scope, gates per milestone | User | New feature requests |
| RK-10 | Low player population makes rooms empty | M | H | Room codes + community channels; bots for practice (needs approval) | Product | Beta metrics |
| RK-11 | Privacy/legal non-compliance in target markets | M | H | Minimal data; legal review before launch (NFR-061) | Owner | Before M4 |
| RK-12 | Knowledge concentrated in one person (user is learning) | H | M | This documentation, ADRs, tests, onboarding README | Owner | — |
| RK-13 | Version mismatch during store-review delays | M | M | Parallel protocol pools (ADR-008 §5) | Tech lead | Each release |
| RK-14 | Abuse/harassment harms community | M | M | Block/report/moderation in MVP-Social; minimal chat | Moderators | Report volume |
| RK-15 | Loss of store signing keys | L | H | Offline backups of keystores/certs | Owner | — |
| RK-16 | Balance archetype structurally weak (42.0% overall in the reproducible v0.4 model; threshold-gated damage favours concentrated attributes). v0.2 "±1 knife-edge" came from a deterministic model and is superseded | H | H | Balance identity via lock/mass + Adapt skill; AC-1 in S-1 | Game design | AC-1 fails after S-1 |
| RK-17 | Launch dominates outcomes / device unfairness | M | H | Curve compression, cap, S-5 study, NFR-073 | Game design | Device RPS gap > 5% |
| RK-18 | Joystick + server authority feels laggy on mobile | M | H | Local prediction, 30 Hz input, S-2 | Tech lead | NFR-011 fail |
| RK-19 | Burst too rare/too random → "primary" mechanic fails | M | M | Tune c_b/T0/β; staged gauge for readability | Game design | Burst metric below the D-10 target (proposal: M-1 < 30% or M-2 not met) |
| RK-20 | PHP/Godot rule duplication for build preview drifts | M | M | Golden-file contract tests TC-029 | Tech lead | Contract test failure |
| RK-21 | Official-source facts only seen through search extracts | M | L | Manual verification of R-xx "Verify" items before G0 | Owner | — |
| RK-22 | IP: mechanics inspired by a franchise | L | H | Original names/art/formulas only; no franchise names in game; legal review before launch | Owner | Before M4 |
| RK-23 | Launch macros / modified clients always reach the cap (v0.4 linear, cap 35 = 350 RPS: vs a 35-press player 47.1% / 51.0%; vs 32 presses 65.8% / 91.0%); zone check client-side; client input cannot prove human presses | **H** | **H** (re-rated) | Median cap (CHG-13), FC-1 (NFR-074), **ranked gate FR-186**, regularity flags, reports | Game design | FC-1 fails or integrity complaints |
| RK-24 | Combat acceptance criteria AC-1/2/4/7 unmet by the current coefficient candidate | H | H | Spike S-1 with real physics; structural revisit if two iterations fail (ADR-013) | Game design | S-1 exit review |
| RK-25 | NFR-070 as written (≥ 40% uniform mix) not reachable with acceptable match lengths (model 33.8%) | M | M | Decision D-10 adopted as initial target with defined populations (M-1/M-2); post-MVP opposite-spin burst | Owner | G0 |
| RK-27 | Spin-race matchups extremely launch-sensitive — **amplified by the linear launch** (v0.4: 32 vs 35 presses → 91.0% in the Stamina mirror; 3-press swing 77.5–81.5 points in Balance/Stamina mirrors) | H | H | S-1: steering-dependent decay variance, `k_R` review, spin floor options (OQ-CB-10) | Game design | S-1 |
| RK-26 | Custom Pusher-protocol client and custom refresh-token flow (no official Godot/Laravel components) | M | M | Spike S-6; polling fallback; security tests | Tech lead | S-6 |
| RK-28 | Zero-tap / one-tap inversion (D-01 + D-03): 0 presses beats 1 press 98.6% / 99.6% | M | L | Owner decision OQ-LN-08 (recommended R1); regression test documents current rule | Owner | G0 follow-up |
| RK-29 | Accessibility: linear launch + median cap strongly disadvantages players below ~7 presses/s (25 presses → lose 81% / 99%) | H | M | Owner decision OQ-LN-09; S-5 measurement incl. accessibility users; friendly-room assist | Owner / Game design | S-5 |
| RK-30 | 350 RPS cannot be resolved by rotating a 3D rigid body at 60 Hz (5.83 rev/tick) | H | M | Spin as authoritative scalar + capped visual spin (DOC-CMB-001 §2.4); prototype in S-1 | Tech lead | S-1 |
| RK-31 | D-17 outcome requirement fails under linear launch with the absolute 30-RPS threshold | H | M | Owner decision OQ-CB-12; re-test in S-1 | Owner | G0 follow-up |
