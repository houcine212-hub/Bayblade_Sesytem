# Backend API Contract (proposed)

| Document ID | DOC-API-001 | Version 0.2 | **[P] Proposed for review** — implemented in Laravel (ADR-012) if approved |
|---|---|---|---|

## 1. Conventions
- Base URL: `https://api.<domain-TBD>/v1`. JSON bodies, UTF-8. TLS only (SEC-005).
- Auth: `Authorization: Bearer <accessToken>` — Laravel Sanctum token, short-lived (15 min [P]); refresh token rotation via `auth_session`.
- Validation: Laravel FormRequest classes; responses use the error format below.
- Every request sends `X-Client-Version` and `X-Platform` (`windows|linux|macos|android|ios`).
- Request correlation: `X-Request-Id` (generated if missing), echoed in responses and logs (OPS-002).
- Validation: schema-validated bodies (unknown fields rejected); all DB access parameterised (SEC-007).
- Pagination: cursor-based `?limit=&cursor=`.
- Idempotency: mutating endpoints that may be retried accept `Idempotency-Key`.
- Rate limits (SEC-008) return `429` with `Retry-After`.

### Error format
```json
{ "error": { "code": "ROOM_FULL", "message": "Room has 5 competitors.", "requestId": "…" } }
```
| HTTP | Typical codes |
|---|---|
| 400 | VALIDATION_FAILED |
| 401 | UNAUTHENTICATED, INVALID_CREDENTIALS, TOKEN_EXPIRED |
| 403 | FORBIDDEN, NOT_HOST, ACCOUNT_SUSPENDED |
| 404 | NOT_FOUND, ROOM_NOT_FOUND |
| 409 | ROOM_FULL, NOT_READY, NOT_ENOUGH_PLAYERS, ALREADY_IN_ROOM, NAME_TAKEN |
| 422 | RESULT_REJECTED, RULE_VIOLATION |
| 426 | CLIENT_UPDATE_REQUIRED |
| 429 | RATE_LIMITED |
| 503 | NO_SERVER_AVAILABLE, MAINTENANCE |

## 2. Public resources
Auth column: G = guest, P = player, L = team leader (of that team), M = moderator, A = admin.

| # | Method & path | Auth | Purpose | Req | Seq |
|---|---|---|---|---|---|
| API-01 | POST /auth/register | G | `{email, password, displayName}` → 201; e-mail verification sent | FR-002, FR-011 | SQ-01 |
| API-01b | GET /auth/email/verify/{id}/{hash} (signed) · POST /auth/email/resend | G/P | Verify e-mail | FR-002 | SQ-01 |
| API-02 | POST /auth/login | G | Obtain tokens; version gate | FR-003, FR-006 | SQ-01 |
| API-03 | POST /auth/refresh | G (refresh token) | Rotate tokens | FR-003 | SQ-01 |
| API-04 | POST /auth/logout | P | Revoke session | FR-003 | — |
| API-05 | POST /auth/password/forgot · POST /auth/password/reset | G | Password reset by e-mail link | FR-004 | SQ-01 |
| API-06 | GET /meta/client-policy | G | Min version, maintenance flag, community links | FR-006, FR-150 | — |
| API-10 | GET /me | P | Own account + profile | FR-010 | — |
| API-11 | PATCH /me/profile | P | Edit display name/avatar | FR-011 | — |
| API-12 | GET /players/{userId} | P | Public profile | FR-012 | — |
| API-13 | POST /me/deletion-request · POST /me/data-export | P | Privacy rights | FR-005 | — |
| API-20 | GET /catalog/parts?slot= | P | Part definitions (contributions, properties, skill) for current content version | FR-020, FR-195 | — |
| API-20b | GET /catalog/skills · GET /catalog/balance-summary | P | Skill catalogue; public summary of formulas (launch curve table, type thresholds) | FR-230, FR-182 | — |
| API-21 | GET /me/inventory | P | Owned items | FR-021 | — |
| API-22 | GET /me/loadouts · PUT /me/loadouts/{id} `{parts:{RING,CORE,TIP,SPIRIT}}` · POST /me/loadouts/{id}/activate | P | Builds (ownership + one part per slot validated) | FR-022 | — |
| API-23 | POST /builds/preview `{parts}` | P | Server-computed attributes, Energy, primary/secondary type, subtype, skill compatibility (same Shared Rules as Match Server) | FR-196, FR-202 | — |
| API-30 | POST /rooms | P | Create room → `{roomId, code}` | FR-030, FR-031 | SQ-02 |
| API-31 | POST /rooms/join | P | Join by `{code, role}` | FR-032, FR-033, FR-037 | SQ-02 |
| API-32 | GET /rooms/{roomId} | P (member) | Room snapshot | FR-035 | SQ-02 |
| API-33 | POST /rooms/{roomId}/ready | P (competitor) | `{ready, loadoutId}` | FR-035, FR-040 | SQ-02 |
| API-34 | POST /rooms/{roomId}/role | P (member) | Switch competitor ↔ spectator (cap enforced) | FR-033, FR-037 | — |
| API-35 | POST /rooms/{roomId}/leave | P (member) | Leave | FR-038 | — |
| API-36 | POST /rooms/{roomId}/start | P (host) | Allocate match, issue tickets | FR-036, FR-050 | SQ-03 |
| API-37 | WSS (Reverb, Pusher protocol) private channels `private-user.{id}`, `private-room.{id}`; auth via `POST /broadcasting/auth` | P | Push events (see §4) | FR-035 | SQ-02/03/07 |
| API-40 | GET /me/active-match | P | For reconnect | FR-064 | SQ-08 |
| API-41 | POST /matches/{matchId}/tickets | P (participant/room member) | New ticket (reconnect / spectator join) | FR-051, FR-064, FR-091 | SQ-06, SQ-08 |
| API-42 | GET /matches/{matchId} | P | Match details/result incl. finish types, launch presses/RPS, build snapshots | FR-100, FR-223 | — |
| API-43 | GET /players/{userId}/matches | P | Match history | FR-101 | — |
| API-44 | GET /leaderboard | P | Ranking list | FR-104 | — |
| API-50 | POST /teams · GET /teams/{id} · PATCH /teams/{id} (L) | P | Team CRUD | FR-110, FR-111 | — |
| API-51 | POST /teams/{id}/invitations (L) · POST /teams/{id}/join-requests (P) | P/L | Invite / request | FR-112 | — |
| API-52 | POST /team-invitations/{id}/accept · /decline | P/L (recipient side) | Respond | FR-112 | — |
| API-53 | POST /teams/{id}/leave · DELETE /teams/{id}/members/{userId} (L) | P/L | Leave / remove | FR-112 | — |
| API-54 | POST /teams/{id}/transfer-leadership · DELETE /teams/{id} (L) | L | Transfer / dissolve | FR-113 | — |
| API-60 | POST /blocks · DELETE /blocks/{userId} · GET /me/blocks | P | Blocking | FR-130 | — |
| API-61 | POST /reports | P | Report `{reportedUserId, reason, details?, matchId?}` | FR-131 | — |
| API-70 | GET /mod/reports · GET /mod/reports/{id} | M | Queue | FR-132 | — |
| API-71 | POST /mod/actions | M | Apply sanction (audited) | FR-132, FR-133 | — |
| API-72 | GET /mod/audit | A | Audit log | SEC-010 | — |
| API-80 | POST /organizer-applications | P | Apply | FR-121 | — |
| API-81 | GET /admin/organizer-applications · POST /admin/organizer-applications/{id}/decision | A | Approve / reject / revoke (audited) | FR-122 | — |
| API-82 | POST /admin/users/{id}/roles · DELETE /admin/users/{id}/roles/{role} | A | Role management (audited) | SEC-003 | — |

### Example: build preview
```http
POST /v1/builds/preview
{ "parts": { "RING": 101, "CORE": 205, "TIP": 310, "SPIRIT": 402 } }
```
`200` → `{ "attributes": {"atk":85,"def":45,"sta":40,"mag":55}, "energy": 56.3, "primaryType": "ATTACK", "secondaryType": null, "subtype": "SMASH", "properties": {"mass":1.0,"lockStrength":0.95,"mobility":1.0}, "skill": {"key":"rail_dash","compatible":true}, "contentVersion": "c-0.2.0" }` (example values)

### Example: join room
```http
POST /v1/rooms/join
Authorization: Bearer …
{ "code": "K7QX2M9A", "role": "COMPETITOR" }
```
`200` → `{ "roomId": 81, "hostUserId": 12, "status": "OPEN", "members": [ { "userId": 12, "role": "COMPETITOR", "ready": false } ], "limits": { "maxCompetitors": 5 } }`

## 3. Internal (Match Server ↔ Backend) — bound to 127.0.0.1 / private network only
| # | Channel | Direction | Messages / purpose | Seq |
|---|---|---|---|---|
| INT-01 | POST /internal/v1/servers/{instanceId}/heartbeat (1 Hz) | MS → B | Body `{udpPort, protocolVersion, buildId, state: IDLE\|BUSY\|DRAINING, matchId?, peers, ackedCommandIds[]}` (first call registers). **Response** `{commands:[{id, type: ASSIGN_MATCH\|TICKET_GRANT\|TICKET_REVOKE\|DRAIN, payload}]}` | SQ-03, SQ-06, SQ-08 |
| INT-01b | POST /internal/v1/matches/{matchId}/state | MS → B | Phase changes, launch summaries, disconnects, eliminations (for live status & reconciliation) | SQ-04, SQ-08 |
| INT-02 | POST /internal/v1/matches/{matchId}/result | MS → B | Official result incl. finish types & telemetry; `Idempotency-Key: matchId` | SQ-07 |
`ASSIGN_MATCH` payload: `{matchId, mode, contentVersion, seed, participants:[{userId, role, slot, buildSnapshot}], ticketHashes:[{sha256, userId, role, exp}]}`.

Service authentication: per-instance credential (random secret provisioned via environment file readable only by the service user), sent as `Authorization: Service <secret>` on every internal request; Backend also checks source address is loopback/private (SEC-012). Upgrade path: mTLS when services move to separate hosts.

## 4. Realtime events (Reverb private channels) [P]
| Event | Payload | Recipients |
|---|---|---|
| room.updated | room snapshot | room members |
| room.closed | roomId, reason | room members |
| match.allocated | matchId, host, udpPort, **own ticket** | each member individually |
| match.completed | matchId | participants + room |
| match.aborted | matchId, reason | participants + room |
| team.invitation | invitationId | recipient |
| account.sanctioned | type, until | target |

Fallback: if WSS is unavailable, clients poll `GET /rooms/{roomId}` every 2 s (P).

## 5. Versioning
URL major version (`/v1`). Additive changes only within v1. Breaking change → `/v2` + client minimum version bump (ADR-008 §update policy).
