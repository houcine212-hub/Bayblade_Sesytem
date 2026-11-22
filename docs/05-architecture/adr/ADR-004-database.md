# ADR-004: Database
- **Status:** Proposed (MySQL is the user's planned choice) · **Date:** 2026-11-21
## Context
MySQL is planned (Brief §I4). Workload: low write rate (results, profile changes), modest reads; relational integrity matters.
## Options
MySQL 8.4 LTS · MariaDB · PostgreSQL · managed MySQL.
## Decision (proposed)
**Keep MySQL; use 8.4 LTS** (long-term support line) with InnoDB, utf8mb4, UTC, versioned forward-only SQL migrations in the repo, applied by the deploy pipeline. PostgreSQL offers nothing required that MySQL lacks for this scope, so changing would contradict the user's plan without benefit.
## Consequences
Avoid MySQL reserved words as table names (`game_match`). JSON columns used only for snapshot/unsettled-schema data.
## Revisit when
Need for features MySQL lacks (unlikely at this scale) or managed-service pricing favours another engine.
