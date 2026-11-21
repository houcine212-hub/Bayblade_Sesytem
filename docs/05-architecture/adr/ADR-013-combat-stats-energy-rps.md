# ADR-013: Combat statistics, Energy formula and RPS–Energy advantage model
- **Status:** Proposed · **Date:** 2026-11-21
## Context
Confirmed: four primary attributes (ATK, DEF, STA, MAG); Energy derived; RPS separate; RPS influence must decrease smoothly as Energy gap grows, never reaching zero.
## Options
Energy: equal mean / **weighted mean (MAG 0.8)** / power mean / geometric / max-weighted (stats spec §4.2). RPS influence: step thresholds / linear blend / **Gaussian-weighted blend with tanh saturation** / multiplicative ratio model.
## Decision (proposed)
`E = (ATK+DEF+STA+0.8·MAG)/3.8`; `S = (1−w)·tanh(3g) + w·tanh(2.5r)`, `w = 0.15 + 0.45·exp(−(g/0.25)²)`; RPS enters impact only through S. Magic acts on skills only (directly). Component properties separate from attributes. Type modifiers default off.
## Balancing process (how coefficients become final)
1. Analytic duel model (done, report). 2. Spike S-1 headless simulation with real physics + bot launch distributions. 3. Internal playtests with telemetry (win rate per type pair, finish-type shares, match length). 4. Adjust one parameter family at a time; record changes in content_version notes. 5. Acceptance bands: every primary type 45–55% win rate in 1-v-1 equal-Energy samples; no build > 55% overall in FFA; Burst ≥ 40% of finishes.
## Consequences
Coefficients live in content data; changing them needs no code change but must bump `content_version`.
## Revisit when
Telemetry outside acceptance bands after two tuning iterations.
