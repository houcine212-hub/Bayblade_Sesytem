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
| RK-08 | Cheating via launch macros | M | M | Timing-based design, server-side rate caps | Game design | Reports |
| RK-09 | Scope creep (exploration, voice, tournaments) | H | H | Strict MVP scope, gates per milestone | User | New feature requests |
| RK-10 | Low player population makes rooms empty | M | H | Room codes + community channels; bots for practice (needs approval) | Product | Beta metrics |
| RK-11 | Privacy/legal non-compliance in target markets | M | H | Minimal data; legal review before launch (NFR-061) | Owner | Before M4 |
| RK-12 | Knowledge concentrated in one person (user is learning) | H | M | This documentation, ADRs, tests, onboarding README | Owner | — |
| RK-13 | Version mismatch during store-review delays | M | M | Parallel protocol pools (ADR-008 §5) | Tech lead | Each release |
| RK-14 | Abuse/harassment harms community | M | M | Block/report/moderation in MVP-Social; minimal chat | Moderators | Report volume |
| RK-15 | Loss of store signing keys | L | H | Offline backups of keystores/certs | Owner | — |
| RK-16 | Balance archetype structurally weak (39.8–43.6% in the stochastic model; threshold-gated damage favours concentrated attributes). v0.2 "±1 knife-edge" came from a deterministic model and is superseded | H | H | Balance identity via lock/mass + Adapt skill; AC-1 in S-1 | Game design | AC-1 fails after S-1 |
| RK-17 | Launch dominates outcomes / device unfairness | M | H | Curve compression, cap, S-5 study, NFR-073 | Game design | Device RPS gap > 5% |
| RK-18 | Joystick + server authority feels laggy on mobile | M | H | Local prediction, 30 Hz input, S-2 | Tech lead | NFR-011 fail |
| RK-19 | Burst too rare/too random → "primary" mechanic fails | M | M | Tune c_b/T0/β; staged gauge for readability | Game design | Burst share < 40% |
| RK-20 | PHP/Godot rule duplication for build preview drifts | M | M | Golden-file contract tests TC-029 | Tech lead | Contract test failure |
| RK-21 | Official-source facts only seen through search extracts | M | L | Manual verification of R-xx "Verify" items before G0 | Owner | — |
| RK-22 | IP: mechanics inspired by a franchise | L | H | Original names/art/formulas only; no franchise names in game; legal review before launch | Owner | Before M4 |
| RK-23 | Launch macros / modified clients always reach the press cap (68.6–93.3% win rate vs a 7/s human); zone check client-side | H | M | Cap choice after S-5, regularity flags, reports; documented residual risk | Game design | Integrity complaints |
| RK-24 | Combat acceptance criteria AC-1/2/4/7 unmet by the current coefficient candidate | H | H | Spike S-1 with real physics; structural revisit if two iterations fail (ADR-013) | Game design | S-1 exit review |
| RK-25 | Burst-primary target (NFR-070) not reachable with reasonable match lengths in a uniform matchup mix | M | M | Decision CHG-09; post-MVP opposite-spin burst | Owner | G0 |
| RK-26 | Custom Pusher-protocol client and custom refresh-token flow (no official Godot/Laravel components) | M | M | Spike S-6; polling fallback; security tests | Tech lead | S-6 |
