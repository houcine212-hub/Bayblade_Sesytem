# ADR-009: Ranking approach (options only — decision by user, OQ-AC-04)
- **Status:** Open · **Date:** 2026-11-21
## Context
Matches are 2–5 player FFA; Team Battle later. Ranking must resist exploits (win-trading in private rooms, smurfs).
## Options
| Option | Fairness | Exploit resistance | Complexity |
|---|---|---|---|
| A. Record only (W/L, placements), no rating | Transparent | Nothing to exploit | Trivial — **recommended for MVP** |
| B. Points table per placement (e.g. +10/+5/0/−3/−5) | Rewards activity more than skill | Farmable in private rooms | Low |
| C. Elo pairwise over FFA placements | Skill-based | Medium | Medium |
| D. Multiplayer Bayesian rating (TrueSkill-like / OpenSkill / Glicko-2 adaptations) | Best for FFA & teams; uncertainty handles new players | Better | Medium-high |
## Key policy questions
Should **private-code rooms count** for rank (farming risk)? Seasons/resets? Penalties for disconnects? Minimum matches before appearing on leaderboard?
## Proposal
MVP: Option A + leaderboard by wins (labelled "unofficial"). After MVP with matchmaking/ranked queue: Option D, ranked only in system-matched games.
