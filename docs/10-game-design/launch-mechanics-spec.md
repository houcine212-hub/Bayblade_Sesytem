# Launch Mechanics Specification — 5-Second Rapid Press

| Document ID | DOC-LAUNCH-001 | Version | 0.3 | Status | Mechanic **[C]**; curve, caps, counting and validation **[P] proposals** |
|---|---|---|---|---|---|---|---|

## 1. Confirmed [C]
Before each battle: a **5-second launch window**; a dedicated **launch zone** appears; players press it repeatedly as fast as possible; the **number of successful presses** determines the initial rotation; reference **5 presses → 50 RPS**. Rapid-press must be preserved (no hold-to-charge).

Official context (DOC-RES-001): physical launches are started with "Three, Two, One, Go Shoot" (O-2); Takara Tomy's Beylogger/Battlepass measure "shoot strength/power and rotation/spin numbers" (O-3). The rapid-press curve is our original digital analogue — no official formula exists.

## 2. Timeline [P]
| Phase (server clock) | Duration | Presses counted? |
|---|---|---|
| READY cue ("3-2-1", launch zone shown) | 1.5 s | No (OQ-LN-01) |
| **LAUNCH_WINDOW** | **5.000 s**, half-open interval `[W0, W0 + 5000 ms)` | Yes |
| RELEASE | 0.5 s | No |
| BATTLE | — | — |

## 3. Successful press [P]
A press counts only if **all** hold:
1. Edge-triggered: touch-begin, mouse-button-down, key-down **without OS key repeat** (Godot 4.7 `InputEvent.is_echo()` = false; echo events exist only for `InputEventKey` — verified), gamepad button-down.
2. Released before the next press (per input source).
3. Inside the launch zone (touch/mouse) or the bound key/button.
4. Inside the window (server-validated, §6).
5. At least **83.3 ms** after the previous counted press (12 presses/s), **and** fewer than `n_max = 60` presses counted so far.
6. Sequence numbers strictly increasing.

## 4. RPS model
### 4.1 Confirmed reference
5 presses → 50 RPS (literal reading: `RPS = 10·n`, linear).

### 4.2 Proposed curve (CHG-01, ADR-015)
```
RPS(n) = 20 + 130 · (1 − e^(−n / k)),   k = −5 / ln(1 − 30/130) = 19.0575      ⇒ RPS(5) = 50.000
n = min(accepted presses, n_max),   n_max = 60
```
| n | 0 | 1 | 3 | **5** | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | **60** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RPS | 20.00 | 26.6 | 38.9 | **50.00** | 73.1 | 90.8 | 104.5 | 115.0 | 123.1 | 129.3 | 134.1 | 137.7 | 140.6 | 142.7 | **144.42** |
| Linear 10·n (literal reading) | 0 | 10 | 30 | 50 | 100 | 150 | 200 | 250 | 300 | 350 | 400 | 450 | 500 | 550 | 600 |

### 4.3 Boundary values (item 4 of the correction pass)
| Question | Answer [P] | Reason / measured effect |
|---|---|---|
| **Zero presses** | **20.00 RPS** (auto-launch) | The match never stalls on an absent/AFK player and the Bey still enters the arena. Measured: a 0-press Bey vs a 35-press Bey wins 3.5% (Attack mirror, median 1.9 s) and 0.1% (Stamina mirror, median 8.7 s) — it is effectively a forfeit but not a crash. Alternative (OQ-LN-07): 0 presses → 0 RPS → immediate SPIN finish at RELEASE (simpler, harsher). |
| **Maximum counted presses** | **60** = 12 presses/s × 5 s | With an inclusive window and exactly 83.3 ms spacing a 61st press could fit at t = 5000 ms; the half-open window **and** the explicit `n_max = 60` remove that edge case. |
| **Maximum RPS** | **144.42 RPS** (= RPS(60)) | The asymptote 150 is never reached. |
| Minimum RPS | 20.00 | — |
| Typical range (assumption A-11) | 25–45 presses → 115.0–137.7 RPS | spike S-5 must measure real distributions per device |

Top attributes do **not** change launch RPS (launch = pure player skill); OQ-LN-03 keeps the alternative open.

## 5. Device fairness [P]
| Risk | Mitigation | Limitation (honest) |
|---|---|---|
| Keyboard auto-repeat | echo ignored; release required | — |
| Mechanical keyboards / mice / gamepads tap faster than touch | 12/s cap + saturating curve | The cap only equalises **above** 12/s. If touch players' realistic maximum is ~7–9/s, keyboard/mouse players can still reach a higher RPS. Measured: a capped presser beats a 35-press (7/s) player 68.6% (Attack mirror) / 93.3% (Stamina mirror). |
| Device detection | not used for rules | Device type cannot be verified (a client can claim anything), so per-device curves are rejected. |
| Touch sampling 60–240 Hz | ≥ 5 samples per 83 ms at 60 Hz | Display/touch latency differs per phone (not measurable server-side). |
| Small screens | launch zone ≥ 30% screen width, thumb-reachable | — |
| Motor accessibility | OQ-LN-02 assisted launch in friendly rooms only | Not available in ranked play under the current proposal |
**Proposed metric (NFR-073):** median launch RPS per input type within 5% — to be measured in spike S-5 and beta telemetry. **Option (OQ-LN-06):** set the cap to the measured 90th-percentile touch tapping rate (provisional alternatives measured below).

| Cap option | RPS at cap | P(capped presser beats 35-press player) Stamina / Attack mirror |
|---|---|---|
| **12/s, RPS_max 150 (current proposal)** | 144.4 | 93.3% / 68.6% |
| 10/s, RPS_max 150 | 140.6 | 88.2% / 64.2% |
| 8/s, RPS_max 150 | 134.1 | 70.9% / 55.0% |
| 12/s, RPS_max 130 (k = 15.70, still 5 → 50) | 127.6 | 87.0% / 63.3% |
| 10/s, RPS_max 130 | 125.4 | 82.4% / 59.9% |
A lower cap shrinks both the device gap and the macro advantage but stops rewarding legitimate players above the cap. Recommendation: keep 12/s until S-5 data exists; then choose from this table.

## 6. Server validation [P]
1. During WAITING/READY: ≥ 5 ping samples → clock offset `Δ` (median) and RTT.
2. Server announces `W0`; the client stamps presses with its monotonic clock and sends `C2S_LaunchPressBatch {seq[], tClientMs[]}` every 100 ms (reliable).
3. For each press `t = tClient + Δ`; accept if `W0 ≤ t < W0 + 5000`; batch arrived by `W0 + 5300`; `t ≤ arrival + 20 ms`; `t ≥ arrival − (RTT/2 + 250 ms)`; ≥ 83.3 ms after the previous accepted press; `n < 60`.
4. Server computes `launch_rps = RPS(n)` and broadcasts `S2C_LaunchResult`. Client counters are cosmetic.

## 7. Anti-cheat — what it does and does not achieve [P]
| Measure | Prevents | Does **not** prevent |
|---|---|---|
| 12/s counting cap, `n_max = 60` | More than the human maximum; unbounded macro gains | A macro (or modified client) sending exactly 12 presses/s **reliably** — it always reaches the best possible RPS (144.42). Its advantage over typical humans is the table in §5. |
| Edge + release rule | Key-repeat abuse | Hardware turbo buttons and software macros that emit proper down/up pairs |
| Server timestamp bounds | Future-dated or back-dated presses beyond ~RTT/2 + 250 ms | Small timing shifts within that tolerance |
| Server-side counting | Inflated client totals | — |
| Launch-zone check | — | **Performed on the client only** — the server receives timestamps, not touch positions; a modified client can ignore the zone |
| Regularity flag (CV of intervals < 0.03 over ≥ 20 presses) | Naive constant-interval macros (flag for review) | Macros that add random jitter; false positives possible for very consistent humans → **no automatic penalty in MVP** |
| Moderation reports | Repeated suspicious players | Real-time prevention |
**Residual risk (documented, RK-17/RK-23):** the launch mechanic cannot be made cheat-proof on an untrusted client; the design bounds the benefit to "always at the cap". If competitive integrity requires more, options are a lower cap, ranked-only device attestation (not available cross-platform), or reducing the launch's weight in outcomes.

## 8. Tests (excerpt)
TC-L01 5 valid presses → 50.00 RPS · TC-L02 key repeat → 1 press · TC-L03 presses at 20 Hz → 12/s counted · TC-L04 press at exactly W0 + 5000 → rejected · TC-L05 back-dated 1 s → rejected · TC-L06 0 presses → 20.00 RPS · TC-L07 300 ms RTT player loses no in-window presses · TC-L08 61st press → rejected · TC-L09 60 presses → 144.42 RPS.
