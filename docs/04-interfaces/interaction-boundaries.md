# Interaction Boundaries & Trust

| Document ID | DOC-INT-001 | Status | [P] |
|---|---|---|---|

## 1. Client ↔ Backend
| Client may | Client may not |
|---|---|
| Authenticate, read own/public data, request room/team/report operations | Write results, ranks, inventory directly; choose arbitrary Match Server; see other users' tickets |
| Receive push events over WSS | Connect to MySQL (SEC-001) |
Trust: **untrusted**. Every request is authenticated, authorised and validated server-side.

## 2. Client ↔ Match Server
| Client may | Client may not |
|---|---|
| Connect with its own valid ticket; send launch (and later control) inputs as competitor; receive snapshots | Send positions/velocities/spin; declare eliminations or winners; send input as spectator; reuse tickets |
Trust: **untrusted input source**. Server validates phase, role, rate and value ranges.

## 3. Backend ↔ Match Server
Trusted service-to-service channel on loopback/private network (INT-01/02). Responsibilities:

| Concern | Owner |
|---|---|
| Who may play / spectate (tickets) | Backend issues; Match Server enforces |
| Live match state, eliminations, result | **Match Server (sole authority)** |
| Durable result, history, records, ranks | Backend (after validation) |
| Which instance runs a match | Backend Match Allocator |
| Room state before the match | Backend |

**No duplicated authority:** the Backend never recomputes match outcomes; it only validates consistency (correct instance, participants, placements well-formed).

## 4. Match authorization & result reporting
See `../02-uml/sequence/SQ-03-match-authorization.puml` and `SQ-07-match-completion.puml`.
Ticket design [P]: opaque 256-bit random string; Backend sends only `SHA-256(ticket)` with userId/role/expiry to the Match Server; the client presents the raw ticket. Benefits: no signing keys inside Godot, single-use enforced in Match Server memory, a leaked server memory dump does not reveal usable tickets. Alternative considered: signed JWT verified by Match Server (works without the Backend push, but needs key distribution and replay cache anyway).
