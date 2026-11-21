# ADR-011: Room ownership & lobby updates
- **Status:** Proposed · **Date:** 2026-11-21
## Options
| Option | Pros | Cons |
|---|---|---|
| A. **Rooms in Backend (MySQL rows) + WSS push events**; Match Server only after Start | Rooms survive Match Server restarts; no process held by idle rooms; clear boundary (pre-match = Backend, match = Match Server) | Backend needs a WebSocket hub |
| B. Room lives on a Match Server from creation | One connection; simple lobby | Idle rooms consume match processes; pool exhaustion by idle rooms; harder abuse control |
| C. Backend rooms with polling only | Simplest | 2 s lag; more requests |
## Decision (proposed)
**A**, with C as automatic fallback.
## Revisit when
Multiple Backend instances are needed (then add Redis pub/sub for events).
