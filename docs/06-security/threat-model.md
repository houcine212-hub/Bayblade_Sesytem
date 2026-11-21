# Threat Model, Trust Boundaries & Match Integrity

| Document ID | DOC-SEC-001 | Status | [P] — STRIDE-based, to be reviewed each milestone |
|---|---|---|---|

## 1. Assets
Accounts & credentials · official match results & records · inventory · roles (admin/mod/organizer) · personal data · service availability · service secrets.

## 2. Trust boundaries
| TB | Boundary | Crossing |
|---|---|---|
| TB-1 | Internet ↔ VPS firewall | HTTPS 443, UDP match range, SSH |
| TB-2 | Client ↔ Backend | untrusted HTTP/WSS requests |
| TB-3 | Client ↔ Match Server | untrusted ENet messages |
| TB-4 | Match Server ↔ Backend | trusted service channel (loopback) |
| TB-5 | Backend ↔ MySQL | localhost, least-privilege DB user |
| TB-6 | Operator ↔ VPS | SSH keys, sudo |

## 3. Threats & mitigations (STRIDE)
| ID | Threat | STRIDE | Mitigation | Req |
|---|---|---|---|---|
| T-01 | Credential stuffing / brute force | S | Rate limits per IP+account, generic errors, Argon2id, optional lockout backoff | SEC-004, SEC-008 |
| T-02 | Stolen refresh token | S | Rotation + reuse detection (revoke family), per-device sessions, logout-all | FR-003 |
| T-03 | Modified client claims victory | T | Results only from Match Server; no client result API | SEC-002, FR-071 |
| T-04 | Modified client sends impossible state | T | Clients send inputs only; server ignores client positions | ADR-005 |
| T-05 | Launch-input macros / autoclickers | T | Server-timed window, per-peer press-rate cap, design favouring timing over raw rate; statistical flags for review | SEC-013 |
| T-06 | Joining arbitrary matches | E | Single-use hashed tickets bound to user+match+role | SEC-006 |
| T-07 | Spectator injects inputs | E | Role check in every C2S handler | FR-090 |
| T-08 | Room-code enumeration / spam joins | I/D | 8-char codes from 31-symbol alphabet (31^8 ≈ 8.5×10^11 combinations), join attempts rate-limited, code invalid after room closes | SEC-011 |
| T-09 | SQL injection | T/I | Parameterised queries only; DB user without DDL rights at runtime | SEC-007 |
| T-10 | UDP flood on match ports | D | Provider DDoS protection (verify plan), per-peer message caps, drop peers without Hello in 5 s, ENet max peers = competitors+spectators+margin | SEC-014 |
| T-11 | API flood | D | Proxy + app rate limits, body size limits | SEC-008 |
| T-12 | Privilege escalation (organizer/admin) | E | Server-side permission checks on every endpoint; roles only via admin API; audited | SEC-003, SEC-010 |
| T-13 | Moderator abuse | R | Immutable audit log; admin review | FR-133 |
| T-14 | MySQL exposed | I | bind 127.0.0.1, firewall, external scan test | SEC-001 |
| T-15 | Secrets leaked in repo/client | I | No secrets in client builds; `.env` outside repo; secret scanning in CI | SEC-009 |
| T-16 | Result report forgery by a non-match process | S | Service credential + loopback check + instance↔match binding | SEC-012 |
| T-17 | Win-trading / collusion in private rooms | T | Do not rate private rooms (ADR-009), anomaly reports | FR-103 |
| T-18 | Ticket sniffing on unencrypted UDP | I | Tickets single-use & 60 s expiry; DTLS evaluated in S-2 | SEC-006 |
| T-19 | Harassment via names/chat | — | Name filter + report + rename action; chat scope minimal (OQ-AC-07) | FR-131 |
| T-20 | Loss of data | D | Off-site backups + restore tests | OPS-004 |

## 4. Anti-cheat stance [P]
Server authority removes most cheats in this design. Client-side anti-tamper is **not** planned for MVP (low value, high cost); integrity comes from server validation and moderation of reports. Revisit if in-battle control is added.
