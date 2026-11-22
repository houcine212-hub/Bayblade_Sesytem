# ADR-006: Match hosting model & allocation
- **Status:** Proposed · **Date:** 2026-11-21
## Options
| Option | Fault isolation | Resource use | Complexity |
|---|---|---|---|
| A. **One match per Godot process, pre-warmed pool** (systemd template units) | High — crash affects one match | Per-process baseline memory × N (measure in S-3) | Low; matches Godot's one-SceneTree model |
| B. Many matches per process (multiple MultiplayerAPI branches / scene instances) | Low — one crash ends all | Lower memory | High; Godot multiplayer branches per subtree add subtle bugs |
| C. Spawn a process on demand per match | High | Minimal idle | Startup latency; orchestration code |
## Decision (proposed)
**A**, with a small warm pool (e.g. 4 idle) and a configured maximum (e.g. 24, sized by S-3). Pool size adjusts by starting/stopping units (NFR-003). Each process registers with the Backend allocator over INT-01, serves one match at a time, then resets to IDLE (or restarts after K matches to bound memory leaks).
## Allocation
Allocator keeps in-memory registry {instanceId, host, udpPort, protocolVersion, state, lastHeartbeat}; picks IDLE + matching protocol; marks BUSY; no instance → 503 + alert.
## Revisit when
Per-process RAM makes the target matches unaffordable → evaluate B or C.
