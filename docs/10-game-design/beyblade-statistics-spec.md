# Beyblade Statistics & Energy Specification

| Document ID | DOC-STAT-001 | Version | 0.3 | Status | Attributes [C]; formulas/values **[P] proposals** — all numbers are starting values for balancing, not final |
|---|---|---|---|---|---|---|---|

## 1. The six quantities that must never be confused
| Concept | What it is | Changes during battle? | Range / unit | Code / DB identifier | UI label | Status |
|---|---|---|---|---|---|---|
| **Attack** | Primary attribute: impact power | No | 0–100 | `stat_atk` | ATK bar | C |
| **Defense** | Primary attribute: resistance to impact & knockback | No | 0–100 | `stat_def` | DEF bar | C |
| **Stamina (attribute)** | Primary attribute: **how slowly** spin is lost (decay & collision spin-loss resistance) | No | 0–100 | `stat_sta` | STA bar | C |
| **Magic** | Primary attribute: skill charge & potency | No | 0–100 | `stat_mag` | MAG bar | C (role P) |
| **Energy** | **Derived** overall power value from the four attributes. Not an attribute, never stored as an input | No | 0–100 | `energy` (computed; snapshot only) | "Energy" number on build screen | C (derived) / P (formula) |
| **Launch RPS** | Initial rotation produced by the launch mechanic | Set once | 20–150 RPS | `launch_rps` | "Launch: 104 RPS" | C (separate variable) |
| **Spin (current)** | Remaining rotation at this moment — the "endurance left" | **Yes**, decays to 0 | 0–150 RPS | `spin_rps` (transient) | HUD **Spin** meter with RPS number | C (distinction) |
| **Lock Integrity** | Remaining burst resistance this match (burst gauge) | Yes, decreases | 0–100 | `lock_integrity` (transient) | HUD **Burst gauge** (4 stages) | P |
| **Skill Gauge** | Charge toward skill activation | Yes | 0–100 | `skill_gauge` (transient) | Skill button ring | P |

**Rules:** (1) A UI element labelled "Stamina" always means the attribute; the live meter is always "Spin". (2) The database stores attributes per part and snapshots computed attributes + Energy in the match loadout snapshot; transient values (`spin_rps`, `lock_integrity`, `skill_gauge`) exist only in Match Server memory, with final values written to the result summary. (3) "RPS" in this project always means rotations per second; 1 RPS = 60 RPM.

## 2. Where attributes come from (part model) [P]
**Official vs ours:** official Beyblade X tops have exactly three parts — Blade, Ratchet, Bit — and **no numeric attributes** (DOC-RES-001 §2.1). Our four slots and all attributes are original game design; three slots are *inspired by* the official parts, the SPIRIT slot has no official equivalent.

| Slot | Role (inspiration) | Main attribute contributions | Component properties it sets |
|---|---|---|---|
| **RING** | Outer contact layer (Blade / Layer / Fusion Wheel) | ATK, DEF | `mass` (major), `contact_profile` |
| **CORE** | Lock + height (Ratchet / Spin Track) | DEF, STA | `lock_strength` (major), `height` |
| **TIP** | Floor contact (Bit / Driver / Performance Tip) | STA, ATK | `mobility`, `friction`, `lock_strength` (minor) |
| **SPIRIT** | Emblem chip (Burst chip / Bit-Beast idea) | MAG | grants the **skill**, `spin_direction` default |

`stat_x = clamp( Σ_slots part.contrib_x , 0, 100 )`. Parts carry a **tier** (T1–T5, progression rules TBD, OQ-GP-11). A build's total attribute budget is bounded by tier (e.g. Σ attributes ≤ 200 + 20·(avg tier − 1), example only) so no build can max every attribute.

## 3. Component properties (not attributes, not in Energy) [P — CHG-02]
| Property | Range | Effect | Evidence |
|---|---|---|---|
| `mass` | 0.85–1.20 (relative) | Impact (√m), knockback resistance, ring-out resistance | R-14 |
| `lock_strength` | 0.80–1.25 | Burst threshold multiplier | R-09, R-10, R-11 |
| `mobility` | 0.30–1.00 | Steering authority, speed cap, contact rate, spin cost of movement, ring-out risk | R-12, R-14 |
| `friction` | 0.8–1.2 | Natural spin decay multiplier | R-14 (tip) |
| `height` | LOW / MID / HIGH | Upper-attack geometry: lower attacker hitting higher target gets upper factor | R-12 (ratchet height) |
| `contact_profile` | SMASH / UPPER / ABSORB / ROUND | Splits impact into knockback vs burst damage (matrix in combat spec) | SEC (community "smash/upper attack") |
| `spin_direction` | RIGHT / LEFT / DUAL | MVP: cosmetic + data only; opposite-spin effects post-MVP (OQ-ST-04) | R-20 |

## 4. Energy model
### 4.1 Current (confirmed) design
Energy is derived from Attack, Defense, Stamina and Magic [C]. No formula was specified by the user. Neither formula below is approved.

### 4.2 Options evaluated
| Model | Formula | Effect on types | Verdict |
|---|---|---|---|
| **A. Equal arithmetic mean** | **(ATK + DEF + STA + MAG) / 4** | Type-neutral; every attribute point counts the same | **v0.3 recommendation** (see §4.5) |
| B. Weighted arithmetic mean (v0.2 proposal) | (ATK + DEF + STA + 0.8·MAG) / 3.8 | Type-neutral; Magic slightly lighter | v0.2 recommendation — **weight 0.8 had no derivation**; tests in §4.5 do not support it |
| C. Power mean p=0.5 | ((Σ√A_i)/4)² | Rewards even spreads → systematically raises **Balance** Energy, which then wins more clashes (bias) | Rejected |
| D. Geometric mean | (Π A_i)^(1/4) | Strongly punishes a low "dump" stat → kills specialists | Rejected |
| E. Max-weighted | 0.5·max + 0.5·mean | Rewards extreme specialisation → Attack/Stamina extremes dominate | Rejected |

Example (archetype example values, not approved), Model B / Model A: Attack 85/45/40/55 → 56.32 / 56.25 · Defense 40/85/50/50 → 56.58 / 56.25 · Stamina 35/50/88/50 → 56.05 / 55.75 · Balance 57/57/57/55 → 56.58 / 56.50. Model C would give Balance ≈ 56.6 vs Attack ≈ 55.0 — a hidden bias.

### 4.3 What Energy is used for
1. The **advantage function** (combat spec §3): Energy difference decides how much RPS differences matter, and contributes its own advantage term.
2. Displayed "power level" and future matchmaking bands.
Energy is **not** hit points and is not consumed.

### 4.4 Known consequence
Because Energy includes Magic, Magic indirectly affects physical clashes through the advantage function: each Magic point adds `wM/(3 + wM)` Energy (0.21 at wM = 0.8, 0.25 at wM = 1.0), while each physical point adds `1/(3 + wM)` Energy **plus** its direct physical effect.

### 4.5 Review of the Magic weight (v0.3) [MEAS — DOC-BAL-001 §8]
**Why 0.8 was proposed (v0.2):** Magic acts only through skills (bounded ±20%, ≤ 3 uses per match), so it was judged "slightly less valuable" than physical attributes. This was a judgement, not a derivation.

**Test 1 — equal attribute budget (226), Balance 57/57/57/55 vs physical-shift 66/66/66/28** (27 points moved from Magic to physical; N = 4,000, skills not modelled):

| wM | E (shift) | E (base) | g | P(physical-shift wins) |
|---|---|---|---|---|
| 0.0 | 66.00 | 57.00 | +0.146 | 0.915 |
| 0.3 | 62.55 | 56.82 | +0.096 | 0.872 |
| 0.5 | 60.57 | 56.71 | +0.066 | 0.845 |
| 0.6 | 59.67 | 56.67 | +0.052 | 0.832 |
| 0.7 | 58.81 | 56.62 | +0.038 | 0.823 |
| **0.8** | 58.00 | 56.58 | +0.025 | **0.811** |
| **1.0** | 56.50 | 56.50 | 0.000 | **0.789** |

**Test 2 — equal budget (225), Attack 85/45/40/55 vs High-Magic 75/40/35/75:** P(High-Magic wins) = 0.227 (wM 0.0), 0.301 (0.5), 0.315 (0.6), 0.333 (0.8), 0.351 (1.0).

**Interpretation:** at every weight, points in Magic are worth far less in clashes than physical points. A *lower* weight makes Magic investment even worse; the weight is not the main lever. Magic's fairness depends on the **skill system** (not modelled here).

**v0.3 recommendation [P] (CHG-07):** use the **plain mean (wM = 1.0)** — simplest, matches "attributes collectively determine Energy", and is the most Magic-friendly of the tested options. Calibrate skills in spike S-1 until an equal-budget shift between Magic and physical attributes is within 45–55%. If skills cannot reach that, revisit (options: Magic also raises lock strength or gauge-independent passive effects).

## 5. Spin dynamics (battle variable)
- Initial: `spin_rps = launch_rps` (launch spec).
- Natural decay per second: `c_d · (1.25 − STA/100) · friction · (1 + c_move·mobility·|u|)` where `|u|` = joystick magnitude (moving costs spin — the "stamina consumption" of control). v0.3 candidate: `c_d = 0.85`, `c_move = 1.0` (v0.2: 0.55, 0.5).
- Collision spin loss: combat spec §4.4.
- **Wobble:** below 25 RPS stability drops linearly (resistance × 0.45–1.0).
- **Spin Finish:** `spin_rps < 8 RPS` → eliminated (reason SPIN). Official Spin Finish is spin "becomes zero" (O-2); 8 RPS is a game threshold (a top below it is visually stopping).

## 6. Content data
All values in this document live in versioned balance data (`content_version`), not in code (FR-240). Example schema in `../03-data/data-dictionary.md` §7.
