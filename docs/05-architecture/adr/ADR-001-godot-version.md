# ADR-001: Godot engine version
- **Status:** Proposed · **Date:** 2026-11-21
## Context
Godot is confirmed (CON-01); version is open (OQ-TO-02). At the time of writing, the official download archive lists **Godot 4.7.2 (stable, 18 Aug 2026)** as the latest stable release, with 4.8 in beta (beta4, 18 Nov 2026) [source S1, S2]. The official release policy lists 4.7 as supported [S3].
## Options
| Option | Pros | Cons |
|---|---|---|
| A. 4.7.x stable (pinned to a patch) | Current supported stable; maintenance fixes | Will need an upgrade when 4.8 stabilises |
| B. 4.8 beta now | Newest features | Beta: regressions, unsupported for production |
| C. Older 4.x (e.g. 4.6) | Possibly more battle-tested | Shorter remaining support window |
## Decision (proposed)
Use **Godot 4.7.x stable**, pin exact patch for client and server builds (same binary version on both, AP-5). Evaluate 4.8 after its stable release in a branch, never mid-milestone.
## Consequences
Use the "standard" (non-.NET) editor build if ADR-002 is accepted (GDScript).
## Revisit when
4.8 stable is released and its maintenance release exists; a blocking engine bug is found in spikes.
