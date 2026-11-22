# Beyblade Classification Specification

| Document ID | DOC-CLS-001 | Version | 0.4 (G0: D-08 decided under owner delegation) | Status | 4 primary types [official, verified]; our classification rules **[P] proposals** |
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
| C. Combined | Headline type = the equipped TIP part's `tip_type`; **computed profile** (primary/secondary/subtype from §2.1) shown as secondary information; the two are stored and displayed separately | Official feel + transparent stats | Two type notions to explain |
**Decision D-08 (owner-delegated): Option C** (headline type from the TIP's `tip_type`; computed profile kept separate for analytics/UI; UNCLASSIFIED and deterministic tie/zero handling preserved). Former recommendation text: **Option C** — keeps the official convention for the headline type and our computed profile for depth. Option A remains the v0.2 proposal. Gameplay effects never depend on the label (they emerge from attributes and properties), so the choice affects UI, matchmaking display and skill compatibility only.

### 2.1 Distribution rules (used by Option A, and for the profile in Option C) [P] — "both components and distribution"
1. **Primary type** is computed from the **distribution of physical attributes** (ATK, DEF, STA). Magic is excluded (it is not a physical axis in any source).
   `P = ATK + DEF + STA`. **Guard (v0.3.1, audit H-05):** if `P < P_min` (proposal `P_min = 30`, includes P = 0) → profile = **UNCLASSIFIED** (no division is performed).
   Otherwise `s_x = stat_x / P` for x ∈ {ATK, DEF, STA}; `spread = max(s) − min(s)`.
   - `spread ≤ 0.10` → **BALANCE**
   - else primary = argmax(s); exact ties broken in the fixed order ATTACK, DEFENSE, STAMINA (deterministic)
2. **Secondary type (hybrid):** if second-largest share `s₂ ≥ 0.34` and `s₁ − s₂ ≤ 0.08` → display "ATTACK / STAMINA" etc.
3. **Subtype** from **component properties** (RING `contact_profile`, TIP `mobility`, CORE `lock_strength`) — table §3.
4. **Single source for the headline type (v0.3.1, audit H-05):** only TIP parts carry a type label, stored in `item_definition.tip_type` (NULL for every other slot; enforced by a CHECK constraint). RING parts carry **no** designed type (the v0.3 statement that RING parts have a designed type is withdrawn). If the computed profile differs from the TIP label, the build screen shows both, e.g. "Type: ATTACK (tip) · Profile: STAMINA". Gameplay never uses either label — effects come from attributes and properties.
5. All thresholds are content data (configurable, FR-203). A Bey may legitimately be "unclassified-hybrid" — not every build is forced into a pure type.

Examples: 85/45/40 → shares .49/.26/.24 → ATTACK. 60/30/58 → .41/.20/.39 → ATTACK/STAMINA hybrid. 57/57/57 → spread 0 → BALANCE. 70/70/30 → .41/.41/.18 → tie → primary ATTACK (tie order), hybrid ATTACK/DEFENSE. 0/0/0 or 10/10/5 → P < 30 → UNCLASSIFIED.

Boundary tests (TC-021): P = 0, P = 29, P = 30; spread exactly 0.10 (→ BALANCE) and 0.1001; s₂ exactly 0.34; s₁ − s₂ exactly 0.08; exact ties.

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

## 4. Classification matrix (official tendency + measured v0.4 candidate)
| Type | Definition | Strengths | Weaknesses | Preferred strategy | ATK/DEF/STA/MAG relation | RPS relation | vs ATTACK | vs DEFENSE | vs STAMINA | vs BALANCE |
|---|---|---|---|---|---|---|---|---|---|---|
| **ATTACK** | Highest share ATK, high mobility | Fast BURST/OVER finishes, steering, skill gain from hits | Spends spin quickly (mobility cost, low STA); bounces off heavy defenders | Hunt, use Dash skill, finish before spin runs low | ATK high; DEF/STA low–mid; MAG fuels Dash | Needs high launch RPS early; poor launch = spins out vs Defense | Mirror: 48.5/48.5%, draw 3.1%, median 8.5 s (too fast — open) | **Unfavoured**: wins 20.2% | **Favoured**: wins 86.3% (BURST 66.6%) | Favoured: wins 60.1% |
| **DEFENSE** | Highest share DEF, low mobility, heavy | Resists knockback and burst; punishes attackers | Low damage output; out-spun by Stamina | Hold centre, absorb, counter with skill | DEF high; STA mid; ATK low | Moderate RPS sufficient; large RPS deficit vs Attack is fatal | **Favoured**: wins 79.5% | Mirror: 50.0/50.0%, SPIN 66.3%, time limit 33.5%, median 109.8 s | **Unfavoured**: wins 19.1% | Favoured: wins 61.3% |
| **STAMINA** | Highest share STA, low friction | Longest spin, wins long matches | Low DEF → bursts under sustained attack | Avoid contact, outlast, Second Wind skill late | STA high; DEF mid; ATK low | Launch RPS strongly matters in mirrors (pure spin race) | **Unfavoured**: wins 13.0% | **Favoured**: wins 80.8% | Mirror: 50.0/50.0%, time limit 26.1%, median 99.5 s | Slightly favoured: 51.9% vs 47.7% |
| **BALANCE** | Spread ≤ 0.10 | No hard counter; flexible skill | No hard advantage; outcome very sensitive to exact values | Read opponent, Adapt skill | All ≈ equal | Medium sensitivity | Unfavoured: 38.8% | Unfavoured: 38.6% | Slightly unfavoured: 47.7% | Mirror |
**v0.4 measured values** (DOC-BAL-001 §5.1, `tools/analysis/results/e2_type_pairs_v0.4.csv`, seat-averaged, N = 4,000 per cell, linear launch D-01/D-04, 1-v-1 analytic model only): Defense beats Attack **79.5%** · Attack beats Stamina **86.3%** · Stamina beats Defense **80.8%** · Attack beats Balance 60.1% · Defense beats Balance 61.3% · Stamina beats Balance 51.9%. Overall vs other types: Attack 55.9%, Defense 53.4%, Stamina 48.8%, Balance 42.0%. A>S and S>D exceed the 55–80% band (AC-2). Not proof of balance; FFA not modelled; no M1 test run.

## 5. Why no type is universally superior (design levers)
1. Triangle emerges from attributes + properties (not hard-coded multipliers).
2. Launch RPS and Energy can overturn type matchups (combat spec §3).
3. Skills are type-linked and bounded.
4. FFA with up to 5 competitors: a counter-type in the room changes the best choice (rock-paper-scissors pressure at room level).
5. Optional bounded type modifier table (±5%) exists in config, **default disabled**; enable only if telemetry shows the triangle failing (ADR-013).
