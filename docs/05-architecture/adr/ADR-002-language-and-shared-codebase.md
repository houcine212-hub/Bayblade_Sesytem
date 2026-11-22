# ADR-002: Client and Match Server language; shared project
- **Status:** Proposed · **Date:** 2026-11-21
## Context
Client and Match Server must apply identical rules and content data (NFR-051). Mobile export is required.
## Options
| Option | Pros | Cons |
|---|---|---|
| A. GDScript, one Godot project, two exports (client, dedicated server) | Simplest toolchain; works on all export targets; beginner friendly; shared code | Slower than C#/C++ for heavy CPU work |
| B. C# (.NET) | Static typing, performance, ecosystem | Mobile/.NET export support has historically lagged GDScript — must verify for 4.7 before considering; larger builds |
| C. Separate server (non-Godot, e.g. Rust/Go simulation) | Max performance, small processes | Rules duplicated in two languages; much higher cost |
## Decision (proposed)
**Option A.** Use static typing in GDScript (typed variables) for maintainability. Keep simulation code isolated so a hot path can later move to GDExtension (C++) if benchmarks require.
## Revisit when
Spike S-3 shows a match process uses too much CPU for 20 concurrent matches on affordable hardware.
