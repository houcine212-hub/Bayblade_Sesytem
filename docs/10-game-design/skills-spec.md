# Skills & Magic Specification

| Document ID | DOC-SKILL-001 | Version | 0.4 | Status | Skill button & type-linked skills [C]; catalogue, numbers [P] |
|---|---|---|---|---|---|---|---|

## 1. Research basis
**Verified official precedent:** BEYBLADE X XONE (FURYU) — "Active Gauge … increases over time" and "Active Move — A command that uses the Active Gauge to perform an Attack or Counter"; "Xtreme Gauge — increases through attacks and counters" (O-5). X Dash acceleration (O-1). **Search-index only:** Hasbro app Avatar attacks (R-18), EVOBATTLE skills (R-17). Magic itself and every number below are original [P].

## 2. Magic options
| Option | Verdict |
|---|---|
| Magic as extra damage stat | Rejected — duplicates Attack, unreadable |
| Elemental/mana RPG system | Rejected — not Beyblade-like (user rule) |
| **Magic = skill charge & potency + skill resistance (bounded)** | **Recommended** (CHG-03) |
`Pot(MAG) = 0.8 + 0.4·MAG/100` (×0.80–1.20) · `Fill(MAG) = 0.85 + 0.30·MAG/100` (×0.85–1.15) · Resistance in combat spec §4.6.

## 3. Skill gauge [P]
- 0–100, starts at 0. Gains (× Fill(MAG)):
  - passive 1.5/s;
  - per contact: ATTACK-primary +6·N given; DEFENSE-primary +6·N received; STAMINA-primary +2.5/s while spin > 50% of launch; BALANCE +3 per any contact.
- Cost 100 (MVP: one skill per Bey, granted by the SPIRIT part).

## 4. Activation conditions & limits [P]
| Rule | Value |
|---|---|
| Gauge | full (100) |
| Opening lockout | no skill in first 3 s of BATTLE (launch result matters) |
| Cooldown | 10 s after skill ends |
| Minimum spin | ≥ 47 RPS (v0.4, 350-RPS scale; v0.3.1: 20 RPS) |
| Max uses / match | 3 |
| Duration | 0.8–3 s |
| Stacking | same effect never stacks; total self-buff on any quantity ≤ +30% |
| Elimination | **no skill eliminates directly**; burst/over must still come from contact physics |
| Validation | server checks all rules; client effect starts on `S2C_SkillEvent` |

## 5. MVP skill catalogue (examples for review)
| Skill | Compatible types | Effect (× Pot(MAG), opponent effects × (1−ρ·Res)) | Cost/limit |
|---|---|---|---|
| **Rail Dash** | ATTACK | 0.8 s burst of speed along joystick (+60% v_cap); next contact within 1 s: impact +25% | costs 5% current spin |
| **Upper Edge** | ATTACK (UPPER) | 2 s: Pb +20% when hitting from below | — |
| **Iron Stance** | DEFENSE | 2.5 s: knockback received −40%, steering ×0.3 | — |
| **Counter Guard** | DEFENSE (ABSORB) | 2 s: lock damage received −35%, attacker staggered | — |
| **Second Wind** | STAMINA | instant: spin + 8% of launch RPS (≤ +28 RPS on the 350-RPS scale, never above launch RPS) | only when spin < 50% launch |
| **Feather Glide** | STAMINA (EVASIVE) | 3 s: decay −50%, contact rate reduced by evasive push | — |
| **Adapt** | BALANCE | 2.5 s: +15% to the attribute that counters nearest opponent's primary type (vs ATTACK→DEF, vs DEFENSE→STA, vs STAMINA→ATK) | — |
### 5.1 Skill → equation modifier mapping (v0.3.1, audit C-04)
| Skill | Modifier | Value (× Pot(MAG) on the bonus part) | Equation | Cap |
|---|---|---|---|---|
| Rail Dash | `K_atk_i` on the next contact event within 1 s; steering speed cap +60% for 0.8 s | 1 + 0.25·Pot | DOC-CMB-001 §4.1 | K_atk ≤ 1.30 |
| Upper Edge | `K_burst_i` | 1 + 0.20·Pot (only if hitting from below) | DOC-BURST-001 §2.2 | K_burst ∈ [1.0, 1.3] |
| Iron Stance | knockback received Δv × (1 − 0.40·Pot) | — | DOC-CMB-001 §4.3 | ≥ × 0.52 |
| Counter Guard | `K_guard_j` | 1 − 0.35·Pot | DOC-BURST-001 §2.2 | K_guard ∈ [0.65, 1.0] |
| Second Wind | instant Δω = +min(0.08·launch_rps·Pot, 28) | — | DOC-STAT-001 §5 | never above launch_rps |
| Feather Glide | decay × (1 − 0.50·Pot) for 3 s | — | DOC-STAT-001 §5 | ≥ × 0.40 |
| Adapt | `K_def_j` or attribute +15%·Pot as listed in §5 | — | DOC-CMB-001 §4.1 | total self-buff ≤ +30% |
Opponent-directed effects are additionally multiplied by `(1 − 0.3·Res_target)` (DOC-CMB-001 §4.7). With no active skill every modifier is exactly 1.0. **Not yet validated:** no skill is included in the analysis model (DOC-BAL-001 scope).

SPIRIT parts may only carry skills compatible with the build's computed primary **or** secondary type; otherwise the skill works at 50% potency ("mismatched spirit") — keeps skills related to classification (FR-230).
