# Launch Mechanics Specification — 5-Second Rapid Press

| Document ID | DOC-LAUNCH-001 | Version | 0.3.1 | Status | Mechanic **[C]**; curve, caps, counting, fairness and validation **[P] proposals** |
|---|---|---|---|---|---|---|---|

v0.3.1 changes (audit C-01): fairness criterion FC-1; proposal to cap counted presses at the measured **median** human rate instead of 12/s; evaluation of layered alternatives; **ranked-play gate** until FC-1 passes; explicit statement of what client timestamps cannot prove. All numbers from `tools/analysis/results/e5_launch.csv`.

## 1. Confirmed [C]
Before each battle: a **5-second launch window**; a dedicated **launch zone**; players press repeatedly as fast as possible; the **number of successful presses** determines the initial rotation; reference **5 presses → 50 RPS**; no hold-to-charge.
Official context: launches start with "Three, Two, One, Go Shoot" (O-2); Takara Tomy's Beylogger/Battlepass record shoot strength/power and spin numbers (O-3). The curve is original — no official formula exists.

## 2. Timeline [P]
| Phase (server clock) | Duration | Presses counted? |
|---|---|---|
| READY cue ("3-2-1") | 1.5 s | No (D-02) |
| **LAUNCH_WINDOW** | **5.000 s**, half-open `[W0, W0 + 5000 ms)` | Yes |
| RELEASE | 0.5 s | No |

## 3. Successful press [P]
1. Edge-triggered (touch-begin, mouse-down, key-down **without echo** — Godot 4.7 `InputEvent.is_echo()`, gamepad button-down).
2. Released before the next press (per input source).
3. Inside the launch zone (touch/mouse) or bound key/button — **checked on the client only** (§7).
4. Inside the window (server-validated, §6).
5. ≥ 1000/r_cap ms after the previous counted press, and fewer than `n_max` presses counted (`n_max = 5 × r_cap`).
6. Strictly increasing sequence numbers.

## 4. RPS model
```
RPS(n) = 20 + 130 · (1 − e^(−n / 19.0575)),   n = min(accepted presses, n_max)      ⇒ RPS(5) = 50.000 [C anchor]
```
| n | 0 | 1 | 3 | **5** | 10 | 15 | 20 | 25 | 30 | **35** | 40 | 45 | 50 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RPS | 20.00 | 26.6 | 38.9 | **50.00** | 73.1 | 90.8 | 104.5 | 115.0 | 123.1 | **129.3** | 134.1 | 137.7 | 140.6 | 144.42 |

### 4.1 Boundary values
| Question | v0.3 proposal | **v0.3.1 proposal (CHG-13)** | Notes |
|---|---|---|---|
| Zero presses | 20.00 RPS | 20.00 RPS (D-03) | wins 3.7% (Attack mirror) / 0.1% (Stamina mirror) vs a 35-press player; alternative: 0 RPS = immediate Spin Finish |
| Counted-press rate cap `r_cap` | 12 presses/s | **= measured median sustained touch rate** (provisional **7/s** until spike S-5) | §5 |
| Maximum counted presses `n_max` | 60 | **5 × r_cap** (provisional **35**) | half-open window removes the 61st-press edge case |
| Maximum RPS | 144.42 | **RPS(n_max)** (provisional **129.3**) | asymptote 150 never reached |
| Minimum RPS | 20.00 | 20.00 | |
Top attributes do not change launch RPS (OQ-LN-03).

## 5. Fairness [P]
### 5.1 Criterion FC-1 (new, NFR-074)
> A player who always reaches the cap must not win more than **60%** of 1-v-1 equal-build mirrors (Attack and Stamina archetypes) against a player at the **median measured touch press count**.
Measured in the analysis model and, decisively, in spike S-5 (real press distributions) + S-1 (real physics).

### 5.2 Measured options (`e5_launch.csv`, P(capped presser wins) Attack / Stamina mirror)
| Cap | vs 25 presses | vs 30 | vs 35 | vs 45 | FC-1 if median = 35 |
|---|---|---|---|---|---|
| 12/s (n_max 60, v0.3) | 78.4% / 98.8% | 74.3% / 97.9% | 68.9% / 93.6% | 57.3% / 77.1% | **fail** |
| 10/s (50) | 77.4% / 98.6% | 71.7% / 96.3% | 65.0% / 88.6% | 51.6% / 63.0% | fail |
| 8/s (40) | 74.0% / 97.6% | 65.4% / 89.4% | 55.1% / 71.0% | — | fail (Stamina) |
| **7/s (35) = median** | 70.1% / 94.6% | 57.9% / 77.8% | **47.5% / 50.8%** | — | **pass** |
Reading: with the cap at the median, macro users gain nothing over median-or-better players; below-median players stay disadvantaged — exactly as against a fast human. **Trade-off:** pressing faster than the median earns nothing extra, so the rapid-press skill ceiling becomes "reach the median reliably". The rapid-press mechanic itself is unchanged.

### 5.3 Other approaches evaluated (audit C-01 suggestions)
| Approach | What it adds | Limitation | Verdict |
|---|---|---|---|
| A. Median cap (above) | bounds the macro benefit to zero vs median players | lowers the skill ceiling | **recommended** |
| B. Accuracy layer: presses count only inside a small moving "sweet spot" within the launch zone | defeats off-the-shelf fixed-position autoclickers and turbo buttons on touch | client-checked → a modified client ignores it; harder on small phones; accessibility cost | evaluate in S-5 as optional addition |
| C. Server challenge windows (server announces short "power pulses"; presses count only during pulses) | raises effort for naive macros | the pulse schedule reaches the client → a modified client can still press perfectly; latency makes pulses unfair at high RTT | not recommended |
| D. Lower the launch's weight in outcomes | reduces every launch advantage | conflicts with F-11 only partly; affects confirmed "presses determine rotation" only in degree | consider in S-1 together with F-11 |

### 5.4 Device fairness
Keyboard echo ignored; device type is **not** verifiable, so no per-device curves. Target NFR-073: median launch RPS per input type within 5% (S-5, telemetry). A median cap also narrows device gaps because faster input devices cannot exceed it.

## 6. Server validation [P]
1. ≥ 5 ping samples during WAITING/READY → clock offset Δ, RTT.
2. Client sends `C2S_LaunchPressBatch {seq[], tClientMs[]}` every 100 ms.
3. Accept a press if `W0 ≤ tClient + Δ < W0 + 5000`, batch arrived by `W0 + 5300`, not future-dated (> arrival + 20 ms), not back-dated (< arrival − (RTT/2 + 250 ms)), interval ≥ 1000/r_cap ms, count < n_max.
4. Server computes `launch_rps` and broadcasts `S2C_LaunchResult`.
**What this cannot do:** client timestamps and batches **cannot prove that a physical human pressed anything**. They only bound *when* claimed presses happened. Any client-side input can be automated.

## 7. Anti-cheat — residual limitations (stated explicitly)
| Measure | Prevents | Does **not** prevent |
|---|---|---|
| Rate cap + `n_max` | more than the cap | a macro/modified client always reaching the cap |
| Edge + release rule | key-repeat abuse | macros emitting down/up pairs |
| Timestamp bounds | gross back/future-dating | small shifts inside the tolerance |
| Server-side counting | inflated totals | — |
| Launch-zone check | — | it is client-side only |
| Regularity flag (CV < 0.03 over ≥ 20 presses) | naive constant-interval macros (flag only) | jittered macros; false positives → no automatic penalty |
| **Ranked gate (FR-186, new)** | competitive damage from the above | — |

### 7.1 Ranked-play gate [P] (FR-186)
Ranked matchmaking, ratings and any rank-affecting results stay **disabled** until FC-1 passes with spike S-5 data and S-1 physics, and RK-23 is re-assessed. Friendly code rooms remain available. (MVP already plans records-only ranking — ADR-009 option A — so the gate does not remove planned MVP scope.)

## 8. Tests (excerpt)
TC-L01 5 presses → 50.00 RPS · TC-L02 key repeat → 1 press · TC-L03 presses at 20 Hz → r_cap counted · TC-L04 press at exactly W0 + 5000 → rejected · TC-L05 back-dated 1 s → rejected · TC-L06 0 presses → 20.00 RPS · TC-L07 300 ms RTT → no valid press lost · TC-L08 press n_max + 1 → rejected · TC-L09 FC-1 evaluated from S-5 data (TC-034).
