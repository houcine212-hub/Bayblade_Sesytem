# Design Change Proposals (changes to confirmed decisions)

| Document ID | DOC-CHG-001 | Version 0.3 | **Each item awaits user decision** — nothing here is applied silently; every CHG is a PROPOSAL until approved |
|---|---|---|---|

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
| v0.3 boundaries | 0 presses → 20.00 RPS; max 60 counted presses (half-open window + explicit cap); max 144.42 RPS. Limitations: a macro always reaches the cap (68.6–93.3% win rate vs a 7/s human); zone check is client-side; cap options measured in DOC-LAUNCH-001 §5. |

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
| Evidence | Measured (DOC-STAT-001 §4.5): moving Magic points into physical attributes wins 78.9–91.5% at every weight 0–1.0; lower weights make Magic investment worse. No official source defines Energy or Magic. |
| Advantages | Simplest; every attribute point counts equally toward Energy; most Magic-friendly option tested |
| Disadvantages | Does not by itself make Magic competitive — skills must be tuned (AC-7) |
| Recommendation | Adopt 1.0; keep 0.8 as documented alternative |

## CHG-08 Combat coefficient set v0.3 + recoil term
| Field | Content |
|---|---|
| Existing | v0.2 coefficients (proposal) |
| Proposal | T0 0.20, β 2.0, c_b 3, c_d 0.85, c_move 1.0, **new recoil ρ_rec 0.15** (×2.5 vs ABSORB); Balance example content lock 1.15 / mass 1.08 / mobility 0.75 |
| Evidence | Spec-consistent Monte Carlo: v0.2 set fails every band (Attack 77%, Burst 14.8%, 150 s matches); v0.3 improves all metrics (Attack 57.5%, Burst 35.0%, overall median 50.9 s) but still fails AC-1, AC-2, AC-4, AC-7 (DOC-BAL-001 §5.3) |
| Advantages | Official triangle directions all hold; Defense now counters Attack; recoil implements "ABSORB rebounds attackers" |
| Disadvantages | Not balanced; Attack mirrors 7.6 s; favoured matchups 83–90% |
| Recommendation | Adopt as the **starting point for spike S-1 only**, not as final values |

## CHG-09 What "Burst is primary" must mean numerically
| Field | Content |
|---|---|
| Existing | [C] Burst Finish is the primary elimination mechanic; [P] NFR-070: BURST ≥ 40% of eliminations |
| Conflict | Measured: ≥ 40% in a uniform matchup mix only with Attack matches ending in 2–4 s; with reasonable lengths Burst ≈ 35% and SPIN ≈ 46%. Defense-vs-Defense/Stamina pairings produce 0–3% bursts. |
| Options | **(a)** keep ≥ 40% over a uniform mix → needs further rule changes (none found in 810 tested combinations); **(b)** "primary" = featured finish + **≥ 30% of all eliminations and the most frequent finish in pairings involving an Attack- or Balance-type Bey**, measured on real match telemetry (model: 35.0% overall; 56–72% in those pairings); **(c)** add a stronger burst mechanic (e.g. opposite-spin burst, officially documented — post-MVP) |
| Recommendation | **(b)** for MVP, re-measure in S-1; consider (c) after MVP |

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
| Proposal | AC-1…AC-7 in ADR-013 (adds favoured-matchup band 55–80%, per-pairing duration, draws, outcome-level RPS requirement, Magic equal-budget test) |
| Recommendation | Adopt as the gate for leaving spike S-1 |
