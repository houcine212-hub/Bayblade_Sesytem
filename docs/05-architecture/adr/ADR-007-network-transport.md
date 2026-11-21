# ADR-007: Network transport
- **Status:** Proposed · **Date:** 2026-11-21
## Options (Godot built-in)
| Option | Notes |
|---|---|
| A. **ENet (UDP)** — `ENetMultiplayerPeer` | Reliable + unreliable channels; low latency; default for Godot high-level multiplayer; requires UDP ports open on host [S4,S5] |
| B. WebSocket (TCP) — `WebSocketMultiplayerPeer` | Works through most firewalls and in browsers; TCP head-of-line blocking hurts real-time snapshots |
| C. WebRTC — `WebRTCMultiplayerPeer` | Needed only for browser real-time; requires signalling + STUN/TURN; overkill without a web client |
## Decision (proposed)
**ENet** for client↔Match Server (no web client, A-08). **HTTPS + WSS** for Backend.
## Consequences
VPS must allow inbound UDP on the match port range (Hostinger: dashboard firewall drops traffic by default; UDP rules must be added, plus UFW on the OS [S6,S7]). Some restrictive networks block UDP (RK-03) — measure in beta; fallback option B is possible because Godot's high-level API is transport-agnostic.
## Revisit when
UDP-blocked connection failures > 2% in beta telemetry, or a web client is requested.
