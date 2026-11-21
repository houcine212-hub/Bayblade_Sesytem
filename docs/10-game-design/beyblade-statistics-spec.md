# Beyblade Statistics & Energy Specification

| Document ID | DOC-STAT-001 | Version | 0.2 | Status | Attributes [C]; formulas/values [P] — all numbers are starting values for balancing, not final |
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
Inspired by the official 3-part Beyblade X structure (Blade/Ratchet/Bit, R-12) and the Burst-era chip, with **original names**:

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
Energy is derived from Attack, Defense, Stamina and Magic. No formula was specified.

### 4.2 Options evaluated
| Model | Formula | Effect on types | Verdict |
|---|---|---|---|
| A. Equal arithmetic mean | (ATK+DEF+STA+MAG)/4 | Type-neutral | Good, but Magic weighs as much as physical stats |
| **B. Weighted arithmetic mean** | **(ATK + DEF + STA + 0.8·MAG) / 3.8** | Type-neutral; Magic slightly lighter because it acts only through skills | **Recommended** |
| C. Power mean p=0.5 | ((Σ√A_i)/4)² | Rewards even spreads → systematically raises **Balance** Energy, which then wins more clashes (bias) | Rejected |
| D. Geometric mean | (Π A_i)^(1/4) | Strongly punishes a low "dump" stat → kills specialists | Rejected |
| E. Max-weighted | 0.5·max + 0.5·mean | Rewards extreme specialisation → Attack/Stamina extremes dominate | Rejected |

Example (archetype example values, not approved): Attack 85/45/40/55 → E=56.3 · Defense 40/85/50/50 → 56.6 · Stamina 35/50/88/50 → 56.1 · Balance 57/57/57/55 → 56.6. Model C would give Balance ≈ 56.6 vs Attack ≈ 55.0 — a hidden bias.

### 4.3 What Energy is used for
1. The **advantage function** (combat spec §3): Energy difference decides how much RPS differences matter, and contributes its own advantage term.
2. Displayed "power level" and future matchmaking bands.
Energy is **not** hit points and is not consumed.

### 4.4 Known consequence (needs decision OQ-ST-02)
Because Energy includes Magic, a higher Magic raises Energy and therefore indirectly improves physical clashes (≈ +0.21 Energy per Magic point). Options: (a) accept (weight 0.8 bounds it) — recommended; (b) weight 0.5; (c) exclude Magic from the Energy *term* but keep it in displayed Energy (contradicts "Energy determines" spirit).

## 5. Spin dynamics (battle variable)
- Initial: `spin_rps = launch_rps` (launch spec).
- Natural decay per second: `c_d · (1.25 − STA/100) · friction · (1 + 0.5·mobility·|u|)` where `|u|` = joystick magnitude (moving costs spin — this is the "stamina consumption" of control).
- Collision spin loss: combat spec §4.4.
- **Wobble:** below 25 RPS stability drops linearly (resistance × 0.45–1.0).
- **Spin Finish:** `spin_rps < 8 RPS` → eliminated (reason SPIN).

## 6. Content data
All values in this document live in versioned balance data (`content_version`), not in code (FR-240). Example schema in `../03-data/data-dictionary.md` §7.
