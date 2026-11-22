# MVP Scope (recommendation for approval)

| Document ID | DOC-MVP-001 | Status | v0.4 — G0 decisions D-01…D-18 recorded (see G0 decision sheet);  — battle-first focus, platforms & exploration deferral **confirmed**; remaining boundaries [P] |
|---|---|---|---|

## 1. MVP definition
The **public MVP** is the first release real players can download and play online: battle loop +
small social layer + operational readiness. It is delivered in three internal steps (see roadmap):

| Step | Milestone | Audience |
|---|---|---|
| Battle MVP | M2 | Internal alpha (team + friends) |
| Social MVP | M3 | Closed beta |
| Hardening + 100-CCU load test | M4 | Public MVP |

## 2. In scope
**MVP-Core:** FR-170–FR-241 (controls, launch, stats, classification, combat, burst, skills, balance data), FR-001–006, FR-010–012, FR-020–024, FR-030–040, FR-050–071 (open rules must be answered
first), FR-080, FR-081, FR-090, FR-091 (once decided), FR-100, FR-101, FR-150 (optional), FR-160 (first
platforms only), FR-161, FR-162, FR-164; all NFR/SEC/OPS marked Core.

**MVP-Social:** FR-102–104 (simple record/rank), FR-110–115 (basic teams — may slip to M5 if needed),
FR-130–133 (block, report, moderation queue, audit).

**Data model ready but feature off:** organizer application/approval (FR-121/122).

## 3. Out of scope for MVP
Exploration (FR-140–142), Team Battle (FR-082), stakes (FR-083), tournaments (FR-120, FR-123),
voice (FR-151/152), gamepad (FR-163), loot economy (FR-025), appeals tooling (FR-134), seasons.
Real-money wagering (FR-084) is excluded permanently unless the user decides otherwise.

## 4. First platforms — **confirmed v0.2**: Windows, Android, Linux (macOS, iOS later)
| Platform | MVP? | Reason |
|---|---|---|
| Windows | Yes | Largest desktop audience; simple distribution (direct download/itch.io/Steam TBD) |
| Android | Yes | Large mobile audience; sideload/closed testing tracks make beta easy |
| Linux | Yes (low cost) | Same export pipeline; server already Linux; low extra test cost |
| macOS | After MVP | Signing/notarization requires Apple developer account |
| iOS | After MVP | Requires Mac + Xcode, paid account, App Store review |

The architecture supports all five from day one (FR-160); only release order is staged (confirmed).

## 5. Minimum content [P]
One arena (dash rail; Xtreme zone optional), ~8–12 parts per slot (RING/CORE/TIP/SPIRIT) giving at least one build of each primary type and two hybrids, 7 skills, FFA friendly mode. Starter set: one build per type.

## 6. Pre-conditions before implementation of M2
G-01…G-03 answered in v0.2; G0 decisions D-01…D-18 recorded in v0.4 (owner acceptance of the approval-with-changes review pending). Remaining: owner questions OQ-LN-08, OQ-LN-09, OQ-CB-12; successful technical spikes S-1…S-6 (roadmap) with exit criteria AC-1…AC-9. Ranked play stays gated (FR-186).
