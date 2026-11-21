# System Architecture

| Document ID | DOC-ARC-001 | Status | **[P] Proposed** — pending Gate G0 approval |
|---|---|---|---|

## 1. Architecture at a glance
```
 Game Client (Godot) ──HTTPS/WSS──▶ Reverse proxy ──▶ Backend API ──SQL──▶ MySQL (localhost)
        │                                                  ▲   │
        └────────── ENet/UDP ──────▶ Match Server(s) ──────┘   │ internal WS + HTTP (loopback)
                                     (headless Godot, 1 match/process)
```
Diagrams: `../02-uml/context.puml`, `component.puml`, `deployment.puml`.

## 2. Architectural principles
| ID | Principle | Basis |
|---|---|---|
| AP-1 | Server authority: the Match Server alone decides match state and results | C (O-7) |
| AP-2 | Single writer to MySQL: only the Backend | C (SEC-001) + P |
| AP-3 | Logical separation now, physical separation later (separate processes, configs, ports, credentials) | C (I5) |
| AP-4 | Data-driven content (items, stats, arenas, launch formula parameters) | C (E3) |
| AP-5 | One Godot project, two export targets (client, headless server) sharing rules code | P (ADR-002) |
| AP-6 | Explicit versioning: protocolVersion, contentVersion, API v1 | P |
| AP-7 | Design only for confirmed scope; extension points for exploration, team battle, tournaments, voice | C (A5) |

## 3. Service responsibility boundaries
| Service | Owns | Does not own |
|---|---|---|
| **Game Client** | UI, input capture, rendering, interpolation, local settings | Any authoritative state |
| **Backend API** | Accounts, sessions, profiles, inventory, loadouts, rooms (pre-match), allocation, tickets, persisted results/history/records, teams, moderation, roles, audit | Live match simulation |
| **Match Server** | Live match: ticket enforcement, peer roles, phases, launch evaluation, simulation, eliminations, spectators, official result | Persistence, account data, deciding who may join (it only enforces tickets) |
| **MySQL** | Durable relational data | Real-time state |

## 4. Key design answers (Brief §M)
| # | Question | Proposed answer | ADR | Needs spike/benchmark |
|---|---|---|---|---|
| 1 | Godot version & export constraints | Godot 4.7.x stable, pinned; Linux headless server export; mobile export constraints per platform | ADR-001, ADR-008 | S-4 mobile render |
| 2 | Transport | ENet/UDP; WebSocket only for Backend events | ADR-007 | S-2 network |
| 3 | Match process model | One match per OS process, pre-warmed pool | ADR-006 | S-3 resource benchmark |
| 4 | Room → server assignment | Backend Match Allocator picks an IDLE registered instance of matching protocolVersion | ADR-006 | — |
| 5 | Match authorization | Single-use hashed tickets pushed to Match Server | DOC-INT-001 §4 | — |
| 6 | Physics authority | Server-only fixed-tick simulation; custom simplified "top model" recommended over generic rigid bodies | ADR-005 | **S-1 physics feel** |
| 7 | State over network | Snapshots 20–30 Hz, interpolation ~100 ms, events reliable | DOC-NET-001 | S-2 |
| 8 | Spectators | Role in ticket; inputs dropped server-side; same/delayed snapshots | DOC-NET-001 §6 | — |
| 9 | Reconnect/failure | Grace period + re-ticketing; heartbeat-based abort; result journal & retry | SQ-08 | S-2 |
| 10 | Shared VPS | Yes initially, with systemd resource limits, localhost-only DB, separate users | ADR-010 | S-3 |
| 11 | Smallest viable deployment | 1 VPS: proxy + backend + N match processes + MySQL + off-site backups | ADR-010 | load tests |
| 12 | Cross-platform limits | See ADR-008 compatibility matrix | ADR-008 | S-4 |
| 13 | Memory vs MySQL | See data dictionary §6 | — | — |
| 14 | Version compatibility | protocolVersion exact match, min client version gate, staged server rollout | ADR-008 §5 | — |

## 5. Local development architecture [P]
- **Backend + MySQL:** Docker Compose (`mysql:8.4` + backend in watch mode) or native install; seeded with content data and test accounts.
- **Match Server:** run the Godot project with `--headless` and a `--server` user argument locally; it registers with the local Backend on `127.0.0.1`.
- **Clients:** run several editor instances (Godot "Run Multiple Instances" debug option) or exported builds against `localhost`.
- **Bots:** a headless "bot client" mode (same project) that joins rooms and sends scripted launch inputs — used for E2E and load tests.
- One `.env.example` per service; real secrets never committed.

## 6. Initial deployment topology
See `../02-uml/deployment.puml` and ADR-010. Public surface: TCP 443 (API/WSS), UDP match range, restricted SSH. Everything else localhost.

## 7. Growth / separation strategy
| Trigger (measured) | Step |
|---|---|
| CPU saturation from matches, or match pool exhausted | Move Match Servers to a second VPS ("match node"); they register with Backend over private network/mTLS. No client change: tickets carry host:port. |
| DB I/O or memory contention | Move MySQL to its own VPS or managed MySQL; Backend connection string change only. |
| Backend CPU | Run 2+ Backend instances behind proxy; move room/allocator state + event fan-out to Redis (introduce only then — ADR revisit). |
| Players in distant regions with high RTT | Regional match nodes; allocator chooses by region; Backend stays central. |
| > single-region scale | Re-evaluate orchestration (e.g. Agones/Kubernetes or a hosted game-server fleet). |

## 8. Extension points (no MVP cost)
- `game_match.room_id` nullable → world challenges (FR-142) create matches without rooms.
- `match_participant.side_id` → Team Battle.
- `inventory_item.source` → chests/rewards.
- `game_match.stake_type` fixed to NONE → stakes only via approved design.
- Input adapter abstraction in client → voice commands later map to the same `C2S_ControlInput` (if confirmed).
- Match mode strategy interface in Match Controller (FFA now; TeamBattle later).
