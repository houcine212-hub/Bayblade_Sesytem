# ADR-010: Initial deployment & hosting
- **Status:** Proposed — provider/plan TBD (OQ-TO-06) · **Date:** 2026-11-21
## Context
Single Linux VPS candidate (Hostinger KVM). Hostinger documents root/SSH access on VPS, a dashboard firewall that drops traffic by default with configurable TCP/UDP accept rules, and UFW usage for game-server ports [S6, S7, S11].
## Options
| Option | Pros | Cons |
|---|---|---|
| A. **Single KVM VPS**, all services, systemd | Cheapest; simple | SPOF; noisy-neighbour between services |
| B. VPS + managed MySQL | Managed backups | Cost; latency; may not be needed yet |
| C. Containers (Docker Compose) on VPS | Reproducible; same as local dev | Extra layer to learn; UDP port mapping for many match processes |
| D. Kubernetes / Agones | Scales | Far too complex for MVP |
## Decision (proposed)
**A** with systemd units and resource limits (`MemoryMax`, `CPUQuota`/`CPUWeight`) per service; separate OS users per service; MySQL bound to 127.0.0.1; Caddy (or Nginx) TLS reverse proxy; nightly encrypted off-site backups; monitoring agent. Docker Compose used for local dev; may be adopted on the server later.
## Sizing
**Not chosen yet.** Decide after spike S-3 + load tests (OPS-007). Planning formula: `RAM ≈ OS + MySQL buffer + Backend + N_pool × RAM_per_match_process + 30% headroom`; CPU from measured per-match tick cost × 20.
## Firewall (deliberate, OPS-005)
Allow: 443/tcp, match UDP range, 22/tcp from restricted IPs/keys only. Deny all else. Apply in **both** provider firewall and UFW.
## Revisit when
Any growth trigger in architecture §7 is measured.
