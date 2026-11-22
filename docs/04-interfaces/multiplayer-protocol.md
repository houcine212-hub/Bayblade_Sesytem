# Multiplayer Protocol & Transport Proposal

| Document ID | DOC-NET-001 | Version 0.4 (protocol version 1; v0.4 widens `spinRps` to u16 for the 350-RPS scale) | **[P] Proposed** — joystick, launch, skills added; values to verify in spike S-2 |
|---|---|---|---|
| Decision | ADR-007 (transport), ADR-005 (simulation), ADR-006 (process model) |

## 1. Transport
- **ENet over UDP** via Godot `ENetMultiplayerPeer` and Godot's high-level multiplayer API (RPCs) [P].
- Match Server listens on one UDP port per process (example range 40001–40032).
- ENet channels [P]: **0** reliable-ordered — control (Hello/Welcome, phases, launch results, eliminations, skill events, results, role changes); **1** unreliable-sequenced — snapshots (S→C) and control inputs (C→S); **2** reliable-ordered — launch press batches and skill activation requests.
- Encryption: ENet traffic is not encrypted by default. Tickets are single-use, so sniffing a ticket after use has no value. Godot supports DTLS for ENet (`ENetConnection.dtls_server_setup` / `dtls_client_setup`) — evaluate in spike S-2 (cost: certificate management) [P].

## 2. Message catalogue (protocol version 1, draft)
| Msg | Dir | Channel | Fields | Notes |
|---|---|---|---|---|
| C2S_Hello | C→S | 0 | ticket, protocolVersion, matchId, clientBuild | First message; must arrive within 5 s of connect or peer is dropped |
| S2C_Welcome | S→C | 0 | role, slot, phase, serverTimeMs, tickRate, arenaId, participants[] | Followed by full snapshot |
| S2C_Kick | S→C | 0 | code (TICKET_INVALID, PROTOCOL_MISMATCH, FLOOD, SERVER_SHUTDOWN) | Then disconnect |
| C2S_Ping / S2C_Pong | both | 0 | clientTimeMs / serverTimeMs | Clock offset & RTT estimate |
| S2C_PhaseChanged | S→C | 0 | phase, startsAtServerTimeMs, durationMs, extra | PRE_LAUNCH, BATTLE, ENDED |
| C2S_LaunchPressBatch | C→S | 2 | seq[], tClientMs[] (presses since last batch) | every 100 ms during LAUNCH_WINDOW; validation in launch spec §6 |
| S2C_LaunchResult | S→C | 0 | [{userId, presses (0–35), launchRps (u16: 10 × presses, or 20 for 0 presses)}] | at RELEASE (FR-185, D-01/D-03) |
| C2S_ControlInput | C→S | 1 | seq, tick, x:int8, y:int8, prev3[] | **Confirmed joystick**; 30 Hz; clamped & rate-limited |
| C2S_SkillActivate | C→S | 2 | seq, tick | Validated server-side (SQ-10) |
| S2C_SkillEvent | S→C | 0 | userId, skillKey, START\|END\|REJECTED, endsAtTick?, reason? | |
| S2C_Snapshot | S→C | 1 | tick, lastProcessedSeq (per receiver), tops[{slot, pos, rot, vel, spinRps(u16, 0.1 RPS units; authoritative value, displayed without rescaling), burstStage(2 bit), skillGauge(u8), state}] | 30 Hz [P] |
| S2C_Eliminated | S→C | 0 | userId, finishType (BURST\|OVER\|XTREME\|SPIN), tick, creditedTo? | BR-015 |
| S2C_RoleChanged | S→C | 0 | role | FR-058 |
| S2C_MatchEnded | S→C | 0 | endReason, placements[] | Provisional until Backend persists |

All RPCs on the Match Server are declared so that only the server may call S2C methods; C2S handlers first check `peerRole[senderId]` (spectator inputs dropped, FR-090).

## 3. Simulation & replication model [P]
- Server: fixed-step simulation at **60 Hz** (provisional), authoritative for positions, spin, collisions, eliminations.
- Clients: **no authoritative physics**. They render an **interpolation buffer** ~100 ms behind the latest snapshot (2–3 snapshots), extrapolating briefly on loss.
- **Client-side prediction for the local top's movement** (joystick confirmed, v0.2): client applies its own inputs immediately, server echoes `lastProcessedSeq`, client re-simulates unacknowledged inputs on each snapshot (SQ-09). Collisions, spin, burst, skills are server-confirmed only.
- Launch presses: client timestamps converted with the measured clock offset and **bounded by arrival time** (no future stamps, no back-dating beyond RTT/2 + 250 ms) — fair for high-latency players, safe against backdating (launch spec §6).

## 4. Bandwidth estimate (example, to be measured)
Per top per snapshot: position 3×f32 (12 B) + quantised rotation (8 B) + velocity 2×f16 (4 B) + spin (2 B, u16) + burst stage/state (1 B) + skill gauge (1 B) + slot (1 B) ≈ 28 B.
5 tops ≈ 145 B + headers ≈ 175 B/snapshot. At 30 Hz ≈ 5.3 KB/s ≈ 42 kbit/s per client (+ overhead). Upstream control input: 30 Hz × ~12 B ≈ 2.9 kbit/s.
20 matches × (5 competitors + 2 spectators) × 42 kbit/s ≈ **5.9 Mbit/s** server egress — well within typical VPS links, but must be measured (NFR-008).
Godot RPC argument encoding (Variant) adds overhead; packing snapshots into a `PackedByteArray` is an optimisation candidate for spike S-2.

## 5. Jitter, loss, latency
- Snapshots unreliable-sequenced (old ones discarded). Interpolation delay adapts between 66–150 ms based on measured jitter [P].
- Reliable channel for events, so eliminations/results are never lost.
- Peer timeout: ENet default timeouts tuned in spike; disconnect handled per SQ-08.

## 6. Spectators
Same snapshot stream; optional delay (e.g. 2 s) to reduce ghosting/collusion value [P]. Spectator peers are never processed by input handlers.

## 7. Flood protection (SEC-014)
Per-peer caps: ControlInput ≤ 60/s, LaunchPressBatch ≤ 15/s, SkillActivate ≤ 5/s, Ping ≤ 2/s; exceeding → drop, then `S2C_Kick{FLOOD}`.

## 8. Version compatibility (Brief §M-14)
`protocolVersion` integer is compiled into both client and server. Backend allocates only instances with the same protocolVersion as the requesting clients (all room members must share it; room join rejects mismatched versions with 426). Match Server rejects mismatches in Hello.
