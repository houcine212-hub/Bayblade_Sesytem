# ADR-005: Server authority & battle simulation model
- **Status:** Proposed — **updated v0.2**: in-battle 360° joystick control is now confirmed · **Date:** 2026-11-21
## Context
Official results must come from a trusted server (O-7). Tops collide, lose spin, and ring out. Mobile clients have variable latency. Physics fidelity is not specified (G-04).
## Options
| Option | Description | Pros | Cons |
|---|---|---|---|
| A. Server-authoritative, **custom simplified top model** (planar motion in bowl + spin decay + collision impulses), fixed tick | Small deterministic-ish code under our control | Tunable "feel"; cheap CPU; data-driven parameters; easy to unit-test | Must design the model; less "realistic" |
| B. Server-authoritative, Godot 3D physics (RigidBody3D) | Engine handles collisions | Fast to start | Spinning bodies are hard to tune; CPU cost × 20 processes; non-determinism makes tests harder |
| C. Client-authoritative / P2P host | No server cost | Violates O-7; cheatable | **Rejected** |
| D. Deterministic lockstep | Low bandwidth | Requires bit-exact determinism across ARM/x86 float — impractical with Godot | Rejected |
## Decision (proposed)
**A** — server simulates at 60 Hz; clients interpolate snapshots; no client prediction unless in-battle control is confirmed. Spike S-1 compares A vs B for feel and CPU before final acceptance.
## v0.2 update (joystick confirmed)
The revisit trigger fired: players steer during battle. Decision becomes: server-authoritative simulation at 60 Hz **plus client-side prediction of the local top's movement** with reconciliation on each snapshot; collisions, spin, burst and skills are confirmed only by the server; remote tops interpolated (~100 ms). Combat rules: ADR-013/014.

## v0.4 note (G0 D-04)
With launches up to 350 RPS, spin is an **authoritative scalar state** (`spin_rps`); the 3D body is not rotated physically at that rate (5.83 rev/tick at 60 Hz) and clients render a capped/blurred visual spin. Prototype in S-1 (DOC-CMB-001 §2.4).

## Revisit when
S-1 shows B is clearly better, or OQ-GP-16 confirms responsive in-battle control (add local prediction + reconciliation).
