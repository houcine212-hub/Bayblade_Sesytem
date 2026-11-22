# Design Change Proposals (changes to confirmed decisions)

| Document ID | DOC-CHG-001 | Version 0.4.1 | G0 outcomes recorded below (G0 accepted with changes by the owner, M1 only, 2026-11-22) (owner-confirmed D-01…D-03; delegated D-04…D-18) — technical verification pending M1 |
|---|---|---|---|

## G0 outcome (2026-11-22)
| CHG | Topic | G0 decision | Outcome |
|---|---|---|---|
| CHG-01 | Saturating launch curve | D-01 (owner) | **Rejected** — replaced by linear 10 RPS per press; amended by owner decision OQ-LN-08 to **RPS = max(20, 10 × n)** |
| CHG-02 | Component properties | D-05 (delegated) | Adopted |
| CHG-03 | Magic → skills only | D-06 (delegated) | Adopted (indirect Energy contribution intentional) |
| CHG-04 | Elimination set | D-09 (delegated) | Adopted (XTREME only where the arena defines the zone) |
| CHG-05/06 | Laravel stack, heartbeat-pull | D-15 (delegated) | Adopted **conditionally** on M1 spikes |
| CHG-07 | Energy plain mean | D-07 (delegated) | Adopted **provisionally** until AC-7 |
| CHG-08 | Coefficient set | D-12 (delegated) | Structure adopted; values = S-1 experimental (re-expressed v0.4 for the 350-RPS scale) |
| CHG-09 | Burst metrics | D-10 (delegated) | Adopted as initial target (M-1/M-2) |
| CHG-10 | TIP headline type | D-08 (delegated) | Adopted |
| CHG-11 | Same-tick eliminations | D-11 (delegated) | Adopted with clarification: all-out = draw, no unique winner, no rank effect |
| CHG-12 | AC-1…AC-9 | D-13 (delegated) | Adopted; unmeasured = not passing |
| CHG-13 | Median cap + ranked gate | D-04 (delegated) | Adopted with change: cap 35 → **max 350 RPS** (linear) |
| CHG-14 | Units, burst guarantees | D-18 / D-14 (delegated) | Adopted |
| CHG-15 | Data-model alignment | D-18 (delegated) | Adopted |
Owner questions created by these decisions: OQ-LN-08 (zero/one-tap inversion) — **decided 2026-11-22: `max(20, 10 × n)`**; OQ-CB-12 (D-17 threshold) — **decided: 7-press (70-RPS) difference**; OQ-LN-09 (accessibility) — open. G0 accepted with changes for M1 only (2026-11-22).

Format per Brief rule: existing decision → proposal → evidence → advantages → disadvantages → recommendation.

## CHG-01 Launch: linear "×10" vs saturating curve
| Field | Content |
|---|---|
| Existing (C) | Rapid presses in 5 s; **5 successful presses = 50 RPS** (reference example). Read literally: 10 RPS per press, linear. |
| Proposal | Keep rapid-press and the 5→50 anchor; use a **saturating curve** `RPS(n) = 20 + 130·(1 − e^(−n/19.06))` (min 20, max 150) plus a counted-press rate cap of 12 Hz. |
| Evidence | Official: Takara Tomy's Beylogger/Battlepass record "shoot strength/power and rotation/spin numbers" (O-3, verified); Hasbro launcher gauge (R-19, search index only). "Diminishing returns" is our design interpretation — no source gives a formula. Linear growth has no natural ceiling. |
| Advantages | Linear: 30 presses (6/s, normal human) = 300 RPS, 60 presses = 600 RPS → a 12× spread between players; macro/autoclicker gains are unbounded. Curve: 30 presses → 123 RPS, 60 → 144 RPS: skill still rewarded, extremes compressed, device differences shrink. |
| Disadvantages | Less intuitive than "1 press = 10 RPS"; very fast tappers gain less. |
| Recommendation | Adopt curve (ADR-015). Alternative kept: linear with hard cap at 15 presses (150 RPS) — simpler but flat above 15 presses (no reward for >3 presses/s), which removes most skill expression. |
| v0.3 boundaries (updated v0.3.1) | 0 presses → 20.00 RPS; n_max and max RPS now depend on the cap (CHG-13: median cap, provisional n_max 35 → 129.3 RPS; v0.3 alternative n_max 60 → 144.42 RPS). With the 12/s cap a capped presser beats a 35-press player 68.9% / 93.6% (Attack / Stamina mirror); zone check is client-side. |

## CHG-02 Attributes: keep four, add component properties (not attributes)
| Field | Content |
|---|---|
| Existing (C) | Primary attributes Attack, Defense, Stamina, Magic; Energy derived. |
| Proposal | **Keep the four unchanged.** Add **component properties** that are *not* attributes and *not* in Energy: `mass`, `lock_strength` (burst resistance), `mobility`, `height`, `contact_profile`, `spin_direction`. |
| Evidence | **Verified official:** "Dash performance and burst resistance are depending on the type of bit"; Ratchet determines "balance of the center of gravity"; Blade performance "varies depending on its shape and weight" (O-1); Burst Stopper on strong shoot (O-3). Search-index only: "burst rates vary" (R-09). Secondary: spring/teeth (R-11). In the official system burst resistance is a part property separate from the type label. |
| Advantages | Allows "Defense type with weak lock" or "Attack with strong lock" builds — real strategic variety; avoids overloading DEF with three meanings. |
| Disadvantages | More numbers for players; UI must show them simply (icons/bars). |
| Recommendation | Adopt. Do **not** add a fifth attribute. |

## CHG-03 Magic: scope restricted to the skill system
| Field | Content |
|---|---|
| Existing (C) | Magic is a primary attribute contributing to Energy; influence on abilities to be investigated. |
| Proposal | Magic affects **only** skills directly: gauge charge rate (×0.85–1.15), skill potency (×0.80–1.20), and resistance to opponent skill effects. It never changes base collision physics directly (indirectly through Energy). Energy weight: **see CHG-07 (v0.3: 1.0, was 0.8)**. Name stays "Magic" in UI (alternative "Spirit" offered). |
| Evidence | No official Beyblade attribute named Magic exists (INT). Verified official precedent for a gauge-driven in-battle command: XONE "Active Gauge … increases over time" and "Active Move — A command that uses the Active Gauge to perform an Attack or Counter" (O-5). Search-index only: Hasbro app Avatar attacks (R-18), EVOBATTLE skills (R-17). |
| Advantages | Prevents Magic from being a hidden fourth damage stat; gives a clear identity; bounded influence keeps physics readable. |
| Disadvantages | Players who expect "Magic = damage" must learn its role; weight 0.8 is a judgement. |
| Recommendation | Adopt; weight validated in playtests (ADR-013). |

## CHG-04 Elimination set: Burst primary + ring-out + spin finish
| Field | Content |
|---|---|
| Existing (C) | v0.1: ring-out eliminates (FFA), last top wins. v0.2: **Burst Finish is the primary elimination mechanic.** |
| Conflict | Both are confirmed; the brief does not say whether ring-out still eliminates, or what happens when a top stops spinning. |
| Proposal | **BURST** = primary [C]. Secondary: **OVER** ring-out [C, Brief §E1 — already confirmed, not a new proposal]; **SPIN** spin < 8 RPS [P, structurally required — official Spin Finish]; **XTREME** zone [P, optional, arena-dependent]. v0.2 text "most common by design" is withdrawn: measured Burst share is 34.9% (CHG-09). |
| Evidence | Official finishes verified: Spin, Over, Burst, Xtreme with 1/2/2/3 points (O-2). Without SPIN finish a stopped top would stay "alive" forever (spin is a tracked variable). |
| Advantages | Faithful to established rules; Stamina types win by outlasting (SPIN), Attack by BURST/OVER — supports the type triangle. |
| Disadvantages | "Primary" becomes a tuning target (Burst share of finishes ≥ 40% target, NFR-070), not a guarantee. |
| Recommendation | Adopt; user to confirm whether XTREME zone exists in MVP arena (OQ-CB-03). |

## CHG-05 Supersede ADR-003 (backend stack)
Existing: TypeScript/Node proposed (never approved). Proposal: **PHP 8.x + Laravel 13 + Reverb** for Backend/API; Godot headless remains the real-time Match Server. Full objective comparison in ADR-012 (Laravel leads even when the "familiarity" criterion is removed). Recommendation: adopt ADR-012; ADR-003 → Superseded.

## CHG-06 Internal Backend ↔ Match Server channel
Existing (P): Match Server holds a WebSocket control channel to Backend. Proposal: **heartbeat-pull over HTTP** (1 Hz) carrying commands in the response, because PHP-FPM is stateless. Adds ≤ 1 s to allocation/reconnect. Recommendation: adopt (ADR-012 §5).

## CHG-07 Energy weight of Magic: 0.8 → 1.0 (v0.3)
| Field | Content |
|---|---|
| Existing | v0.2 proposal (never approved): Energy = (ATK + DEF + STA + 0.8·MAG)/3.8 |
| Proposal | Energy = (ATK + DEF + STA + MAG)/4 |
| Evidence | Measured, skills **not** modelled (`tools/analysis/results/e4_magic_weight.csv`): moving Magic points into physical attributes wins 79.4–91.5% at every weight 0–1.0. No official source defines Energy or Magic. These tests cannot establish fairness for Magic (audit H-04). |
| Advantages | Simplest; every attribute point counts equally toward Energy. (v0.3 claim "most Magic-friendly" withdrawn — not supported without skill-inclusive tests.) |
| Disadvantages | Does not by itself make Magic competitive — skills must be tuned (AC-7) |
| Recommendation | Adopt 1.0; keep 0.8 as documented alternative |

## CHG-08 Combat coefficient set v0.3 + recoil term
| Field | Content |
|---|---|
| Existing | v0.2 coefficients (proposal) |
| Proposal | T0 0.20, β 2.0, c_b 3, c_d 0.85, c_move 1.0, **new recoil ρ_rec 0.15** (×2.5 vs ABSORB); Balance example content lock 1.15 / mass 1.08 / mobility 0.75 |
| Evidence | Reproducible model (`tools/analysis/`): v0.2 reference fails every band (Attack 76.4%, Burst 14.9%, cells up to 152 s); v0.3.1 candidate: Attack 56.3%, Burst 32.5%, overall median 53.3 s, but fails AC-1, AC-2, AC-4, AC-7 (AC-8 untested) |
| Advantages | Official triangle directions all hold; Defense now counters Attack; recoil implements "ABSORB rebounds attackers" |
| Disadvantages | Not balanced; Attack mirror median 8.7 s; favoured matchups 85.0–91.2% |
| Recommendation | Adopt as the **starting point for spike S-1 only**, not as final values |

## CHG-09 What "Burst is primary" must mean numerically (population defined in v0.3.1, audit H-02)
| Field | Content |
|---|---|
| Existing | [C] Burst Finish is the primary elimination mechanic; [P] NFR-070: BURST ≥ 40% of eliminations |
| Conflict | Uniform matchup mix: Burst 32.5%, SPIN 48.1%. Burst is rare in every Defense pairing (Attack–Defense 9.6%, Defense–Defense 0.0%, Defense–Stamina 2.0%, Defense–Balance 0.0%). v0.3 wording "most frequent finish in pairings involving an Attack- or Balance-type Bey" was **wrong** (Attack–Defense contradicts it) and is withdrawn. |
| Options | **(a)** keep ≥ 40% over a uniform mix — no tested coefficient set reached it with acceptable match lengths; **(b)** two metrics with defined populations (DOC-BURST-001 §3.1): **M-1** BURST ≥ 30% of *all* eliminations in all completed matches (model 32.5%); **M-2** BURST is the most frequent finish in each of the attributed pairs **Attack→Attack, Attack→Stamina, Attack→Balance** (model 54.2% / 69.5% / 59.1%); eliminations without a credited eliminator count for M-1 only; **(c)** add a stronger burst mechanic later (official opposite-spin "low-speed burst") |
| Recommendation | **(b)** for MVP, measured on telemetry; reconsider (c) post-MVP |

## CHG-10 Classification label: official-style headline type
| Field | Content |
|---|---|
| Existing | v0.2 proposal: type computed from attribute distribution |
| Proposal | Option C: headline type = TIP part's designed type (official rule "type is determined by the Bit", O-1); computed profile (hybrid/subtype) shown as secondary |
| Evidence | Verified official quote (DOC-RES-001 §2.2) |
| Advantages | Familiar to Beyblade X players; still transparent |
| Disadvantages | Two notions of type to explain |
| Recommendation | Adopt C (or keep A) — gameplay is unaffected either way |

## CHG-11 Same-tick eliminations
| Field | Content |
|---|---|
| Existing | Official rule: simultaneous finishes = draw and battle restart (O-2); v0.2 proposal: shared placement |
| Proposal | Online FFA: shared placement, no restart (restarting a 5-player online match is disruptive) |
| Recommendation | Adopt shared placement; record as a deliberate deviation from official rules |

## CHG-12 ADR-013 acceptance criteria rewritten
| Field | Content |
|---|---|
| Existing | v0.2 bands (type 45–55%, Burst ≥ 40%) — never measured |
| Proposal | AC-1…AC-9 in ADR-013 (v0.3.1 adds AC-8 FFA and AC-9 launch fairness) (adds favoured-matchup band 55–80%, per-pairing duration, draws, outcome-level RPS requirement, Magic equal-budget test) |
| Recommendation | Adopt as the gate for leaving spike S-1 |

## CHG-13 Launch fairness: median press cap + ranked gate (v0.3.1, audit C-01)
| Field | Content |
|---|---|
| Existing | v0.3 proposal: 12 presses/s cap (n_max 60, max 144.42 RPS); macro risk accepted as residual |
| Proposal | Counted-press cap = **measured median sustained touch rate** (provisional 7/s → n_max 35 → max 129.3 RPS) + fairness criterion FC-1 (≤ 60%) + **ranked gate** (FR-186) until FC-1 passes with S-5/S-1 data; accuracy layer evaluated in S-5 |
| Evidence | `e5_launch.csv`: capped presser vs median player 68.9% / 93.6% (12/s) → 47.5% / 50.8% (median cap) |
| Advantages | Macro gains nothing over median-or-better players; device gaps narrow; rapid-press concept and 5 → 50 anchor unchanged |
| Disadvantages | Lower skill ceiling (no reward above the median); below-median players still disadvantaged; real median unknown until S-5 |
| Recommendation | Adopt for design; final cap value after S-5 |

## CHG-14 Units, normalisation and burst guarantees (v0.3.1, audit C-02…C-04)
| Field | Content |
|---|---|
| Existing | `N_ij` carried speed units; knockback ∝ v²; mobility factor in the game impact formula; burst equation duplicated and partly undefined; full-lock guarantee only in prose |
| Proposal | `v_norm = clamp(v_n/v_ref, 0, 3)`, `v_ref = 1.0 m/s`, `v_min = 0.05·v_ref`; linear knockback Δv in m/s; mobility factor only as analysis proxy; contact-event definition with 100 ms debounce and per-tick aggregation; one canonical burst equation with `K_burst`, `K_guard`, `θ_up` (radians); per-tick damage cap 49 + start-of-tick critical gate with proof |
| Evidence | DOC-CMB-001 §2, §4.6 worked examples; DOC-BURST-001 §2.3 proof; analysis check up to N = 10⁶ |
| Recommendation | Adopt (structure); values remain S-1 starting points |

## CHG-15 Data model alignment (v0.3.1, audit D-01…D-04, H-05)
| Field | Content |
|---|---|
| Changes | e-mail NOT NULL; no `stats_json` (columns + `properties_json`); `loadout_slot` PK (loadout_id, slot_type); canonical FK `game_match.server_instance_id` (current match derived, `current_match_id` removed); `finish_type` physical only + new `outcome_reason`; `tip_type` only on TIP (replaces generic `designed_type`); match status `LAUNCHING` aligned with state-match |
| Recommendation | Adopt |
