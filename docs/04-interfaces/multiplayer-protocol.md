# Multiplayer Protocol & Transport Proposal

| Document ID | DOC-NET-001 | Status | **[P] Proposed** — values are estimates to verify in spike S-2 |
|---|---|---|---|
| Decision | ADR-007 (transport), ADR-005 (simulation), ADR-006 (process model) |

## 1. Transport
- **ENet over UDP** via Godot `ENetMultiplayerPeer` and Godot's high-level multiplayer API (RPCs) [P].
- Match Server listens on one UDP port per process (example range 40001–40032).
- ENet channels [P]: **0** reliable-ordered — control (Hello/Welcome, phase changes, eliminations, results, role changes); **1** unreliable-sequenced — snapshots; **2** reliable — launch inputs (low rate, must not be lost).
- Encryption: ENet traffic is not encrypted by default. Tickets are single-use, so sniffing a ticket after use has no value. Godot supports DTLS for ENet (`ENetConnection.dtls_server_setup` / `dtls_client_setup`) — evaluate in spike S-2 (cost: certificate management) [P].

## 2. Message catalogue (protocol version 1, draft)
| Msg | Dir | Channel | Fields | Notes |
|---|---|---|---|---|
| C2S_Hello | C→S | 0 | ticket, protocolVersion, matchId, clientBuild | First message; must arrive within 5 s of connect or peer is dropped |
| S2C_Welcome | S→C | 0 | role, slot, phase, serverTimeMs, tickRate, arenaId, participants[] | Followed by full snapshot |
| S2C_Kick | S→C | 0 | code (TICKET_INVALID, PROTOCOL_MISMATCH, FLOOD, SERVER_SHUTDOWN) | Then disconnect |
| C2S_Ping / S2C_Pong | both | 0 | clientTimeMs / serverTimeMs | Clock offset & RTT estimate |
| S2C_PhaseChanged | S→C | 0 | phase, startsAtServerTimeMs, durationMs, extra | PRE_LAUNCH, BATTLE, ENDED |
| C2S_LaunchInput | C→S | 2 | seq, kind, clientTimeMs | Semantics TBD (OQ-GP-02); server-timed acceptance |
| C2S_ControlInput | C→S | 1 | seq, payload | **Reserved — only if in-battle control is confirmed (OQ-GP-16)** |
| S2C_Snapshot | S→C | 1 | tick, tops[{slot, pos, rot, linVel?, spinRate, state}] | 20–30 Hz [P] |
| S2C_Eliminated | S→C | 0 | userId, reason, tick | BR-002 |
| S2C_RoleChanged | S→C | 0 | role | FR-058 |
| S2C_MatchEnded | S→C | 0 | endReason, placements[] | Provisional until Backend persists |

All RPCs on the Match Server are declared so that only the server may call S2C methods; C2S handlers first check `peerRole[senderId]` (spectator inputs dropped, FR-090).

## 3. Simulation & replication model [P]
- Server: fixed-step simulation at **60 Hz** (provisional), authoritative for positions, spin, collisions, eliminations.
- Clients: **no authoritative physics**. They render an **interpolation buffer** ~100 ms behind the latest snapshot (2–3 snapshots), extrapolating briefly on loss.
- **No client-side prediction in MVP** if there is no in-battle control (OQ-GP-16): with launch-only input there is nothing to predict except the local button feedback, which is shown immediately (cosmetic). If in-battle control is confirmed, add prediction + reconciliation for the local top only (ADR-005 revisit trigger).
- Launch inputs are time-stamped by the **server on receipt** (server window). Client timestamps are used only for diagnostics, so a modified client cannot backdate presses.

## 4. Bandwidth estimate (example, to be measured)
Per top per snapshot: position 3×f32 (12 B) + quantised rotation (8 B) + spin (2 B) + state/slot (2 B) ≈ 24 B.
5 tops ≈ 120 B + headers ≈ 150 B/snapshot. At 30 Hz ≈ 4.5 KB/s ≈ 36 kbit/s per client (+ UDP/ENet overhead).
20 matches × (5 competitors + 2 spectators) × 36 kbit/s ≈ **5 Mbit/s** server egress — well within typical VPS links, but must be measured (NFR-008).
Godot RPC argument encoding (Variant) adds overhead; packing snapshots into a `PackedByteArray` is an optimisation candidate for spike S-2.

## 5. Jitter, loss, latency
- Snapshots unreliable-sequenced (old ones discarded). Interpolation delay adapts between 66–150 ms based on measured jitter [P].
- Reliable channel for events, so eliminations/results are never lost.
- Peer timeout: ENet default timeouts tuned in spike; disconnect handled per SQ-08.

## 6. Spectators
Same snapshot stream; optional delay (e.g. 2 s) to reduce ghosting/collusion value [P]. Spectator peers are never processed by input handlers.

## 7. Flood protection (SEC-014)
Per-peer caps: max messages/s per type (e.g. LaunchInput ≤ 30/s, Ping ≤ 2/s); exceeding → drop, then `S2C_Kick{FLOOD}`.

## 8. Version compatibility (Brief §M-14)
`protocolVersion` integer is compiled into both client and server. Backend allocates only instances with the same protocolVersion as the requesting clients (all room members must share it; room join rejects mismatched versions with 426). Match Server rejects mismatches in Hello.
