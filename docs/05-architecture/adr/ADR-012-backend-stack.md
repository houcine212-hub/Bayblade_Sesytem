# ADR-012: Backend/API technology stack (supersedes ADR-003)
- **Status:** Proposed — user decision required · **Date:** 2026-11-21

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
| API tokens for Godot clients | **Sanctum** personal access tokens (short-lived) + refresh flow |
| Validation | FormRequest |
| Authorisation (roles, team leader, organizer approval) | Gates & Policies |
| Rate limiting | `RateLimiter` (login, room-code join, reports) |
| Push events (room updates, match allocated) | **Reverb** private channels `private-user.{id}`, `private-room.{id}`; polling fallback |
| Background work | Queue worker (emails, result post-processing, rating updates) |
| Periodic tasks | Scheduler (stale rooms, server reconciliation) |
| Admin & moderation UI | Admin panel package (choice at implementation) |
Release facts (Laravel 13 date, PHP minimum, Reverb event-loop requirements) must be re-verified against laravel.com before acceptance (T-04, T-05).

## 5. Consequence: internal Match Server ↔ Backend channel (CHG-06)
PHP-FPM cannot hold an outgoing control socket per Match Server, so:
- Match Server → `POST /internal/v1/servers/{id}/heartbeat` every **1 s** with state; **response carries pending commands** (`AssignMatch`, `TicketGrant`, `TicketRevoke`, `Drain`) from table `match_server_command` (outbox). Commands are acknowledged in the next heartbeat (at-least-once, idempotent by command id).
- Match Server → `POST /internal/v1/matches/{id}/state` (phase/elimination events) and `/result` (idempotent).
- Registry in MySQL table `match_server_instance` (24 instances × 1 Hz ≈ 24 writes/s — trivial). Redis optional later.
- Cost: + ≤ 1 s to allocation and reconnect ticketing (NFR-009 still ≤ 5 s).

## 6. Real-time Match Server re-confirmed
Godot 4.7.x headless, GDScript, ENet/UDP, one match per process (ADRs 001/002/006/007). Reason: the battle simulation, launch validation and skill rules are shared with the client project; no other option avoids duplicating game rules in two languages.

## 7. Revisit when
Backend p95 > 300 ms at 100 CCU; > ~1,000 concurrent WebSocket connections (Reverb event-loop change, T-04); the team composition changes.
