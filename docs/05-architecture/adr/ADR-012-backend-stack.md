# ADR-012: Backend/API technology stack (supersedes ADR-003)
- **Status:** Proposed — user decision required · **Date:** 2026-11-21 · **Reviewed v0.3** (facts verified against laravel.com and docs.godotengine.org/en/4.7)

## 1. Scope of this decision
Two different servers exist and are decided separately:
| Server | Role | Real-time? | Decision |
|---|---|---|---|
| **Backend / API** | Accounts, profiles, inventory/parts, rooms, matchmaking metadata, tickets, results, teams, rankings, moderation, tournaments | No (request/response + push events) | **This ADR** |
| **Match Server** | Authoritative simulation of battles, launch validation, joystick input, skills, bursts | Yes (60 Hz, UDP) | Godot headless (ADR-002, ADR-006, ADR-007) — re-confirmed in §6 |

## 2. Constraints
~100 CCU peak; ≤ 5 competitors per room; MySQL private; client never touches MySQL; server-authoritative combat; one VPS initially; maintainable by a small team that includes a learning developer.

## 3. Options and weighted comparison (score 1–5)
| Criterion (weight) | PHP 8.x + **Laravel 13** + Reverb | TypeScript + Node.js + Fastify | Go (net/http/chi) | C# ASP.NET Core + SignalR | Nakama |
|---|---|---|---|---|---|
| Maintainability by expected team incl. learning curve (20) | 5 — conventions, docs, user already learning it | 2 | 1 | 1 | 1 |
| Built-in security: auth, hashing, validation, rate limiting, policies (15) | 5 — Sanctum, Hash (bcrypt/argon2), FormRequest validation, RateLimiter, Gates/Policies | 3 — assembled from libraries | 3 | 5 | 4 |
| MySQL integration & migrations (10) | 5 — Eloquent/Query Builder, migrations first-class | 3 | 3 | 4 | **0 — no MySQL (T-06)** |
| WebSockets for social/lobby (10) | 4 — Reverb first-party (Pusher protocol; Godot needs a small Pusher-protocol client) | 5 | 4 | 5 | 5 |
| Integration with Godot Match Server (10) | 3 — stateless PHP → heartbeat-pull design (§5) | 5 | 5 | 4 | 3 — Nakama wants to own match logic |
| Performance at 100 CCU (5) | 5 (ample) | 5 | 5 | 5 | 5 |
| Admin/moderation tooling (10) | 5 — Filament/Nova-class admin panels | 3 | 2 | 3 | 4 (console) |
| Hiring pool & community (10) | 5 | 5 | 3 | 4 | 2 |
| Hosting cost/ops on 1 VPS (10) | 4 — PHP-FPM + Reverb + queue worker + scheduler processes | 5 | 5 | 4 | 3 (+DB engine change) |
| **Weighted total (/100)** | **92** | 74 | 62 | 72 | disqualified (MySQL) |
| **Total without the "team" criterion (/80)** | **72** | 66 | 58 | 68 | — |

Sensitivity: Laravel leads even when familiarity is removed, because the backend workload is classic web/API work (auth, CRUD, validation, admin, jobs) where Laravel is strongest, while the hard real-time part lives in Godot.
Also considered and rejected: **Colyseus** (Node real-time framework — would duplicate the battle simulation outside Godot); **Firebase/PlayFab** (vendor lock-in, no MySQL, results authority outside our servers).

## 4. Decision (proposed)
**Backend = PHP 8.x (version required by the chosen Laravel release) + Laravel 13 + MySQL 8.4 LTS**, structured as a modular monolith (Laravel domain modules: Auth, Profile, Inventory, Rooms, Matches, Social, Moderation, Admin).
| Need | Laravel component |
|---|---|
| Email + password accounts, verification, password reset (C) | Built-in auth scaffolding (API-only), `Hash`, notifications via queue |
| API tokens for Godot clients | **Sanctum** personal access tokens with per-token expiry (15 min) + **custom refresh-token endpoint** (Sanctum has no refresh tokens and its tokens never expire by default — T-08) |
| Validation | FormRequest |
| Authorisation (roles, team leader, organizer approval) | Gates & Policies |
| Rate limiting | `RateLimiter` (login, room-code join, reports) |
| Push events (room updates, match allocated) | **Reverb** private channels `private-user.{id}`, `private-room.{id}`; polling fallback. Laravel's official client (Echo) is JavaScript; Godot needs a **custom GDScript Pusher-protocol client** on `WebSocketPeer` (T-10) |
| Background work | Queue worker (emails, result post-processing, rating updates) |
| Periodic tasks | Scheduler (stale rooms, server reconciliation) |
| Admin & moderation UI | Admin panel package (choice at implementation) |
Release facts were verified in v0.3 (§7).

## 5. Consequence: internal Match Server ↔ Backend channel (CHG-06)
PHP-FPM cannot hold an outgoing control socket per Match Server, so:
- Match Server → `POST /internal/v1/servers/{id}/heartbeat` every **1 s** with state; **response carries pending commands** (`AssignMatch`, `TicketGrant`, `TicketRevoke`, `Drain`) from table `match_server_command` (outbox). Commands are acknowledged in the next heartbeat (at-least-once, idempotent by command id).
- Match Server → `POST /internal/v1/matches/{id}/state` (phase/elimination events) and `/result` (idempotent).
- Registry in MySQL table `match_server_instance` (24 instances × 1 Hz ≈ 24 writes/s — trivial). Redis optional later.
- Cost: + ≤ 1 s to allocation and reconnect ticketing (NFR-009 still ≤ 5 s).

## 6. Real-time Match Server re-confirmed
Godot 4.7.x headless, GDScript, ENet/UDP, one match per process (ADRs 001/002/006/007). Reason: the battle simulation, launch validation and skill rules are shared with the client project; no other option avoids duplicating game rules in two languages.

## 7. v0.3 verification review
### 7.1 Verified facts
| Claim in this ADR | Verified fact | Source | Effect |
|---|---|---|---|
| Laravel 13 is current | Released **March 17th, 2026**; bug fixes until **Q3 2027**; security fixes until **March 17th, 2028** | laravel.com/docs/13.x/releases | Plan an upgrade to Laravel 14 (expected ~Q1 2027) within the support window |
| PHP version | **PHP 8.3 – 8.5** (minimum 8.3) | laravel.com/docs/13.x/releases, /deployment | VPS image must provide PHP ≥ 8.3 |
| Reverb limits | ReactPHP loop; `stream_select` ≈ 1,024 open files; > 1,000 connections → `ext-uv`; raise `nofile`; horizontal scaling via **Redis** pub/sub | laravel.com/docs/13.x/reverb | 100 CCU is far below limits; Redis only when scaling out |
| Sanctum | Tokens **never expire by default**; per-token expiry supported; `sanctum:prune-expired` | laravel.com/docs/13.x/sanctum | Refresh flow is custom code (risk TR-03) |
| Scheduler | Sub-minute tasks supported (`everySecond`, `everyTenSeconds`) | laravel.com/docs/13.x/scheduling | Heartbeat-timeout reconciliation every 10 s is feasible |
| Broadcast client | Laravel Echo is a JavaScript library | laravel.com/docs/13.x/broadcasting | Custom Godot client needed (TR-02) |
| Godot HTTP | `HTTPRequest` sends HTTP(S); Android export needs the INTERNET permission | docs.godotengine.org/en/4.7 | Heartbeat-pull from the Match Server is supported |
| Godot WebSocket | `WebSocketPeer` exists | docs.godotengine.org/en/4.7 | Basis for the Pusher-protocol client |
| Godot ENet | `ENetMultiplayerPeer.create_server(port, max_clients…)`; "ENet only uses UDP" | docs.godotengine.org/en/4.7 | UDP ports must be opened (Hostinger firewall + UFW) |
| ENet encryption | `ENetConnection.dtls_server_setup()` / `dtls_client_setup()` exist | docs.godotengine.org/en/4.7 | DTLS option confirmed for spike S-2 |
| Dedicated server | Dedicated-server export and `--headless` documented | docs.godotengine.org/en/4.7 | Match Server build path confirmed |
| Nakama | Requires CockroachDB / PostgreSQL-wire DB | search index (README) | Still disqualified by MySQL constraint |
| Earlier secondary claim | "Reverb database scaling driver in Laravel 13" (v0.2 source T-05) | **not found** in the 13.x Reverb docs, which describe Redis | Removed |

### 7.2 Comparison robustness
Scores are engineering judgement. Sensitivity checks on the §3 table: weighted total (Laravel 92, Node 74, ASP.NET 72, Go 62); without the team criterion (72/80, 66, 68, 58); **equal weights** (mean score: Laravel 4.56, Node 4.00, ASP.NET 3.89, Go 3.44). Laravel leads in all three. It would lose if real-time features were moved into the Backend (Node/ASP.NET score higher there) — they are not: real-time combat stays in Godot.

### 7.3 Remaining technical risks
| ID | Risk | L | I | Mitigation | Spike |
|---|---|---|---|---|---|
| TR-01 | Two languages (PHP Backend, GDScript game) duplicate build/stat formulas (API-23 preview) | M | M | Golden-file contract tests (TC-029); Match Server re-validates snapshots | S-6 |
| TR-02 | No official Godot client for Reverb/Pusher protocol → custom GDScript client (auth via `/broadcasting/auth`, reconnect, ping) | M | M | Polling fallback (2 s); small protocol subset (private channels only) | S-6 |
| TR-03 | Custom refresh-token flow on top of Sanctum | M | H | Rotation + reuse detection, short expiry, security tests | S-6 |
| TR-04 | Heartbeat-pull adds ≤ 1 s to allocation/reconnect; ~24 writes/s to MySQL | L | L | Measure in S-6; Redis registry if needed | S-6 |
| TR-05 | PHP-FPM, Reverb, queue worker, scheduler, MySQL and N Godot processes share one VPS (memory pressure) | M | H | systemd `MemoryMax` per unit; benchmark S-3 decides VPS size | S-3 |
| TR-06 | Godot headless RAM/CPU per match process unknown | M | H | Benchmark 20 concurrent processes | S-3 |
| TR-07 | UDP blocked on some mobile/corporate networks | M | M | Telemetry; WebSocket fallback possible (Godot multiplayer is transport-agnostic) | S-2 |
| TR-08 | Laravel 13 support ends (bug fixes Q3 2027) | H | L | Planned major upgrade in roadmap | — |
| TR-09 | Engine maintenance: Godot 4.7 → 4.8 upgrade during development | M | M | Pin patch version; upgrade between milestones | — |
| TR-10 | Single VPS = single point of failure | M | H | Backups, restore rehearsal (OPS-004) | — |

## 8. Revisit when
Backend p95 > 300 ms at 100 CCU; > ~1,000 concurrent WebSocket connections (Reverb event-loop change, T-04); the team composition changes.
