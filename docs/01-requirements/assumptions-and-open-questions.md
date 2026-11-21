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
| A-06 | One Backend instance at launch | ADR-003, allocator | Load requires horizontal scaling |
| A-07 | GDScript for client and Match Server, same Godot version | ADR-002 | Team prefers C# |
| A-08 | No web-browser client | ADR-007 transport | Web build becomes required |
| A-09 | Players are identified in-game by a unique display name | FR-011 | Name collisions allowed with discriminator |
| A-10 | Spectators do not count against the 5-competitor cap | BR-001 | — (strongly implied by Brief) |

## 2. Open questions
### 2.1 Gameplay (OQ-GP)
| ID | Question | Pri | Options / notes | Related |
|---|---|---|---|---|
| OQ-GP-01 | Meaning of the five-second period: countdown before presses? press window? delay after all enter? | **B** | (a) 5 s press window then release; (b) 3 s countdown + 2 s window; (c) 5 s wait then single-timing press | FR-052, ST-MATCH |
| OQ-GP-02 | Launch input: count presses? rhythm/timing? press limit? formula with top stats? | **B** | Press-count is the most macro/hardware-sensitive; timing-based is fairer across devices | FR-053, SEC-013 |
| OQ-GP-03 | Top stats, part categories, abilities, physics model | H | Proposed data schema in data dictionary | FR-020, FR-025 |
| OQ-GP-04 | Simultaneous ring-out; draw / no winner | H | (a) same tick = shared placement; (b) tie-break by remaining spin; (c) draw | FR-062, FR-067 |
| OQ-GP-05 | Disconnect rules | H | (a) top keeps spinning under simulation; (b) top removed = eliminated after grace | FR-063 |
| OQ-GP-06 | AFK / no launch | H | (a) auto-launch at minimum spin; (b) eliminated before battle | FR-065 |
| OQ-GP-07 | Spectator capacity; mid-match join | H | Proposed default: up to 10 spectators, join allowed any time | FR-037, FR-091 |
| OQ-GP-08 | Room visibility: public list / private code / both | H | Code-only is simplest and safest for MVP | FR-039 |
| OQ-GP-09 | Team Battle rules | L | sizes, assignment, friendly fire, victory | FR-082 |
| OQ-GP-10 | Stakes in MVP or later | L | Recommendation: later (A-03) | FR-083 |
| OQ-GP-11 | Loot, inventory, progression economy | L | No monetisation invented | FR-025 |
| OQ-GP-12 | Exploration in MVP or after | **B** | Recommendation: after (M5) | FR-140 |
| OQ-GP-13 | Host leaves room: transfer host or close room? | H | | FR-038 |
| OQ-GP-14 | Room code lifetime; does room persist after match (rematch)? | H | Proposal: room persists for rematch; expires after 30 min idle | FR-039 |
| OQ-GP-15 | Elimination by spin-out/burst? | **B** | Strongly affects physics model and match length | FR-060 |
| OQ-GP-16 | Any in-battle control after launch? | **B** | Affects prediction, input protocol, UI | FR-061 |
| OQ-GP-17 | Only one competitor left before battle starts | H | (a) cancel match; (b) walkover win (no rank effect) | FR-066 |
| OQ-GP-18 | Match time limit and what happens at time-out | **B** | Needed if no spin-out exists | FR-069 |
| OQ-GP-19 | Does launch aiming (position/angle/direction) exist? | H | | FR-053 |

### 2.2 Accounts & social (OQ-AC)
| ID | Question | Pri | Notes |
|---|---|---|---|
| OQ-AC-01 | Registration methods: e-mail+password, username-only, Google/Apple/Steam sign-in? | **B** | Apple requires "Sign in with Apple" in some cases when other third-party logins are offered on iOS — verify current App Store guideline before choosing |
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
| OQ-PL-02 | First release platforms / order | **B** |
| OQ-PL-03 | Distribution channels (Steam, itch.io, own site, Google Play, App Store) | H |
| OQ-PL-04 | Localization languages (Arabic RTL UI?) | H |
| OQ-PL-05 | Controller and accessibility requirements | L |
| OQ-PL-06 | Update policy (forced update? grace period?) | H |

### 2.4 Technology & operations (OQ-TO)
| ID | Question | Pri | Recommendation |
|---|---|---|---|
| OQ-TO-01 | Backend language/framework | **B** | TypeScript + Node.js LTS + Fastify (ADR-003) |
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
