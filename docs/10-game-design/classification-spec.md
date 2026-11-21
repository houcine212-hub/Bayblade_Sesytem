# Beyblade Classification Specification

| Document ID | DOC-CLS-001 | Version | 0.2 | Status | 4 primary types [research-backed]; hybrid/subtype rules [P] |
|---|---|---|---|---|---|---|---|

## 1. Research findings
- Four official primary types — **Attack, Defense, Stamina, Balance** — used by Takara Tomy and Hasbro (R-01, R-03). Metal-era names Endurance/Combination/Survival were consolidated (R-04).
- Official matchup *tendency*: Attack > Stamina > Defense > Attack; Balance combines the others with no glaring weakness (R-01, R-02). Sources stress it is a tendency affected by launch and stadium.
- Type is a **designed property of products/parts** (R-03), while performance comes from **part combination** (R-12, R-15).
- Community terms (secondary): *smash* vs *upper* attack, *absorb* defense, *spin-equalisation* — useful for subtypes but not official.
- No evidence of an official fifth primary type. Spin direction (right/left/dual) is an official **orthogonal** property (R-20).

## 2. Classification model [P] — "both components and distribution"
1. **Primary type** is computed from the **distribution of physical attributes** (ATK, DEF, STA). Magic is excluded (it is not a physical axis in any source).
   `s_x = stat_x / (ATK+DEF+STA)` for x ∈ {ATK, DEF, STA}; `spread = max(s) − min(s)`.
   - `spread ≤ 0.10` → **BALANCE**
   - else primary = argmax(s)
2. **Secondary type (hybrid):** if second-largest share `s₂ ≥ 0.34` and `s₁ − s₂ ≤ 0.08` → display "ATTACK / STAMINA" etc.
3. **Subtype** from **component properties** (RING `contact_profile`, TIP `mobility`, CORE `lock_strength`) — table §3.
4. Each RING part also has a **designed type** (catalogue label, like official packaging). If the computed type differs, the build screen says "Built as STAMINA (ring designed for ATTACK)". Gameplay uses the **computed** type only.
5. All thresholds are content data (configurable, FR-203). A Bey may legitimately be "unclassified-hybrid" — not every build is forced into a pure type.

Examples: 85/45/40 → shares .49/.26/.24 → ATTACK. 60/30/58 → .41/.20/.39 → ATTACK/STAMINA hybrid. 57/57/57 → spread 0 → BALANCE. 70/70/30 → .41/.41/.18 → ATTACK/DEFENSE hybrid.

## 3. Subtypes [P / SEC-inspired]
| Primary | Subtype | Rule | Identity |
|---|---|---|---|
| ATTACK | **SMASH** | `contact_profile = SMASH` | Knockback → OVER finishes |
| ATTACK | **UPPER** | `contact_profile = UPPER`, height LOW/MID | Lifts opponents → BURST finishes, weaker knockback |
| DEFENSE | **ANCHOR** | `mobility ≤ 0.45`, mass ≥ 1.05 | Knockback/ring-out resistance |
| DEFENSE | **ABSORB** | `contact_profile = ABSORB` | Reduces incoming lock damage, rebounds attackers |
| STAMINA | **ENDURANCE** | `friction ≤ 0.9` | Slowest decay, wins SPIN finishes |
| STAMINA | **EVASIVE** | `mobility 0.5–0.7`, ROUND profile | Avoids contacts, low contact rate |
| BALANCE | **ADAPTIVE** | Balance + any profile | Flexible; skill "Adapt" |
Spin direction is shown as a badge (RIGHT/LEFT/DUAL); MVP gameplay effect: none (OQ-ST-04).

## 4. Classification matrix
| Type | Definition | Strengths | Weaknesses | Preferred strategy | ATK/DEF/STA/MAG relation | RPS relation | vs ATTACK | vs DEFENSE | vs STAMINA | vs BALANCE |
|---|---|---|---|---|---|---|---|---|---|---|
| **ATTACK** | Highest share ATK, high mobility | Fast BURST/OVER finishes, steering, skill gain from hits | Spends spin quickly (mobility cost, low STA); bounces off heavy defenders | Hunt, use Dash skill, finish before spin runs low | ATK high; DEF/STA low–mid; MAG fuels Dash | Needs high launch RPS early; poor launch = spins out vs Defense | Mirror: decided by RPS/Energy/skill timing, ends fast (~10–18 s) | **Unfavoured** (model: Defense by SPIN at 42 s) | **Favoured** (model: Attack by BURST at 30 s) | Slightly favoured at equal budget (model) |
| **DEFENSE** | Highest share DEF, low mobility, heavy | Resists knockback and burst; punishes attackers | Low damage output; out-spun by Stamina | Hold centre, absorb, counter with skill | DEF high; STA mid; ATK low | Moderate RPS sufficient; large RPS deficit vs Attack is fatal | **Favoured** | Mirror: long, often double spin-out → tie rules matter | **Unfavoured** (model: Stamina by SPIN at 84 s) | Favoured at Balance ≤ 57 (model) |
| **STAMINA** | Highest share STA, low friction | Longest spin, wins long matches | Low DEF → bursts under sustained attack | Avoid contact, outlast, Second Wind skill late | STA high; DEF mid; ATK low | Launch RPS strongly matters in mirrors (pure spin race) | **Unfavoured** | **Favoured** | Mirror: launch RPS decides | Depends on Balance's exact values (knife-edge) |
| **BALANCE** | Spread ≤ 0.10 | No hard counter; flexible skill | No hard advantage; outcome very sensitive to exact values | Read opponent, Adapt skill | All ≈ equal | Medium sensitivity | Slightly unfavoured | Slightly unfavoured | Even | Mirror |
Model predictions are from `balancing-simulation-report.md` (equal Energy ≈ 56, equal launch 90 RPS) and **are not proof of balance**.

## 5. Why no type is universally superior (design levers)
1. Triangle emerges from attributes + properties (not hard-coded multipliers).
2. Launch RPS and Energy can overturn type matchups (combat spec §3).
3. Skills are type-linked and bounded.
4. FFA with up to 5 competitors: a counter-type in the room changes the best choice (rock-paper-scissors pressure at room level).
5. Optional bounded type modifier table (±5%) exists in config, **default disabled**; enable only if telemetry shows the triangle failing (ADR-013).
