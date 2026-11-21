# ADR-003: Backend language and framework
- **Status:** Proposed — **user decision required (OQ-TO-01)** · **Date:** 2026-11-21
## Criteria
Learnability for the user, hiring pool, MySQL support, WebSocket support, typing, testability, low memory on a small VPS.
## Options
| Option | Pros | Cons |
|---|---|---|
| A. **TypeScript on Node.js LTS + Fastify**, query builder (e.g. Kysely) + SQL migrations | Huge community; one language for API + tooling; good WebSocket support; JSON-schema validation built into Fastify; low memory | Single-threaded (fine at this scale); discipline needed for types |
| B. C# ASP.NET Core + EF Core | Excellent performance & tooling; strong typing | Heavier; steeper for a beginner |
| C. Python FastAPI | Very readable; quick to learn | Async MySQL drivers less mature; slower |
| D. Go | Fast, small binaries, simple deploy | Less "batteries included"; fewer beginner tutorials for game backends |
| E. Backend-as-a-service (e.g. Nakama, PlayFab) | Accounts/social out of the box | Different DB model (Nakama default is PostgreSQL/CockroachDB, not MySQL — verify); vendor lock-in; conflicts with confirmed MySQL |
## Decision (proposed)
**Option A**, a modular monolith (modules per domain, see component diagram) — not microservices.
## Revisit when
User prefers another language; measured Backend CPU > 60% at 100 CCU.
