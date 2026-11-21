# Operations: Monitoring, Logs, Alerts, Backup/Restore, Incidents

| Document ID | DOC-OPS-001 | Status | [P] — tools to choose at implementation; lightweight options preferred |
|---|---|---|---|

## 1. Metrics (OPS-001)
| Layer | Metrics |
|---|---|
| Host | CPU, load, RAM, swap, disk %, disk I/O, network in/out (TCP/UDP) |
| Backend (Laravel) | request rate/latency/errors per route, PHP-FPM active/idle workers, queue length & failed jobs, Reverb connections, CCU, rooms open, allocations, 503 count, heartbeat age per instance |
| Match Server | instances IDLE/BUSY, tick time, peers, snapshot bytes/s, kicks by reason, matches/hour, launch flags, skill rejects |
| Balance (telemetry) | finish-type shares, win rate per type pair, launch RPS by device, match length |
| MySQL | connections, slow queries, buffer pool hit rate, replication/binlog size |
| Backups | last success time, size |
Candidate stack [P]: Prometheus node_exporter + app `/metrics` + Grafana, or a hosted free tier; or minimal: Netdata. Decision TBD (OQ-TO-08).

## 2. Logs (OPS-002)
JSON structured logs with `ts, level, service, requestId, userId, matchId, instanceId`. journald → rotation; retention 14–30 days (personal data: IPs). No passwords/tokens in logs.

## 3. Alerts (OPS-003)
| Alert | Condition |
|---|---|
| Service down | backend / mysql / proxy not healthy 1 min |
| Pool exhausted | 0 IDLE match instances for 2 min or any 503 NO_SERVER_AVAILABLE |
| Disk | > 80% |
| Backup | no successful backup in 26 h |
| Error spike | API 5xx > 2% for 5 min |
| Disputed results | any DISPUTED match |
| Cert | TLS expiry < 14 days |

## 4. Deploy (OPS-006)
Versioned release artifacts (backend bundle, server `.pck`/binary, migrations). Steps: backup → migrate (forward-only, backwards-compatible) → deploy backend → start new match pool → drain old pool → verify smoke test. Rollback: previous artifacts; migrations designed expand/contract so old code still works.

## 5. Incident notes
Runbook stubs: Backend down; MySQL down (Backend returns 503; running matches continue and journal results); Match Server crash loop; VPS unreachable (restore from backup to new VPS — practise once before public launch); suspected data breach (rotate secrets, revoke sessions, notify per legal review).
Operational owner / on-call: **TBD (OQ-TO-08)**.
