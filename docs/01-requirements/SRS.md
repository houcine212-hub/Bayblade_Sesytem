# Software Requirements Specification (SRS)

| Field | Value |
|---|---|
| Document ID | DOC-SRS-001 |
| Version | 0.4.1 (G0 accepted with changes for M1 only, 2026-11-22; owner decisions OQ-LN-08, OQ-CB-12) |
| Status | Requirements marked [C] are user-confirmed; [P]/[A]/[TBD] are not |
| Related | `MVP-scope.md`, `assumptions-and-open-questions.md`, `glossary.md`, `../08-planning/traceability-matrix.md`, `../10-game-design/` (GDD and combat specifications) |
| Change log | v0.4.1: owner set RPS = max(20, 10 × n) (OQ-LN-08) and restated D-17 with a 7-press (70-RPS) difference (OQ-CB-12); owner accepted G0 with changes, M1 spikes only. v0.4: G0 decision register applied — D-01…D-03 owner-confirmed (linear launch 10 RPS/press, READY cue, zero presses = 20 RPS); D-04…D-18 decided under owner delegation (see DOC-CHG-040). v0.3.1: audit fixes — units/normalisation, burst guarantee, launch fairness + ranked gate, data-model alignment, reproducible analysis (`tools/analysis/`), new FR-186/FR-225/FR-226/NFR-074. v0.3: official sources verified; Energy recommendation, combat coefficients, burst targets, launch boundaries and acceptance criteria corrected (CHG-07…12). v0.2: joystick, skill button, rapid-press launch, Burst Finish, attributes/Energy confirmed; email+password accounts, unique display names, first platforms confirmed; backend stack re-evaluated (ADR-012). |

**Status column:** C = Confirmed by the owner; **D = decided under owner delegation at Gate G0 (D-04…D-18) — recorded decision, pending M1 technical verification**; P = Proposed; A = Assumption-based; TBD = placeholder for an open rule.
**Tier column:** Core = MVP-Core, Soc = MVP-Social, Post = Post-MVP, Excl = Excluded.

---

## 1. Introduction

### 1.1 Purpose
Defines what the system must do (functional), how well (non-functional), under which rules and
constraints, so that design, implementation and tests can be traced to user intent.

### 1.2 System overview
Four logical subsystems (see `../05-architecture/architecture.md`):
**Game Client** (Godot), **Backend API** (Laravel, proposed ADR-012), **Match Server** (headless Godot, authoritative real-time),
**MySQL database**. External: app stores/distribution, e-mail provider (needed: e-mail accounts confirmed), community channels.

### 1.3 Definitions
See `glossary.md`. Note the distinction **Team** (social group) vs **MatchSide** (in-match grouping) [P].

---

## 2. Roles (actors)

| Role ID | Role | Scope | Status |
|---|---|---|---|
| ROLE-GUEST | Unauthenticated user | Can register/log in only | P |
| ROLE-PLAYER | Registered player | Default role for every account | C |
| ROLE-TEAM-LEADER | Leader of a specific Team | Scoped to that team | C (concept) |
| ROLE-ORGANIZER | Approved tournament organizer | Global, granted by Admin | C (concept) |
| ROLE-MODERATOR | Handles reports, applies sanctions | Global | C (concept), names TBD |
| ROLE-ADMIN | Owner/admin; approves organizers, grants roles | Global | C |
| ROLE-SPECTATOR | In-room/in-match participation mode (not an account role) | Per match | C (concept) |
| SYS-MATCH | Match Server service identity | Trusted service | P |

Exact role names and permission policies remain **TBD** (OQ-AC-05). Permission matrix proposal: `../06-security/auth-and-permissions.md`.

---

## 3. Functional requirements

### 3.1 Accounts & identity
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-001 | One account works on all supported platforms, with the same profile, inventory, team, rank and history. | C | Core |
| FR-002 | A guest registers with **e-mail and password**; e-mail verification required before ranked/social features [P]. Third-party authentication is postponed. | C | Core |
| FR-003 | A player can log in and log out; the Backend issues a session (access + refresh token) [P mechanism]. | C need / P mechanism | Core |
| FR-004 | Password reset via e-mailed single-use link (expiry 60 min [P]). | C need / P policy | Core |
| FR-005 | A player can request account deletion and personal-data export. | P (privacy, J6) | Core |
| FR-006 | The Backend rejects login from client builds below the minimum supported version, telling the user to update. | P | Core |

### 3.2 Profile
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-010 | Each account has a player profile showing display name, team (if any), competitive record/rank, and recent matches. | C | Core |
| FR-011 | Every player has a **unique in-game display name** (case-insensitive uniqueness [P]); editable within validation and rename-limit rules [P]. | C | Core |
| FR-012 | A player can view other players' public profiles. | P | Core |

### 3.3 Items, inventory and loadout
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-020 | Top/part definitions and balance statistics are data-driven (versioned content data), not hard-coded in unrelated systems. Part slots RING/CORE/TIP/SPIRIT [P]. | C (E3 separation) / P (format) | Core |
| FR-021 | Each player owns persistent inventory items referencing item definitions. | C | Core |
| FR-022 | A player selects/equips a loadout (a top, possibly assembled from parts) to use in a match. | C | Core |
| FR-023 | A new account receives at least one starter top. | A (A-04) | Core |
| FR-024 | The loadout used in a match is snapshotted at match start so later edits do not alter history. | P | Core |
| FR-025 | Part categories, stats, rarity, duplication, trading, crafting, purchase rules. | TBD (OQ-GP-03, OQ-GP-11) | Post |

### 3.4 Rooms
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-030 | A player can create a room and becomes its host. | C (create) / A (host, A-02) | Core |
| FR-031 | The system generates a shareable room code for each room. | C | Core |
| FR-032 | A player can join a room by entering its code. | C | Core |
| FR-033 | A room admits **at most 5 competitors**; a 6th competitor join is rejected by the Backend. | C | Core |
| FR-034 | A match may start with fewer than 5 competitors; the minimum is 2. | C (<5) / A (min 2, A-01) | Core |
| FR-035 | Competitors mark ready/unready before the battle starts. | C | Core |
| FR-036 | The host starts the match when all competitors are ready. | A (A-02) | Core |
| FR-037 | A room member may join as a spectator (not counted toward the 5). Capacity TBD (OQ-GP-07). | C concept / TBD capacity | Core |
| FR-038 | A member can leave a room; host leaving → transfer or close is TBD (OQ-GP-13). | P / TBD | Core |
| FR-039 | Room visibility (public/private/invite), code lifetime, persistence after match. | TBD (OQ-GP-08, OQ-GP-14) | Core |
| FR-040 | A player selects their loadout while in the room before readying. | P | Core |

### 3.5 Match lifecycle & battle
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-050 | On start, the Backend allocates an authoritative Match Server instance and issues each participant a short-lived match ticket. | P | Core |
| FR-051 | Only ticket holders can connect to a match; tickets bind user, match and role (competitor/spectator). | P | Core |
| FR-052 | Before each battle a **1.5 s READY cue** (no accepted presses) is followed by **exactly 5.0 s** launch window with a dedicated launch zone (DOC-LAUNCH-001). | C (D-02) | Core |
| FR-053 | Players **rapid-press** the launch zone; initial rotation = **max(20, 10 × accepted presses)** RPS (5 presses = 50 RPS); details FR-180–FR-186. | C (D-01 as amended by OQ-LN-08) | Core |
| FR-054 | The top's characteristics and abilities influence performance (through attributes, component properties and skills during battle; launch RPS itself is input-only [P]). | C / P | Core |
| FR-055 | The Match Server simulates the battle authoritatively; clients send inputs and render state. | C (O-7) / P (method) | Core |
| FR-056 | **FFA:** a top that exits the arena eliminates its player (finish OVER / XTREME). | C | Core |
| FR-057 | **FFA:** the last remaining top/player wins. | C | Core |
| FR-058 | An eliminated player switches to spectating the rest of the battle. | C | Core |
| FR-059 | All participants see understandable feedback for launch timing, spin state, collisions, elimination and results. | C (C3) | Core |
| FR-060 | **Burst Finish is the primary elimination mechanic**; Spin Finish (spin below stop threshold) also eliminates [P, CHG-04]. Details FR-220–FR-224. | C (burst) / P (spin) | Core |
| FR-061 | In battle each player steers with a 360° analog joystick and activates skills with a Skill button (FR-170–FR-175, FR-230–FR-234). | C | Core |
| FR-062 | Simultaneous eliminations in the same tick share a placement; no match restart. | D (D-11) | Core |
| FR-063 | Competitor disconnect / app close during match. | TBD (OQ-GP-05) | Core |
| FR-064 | Competitor reconnect during active match (proposal: grace period, see sequence SQ-08). | TBD rule / P mechanism | Core |
| FR-065 | Zero accepted presses → automatic launch at **20 RPS**, no automatic elimination (covered by the 20-RPS floor of FR-182); idle (no input) during battle: rule TBD (OQ-GP-06). | C (D-03, OQ-LN-08) / TBD | Core |
| FR-066 | Only one competitor left before battle begins (e.g. others left). | TBD (OQ-GP-17) | Core |
| FR-067 | If the last remaining competitors are all eliminated in the same tick, the match is a draw with no unique winner; deterministic outcome persisted; no rank-affecting result in MVP. | D (D-11) | Core |
| FR-068 | Match Server interruption → match marked aborted; no competitive effect (proposed). | TBD rule / P default | Core |
| FR-069 | Match time limit **120 s**; at timeout survivors are ranked by current spin (higher = better), exact ties share placement; provisional tuning. | D (D-16) | Core |
| FR-070 | The Match Server reports the official result to the Backend; the Backend persists it once (idempotent). | P | Core |
| FR-071 | Clients can never submit or alter official results. | C | Core |

### 3.6 Match modes
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-080 | Free-for-All mode. | C | Core |
| FR-081 | Friendly (no-stake) match; all MVP matches are friendly. | C concept / A (A-03) | Core |
| FR-082 | Team Battle mode (team sizes, assignment, friendly fire, elimination, victory). | TBD | Post |
| FR-083 | Virtual-item stake mode — only after explicit user approval of rules. | C (gate) | Post |
| FR-084 | Real-money wagering is not supported. | C | Excl |

### 3.7 Spectating
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-090 | Spectators receive match state but cannot submit competitor inputs (enforced server-side). | C concept / P enforcement | Core |
| FR-091 | Mid-match spectator join. | TBD (OQ-GP-07) | Core |

### 3.8 Match history, records and ranks
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-100 | Completed matches are persisted with participants, loadout snapshots, placements and end reason. | C | Core |
| FR-101 | A player can view their match history and other players' public history. | C | Core |
| FR-102 | The system maintains a competitive record per player (matches, wins, placements). | P | Soc |
| FR-103 | Ranks / competitive standing. Algorithm, seasons, penalties TBD (OQ-AC-04; options in `../05-architecture/adr/ADR-009-ranking-approach.md`). | C concept / TBD | Soc |
| FR-104 | Leaderboard view. | P | Soc |

### 3.9 Teams (social)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-110 | A player can create a Team with name, identity (tag/emblem) and description; eligibility TBD. | C concept / TBD rules | Soc |
| FR-111 | A Team has leader and member roles. | C | Soc |
| FR-112 | Leaders invite; players request to join; leaders accept/reject; members leave; leaders remove. | C (investigate) / P | Soc |
| FR-113 | Leader transfer and team dissolution. | C (investigate) / P | Soc |
| FR-114 | Team membership history is retained. | C (investigate) / P | Soc |
| FR-115 | Team size limits / multi-team membership. | TBD (OQ-AC-03) | Soc |
| FR-116 | Team history and achievements. | TBD ("if approved") | Post |

### 3.10 Tournaments & organizer authorization
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-120 | Tournament creation is restricted to approved organizers. | C | Post |
| FR-121 | A player may apply for organizer status; rank may make them eligible (threshold TBD). | C concept / TBD | Post |
| FR-122 | Only an Admin can approve or revoke organizer status; every decision is audited. | C / P audit | Post (model in Core) |
| FR-123 | Tournament formats, registration, brackets. | TBD (OQ-AC-06) | Post |

### 3.11 Safety & moderation
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-130 | A player can block another player (hides chat/invites from them). | P | Soc |
| FR-131 | A player can report another player with a reason category, optional text and optional match reference. | C (design) | Soc |
| FR-132 | Moderators view a report queue and apply actions (warn, mute, temporary/permanent suspension). | P | Soc |
| FR-133 | All moderation actions are recorded in an audit history. | P | Soc |
| FR-134 | Appeal workflow (MVP: manual via official contact). | P | Post |
| FR-135 | Chat scope (room chat? global? none?) | TBD (OQ-AC-07) | TBD |

### 3.12 Exploration (vision)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-140 | Bounded first-person exploration area — **postponed beyond the Battle MVP**. | C | Post |
| FR-141 | Chests containing parts/items — postponed. | C | Post |
| FR-142 | Challenge another player in the world; on acceptance a battle starts (arena rises). | C (vision) | Post |

### 3.13 Community & voice
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-150 | The client may show links to official external community channels. No API integration. | C (not authoritative) / P links | Core (optional) |
| FR-151 | Proximity voice chat in exploration. | C (later) | Post |
| FR-152 | Voice commands for top control. | C (later, excluded from MVP) | Post |

### 3.14 Client platforms & input
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-160 | Clients from one cross-platform Godot project. **Initial release: Windows, Android, Linux; macOS and iOS in later releases.** | C | Core (Win/Android/Linux) |
| FR-161 | Mobile: touch controls, touch-friendly UI, safe-area handling. | C | Core |
| FR-162 | Desktop: keyboard and mouse. | C | Core |
| FR-163 | Game-controller support for joystick, skill and launch (confirmed by joystick requirement). | C | Core |
| FR-164 | Graphics quality presets for device tiers. | P | Core |

### 3.15 Battle controls (v0.2)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-170 | Each competitor has a 360° **analog** directional joystick controlling direction and trajectory of their top during battle. | C | Core |
| FR-171 | Joystick input works on touchscreen, keyboard/mouse (mouse-vector analog mode; keyboard 8-way with ramp) and game controllers. | C / P (mappings) | Core |
| FR-172 | Steering is responsive (local prediction) and synchronised by the authoritative server. | C / P (method) | Core |
| FR-173 | A Skill button is placed on the opposite side of the joystick. | C | Core |
| FR-174 | Mirrored (left-handed) layout option. | P | Core |
| FR-175 | Steering authority scales with mobility and spin; steering consumes spin. | P | Core |

### 3.16 Launch (v0.2)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-180 | A launch zone appears for the 5-second window; presses outside it do not count (touch/mouse). | C | Core |
| FR-181 | A successful press is edge-triggered, released before the next, inside the half-open window [W0, W0+5000 ms), at least 142 857 µs (1000/7 ms) after the previous accepted press, at most **35** accepted presses (provisional, from a provisional 7 presses/s median), key repeat ignored; enforced by the server. | D (D-04) | Core |
| FR-182 | Launch RPS = **max(20, 10 × n)**, n = accepted presses (≤ 35); linear 10 RPS per press above the floor; no exponential, saturating or rescaled formula. | C (D-01, D-03, OQ-LN-08) | Core |
| FR-183 | Launch RPS range: **20** (n ≤ 2) to **350** (n = 35). Displayed RPS equals the authoritative value. | C / D (cap D-04) | Core |
| FR-184 | The Match Server counts presses from timestamped batches and determines launch RPS; client counts are cosmetic. | C (server authority) / P | Core |
| FR-185 | All competitors see every launch result (presses, RPS) before battle starts. | P | Core |
| FR-186 | Ranked matchmaking, ratings and rank-affecting results stay disabled until launch fairness criterion FC-1 (NFR-074) passes with spike S-5/S-1 data. Friendly code rooms unaffected. | D (D-04) | Core |

### 3.17 Statistics & Energy (v0.2)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-190 | Each Bey build has four primary attributes: Attack, Defense, Stamina, Magic (0–100). | C | Core |
| FR-191 | Energy is derived from the four attributes and is not an independent attribute. | C | Core |
| FR-192 | Energy = (ATK + DEF + STA + MAG) / 4 — **provisional**, not balance-certified until skill-inclusive AC-7 (S-1). | D (D-07) | Core |
| FR-193 | RPS (launch and current spin) is a separate battle variable, not an attribute. | C | Core |
| FR-194 | The Stamina attribute (decay resistance) is distinct from current spin (remaining rotation) in data, calculations and UI ("Stamina" vs "Spin"). | C | Core |
| FR-195 | Component properties mass, lock strength, mobility, friction, height, contact profile, spin direction exist separately from attributes. | D (D-05) | Core |
| FR-196 | Attributes are computed from equipped parts within a tier budget; shown on the build screen with Energy and type. | P | Core |

### 3.18 Classification (v0.2)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-200 | Primary types ATTACK, DEFENSE, STAMINA, BALANCE. | C (investigate) / P (definitions per DOC-CLS-001) | Core |
| FR-201 | Builds may have a secondary type (hybrid) when shares are close. | P | Core |
| FR-202 | Headline type per CHG-10 (proposal: the TIP part's `tip_type`, as in official Beyblade X where the Bit decides the type) with a separately stored computed profile (primary/secondary/subtype, or UNCLASSIFIED when ATK+DEF+STA < 30); alternative: computed type only. | D (D-08) | Core |
| FR-203 | Classification thresholds are configurable content data. | P | Core |
| FR-204 | Spin direction (RIGHT/LEFT/DUAL) is a separate badge; no MVP gameplay effect. | P | Core |
| FR-205 | Subtypes SMASH, UPPER, ANCHOR, ABSORB, ENDURANCE, EVASIVE, ADAPTIVE. | P | Core |

### 3.19 Combat interaction (v0.2)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-210 | Every collision effect is computed from the characteristics of **both** Beys involved. | C | Core |
| FR-211 | RPS influence depends on the relative Energy: strong at similar Energy, progressively weaker with larger gaps. | C | Core |
| FR-212 | The transition is smooth; per contact w ≥ 0.15; outcome-level (D-17 as amended by owner decision OQ-CB-12): a **7-press (70-RPS) launch difference** changes win probability by ≥ 10 points for \|g\| ≤ 0.20. Model: passes in Attack and Balance mirrors; **Stamina mirror 9.9 points at g = 0.20 (borderline fail)**. The superseded 30-RPS wording is not evidence of passing. | C / D (D-17, OQ-CB-12) | Core |
| FR-213 | Collisions determine impact, knockback, stability (stagger), spin loss, lock damage (burst) and skill effectiveness per DOC-CMB-001. | C (list) / D (structure D-12; values experimental) | Core |
| FR-214 | Type advantages emerge from attributes/properties; optional bounded type modifiers (±5%) disabled by default. | P | Core |
| FR-215 | No absolute counter rule exists (any matchup can be overturned by RPS, Energy, steering or skills). Measurable target: favoured matchups 55–80% seat-averaged (ADR-013 AC-2; v0.4.1 model: 79.5–86.3%, A>S and S>D outside — open). | C / P (target) | Core |

### 3.20 Burst Finish & finishes (v0.2)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-220 | A sufficiently powerful impact (cumulatively) separates components → BURST elimination. | C | Core |
| FR-221 | Hybrid burst model (original design; official sources define only that parts separate): Lock Integrity gauge, spin-dependent threshold, bounded seeded variance; canonical equation DOC-BURST-001 §2.2. | D (D-14) | Core |
| FR-222 | Burst/elimination determined and broadcast by the Match Server; eliminated player becomes spectator; remaining competitors continue; results recorded. | C | Core |
| FR-223 | Physical finish types recorded per elimination: BURST (primary, C), OVER (secondary, C), SPIN (secondary, required, P), XTREME (optional, P). Non-physical results (disconnect forfeit, no-show, abort, time-limit rank) are outcome reasons, not finish types. | C / D (D-09) | Core |
| FR-224 | Burst gauge shown in 4 stages. | P | Core |
| FR-225 | A Bey at full Lock Integrity cannot burst from one contact: per-tick lock damage per victim ≤ 49 and critical burst only if Lock Integrity at the **start** of the tick ≤ 50 (proof DOC-BURST-001 §2.3). | D (D-14, D-18) | Core |
| FR-226 | Contact events: physics contact begin with v_n > v_min; 100 ms debounce per pair; resolved in both directions with start-of-tick values; simultaneous contacts summed in deterministic order. | D (D-18) | Core |

### 3.21 Skills & Magic (v0.2)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-230 | Beys have special skills related to their characteristics and classification (granted by SPIRIT part, type compatibility). | C / P | Core |
| FR-231 | Skills have gauge cost, cooldown, activation conditions and per-match limits. | C (need) / P (values) | Core |
| FR-232 | Magic influences skill gauge charge (×0.85–1.15), potency (×0.80–1.20) and skill resistance. | C (investigate) / D (D-06) | Core |
| FR-233 | Skills are bounded: no direct elimination, no stacking, ≤ +30% self-buff, max 3 uses per match. | C (not unlimited) / P | Core |
| FR-234 | Skill activation validated by the Match Server. | P | Core |

### 3.22 Balance data & telemetry (v0.2)
| ID | Requirement | Status | Tier |
|---|---|---|---|
| FR-240 | All combat coefficients, curves, thresholds and part stats are versioned content data (`content_version`). | C | Core |
| FR-241 | Match results include balancing telemetry: per-participant type, Energy, launch presses/RPS, finish type, skill uses. | P | Core |

---

## 4. Business rules
| ID | Rule | Status |
|---|---|---|
| BR-001 | A match has at most 5 active competitors. Spectators are not competitors. | C |
| BR-002 | FFA: a top that exits the arena is eliminated. | C |
| BR-003 | FFA: the last remaining top/player wins. | C |
| BR-004 | An eliminated player may spectate the remainder of the match. | C |
| BR-005 | Only the Match Server (trusted authority) determines official match results. | C |
| BR-006 | Tournament creation requires organizer status explicitly approved by Admin. | C |
| BR-007 | Permissions are enforced by Backend/Match Server, never only by client UI. | C |
| BR-008 | No real-money wagering in MVP. | C |
| BR-009 | Virtual-item stakes cannot be enabled without explicit user approval of their rules. | C |
| BR-010 | Voice-based top control is not part of MVP. | C |
| BR-011 | External channels (Facebook/Messenger) are not authoritative for membership, rank, results or permissions. | C |
| BR-012 | Minimum competitors to start = 2. | A (A-01) |
| BR-013 | Aborted matches (server failure) have no competitive effect. | P |
| BR-014 | A client may only join a match server whose protocol version matches its own. | P |
| BR-015 | Burst Finish is the primary elimination mechanic. | C |
| BR-016 | Initial rotation is determined only by successful launch presses counted by the server. | C |
| BR-017 | Energy is derived; never edited or stored as an input attribute. | C |
| BR-018 | Skills are limited and cannot eliminate directly. | C (not unlimited) / P |
| BR-019 | Each display name is unique. | C |

## 5. Non-functional requirements
Provisional numeric targets are **examples to validate by benchmark**, not achieved capacity.

### 5.1 Performance & capacity
| ID | Requirement | Status |
|---|---|---|
| NFR-001 | Plan for ~100 concurrent connected users at peak (lobby + matches + menus). Not a proven capacity until NFR-004 passes. | C target |
| NFR-002 | Per-match competitor cap of 5 enforced at Backend (room), ticket issuing, and Match Server. | C |
| NFR-003 | Resource use scales with active matches; idle capacity at low population stays small (e.g. a small warm pool). | C intent / P mechanism |
| NFR-004 | Load tests at 10, 25, 50, 100 connected clients pass the criteria in `../07-quality-operations/load-test-plan.md`. | C |
| NFR-005 | Concurrent-match test up to 20 simultaneous 5-competitor matches (theoretical scenario). | C |
| NFR-006 | Match Server simulation tick: provisional 60 Hz; state snapshots to clients: provisional 30 Hz (joystick play). | P (benchmark) |
| NFR-011 | Own-input-to-visual response for steering ≤ 100 ms on target devices (local prediction). | P |
| NFR-012 | Control input upload 30 Hz with 3-input redundancy; ≤ 2 kbit/s per player. | P |
| NFR-007 | Gameplay remains acceptable up to a provisional 150 ms RTT and 2% packet loss. | P (spike) |
| NFR-008 | Downstream bandwidth per match client: provisional ≤ 64 kbit/s average. | P (estimate in protocol doc) |
| NFR-009 | Time from host "Start" to all clients in pre-launch phase: provisional ≤ 5 s (p95). | P |
| NFR-010 | Backend API p95 latency ≤ 300 ms at 100 CCU for non-search endpoints (provisional). | P |

### 5.2 Client performance
| ID | Requirement | Status |
|---|---|---|
| NFR-020 | Designed for mid-range mobile hardware, not only high-end PCs. | C |
| NFR-021 | Frame-rate, memory and thermal targets defined per representative test device after device selection. | C (define later) |
| NFR-022 | Scalable rendering/effects via quality presets; physics cost on clients minimal (clients render, not simulate authoritative physics). | P |

### 5.3 Reliability
| ID | Requirement | Status |
|---|---|---|
| NFR-030 | A crash of one match must not end other matches (process isolation, ADR-006). | P |
| NFR-031 | If the Backend is down, running matches continue to completion; results are retried until accepted. | P |
| NFR-032 | Database backups: provisional RPO ≤ 24 h (daily full + binlog for tighter RPO later), RTO ≤ 4 h. | P |
| NFR-033 | Services restart automatically after failure (process supervisor). | P |

### 5.4 Maintainability
| ID | Requirement | Status |
|---|---|---|
| NFR-040 | Clear modular boundaries between Client, Backend, Match Server and data access. | C |
| NFR-041 | Reproducible local development environment for all services. | C |
| NFR-042 | Documentation, ADRs and diagrams source-controlled and kept in sync with code. | C |
| NFR-043 | Automated tests at unit, integration, contract, simulation and E2E levels. | C |
| NFR-044 | Balance data externalised and versioned (content version). | C intent / P format |
| NFR-045 | Combat simulation deterministic per tick given seed + inputs (replay tests). | P |

### 5.4b Gameplay balance targets (tuning goals, not guarantees)
| ID | Requirement | Status |
|---|---|---|
| NFR-070 | Burst metrics (D-10, initial target): **M-1** BURST ≥ 30% of all eliminations in the evaluation population; **M-2** BURST most frequent in attributed pairs Attack→Attack/Stamina/Balance. "Primary" = signature finish, not globally most frequent (model: SPIN 39.9% vs BURST 33.8%). Reconsider after real playtests. (Superseded wording: ≥ 40%.) | D (D-10) |
| NFR-071 | ADR-013 AC-1 (each type 45–55% vs other types), AC-2 (favoured matchups 55–80%, seat-averaged) and AC-8 (FFA type win share within ±5 points of expectation). Current candidate fails AC-1/AC-2; AC-8 untested (DOC-BAL-001 §5.3). | D (D-13) |
| NFR-072 | Median match length 30–90 s; 120 s time limit (D-16). | P / D |
| NFR-073 | Median launch RPS per input device type within 5%. | P |
| NFR-074 | Launch fairness FC-1: a player always at the press cap wins ≤ 60% of equal-build 1-v-1 mirrors (Attack, Stamina) against a player at the median measured touch press count. | D (D-04) |

### 5.5 Cross-platform
| ID | Requirement | Status |
|---|---|---|
| NFR-050 | A platform compatibility matrix (min OS, input, graphics, release constraints) is maintained. | C |
| NFR-051 | Identical gameplay rules on all platforms (single authoritative server rules). | C |

### 5.6 Privacy
| ID | Requirement | Status |
|---|---|---|
| NFR-060 | Collect only data necessary for the stated purposes (data inventory in `../03-data/data-dictionary.md`). | C |
| NFR-061 | Define retention, deletion and export for personal data; legal review for target markets before public launch. | C |

### 5.7 Security (summary; details in `../06-security/`)
| ID | Requirement | Status |
|---|---|---|
| SEC-001 | Game clients never connect to MySQL; MySQL listens on localhost/private network only. | C |
| SEC-002 | Official results determined server-side; client claims ignored. | C |
| SEC-003 | All authorization checks run in Backend/Match Server. | C |
| SEC-004 | Passwords (if used) hashed with a memory-hard algorithm (Argon2id). | P |
| SEC-005 | All Client↔Backend traffic uses TLS (HTTPS/WSS). | P |
| SEC-006 | Match tickets are signed, short-lived (≤ 60 s to first use), single-use, bound to user+match+role+protocol version. | P |
| SEC-007 | Server-side input validation for all API and match messages; parameterised queries only. | C (analyse) / P |
| SEC-008 | Rate limiting on auth, room-code join, report and chat endpoints. | C (analyse) / P |
| SEC-009 | Secrets kept out of source control and client builds. | C |
| SEC-010 | Audit log for privileged actions (role grants, organizer approval, moderation). | C (analyse) / P |
| SEC-011 | Room codes resistant to enumeration (sufficient entropy + join rate limits). | P |
| SEC-012 | Backend↔Match Server calls authenticated with a service credential over a private channel. | P |
| SEC-013 | Launch anti-automation: 12 Hz cap, edge/release rule, server timestamp validation, regularity flags (no auto-penalty in MVP). | P |
| SEC-015 | Control inputs clamped (|u| ≤ 1) and rate-limited (≤ 60/s); spectator inputs dropped. | P |
| SEC-016 | Skill activation validated server-side (gauge, cooldown, limits, phase). | P |
| SEC-014 | Match message flood protection (per-peer message rate caps). | P |

### 5.8 Operations
| ID | Requirement | Status |
|---|---|---|
| OPS-001 | Monitor CPU, RAM, disk, network, process health. | C |
| OPS-002 | Structured logs with correlation IDs (match_id, user_id, request_id). | P |
| OPS-003 | Alerts for service down, disk > 80%, backup failure, match-server pool exhausted. | P |
| OPS-004 | Automated off-site backups with periodic restore tests. | C (backups) / P (tests) |
| OPS-005 | Deliberate firewall: only HTTPS and the match UDP port range public; SSH restricted. | C |
| OPS-006 | Versioned, repeatable deployments with rollback. | P |
| OPS-007 | VPS sizing decided from benchmarks, not from the 100-CCU figure alone. | C |

## 6. Constraints
| ID | Constraint | Status |
|---|---|---|
| CON-01 | Game engine: Godot. Version: ADR-001 (proposed 4.7.x). | C engine / P version |
| CON-02 | Persistent database: MySQL (re-evaluated in ADR-004). | C planned |
| CON-07 | Backend stack chosen by objective comparison (ADR-012): PHP 8.3+ / Laravel 13 / Reverb / MySQL 8.4 + Godot 4.7 headless authoritative UDP Match Server — conditional on M1 spikes. | C / D (D-15) |
| CON-03 | Initial hosting: single Linux VPS; Hostinger KVM is a candidate only. | C candidate |
| CON-04 | Services logically separated to allow later split. | C |
| CON-05 | Must support UDP if ENet is chosen. | C |
| CON-06 | iOS export requires macOS + Xcode and Apple developer programme. | Fact to verify per ADR-008 |

## 7. Acceptance criteria (MVP level)
High-level acceptance criteria per requirement are traced in `../08-planning/traceability-matrix.md`;
MVP-readiness criteria are in `../07-quality-operations/mvp-readiness.md`. Example criteria:

| Req | Acceptance criterion |
|---|---|
| FR-033 | Given a room with 5 competitors, when a 6th player joins as competitor, then the Backend returns `409 ROOM_FULL` and the room still lists 5 competitors. |
| FR-051 | Given an expired, reused, or other-match ticket, the Match Server rejects the connection within 1 s and logs `TICKET_INVALID`. |
| FR-056/057 | In a simulated 3-top match where tops A and B ring out at distinct ticks, C is recorded as winner, placements are C=1, B=2, A=3. |
| FR-182 | 0, 1, 2 accepted presses → 20 RPS; 3 → 30; 5 → 50; 15 → 150; 25 → 250; 35 → 350; 36th press rejected. |
| FR-211 | With E_A = E_B the RPS weight w = 0.60; with g = 0.30, w = 0.257; for any g, w ≥ 0.15. |
| FR-225 | A Bey at L = 100 never bursts from a single contact, for any N (tested up to 10⁶); L ≤ 0 always bursts. |
| FR-233 | A 4th skill activation in one match is rejected with `SKILL_LIMIT`. |
| FR-058 | After elimination the client receives `RoleChanged(spectator)` and further gameplay inputs from that peer are dropped and counted. |
| FR-070 | Reporting the same result twice yields exactly one persisted result (idempotency). |
| FR-071 | A crafted client RPC claiming victory has no effect on the persisted result. |
| SEC-001 | External port scan of the VPS shows MySQL port closed. |
