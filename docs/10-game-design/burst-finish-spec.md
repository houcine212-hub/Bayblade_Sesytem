# Burst Finish & Elimination Specification

| Document ID | DOC-BURST-001 | Version | 0.4 (G0 decisions integrated) | Status | Burst = primary/signature elimination **[C]**; Lock Integrity model **decided under owner delegation (D-14)**; numbers = S-1 experimental values; boundary cases to verify in S-1 |
|---|---|---|---|---|---|---|---|

v0.4 changes (G0 D-09, D-10, D-11, D-14): threshold reference ω_ref = 350 RPS (linear launch scale); D-10 metrics adopted as the initial target; same-tick rule clarified (D-11); measured shares under the v0.4 model. v0.3.1 changes (audit C-03, C-04, H-02, D-04): canonical equation, K_burst/K_guard/θ_up, per-tick cap and start-of-tick gate with proof, metric populations, disconnect not a finish type.

## 1. Official Burst mechanics (verified, DOC-RES-001 §2)
| # | Official fact | Quote / source |
|---|---|---|
| OB-1 | Definition | Burst Finish "occurs when the parts of the opponent's Bey detach and separate before your Bey. (such as the blade, ratchet, or bit)" (O-2) |
| OB-2 | Timing | "The moment a Bey's parts detach and separate." First finish wins. (O-2) |
| OB-3 | Points | Burst 2 (Over 2, Xtreme 3, Spin 1; first to 4) (O-2, O-4) |
| OB-4 | Burst resistance depends on parts | "Dash performance and burst resistance are depending on the type of bit." (O-1) |
| OB-5 | Strong launch protects | Cho-Z "Burst Stopper that activates upon a strong shoot to prevent bursting" (O-3) |
| OB-6 | Character | Burst Finish added "thrilling, unpredictable battles" (O-3) |
| OB-7 | Opposite-spin tactic | "low-speed burst … with the opposite spin" (O-3) |
| OB-8 | Staged gauge in an official game | XONE "Burst Gauge … changes in stages" (O-5) |
| OB-9 | Simultaneous finishes | draw and restart (O-2) |
**Not official:** any numeric threshold, accumulation, cap, durability or probability.

## 2. Proposed model — "Lock Integrity" (original game design) [P]
### 2.1 Options compared
| Option | Official fit | Fairness | Verdict |
|---|---|---|---|
| Single-impact threshold | OB-1 | one-shots feel unfair | partial |
| Cumulative durability | plausible (secondary R-11), OB-8 stages | readable | good |
| Pure probability | OB-6 | hurts competitive fairness | rejected |
| **Hybrid: cumulative + capped per-tick damage + gated critical burst + bounded seeded variance** | OB-1, OB-4, OB-5, OB-6, OB-8 | no one-shots at full lock (proved §2.3) | **recommended** |

### 2.2 Canonical equation (the only normative definition)
For every contact event i → j in tick t (contact event and `N_ij`: DOC-CMB-001 §2.3, §4.1; contacts with `v_n ≤ v_min` cause nothing):
```
θ_up    = clamp( asin( n̂_ij · ŷ ), 0, π/2 )        radians; n̂_ij = contact normal from i to j, ŷ = arena up vector.
                                                     θ_up > 0 only when i strikes j from below; horizontal/downward contacts give 0.
A(θ)    = 1 + 0.5 · sin(θ_up)                       ∈ [1.0, 1.5]
B_ij    = N_ij · Pb(prof_i, prof_j) · A(θ) · K_burst_i
          K_burst_i = product of the attacker's active burst-skill modifiers, clamped to [1.0, 1.3]; 1.0 if none
          (MVP: Upper Edge = 1.2)
T_j     = T0 · lock_strength_j · (1 + β · ω_j(t_start) / ω_ref)          ω_ref = 350 RPS (v0.4; v0.3.1: 150)
d_ij    = c_b · max(0, B_ij − T_j) · (1 + ε_ij) · K_guard_j
          ε_ij ~ U[−0.10, +0.10] from the match RNG (seed stored in game_match.sim_seed)
          K_guard_j = product of the defender's active guard modifiers, clamped to [0.65, 1.0]; 1.0 if none (MVP: Counter Guard = 0.65)
Per tick t, per victim j (contacts summed in ascending pair-id order):
D_j     = min( Σ_i d_ij , D_cap )                   D_cap = 49 lock points
L_j(t)  = L_j(t_start) − D_j
BURST of j at tick t  ⇔  L_j(t) ≤ 0
                       OR ( L_j(t_start) ≤ 50  AND  max_i B_ij ≥ crit · T_j )     crit = 2.5
```
Coefficients (S-1 experimental starting values, D-12/D-14): `T0 = 0.20, β = 2.0, ω_ref = 350 RPS, c_b = 3, D_cap = 49, crit = 2.5`. `lock_strength` comes mainly from CORE and TIP (OB-4). Values in `tools/analysis/configs/v0.4-candidate.json`.

### 2.3 Guarantee: a Bey at full Lock Integrity cannot burst from one contact (FR-221, TC-023)
1. Tick 1, `L_start = 100`: `D_j ≤ 49` ⇒ `L ≥ 51 > 0`; critical gate needs `L_start ≤ 50` ⇒ false. **No burst.**
2. Tick 2: `L_start ≥ 51 > 50` ⇒ critical gate false; `L ≥ 51 − 49 = 2 > 0`. **No burst.**
3. Earliest possible burst: the **third** damaging tick. With the 100 ms pair debounce, a single attacker needs ≥ 3 contact events over ≥ 200 ms; in FFA several attackers can reduce this to 3 consecutive ticks (≈ 33 ms) — accepted as a multi-attacker consequence.
This holds for any `N_ij`, including physics glitches (analysis check: `results/summary.json` → `e6_tc023_single_contact_damage_cap`: impacts N = 10, 10³, 10⁶ all give damage 49.0, L ≥ 51).

### 2.4 Burst gauge UI (inspired by OB-8)
| L | Stage |
|---|---|
| 100–76 | SECURE |
| 75–51 | LOOSENING |
| 50–26 | CRITICAL (critical bursts possible) |
| 25–1 | DANGER |

## 3. Primary vs secondary elimination
### 3.1 Primary — BURST [C]
Signature/featured finish (UI, effects, feed, parts and skills emphasis) — **D-09/D-10: "primary" means the signature designed finish, not the globally most frequent finish.** Measured (v0.4 candidate, uniform 16-cell mix): **BURST 33.8%**, OVER 20.0%, **SPIN 39.9% (most frequent globally)**, TIME_LIMIT 5.7%, draw 0.6%. Seat-averaged Burst share by pair: Attack–Attack 56.0%, Attack–Defense 14.6%, Attack–Stamina 66.6%, Attack–Balance 58.7%, Defense–Defense 0.0%, Defense–Stamina 6.1%, Defense–Balance 0.0%, Stamina–Stamina 57.1%, Stamina–Balance 36.1%, Balance–Balance 63.9%.

**Numeric meaning — D-10 adopted as the initial target (delegated); reconsider after real playtests if BURST lacks prominence:**
| Metric | Population | Numerator / denominator | Target | Model |
|---|---|---|---|---|
| M-1 global share | all eliminations in all completed matches of the evaluation period (telemetry); in the model: the uniform 16-cell 1-v-1 mix | BURST eliminations / all eliminations (draw eliminations counted) | ≥ 30% | 33.8% |
| M-2 featured pairs | eliminations attributed to the pairs **Attack→Attack, Attack→Stamina, Attack→Balance** (either direction) by primary types of the credited eliminator and the eliminated Bey; eliminations without a credited eliminator are excluded | BURST / all attributed eliminations in those pairs | BURST is the most frequent finish in each of the three pairs | 56.0% / 66.6% / 58.7% — each the most frequent |
Not claimed: Burst being most frequent in Attack–Defense (9.6%) or in any Defense pairing.

### 3.2 Secondary eliminations
| Finish | Condition (server) | Official basis | Status | Can it be switched off? |
|---|---|---|---|---|
| **OVER** | fully leaves the arena or settles in an over pocket ≥ 0.5 s | Over Finish (O-2) | **[C]** Brief §E1 | only by changing a confirmed decision |
| **SPIN** | `ω < 8 RPS` | Spin Finish (O-2) | **Decided (D-09)** — supported, structurally required | no (threshold tunable) |
| **XTREME** | over via a dedicated Xtreme zone | Xtreme Finish (O-2) | **Decided (D-09)** — only when the arena defines an Xtreme zone | yes (arena without zone) |

### 3.3 Non-physical outcomes (not finish types)
Disconnect forfeit (OQ-GP-05), no-show, match abort and time-limit ranking (OQ-GP-18) are **outcome reasons**, stored separately from `finish_type` (data dictionary §2b). They never appear as BURST/OVER/SPIN/XTREME.

### 3.4 Same-tick eliminations — D-11 (delegated)
Official rule: draw and restart (OB-9). **Decided for online FFA:** Beys eliminated in the same tick **share a placement**. If the **last remaining** competitors are all eliminated in the same tick, the match is a **draw with no unique winner**: outcome persisted deterministically (`end_reason = ALL_DRAW`, `outcome_reason = DRAW_SHARED`), **no rank-affecting result in MVP**, and **no restart** of the multi-player match.

## 4. Elimination flow (authoritative)
1. Detection in the server tick → `{userId, finishType, tick, creditedTo?}` (credit: opponent who dealt the last lock damage or knockback within 3 s).
2. `S2C_Eliminated` (reliable) to all; burst visual = client presentation of that event.
3. Eliminated peer → SPECTATOR; inputs ignored.
4. ≤ 1 remaining → ENDED; result with finish types and outcome reasons to Backend (SQ-07).
