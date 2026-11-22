# Assumptions & Open Questions Register

| Document ID | DOC-REG-001 | Status | Living document — update on every decision |
|---|---|---|---|

Priority: **B** = blocks next design/implementation step, **H** = needed before MVP build of that feature, **L** = later.
When a question is answered, move it to §3 (Decision log) with date and source; never delete.

## 1. Assumptions (reversible)
| ID | Assumption | Affects | Reverse if… |
|---|---|---|---|
| A-01 | Min 2 competitors to start | FR-034, BR-012 | User wants solo practice vs bots/empty arena |
| A-02 | Room creator is host and starts the match | FR-030, FR-036 | User prefers auto-start when all ready |
| A-03 | All MVP matches are Friendly | FR-081 | Stakes approved for MVP |
| A-04 | New accounts get a starter top | FR-023 | Different onboarding chosen |
| A-05 | One region / one VPS at launch | Deployment | Players spread across distant regions |
| A-06 | One Backend instance at launch | ADR-012 (supersedes ADR-003), allocator | Load requires horizontal scaling |
| A-07 | GDScript for client and Match Server, same Godot version | ADR-002 | Team prefers C# |
| A-11 | Human sustained tapping ≈ 5–9 presses/s (sets launch curve expectations) | DOC-LAUNCH-001 | Spike S-5 measurements differ |
| A-12 | One skill per Bey in MVP (granted by SPIRIT part) | DOC-SKILL-001 | User wants multiple skills |
| A-13 | No persistent part wear between matches | DOC-BURST-001 | User wants durability economy |
| A-14 | Steering skill varies between players with SD ≈ 15% of impact speed (analysis proxy) | DOC-BAL-001 §2 | Spike S-1/S-2 measures real steering variance |
| A-08 | No web-browser client | ADR-007 transport | Web build becomes required |
| A-09 | ~~Players are identified in-game by a unique display name~~ **Now confirmed (BR-019)** | FR-011 | — |
| A-10 | Spectators do not count against the 5-competitor cap | BR-001 | — (strongly implied by Brief) |

## 2. Open questions
### 2.1 Gameplay (OQ-GP)
| ID | Question | Pri | Options / notes | Related |
|---|---|---|---|---|
| OQ-GP-01 | Meaning of the five-second period: countdown before presses? press window? delay after all enter? | ~~**B**~~ **ANSWERED v0.2: 5-second rapid-press launch window (see decision log)** | (a) 5 s press window then release; (b) 3 s countdown + 2 s window; (c) 5 s wait then single-timing press | FR-052, ST-MATCH |
| OQ-GP-02 | Launch input: count presses? rhythm/timing? press limit? formula with top stats? | ~~**B**~~ **ANSWERED v0.2: press count → RPS (5 = 50); curve proposed CHG-01** | Press-count is the most macro/hardware-sensitive; timing-based is fairer across devices | FR-053, SEC-013 |
| OQ-GP-03 | Top stats, part categories, abilities, physics model | H | Proposed data schema in data dictionary | FR-020, FR-025 |
| OQ-GP-04 | Simultaneous ring-out; draw / no winner (official: draw **and restart**, O-2; proposal CHG-11: shared placement) | **DECIDED — D-11 delegated: shared placement; all-out same tick = draw** | (a) same tick = shared placement; (b) tie-break by remaining spin; (c) draw | FR-062, FR-067 |
| OQ-GP-05 | Disconnect rules | H | (a) top keeps spinning under simulation; (b) top removed = eliminated after grace | FR-063 |
| OQ-GP-06 | AFK / no launch | H | (a) auto-launch at minimum spin; (b) eliminated before battle | FR-065 |
| OQ-GP-07 | Spectator capacity; mid-match join | H | Proposed default: up to 10 spectators, join allowed any time | FR-037, FR-091 |
| OQ-GP-08 | Room visibility: public list / private code / both | H | Code-only is simplest and safest for MVP | FR-039 |
| OQ-GP-09 | Team Battle rules | L | sizes, assignment, friendly fire, victory | FR-082 |
| OQ-GP-10 | Stakes in MVP or later | L | Recommendation: later (A-03) | FR-083 |
| OQ-GP-11 | Loot, inventory, progression economy | L | No monetisation invented | FR-025 |
| OQ-GP-12 | Exploration in MVP or after | ~~**B**~~ **ANSWERED v0.2: exploration postponed beyond Battle MVP** | Recommendation: after (M5) | FR-140 |
| OQ-GP-13 | Host leaves room: transfer host or close room? | H | | FR-038 |
| OQ-GP-14 | Room code lifetime; does room persist after match (rematch)? | H | Proposal: room persists for rematch; expires after 30 min idle | FR-039 |
| OQ-GP-15 | Elimination by spin-out/burst? | ~~**B**~~ **ANSWERED v0.2: Burst Finish primary; Spin Finish proposed (CHG-04)** | Strongly affects physics model and match length | FR-060 |
| OQ-GP-16 | Any in-battle control after launch? | ~~**B**~~ **ANSWERED v0.2: 360° joystick + skill button** | Affects prediction, input protocol, UI | FR-061 |
| OQ-GP-17 | Only one competitor left before battle starts | H | (a) cancel match; (b) walkover win (no rank effect) | FR-066 |
| OQ-GP-18 | Match time limit and what happens at time-out | **DECIDED — D-16 delegated: 120 s, rank by current spin** | Proposal (G0 D-16): 120 s, then remaining Beys ranked by current spin (higher = better), ties shared. Longest measured pairing median 99 s | FR-069 |
| OQ-GP-19 | Does launch aiming (position/angle/direction) exist? | H | | FR-053 |

### 2.1b Combat, launch, stats (OQ-LN / OQ-ST / OQ-BU / OQ-CB / OQ-SK) — v0.2
| ID | Question | Pri | Options / recommendation | Related |
|---|---|---|---|---|
| OQ-LN-01 | Add a 1.5 s non-counted READY cue before the 5 s window? | **DECIDED — D-02 owner-confirmed: 1.5 s READY cue** | Recommended yes | FR-052 |
| OQ-LN-02 | Accessibility: assisted launch allowed in friendly rooms only? | H | Recommended: yes, friendly only, marked in results | FR-181 |
| OQ-LN-03 | Should TIP/part stats modify launch RPS (e.g. ±5% max)? | H | Recommended no (launch = pure skill) | FR-054 |
| OQ-LN-04 | Accept saturating curve (CHG-01) or literal linear ×10? | **DECIDED — D-01 owner-confirmed: linear 10 RPS/press (curve rejected)** | Curve | FR-182 |
| OQ-LN-05 | Can the joystick aim the launch direction during the window? | H | Proposal: yes, initial heading only | FR-170 |
| OQ-ST-01 | Accept component properties beside the four attributes (CHG-02)? | **DECIDED — D-05 delegated: component properties adopted** | Yes | FR-195 |
| OQ-ST-02 | ~~Magic's indirect effect through Energy: accept weight 0.8…~~ **superseded by OQ-ST-06 (v0.3)** | **DECIDED — superseded (D-07)** | — | FR-192 |
| OQ-ST-03 | Keep the name "Magic" in UI, or "Spirit"? | L | User choice | FR-190 |
| OQ-ST-04 | Opposite-spin (left vs right) gameplay effects — MVP or later? | L | Later (secondary evidence only) | FR-204 |
| OQ-ST-05 | Part tier budget values and progression | H | Needs economy decision (still TBD) | FR-196 |
| OQ-BU-01 | Accept hybrid burst model (ADR-014)? | **DECIDED — D-14 delegated: hybrid Lock Integrity** | Yes | FR-221 |
| OQ-BU-02 | Persistent part wear across matches? | H | No (A-13) | — |
| OQ-BU-03 | Can players see opponents' burst-gauge stage? | H | Yes | FR-224 |
| OQ-CB-01 | Accept advantage function S and starting coefficients (ADR-013)? | **DECIDED — D-12 delegated: structure only; values experimental** | Yes, as tuning start | FR-211 |
| OQ-CB-02 | Enable optional type modifiers at launch? | H | No (default off) | FR-214 |
| OQ-CB-03 | Does the MVP arena have an Xtreme zone and dash rail? | H | Dash rail yes, Xtreme zone optional | GDD §8 |
| OQ-CB-04 | Do finish types award different FFA points / rank value? | H | Record only in MVP | FR-223 |
| OQ-CB-05 | Accept CHG-04: OVER (ring-out) and SPIN also eliminate alongside BURST? | **DECIDED — D-09 delegated: BURST signature; OVER, SPIN; XTREME if zone** | Yes | FR-060 |
| OQ-SK-01 | Accept skill limits (cooldown 10 s, 3 uses, opening lockout 3 s)? | H | Yes as tuning start | FR-231 |
| OQ-SK-02 | Skill catalogue (7 skills) for MVP? | H | Review list in skills spec | FR-230 |
| OQ-SK-03 | Mismatched SPIRIT part allowed at 50% potency, or forbidden? | L | 50% | FR-230 |
| OQ-ST-06 | Energy weight of Magic: 1.0 (plain mean, v0.3 recommendation) or 0.8 (v0.2)? | **DECIDED — D-07 delegated: plain mean, provisional until AC-7** | 1.0 (CHG-07) | FR-192 |
| OQ-ST-07 | Headline type rule: A computed only / B TIP decides (official-style) / C TIP headline + computed profile? | **DECIDED — D-08 delegated: TIP tip_type headline + separate profile** | C (CHG-10) | FR-202 |
| OQ-CB-06 | Numeric meaning of "Burst is primary": keep ≥ 40% uniform mix (a), adopt (b) ≥ 30% overall + most frequent in Attack/Balance pairings on telemetry, or (c) add a stronger burst mechanic later? | **DECIDED — D-10 delegated: M-1/M-2 as initial target** | (b) (CHG-09) | NFR-070 |
| OQ-CB-07 | Adopt revised acceptance criteria AC-1…AC-9 as the exit gate of spike S-1? | **DECIDED — D-13 delegated: AC-1…AC-9 exit criteria** | Yes (CHG-12) | ADR-013 |
| OQ-CB-08 | Outcome-level RPS requirement only for Energy gaps g ≤ 0.20; Energy-band matchmaking for ranked play? | H | Yes / yes for ranked | FR-211 |
| OQ-CB-09 | Adopt v0.3.1 coefficient set + recoil as S-1 starting point? | **DECIDED — D-12 delegated: v0.4 values = S-1 starting values** | Yes (CHG-08) | DOC-CMB-001 §4.9 |
| OQ-LN-06 | Launch press cap: median touch rate (CHG-13, provisional 7/s) or 12/s / 10/s / 8/s? | **DECIDED — D-04 delegated: cap 35 (provisional), re-select after S-5** | Median cap; final value after S-5 (D-04) | FR-181, NFR-074 |
| OQ-CB-10 | How to reduce spin-race launch sensitivity (F-11): steering-dependent decay variance, lower k_R, spin floor? | H | Investigate in S-1 | DOC-BAL-001 §9 |
| OQ-LN-08 | **Zero-tap / one-tap inversion** (D-01 + D-03): 0 presses = 20 RPS beats 1 press = 10 RPS (98.6% / 99.6% in the model). Keep (R0), RPS = max(20, 10·n) (R1, recommended), zero = 10 RPS (R2), or zero = 0 RPS → Spin Finish (R3)? Rules unchanged until the owner decides. | **B (owner)** | R1 | FR-065, FR-182 |
| OQ-LN-09 | Accessibility of the linear launch + median cap: players unable to sustain ~7 presses/s lose 81–99% of mirrors at 25 presses. Assisted launch in friendly rooms? Other accommodation? | H (owner) | friendly-room assist (OQ-LN-02) | DOC-LAUNCH-001 §5.3 |
| OQ-CB-12 | D-17 threshold: keep "30 RPS" (fails under linear launch for g ≳ 0.13–0.17) or restate relatively (e.g. 7 presses / r ≥ 0.2, passes in the model)? | **B (owner)** | relative restatement | FR-212, ADR-013 |
| OQ-CB-11 | Meaning of "RPS never completely irrelevant": per-contact only (a), + outcome effect for g ≤ 0.20 (b), or outcome effect for all gaps (c)? | **DECIDED — D-17 delegated: option (b), provisional** | (b) (D-17) | ADR-013 |
| OQ-LN-07 | Zero presses: 20 RPS auto-launch, or 0 RPS = immediate Spin Finish? | **DECIDED — D-03 owner-confirmed: 0 presses = 20 RPS** | 20 RPS | FR-183 |

### 2.2 Accounts & social (OQ-AC)
| ID | Question | Pri | Notes |
|---|---|---|---|
| OQ-AC-01 | Registration methods: e-mail+password, username-only, Google/Apple/Steam sign-in? | ~~**B**~~ **ANSWERED v0.2: e-mail + password; third-party auth postponed** | Apple requires "Sign in with Apple" in some cases when other third-party logins are offered on iOS — verify current App Store guideline before choosing |
| OQ-AC-02 | Password recovery; account deletion policy | H | Recovery needs e-mail provider |
| OQ-AC-03 | Team size limits; can a player be in several teams? | H | |
| OQ-AC-04 | Rank algorithm, seasons, resets, penalties | H | Options in ADR-009 |
| OQ-AC-05 | Exact role names and permissions | H | Proposed matrix in security doc |
| OQ-AC-06 | Tournament formats, registration, brackets, approval workflow | L | |
| OQ-AC-07 | Chat scope (none, room text chat, quick-chat only) | H | Quick-chat/no free text lowers moderation load |
| OQ-AC-08 | External community links and any integration | L | Links only proposed |
| OQ-AC-09 | Minimum age / age rating; parental requirements | H | Legal review |
| OQ-AC-10 | Rank threshold for organizer eligibility | L | |

### 2.3 Platforms & release (OQ-PL)
| ID | Question | Pri |
|---|---|---|
| OQ-PL-01 | Minimum OS versions and device tiers | H |
| OQ-PL-02 | First release platforms / order | ~~**B**~~ **ANSWERED v0.2: Windows, Android, Linux first; macOS, iOS later** |
| OQ-PL-03 | Distribution channels (Steam, itch.io, own site, Google Play, App Store) | H |
| OQ-PL-04 | Localization languages (Arabic RTL UI?) | H |
| OQ-PL-05 | Controller and accessibility requirements | L |
| OQ-PL-06 | Update policy (forced update? grace period?) | H |

### 2.4 Technology & operations (OQ-TO)
| ID | Question | Pri | Recommendation |
|---|---|---|---|
| OQ-TO-01 | Backend language/framework | **DECIDED — D-15 delegated: Laravel 13 + Reverb + MySQL 8.4 + Godot 4.7 headless, conditional on M1** | Alternative (not recommended): TypeScript + Node.js LTS + Fastify (superseded ADR-003) |
| OQ-TO-02 | Godot version | H | 4.7.x stable (ADR-001) |
| OQ-TO-03 | Network transport | H | ENet/UDP (ADR-007) |
| OQ-TO-04 | DB version & migrations | H | MySQL 8.4 LTS, versioned SQL migrations (ADR-004) |
| OQ-TO-05 | Keep MySQL? | H | Yes (ADR-004) |
| OQ-TO-06 | VPS provider, plan, budget | H | Benchmark first (ADR-010) |
| OQ-TO-07 | Domain, TLS, DNS, deployment process | H | |
| OQ-TO-08 | Backup retention, monitoring, operational owner (who is on call?) | H | |
| OQ-TO-09 | Growth expectation beyond 100 CCU; target regions | L | |
| OQ-TO-10 | E-mail provider for verification/recovery | H | Only if e-mail registration |

## 3. Decision log
| Date | ID | Decision | Source |
|---|---|---|---|
| (Brief) | — | Max 5 competitors per match; earlier "10" rejected | User, Brief §D2 |
| (Brief) | — | 100 = approx. peak connected players, planning target | User, Brief §D1 |
| (Brief) | — | No real-money wagering, no voice control in MVP | User, Brief §B3 |
| (Brief) | — | Tournament organizers need admin approval | User, Brief §G5 |
| 2026-11-21 | OQ-GP-16 | 360° analog joystick + Skill button on opposite side | User, Master Update §1–2 |
| 2026-11-21 | OQ-GP-01/02 | 5-second rapid-press launch; 5 presses = 50 RPS reference | User, Master Update §3 |
| 2026-11-21 | — | Primary attributes ATK/DEF/STA/MAG; Energy derived; RPS separate; Stamina ≠ current spin | User, Master Update §4 |
| 2026-11-21 | OQ-GP-15 | Burst Finish is the primary elimination mechanic | User, Master Update §8 |
| 2026-11-21 | — | RPS influence shrinks smoothly with Energy gap, never zero | User, Master Update §7 |
| 2026-11-21 | OQ-GP-12 | Exploration/loot postponed beyond Battle MVP | User, Master Update Part 8 |
| 2026-11-21 | OQ-PL-02 | First platforms Windows, Android, Linux; macOS/iOS later | User, Master Update Part 8 |
| 2026-11-21 | OQ-AC-01 | E-mail + password; unique display names; third-party auth postponed | User, Master Update Part 8 |
| 2026-11-21 | OQ-TO-01 | Backend stack delegated to objective comparison → ADR-012 proposed (Laravel) | User, Master Update Part 7 |
| 2026-11-22 | D-01 | **Owner-confirmed:** RPS = 10 × accepted presses for n ≥ 1, strictly linear | G0 decision register |
| 2026-11-22 | D-02 | **Owner-confirmed:** 1.5 s READY cue, then exactly 5.0 s window | G0 decision register |
| 2026-11-22 | D-03 | **Owner-confirmed:** 0 presses = 20 RPS automatic launch | G0 decision register |
| 2026-11-22 | D-04…D-18 | **Decided under owner delegation** (cap 35 / 350 RPS, FC-1 + ranked gate; component properties; Magic → skills; Energy provisional; TIP headline type; finish set; Burst metrics; same-tick draw; equation structure; AC-1…AC-9; Lock Integrity; conditional stack; 120 s spin ranking; D-17 (b); formula/data corrections) — pending M1 verification | G0 decision register; DOC-CHG-040 |
