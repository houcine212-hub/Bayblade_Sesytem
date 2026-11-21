# Skills & Magic Specification

| Document ID | DOC-SKILL-001 | Version | 0.2 | Status | Skill button & type-linked skills [C]; catalogue, numbers [P] |
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
| Minimum spin | ≥ 20 RPS |
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
| **Second Wind** | STAMINA | instant: spin + 8% of launch RPS (≤ +12 RPS, never above launch RPS) | only when spin < 50% launch |
| **Feather Glide** | STAMINA (EVASIVE) | 3 s: decay −50%, contact rate reduced by evasive push | — |
| **Adapt** | BALANCE | 2.5 s: +15% to the attribute that counters nearest opponent's primary type (vs ATTACK→DEF, vs DEFENSE→STA, vs STAMINA→ATK) | — |
SPIRIT parts may only carry skills compatible with the build's computed primary **or** secondary type; otherwise the skill works at 50% potency ("mismatched spirit") — keeps skills related to classification (FR-230).
