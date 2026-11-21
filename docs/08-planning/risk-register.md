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
