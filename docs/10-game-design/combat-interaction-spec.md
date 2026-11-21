# Combat Interaction Specification (opponent-relative model)

| Document ID | DOC-CMB-001 | Version | 0.2 | Status | Principles [C]; equations & coefficients [P] — starting values for tuning |
|---|---|---|---|---|---|---|---|

## 1. Principles
- [C] A Bey's performance depends on **its opponent's characteristics**, not only its own stats.
- [C] Similar Energy → RPS differences strongly matter. Large Energy gap → RPS matters progressively less, **never zero**; smooth transitions.
- [C] No simplistic rules ("Attack always beats Defense").
- [P] Everything is evaluated **per contact, per pair** on the Match Server at the fixed tick (60 Hz). In a 5-competitor FFA each contact is a pair interaction.
- [P] Physics engine provides contact detection, contact normal, relative normal speed `v_n`, contact height difference; this spec converts them into game effects.

## 2. Symbols
`A_i` attributes, `E_i` Energy, `m_i` mass, `mob_i` mobility, `lock_i` lock strength, `h_i` height, `prof_i` contact profile, `ω_i` current spin (RPS), `L_i` lock integrity, `G_i` skill gauge. `rel(a,b) = (a−b)/((a+b)/2)`.

## 3. Advantage function S (the RPS–Energy model) [C principle / P formula — ADR-013]
```
g   = rel(E_i, E_j)                       relative Energy gap
r   = rel(ω_i, ω_j)                       relative CURRENT spin gap (starts as launch gap)
w   = w_min + (w_max − w_min) · exp(−(g/σ)²)     RPS weight, smooth (Gaussian)
S_ij = (1 − w) · tanh(k_E · g) + w · tanh(k_R · r)    ∈ (−1, 1),   S_ji = −S_ij
```
Starting values: `w_max = 0.60, w_min = 0.15, σ = 0.25, k_E = 3.0, k_R = 2.5`.

| g (Energy gap) | 0 | 0.05 | 0.10 | 0.15 | 0.20 | 0.30 | 0.40 | 0.60 |
|---|---|---|---|---|---|---|---|---|
| w (RPS weight) | 0.600 | 0.582 | 0.533 | 0.464 | 0.387 | 0.257 | 0.185 | 0.151 |

- `w_min = 0.15 > 0` guarantees RPS is never irrelevant; Gaussian gives no thresholds.
- `tanh` saturates both terms so no single factor can exceed ±1.
- Spin is the **current** value, so a launch advantage that is spent (by steering or hits) stops helping — RPS is a resource, not a permanent buff.
- **Single channel rule:** RPS enters impact only through S (an earlier draft also scaled impact by √ω; simulation showed RPS then dominated even large Energy gaps — removed, see report F3).

### 3.1 Required numerical scenarios (computed)
| Scenario | E_A | E_B | RPS_A | RPS_B | g | r | w | Energy term | RPS term | **S (A's advantage)** |
|---|---|---|---|---|---|---|---|---|---|---|
| Almost identical Energy, RPS 120 vs 80 | 60 | 60 | 120 | 80 | 0 | +0.40 | 0.600 | 0 | +0.457 | **+0.457** |
| Identical Energy, RPS 100 vs 95 | 60 | 60 | 100 | 95 | 0 | +0.05 | 0.600 | 0 | +0.077 | **+0.077** |
| Moderately higher Energy (+10%), equal RPS | 66 | 60 | 100 | 100 | +0.095 | 0 | 0.539 | +0.128 | 0 | **+0.128** |
| +10% Energy but RPS 80 vs 120 | 66 | 60 | 80 | 120 | +0.095 | −0.40 | 0.539 | +0.128 | −0.411 | **−0.282** (RPS wins) |
| Significantly higher Energy (+30%), RPS 80 vs 120 | 78 | 60 | 80 | 120 | +0.261 | −0.40 | 0.301 | +0.457 | −0.230 | **+0.227** (Energy wins) |
| +30% Energy, RPS 60 vs 140 | 78 | 60 | 60 | 140 | +0.261 | −0.80 | 0.301 | +0.457 | −0.291 | **+0.166** (RPS still reduces it) |
| Lower Energy (−18%) with much higher RPS 140 vs 60 | 54 | 66 | 140 | 60 | −0.20 | +0.80 | 0.387 | −0.329 | +0.373 | **+0.044** (near even) |
| Higher Energy (+10%) with lower RPS 70 vs 110 | 66 | 60 | 70 | 110 | +0.095 | −0.44 | 0.539 | +0.128 | −0.434 | **−0.306** |
| Huge gap (+60%), RPS 50 vs 150 | 80 | 50 | 50 | 150 | +0.46 | −1.0 | 0.165 | +0.737 | −0.163 | **+0.574** |

## 4. Per-contact effects (pair i → j) [P]
### 4.1 Impact power and resistance
```
I_ij = v_n · (0.5 + ATK_i/100) · √m_i · Pk(prof_i, prof_j) · (1 + α·S_ij) · K_skill_i        α = 0.5
R_j  = (0.5 + DEF_j/100) · √m_j · Stab(ω_j) · Abs(prof_j) · K_skill_j
Stab(ω) = min(1, 0.45 + 0.55·ω/25)          (wobble below 25 RPS)
N_ij = I_ij / R_j                             normalised impact (≈ 1 at parity)
```
### 4.2 Profile matrix (knockback factor Pk / burst factor Pb), example values
| attacker ↓ / defender → | SMASH | UPPER | ABSORB | ROUND |
|---|---|---|---|---|
| SMASH | 1.0 / 1.0 | 1.0 / 1.0 | 0.85 / 0.85 | 1.1 / 0.95 |
| UPPER | 0.85 / 1.2 | 0.9 / 1.1 | 0.8 / 1.0 | 0.9 / 1.25 |
| ABSORB | 0.8 / 0.8 | 0.8 / 0.8 | 0.7 / 0.7 | 0.8 / 0.8 |
| ROUND | 0.9 / 0.9 | 0.9 / 0.9 | 0.8 / 0.8 | 0.85 / 0.85 |
UPPER burst factor applies only if `h_i ≤ h_j` (hitting from below); otherwise use SMASH row. `Abs(ABSORB)=1.15`, others 1.0.

### 4.3 Knockback & movement stability
- Impulse on j along contact normal: `J_j = c_kb · N_ij · v_n · m_i/(m_i+m_j)`; friction from low mobility (anchor) resists sliding. **Ring-out (OVER) emerges physically** from position — no ring-out dice.
- Stagger (control loss) 0.3 s, authority × (1 − 0.5·min(1,N_ij)).
### 4.4 Rotation speed loss & stamina consumption
- Collision: `Δω_j = c_sl · N_ij · (1 − STA_j/250)` (STA reduces up to 40%).
- Continuous: decay & steering cost (stats spec §5).
### 4.5 Component durability (burst damage) → `burst-finish-spec.md`
`D_ij = c_b · max(0, N_ij·Pb·A(θ) − T_j) · (1 + ε)`; `T_j = T0 · lock_j · (1 + β·ω_j/150)`.
### 4.6 Skill effectiveness vs opponent
`Eff = base · Pot(MAG_i) · (1 − ρ·Res_j)`, `Pot = 0.8 + 0.4·MAG/100`, `Res_j = 0.5·DEF_j/100 + 0.5·MAG_j/100`, `ρ = 0.3` → Magic attacks are partly resisted by **defence and the target's own Magic** (max −30%).
### 4.7 Optional type modifier
`M_type(i,j)` ∈ [0.95, 1.05] multiplies I_ij; table in config, default all 1.0.

## 5. Opponent interaction matrix (mechanisms)
| Interaction | Main mechanism | What decides it | What can overturn it |
|---|---|---|---|
| Attack → Defense | High ATK vs high DEF·√m·Abs; low N; attacker pays mobility spin cost | Defense survives early burst (lock+DEF), Attack spins out | Big RPS lead for Attack, UPPER profile vs high-riding defender, Dash skill timing |
| Attack → Stamina | High N vs low DEF → lock damage & spin loss | Attack bursts Stamina before it outlasts | Stamina evasion (mobility+steering), Stamina launch lead, Energy gap |
| Defense → Attack (counter) | ABSORB rebound + Iron Stance; attacker staggers, loses control | Attacker exhausts spin | Attacker Energy +25% or launch +40% |
| Stamina vs aggressive attacks | STA reduces Δω only by ≤ 40%; low DEF lowers resistance | Avoiding contact matters more than STA | Steering skill, Feather Glide |
| Magic vs defensive capabilities | Pot(MAG) vs Res(DEF, MAG) | Skill gives bounded swing ±20–30% | High-DEF targets resist up to 30% |
| RPS differences | S function | Equal Energy → large; Energy gap → smaller but ≥ 15% weight | Spending spin through steering |
| Component properties | mass, lock, mobility, profile | Shift *how* a Bey wins (finish type) | Counter-profile choices |
| Type advantages | Emerge from the above | Tendency, not rule | All of the above |

## 6. Outcome
The match outcome is the sequence of eliminations (BURST / OVER / SPIN / XTREME) determined by the Match Server; the last Bey remaining wins (FFA).
