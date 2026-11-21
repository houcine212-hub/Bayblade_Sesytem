# Secret Management & Backup Guidance

| Document ID | DOC-SEC-004 | Status | [P] |
|---|---|---|---|

## 1. Secrets inventory
| Secret | Used by | Storage |
|---|---|---|
| MySQL app user password | Backend | `/etc/<app>/backend.env` (mode 0600, owner backend user) |
| MySQL migration user | Deploy step only | Not on runtime env |
| JWT signing key | Backend | backend.env; rotate with key ID (`kid`) overlap |
| Match Server service secret(s) | Match Server, Backend | per-instance env file; Backend stores hash |
| TLS private key | Reverse proxy | managed by Caddy/ACME |
| Backup encryption key | Backup job | env file + offline copy held by owner |
| Store signing keys (Android keystore, Apple certs) | Build machine/CI | CI secret store + offline backup — **loss of Android upload key blocks updates** |

Rules: never in git (`.gitignore`, secret scanning), never in client builds, rotate on staff change, least-privilege DB users (runtime user: DML only).

## 2. Backups (OPS-004, NFR-032 provisional)
- Nightly `mysqldump --single-transaction` (or a physical backup tool) → compressed → encrypted → **off-site** object storage; keep 7 daily, 4 weekly, 6 monthly [P].
- Binary logs enabled for point-in-time recovery once player data has value (tighter RPO).
- Also back up: config files, content data version tags, store signing keys (separately, offline).
- **Monthly restore test** into a scratch DB; record duration (validates RTO).
- VPS provider snapshots are a complement, not a replacement (same provider = shared failure domain).
