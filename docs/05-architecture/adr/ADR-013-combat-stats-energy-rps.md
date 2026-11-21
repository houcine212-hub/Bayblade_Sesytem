# ADR-013: Combat statistics, Energy formula and RPS–Energy advantage model
- **Status:** Proposed (revised v0.3, 2026-11-21) — **not approved**
- **Supersedes:** v0.2 text of this ADR

## Context
Confirmed: four primary attributes (ATK, DEF, STA, MAG); Energy derived from them; RPS a separate battle variable; RPS influence must decrease smoothly as the Energy gap grows and never become completely irrelevant (Master Update §7).

## Definitions
`g = (E_A − E_B)/((E_A + E_B)/2)` (ratio `E_A/E_B = (2+g)/(2−g)`); `r = (ω_A − ω_B)/((ω_A + ω_B)/2)` with ω = **current** spin; `w(g) = 0.15 + 0.45·exp(−(g/0.25)²)`; `S = (1 − w)·tanh(3g) + w·tanh(2.5r)`.

## Decision (proposed)
1. **Energy = (ATK + DEF + STA + MAG) / 4** (plain mean; v0.2 proposed weight 0.8 for Magic — see DOC-STAT-001 §4.5 for why it is dropped). Alternative kept: 0.8 weight.
2. Advantage function S as defined; RPS enters *impact* only through S; RPS also acts physically through spin reservoir, stability and burst threshold (DOC-CMB-001 §3.1).
3. Coefficient set **v0.3 candidate** (DOC-CMB-001 §4.8) as the starting point for spike S-1, including the new recoil term.
4. Magic acts directly only through skills.

## Contradictions in v0.2 and their resolution
| ID | v0.2 statement | Test result [MEAS] | v0.3 resolution |
|---|---|---|---|
| C1 | Acceptance bands are win rates and a burst share | v0.2 used a deterministic model that cannot produce win rates; bands never measured | Monte Carlo analysis; bands measured (DOC-BAL-001 §5.3) |
| C2 | Burst ≥ 40% of finishes | v0.2 coefficients: 14.8% | v0.3 candidate 34.9%; decision CHG-09 |
| C3 | "Defense beats Attack" claimed | v0.2 coefficients in the spec model: Attack wins 55.2%; Attack 77% overall | v0.3 candidate: Defense wins 82.8%; Attack 57.3% overall |
| C4 | "+25% Energy" scenario | actual ratio 1.19–1.22 (g 0.174–0.198) | ratio and g printed everywhere |
| C6 | "RPS never irrelevant" (implied for outcomes) | outcome swing 1.8 points at g = 0.26 (Balance mirror) | requirement split: per-contact w ≥ 0.15 (holds); outcome ≥ 10 points for g ≤ 0.20 (holds: 19.7–62.0 points) |
| C7 | "No type universally superior / no absolute counter" | favoured matchups 83–90% | open balancing item for S-1 |

## Acceptance criteria (revised, measurable) — to be evaluated in spike S-1 with real physics and bots, then in playtests
| # | Criterion | v0.3 analytic result |
|---|---|---|
| AC-1 | Each primary type 45–55% average win rate vs the other three types (equal Energy, equal budget, random launches) | 57.5 / 51.8 / 50.2 / 40.2 — **fail** |
| AC-2 | Favoured matchups (A>S, S>D, D>A) 55–80% | 90.2 / 90.0 / 82.8 — **fail** |
| AC-3 | Burst share — target per CHG-09 decision (≥ 40% uniform mix as written in NFR-070, or the proposed alternative) | 35.0% |
| AC-4 | Per-pairing median duration 15–100 s; overall median 30–90 s | 7.6–99.2 s — **fail**; overall 50.9 s — pass |
| AC-5 | Draws ≤ 5% per pairing | ≤ 4.9% — pass |
| AC-6 | For g ≤ 0.20 a 30-RPS launch swing changes win probability by ≥ 10 points; per-contact w ≥ 0.15 | 19.7–95.9 points; w ≥ 0.15 — pass |
| AC-7 | Equal-budget shift between Magic and physical attributes 45–55% (needs real skills) | 78.9% for physical — **fail / not measurable without skills** |

## Balancing process
Analytic screening (done) → spike S-1 headless physics + bots with random launches and steering policies → internal playtests with telemetry → one parameter family at a time, `content_version` bump per change → criteria AC-1…AC-7.

## Consequences
Coefficients live in content data. The current candidate is a starting point, explicitly **not** balanced.

## Revisit when
AC-1…AC-7 still fail after two S-1 tuning iterations → revisit equation structure (e.g. threshold-gated damage favouring concentrated attack; Balance identity).
