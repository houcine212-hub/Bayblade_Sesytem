# Beyblade Classification Specification

| Document ID | DOC-CLS-001 | Version | 0.3 | Status | 4 primary types [official, verified]; our classification rules **[P] proposals** |
|---|---|---|---|---|---|---|---|

## 1. Official Beyblade X classification (verified, DOC-RES-001 §2.2)
| Official fact | Quote |
|---|---|
| Four types | "There are 4 types of BEYBLADE X tops: Attack, Stamina, Defense and Balance types" (O-4) |
| **How type is decided** | "*The type of Beyblade is determined by the type of Bit it used." (O-1) |
| Attack | "High attack power — strong against the Stamina types" (O-1) |
| Stamina | "High endurance — strong against the Defense types" (O-1) |
| Defense | "High defense power — strong against the Attack types" (O-1) |
| Balance | "combining multiple types"; "good balance of attack and defense that improves your ability to repel different opponents" (O-1) |
| Nature of matchups | "Each type of Bey has different advantages and disadvantages." (O-1) |
- **Correction (v0.3):** v0.2 described official type as "a designed property of products/parts". The verified official rule is narrower: **the Bit decides the type**.
- Metal-era names Endurance/Combination/Survival were consolidated (R-04, secondary). Official sources give **no numeric attributes** and **no hybrid types**.
- Community terms (secondary): *smash* vs *upper* attack, *absorb* defense, *spin-equalisation* — useful for subtypes but not official.
- No evidence of an official fifth primary type. Spin direction (right/left/dual) is an official **orthogonal** property (R-20).

## 2. Classification model — official-style vs ours
| Option | Rule | Pros | Cons |
|---|---|---|---|
| **A. Distribution-based (v0.2 proposal, original)** | Type from ATK/DEF/STA shares; subtype from part properties | Reflects the actual build; supports hybrids; players see why | Not the official rule; players familiar with Beyblade X may expect the tip to decide |
| B. Official-style (TIP decides) | The TIP part's designed type is the Bey's type; attributes still computed | Faithful to O-1; simple to read | A TIP labelled "Attack" on an otherwise defensive build gives a misleading type; no hybrids |
| C. Combined | Primary type = TIP type; "profile" (hybrid/subtype) from distribution, shown as secondary information | Official feel + transparent stats | Two type notions to explain |
**Recommendation [P] (OQ-ST-07): Option C** — keeps the official convention for the headline type and our computed profile for depth. Option A remains the v0.2 proposal. Gameplay effects never depend on the label (they emerge from attributes and properties), so the choice affects UI, matchmaking display and skill compatibility only.

### 2.1 Distribution rules (used by Option A, and for the profile in Option C) [P] — "both components and distribution"
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

## 4. Classification matrix (official tendency + measured v0.3 candidate)
| Type | Definition | Strengths | Weaknesses | Preferred strategy | ATK/DEF/STA/MAG relation | RPS relation | vs ATTACK | vs DEFENSE | vs STAMINA | vs BALANCE |
|---|---|---|---|---|---|---|---|---|---|---|
| **ATTACK** | Highest share ATK, high mobility | Fast BURST/OVER finishes, steering, skill gain from hits | Spends spin quickly (mobility cost, low STA); bounces off heavy defenders | Hunt, use Dash skill, finish before spin runs low | ATK high; DEF/STA low–mid; MAG fuels Dash | Needs high launch RPS early; poor launch = spins out vs Defense | Mirror: 47.1/47.9%, draw 4.9%, median 7.6 s (too fast — open) | **Unfavoured**: wins 15.7% | **Favoured**: wins 90.2% (BURST 72%) | Favoured: wins 64.4% |
| **DEFENSE** | Highest share DEF, low mobility, heavy | Resists knockback and burst; punishes attackers | Low damage output; out-spun by Stamina | Hold centre, absorb, counter with skill | DEF high; STA mid; ATK low | Moderate RPS sufficient; large RPS deficit vs Attack is fatal | **Favoured**: wins 82.8% | Mirror: 50.1/49.5%, SPIN 100%, median 99 s | **Unfavoured**: wins 9.5% | Favoured: wins 63.2% |
| **STAMINA** | Highest share STA, low friction | Longest spin, wins long matches | Low DEF → bursts under sustained attack | Avoid contact, outlast, Second Wind skill late | STA high; DEF mid; ATK low | Launch RPS strongly matters in mirrors (pure spin race) | **Unfavoured**: wins 9.8% | **Favoured**: wins 90.0% | Mirror: 51.5/48.3%, median 94 s | Even: 50.6% vs 48.6% |
| **BALANCE** | Spread ≤ 0.10 | No hard counter; flexible skill | No hard advantage; outcome very sensitive to exact values | Read opponent, Adapt skill | All ≈ equal | Medium sensitivity | Unfavoured: 32.9% | Unfavoured: 36.7% | Even: 48.6% | Mirror |
**v0.3 measured values** (DOC-BAL-001 §5.2, Monte Carlo N = 4,000, random launches, skill proxy): Defense beats Attack **82.8%** · Attack beats Stamina **90.2%** · Stamina beats Defense **90.0%** · Attack beats Balance 64.4% · Defense beats Balance 63.2% · Stamina–Balance 50.6/48.6%. Overall vs other types: Attack 57.3%, Defense 51.9%, Stamina 50.4%, Balance 39.8%. The cells above now show these measured values (v0.2 deterministic predictions such as "Defense by SPIN at 42 s" were superseded). Favoured matchups are currently stronger than the proposed 55–80% tendency band (C7). Not proof of balance.

## 5. Why no type is universally superior (design levers)
1. Triangle emerges from attributes + properties (not hard-coded multipliers).
2. Launch RPS and Energy can overturn type matchups (combat spec §3).
3. Skills are type-linked and bounded.
4. FFA with up to 5 competitors: a counter-type in the room changes the best choice (rock-paper-scissors pressure at room level).
5. Optional bounded type modifier table (±5%) exists in config, **default disabled**; enable only if telemetry shows the triangle failing (ADR-013).
