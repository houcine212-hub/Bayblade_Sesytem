# Project Understanding & Gap Analysis

| Field | Value |
|---|---|
| Document ID | DOC-GAP-001 |
| Status | Historical v0.1 analysis, annotated in v0.3.1 — current decisions live in the SRS, register and G0 decision sheet |
| Source | Master Product & Architecture Brief (the "Brief") |
| Date | 2026-11-21 |

Status labels used throughout this repository:

| Label | Meaning |
|---|---|
| **[C] Confirmed** | Explicitly stated by the user in the Brief |
| **[P] Proposed** | Engineering recommendation, not yet approved |
| **[A] Assumption** | Temporary, visible, reversible; registered in `assumptions-and-open-questions.md` |
| **[TBD] Open** | Insufficient information; must not be invented |

---

## 1. Repository inspection (Brief §P Step 1)

The working directory was **empty**: no existing repository, code, scenes, assets or documentation.
All artefacts in `docs/` were created from the Brief alone. Nothing was overwritten or deleted.
No git repository or remote exists yet — see review report, item R-0.

## 2. What we understand about the game

A 3D online multiplayer spinning-top battle game ("Beyblade-style") built with **Godot**, playable on
**desktop (Windows/Linux/macOS)** and **mobile (Android/iOS)** with **one shared account, backend and
multiplayer ecosystem**. Players own and customise tops, create/join rooms by code, launch their tops in
an arena (a launch mechanic driven by button presses plus top statistics), and fight until ring-out.
Last top in the arena wins (FFA). Persistent identity matters: profiles, teams with leaders, ranks,
match history, moderation. A first-person exploration world with chests and in-world challenges is part
of the long-term vision. Tournaments exist but organizers need admin approval. Voice features and
virtual-item stakes are later; real-money wagering is excluded.

## 3. Verification of critical numbers (Brief §P Step 2)

| Check | Result |
|---|---|
| Maximum active competitors per arena | **5** [C] (Brief §B2, §D2). The earlier "10" is explicitly superseded. No conflict remains in the Brief. |
| Meaning of "100" | **~100 concurrent connected players at peak** for the whole deployment, a planning/load-test target [C] (Brief §D1, §J1). It is **not** a match size and **not** a proven capacity. |
| Theoretical match bound | 100 / 5 = 20 simultaneous full matches — a test scenario only, not a promise (Brief §D2). |

## 4. Confirmed requirements (summary — full list with IDs in `docs/01-requirements/SRS.md`)

- Godot-based 3D client; desktop + mobile; shared account/backend/data/matchmaking/rules/history.
- Rooms: create, shareable code, join, fewer than 5 allowed, ready flow, spectators possible.
- Max 5 competitors per match.
- FFA: ring-out eliminates; last remaining top wins; eliminated players may spectate. *(v0.2+: Burst Finish is now the primary elimination; ring-out remains a confirmed secondary elimination — DOC-BURST-001 §3.)*
- Launch: a five-second period exists; launch-button presses contribute to spin; top stats matter (exact semantics TBD). *(Superseded v0.2: 5-second rapid-press window, 5 presses = 50 RPS — DOC-LAUNCH-001.)*
- Separation of balance data, loadout, rules, physics and presentation.
- MySQL for persistent data; never exposed to clients; not written per frame.
- Trusted server-side authority for official results (acceptance criterion O-7).
- Profiles, teams/leaders, ranks, match history; game is source of truth (not Facebook/Messenger).
- Tournament creation requires explicit owner/admin approval, enforced server-side.
- Reporting/moderation must be designed (not overbuilt).
- Exclusions from MVP: real-money wagering, voice control; 100-player arenas never.
- Candidate hosting: single Linux VPS (Hostinger KVM as a candidate only); services logically separated.
- Load tests at 10/25/50/100 CCU; concurrent-match tests separately.

## 5. Assumptions we need (all reversible; see register)

| ID | Assumption | Why needed |
|---|---|---|
| A-01 | Minimum 2 competitors to start a match | A 1-player "battle" has no FFA meaning |
| A-02 | The room creator ("host") starts the match once all competitors are ready | The Brief has a ready flow but no start trigger |
| A-03 | All MVP matches are "Friendly" (no stake) | Stakes need explicit approval |
| A-04 | New accounts receive at least one starter top | Otherwise a new player cannot play (K1 "select a top") |
| A-05 | One region / one VPS at launch | Brief describes one VPS; region is TBD |
| A-06 | A single Backend process instance initially | Simplifies room/allocator state; split later |
| A-07 | Client and match server are both written in GDScript on the same Godot version | Shared rules code; see ADR-002 |
| A-08 | No web-browser client is required | Brief lists only native desktop/mobile families |

## 6. Contradictions, ambiguities and risks

### 6.1 Gaps that change the core design (high impact) — *historical: G-01…G-03 were answered in v0.2 (see §7b); kept for traceability*

| ID | Gap | Why it matters |
|---|---|---|
| G-01 *(answered v0.2: 360° joystick + skill button)* | **Is there any player control during the battle** after launch (steering, abilities, "attack/defend")? The Brief only describes launch input; future voice commands imply in-battle commands exist. | Determines whether client prediction is needed, input bandwidth, anti-cheat surface and mobile UI. |
| G-02 *(answered v0.2: Burst primary; Spin/Over secondary)* | **Other elimination conditions**: does a top that stops spinning ("spin-out") or breaks ("burst") lose? Only ring-out is confirmed. | Without another end condition a match may never end → a timeout rule is mandatory. |
| G-03 *(answered v0.2: rapid-press window)* | **Five-second period semantics** (countdown? press window? delay after all join?) and the spin formula. | Drives match state machine, input sampling and fairness across touch/keyboard. |
| G-04 | **Physics fidelity**: arcade/stylised vs. realistic rigid-body. | Decides custom simulation vs. Godot physics engine on the server (ADR-005). |

### 6.2 Terminology conflict

**"Team" is used for two different things:** (a) a persistent social group with leaders (§G3) and
(b) a side in a Team Battle (§D4). Proposed resolution [P]: `Team` = persistent social group;
`MatchSide` = in-match grouping. A Team Battle side need not equal a social Team. Decision needed.

### 6.3 Other unresolved decisions
Room visibility, code lifetime, spectator capacity/mid-match join, disconnect/reconnect/AFK rules,
simultaneous ring-out, draws, timeout, rank algorithm, team limits, registration method, platforms'
release order and minimum specs, backend language, domain/TLS, budget. All are in the register.

### 6.4 Key risks (full list in `docs/08-planning/risk-register.md`)
- Physics "feel" is unproven; server-authoritative physics + mobile latency may feel laggy (RK-01).
- UDP may be blocked on some mobile/corporate networks (RK-03).
- One VPS is a single point of failure (RK-05).
- iOS requires Apple hardware, a paid developer account and App Store review (RK-07).
- Scope creep from exploration world, voice and tournaments (RK-09).
- The 100-CCU target is unverified until load-tested (RK-04).

## 7. Proposed documentation/design milestones

| Step | Output | Status |
|---|---|---|
| D1 | Requirements baseline (vision, scope, SRS, MVP scope, register, glossary) | Done in this package |
| D2 | System models (context, use case, domain, 8 sequences, activity, 2 state machines, component, deployment) | Done |
| D3 | Data design (ERD + data dictionary) | Done (proposed) |
| D4 | Interface contracts (Backend API, multiplayer protocol, trust boundaries) | Done (proposed) |
| D5 | Architecture + 9 ADRs | Done (proposed) |
| D6 | Security, quality/ops, roadmap, traceability, risks | Done |
| D7 | **User review & decisions** on blocking questions → revise → approval gate G0 | **Pending user** |
| D8 | After approval only: technical spikes (physics feel, network, headless benchmark, mobile render) | Not started |

## 7b. v0.2 update (Master Update, 2026-11-21)
G-01 (in-battle control), G-02 (end conditions → Burst primary), G-03 (launch semantics) were answered by the user. Platforms, accounts and exploration timing confirmed. New decisions are tracked in `docs/10-game-design/design-change-proposals.md` and the register (§2.1b). The questions below are kept for history.

## 8. High-priority questions that block the next step (v0.1 — mostly answered in v0.2)

1. **G-01 In-battle control:** after launch, can players influence their top? If yes, roughly how (direction, special ability, none)?
2. **G-02 End conditions:** besides ring-out, do spin-out or burst eliminate? Should there be a time limit?
3. **G-03 Launch:** what happens during the five seconds, and is "more presses = more spin" intended, or timing/rhythm-based?
4. **MVP boundary:** do you accept the recommendation that exploration is *after* the first public battle MVP?
5. **Platforms first:** which platform(s) must be in the first public release? (Recommendation: Windows + Android.)
6. **Accounts:** registration method (email+password? username only? Google/Apple sign-in?).
7. **Backend language** preference (recommendation: TypeScript/Node.js — ADR-003).
