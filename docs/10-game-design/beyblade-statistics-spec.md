# Beyblade Statistics & Energy Specification

| Document ID | DOC-STAT-001 | Version | 0.4.1 | Status | Attributes [C]; component properties (D-05), Magic scope (D-06), Energy formula (D-07, **provisional**) decided under owner delegation; numeric values = S-1 experimental starting values |
|---|---|---|---|---|---|---|---|

## 1. The six quantities that must never be confused
| Concept | What it is | Changes during battle? | Range / unit | Code / DB identifier | UI label | Status |
|---|---|---|---|---|---|---|
| **Attack** | Primary attribute: impact power | No | 0–100 | `stat_atk` | ATK bar | C |
| **Defense** | Primary attribute: resistance to impact & knockback | No | 0–100 | `stat_def` | DEF bar | C |
| **Stamina (attribute)** | Primary attribute: **how slowly** spin is lost (decay & collision spin-loss resistance) | No | 0–100 | `stat_sta` | STA bar | C |
| **Magic** | Primary attribute: skill charge & potency | No | 0–100 | `stat_mag` | MAG bar | C (role P) |
| **Energy** | **Derived** overall power value from the four attributes. Not an attribute, never stored as an input | No | 0–100 | `energy` (computed; snapshot only) | "Energy" number on build screen | C (derived) / P (formula) |
| **Launch RPS** | Initial rotation produced by the launch mechanic | Set once | 20–350 RPS: max(20, 10 × presses) (D-01/D-03 amended by OQ-LN-08; cap D-04) | `launch_rps` | "Launch: 280 RPS" | C (separate variable) |
| **Spin (current)** | Remaining rotation at this moment — the "endurance left" | **Yes**, decays to 0 | 0–350 RPS | `spin_rps` (transient) | HUD **Spin** meter with RPS number | C (distinction) |
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

## 3. Component properties (not attributes, not in Energy) — decided under owner delegation (D-05)
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

### 4.5 Review of the Magic weight [MEAS — `tools/analysis/results/e4_magic_weight.csv`; skills NOT modelled]
**Why 0.8 was proposed in v0.2:** Magic acts only through skills, so it was judged "slightly less valuable". This was a judgement, not a derivation.

**Equal attribute budget tests (N = 4,000, seat order fixed, v0.4 candidate coefficients, linear launch):**

| Magic weight | P(physical-shift 66/66/66/28 beats Balance 57/57/57/55) | P(High-Magic 75/40/35/75 beats Attack 85/45/40/55) |
|---|---|---|
| 0.0 | 83.2% | 28.5% |
| 0.5 | 76.4% | 34.3% |
| **0.8** | 74.2% | 36.8% |
| **1.0** | 72.7% | 38.5% |

**Interpretation (corrected v0.3.1, audit H-04):** in a model *without skills*, Magic points are worth less than physical points at every weight; raising the weight reduces the gap only slightly. These tests **cannot** show that any weight is fair, because Magic's direct value comes from skills that the model does not contain. The v0.3 wording "most Magic-friendly option" is withdrawn.

**Decision D-07 (owner-delegated), provisional:** Energy = plain mean (weight 1.0), the simplest reading of "the four attributes collectively determine Energy". It is **not balance-certified** until the skill-inclusive AC-7 test in S-1 (equal-budget Magic/physical shift within 45–55%). If AC-7 fails: retune with versioned evidence and re-review the formula (options: stronger or more frequent skills, a non-skill Magic effect, or a different weight). The skill-less tests above do **not** prove Magic parity. Magic's Energy contribution is intentional and indirect (D-06).

## 5. Spin dynamics (battle variable)
- Initial: `spin_rps = launch_rps` (launch spec): max(20, 10 × presses), i.e. 20–350 RPS. Spin is an authoritative **scalar gameplay quantity** (DOC-CMB-001 §2.4); displayed RPS = authoritative RPS.
- Natural decay per second: `c_d · (1.25 − STA/100) · friction · (1 + c_move·mobility·|u|)` with `c_d = 1.983 RPS/s` on the 350-RPS scale (v0.4) where `|u|` = joystick magnitude (moving costs spin — the "stamina consumption" of control). (v0.3.1: 0.85; v0.2: 0.55); `c_move = 1.0`.
- Collision spin loss: combat spec §4.4.
- **Wobble:** below ω_wob = 58.33 RPS stability drops linearly (resistance × 0.45–1.0) (v0.4; v0.3.1: 25 RPS).
- **Spin Finish:** `spin_rps < 8 RPS` → eliminated (reason SPIN). Kept at 8 RPS (not scaled), below the 20-RPS launch floor. Official Spin Finish is spin "becomes zero" (O-2); 8 RPS is a game threshold (a top below it is visually stopping).

## 6. Content data
All values in this document live in versioned balance data (`content_version`), not in code (FR-240). Example schema in `../03-data/data-dictionary.md` §7.
