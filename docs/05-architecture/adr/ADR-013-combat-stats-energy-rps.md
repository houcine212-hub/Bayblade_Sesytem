# ADR-013: Combat statistics, Energy formula and RPS–Energy advantage model
- **Status:** Proposed (revised v0.3.1, 2026-11-21) — **not approved**

## Context
Confirmed: four primary attributes; Energy derived; RPS separate; RPS influence decreases smoothly with the Energy gap and is never completely irrelevant (Master Update §7).

## Definitions
`g = (E_A − E_B)/((E_A + E_B)/2)`, ratio `E_A/E_B = (2+g)/(2−g)`; `r = (ω_A − ω_B)/((ω_A + ω_B)/2)`, ω = current spin; `w(g) = 0.15 + 0.45·exp(−(g/0.25)²)`; `S = (1 − w)·tanh(3g) + w·tanh(2.5r)`. Units and normalisation: DOC-CMB-001 §2 (`N_ij` dimensionless via `v_norm = clamp(v_n/v_ref, 0, 3)`).

## Decision (proposed)
1. Energy = (ATK + DEF + STA + MAG)/4 — **provisional** until skill-inclusive tests (AC-7); alternative 0.8 weight.
2. Advantage function S; RPS enters *impact* only through S; it also acts physically via spin reservoir, stability and burst threshold.
3. v0.3.1 candidate coefficients (DOC-CMB-001 §4.9, `tools/analysis/configs/v0.3.1-candidate.json`) as **spike S-1 starting values only**.
4. Magic acts directly only through skills.

## Meaning of "RPS is never completely irrelevant" — decision D-17 (audit H-03)
| Option | Requirement | Status in the model |
|---|---|---|
| (a) Per-contact only | `w(g) ≥ 0.15` for every contact | holds by construction |
| **(b) Recommended:** per-contact + outcome for comparable builds | (a) and, for `|g| ≤ 0.20`, a 30-RPS launch advantage changes win probability by ≥ 10 points | holds: Attack mirror ≥ 19.2 points, Balance mirror ≥ 31.8 points up to g ≈ 0.18 |
| (c) Outcome for all gaps | a minimum outcome effect at any g | fails (1.7 points at g = 0.261); would need structural change (cap attribute advantage or Energy-band matchmaking for all play) |

## Contradictions and status
| ID | Issue | Status |
|---|---|---|
| C1 | bands were never measured (deterministic v0.2 model) | resolved — stochastic, reproducible model |
| C2 | Burst ≥ 40% vs 14.9% (v0.2 set) | candidate 32.5%; target → D-10 |
| C3 | "Defense beats Attack" claimed | candidate: Defense 85.0% |
| C4 | mislabelled Energy gaps | resolved |
| C5 | ABSORB rebound missing | recoil term added |
| C6 | outcome-level RPS effect can vanish | → D-17 |
| C7 | favoured matchups 85–91% vs "no absolute counter" | open (AC-2) |
| C8 | `N_ij` units; knockback ∝ v² (audit C-02) | resolved (DOC-CMB-001 §2, §4.3) |
| C9 | full-lock guarantee not enforced (audit C-03) | resolved (DOC-BURST-001 §2.3) |
| C10 | not reproducible (audit C-05) | resolved (`tools/analysis/`) |

## Acceptance criteria — exit gate of spike S-1 (CHG-12)
Definitions: 1-v-1 results are **seat-averaged**; equal Energy means |g| ≤ 0.02; launches ~ Normal(35, 8) presses unless stated; ≥ 4,000 duels per cell; S-1 uses real physics and bots, the analytic model only screens.
| # | Criterion | v0.3.1 analytic result |
|---|---|---|
| AC-1 | Each primary type 45–55% average win rate vs the other three types | 56.3 / 52.5 / 51.8 / 39.3 — **fail** |
| AC-2 | Favoured matchups A>S, S>D, D>A each 55–80% ("type advantage" = favoured side's seat-averaged win rate at equal Energy and equal attribute budget) | 89.1 / 91.2 / 85.0 — **fail** |
| AC-3 | Burst metrics per D-10 (proposal: M-1 ≥ 30%; M-2 most frequent in A→A, A→S, A→B) | 32.5%; 54.2 / 69.5 / 59.1% — pass under proposal |
| AC-4 | Cell medians 15–100 s; overall 30–90 s | 8.7–100.3 s — **fail**; overall 53.3 s — pass |
| AC-5 | Draws ≤ 5% per cell | ≤ 4.0% — pass |
| AC-6 | Per D-17 (recommended option b) | pass |
| AC-7 | Equal-budget Magic/physical shift 45–55% with real skills | not measurable (79.4% without skills) |
| AC-8 | **FFA:** in five-competitor bot matches with random type composition, each primary type's win share within ±5 points of its expected share | not measurable in the 1-v-1 model |
| AC-9 | Launch fairness FC-1 (NFR-074) | passes only with the median cap (DOC-LAUNCH-001 §5) |

## Balancing process
Analytic screening (done, reproducible) → S-1 headless physics + bots (1-v-1 and FFA) → playtests with telemetry → one parameter family per iteration with `content_version` bump → AC-1…AC-9.

## Revisit when
AC-1…AC-9 still fail after two S-1 iterations → revisit the equation structure (threshold-gated damage favouring concentrated attack; Balance identity; spin-race launch sensitivity F-11).
