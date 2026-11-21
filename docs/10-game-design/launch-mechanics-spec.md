# Launch Mechanics Specification — 5-Second Rapid Press

| Document ID | DOC-LAUNCH-001 | Version | 0.2 | Status | Mechanic [C]; curve, caps, validation [P] |
|---|---|---|---|---|---|---|---|

## 1. Confirmed
- Before each battle: a **5-second launch window**; a dedicated **launch zone** appears; players press it repeatedly as fast as possible; the **number of successful presses** determines initial rotation; reference **5 presses → 50 RPS**. Rapid-press must be preserved (no hold-to-charge).

## 2. Timeline [P]
| Phase (server clock) | Duration | Presses counted? |
|---|---|---|
| READY cue ("3-2-1" visual, launch zone shown) | 1.5 s | **No** (prevents "early-start" disputes) — addition, needs approval (OQ-LN-01) |
| **LAUNCH_WINDOW** | **5.000 s** | Yes |
| RELEASE (tops drop into arena, results shown) | 0.5 s | No |
| BATTLE starts | — | — |

## 3. What is a "successful press" [P]
A press counts only if **all** hold:
1. **Edge-triggered:** touch-begin, mouse-button-down, key-down **without OS key repeat** (Godot `InputEvent.is_echo()` false), or gamepad button-down.
2. **Released before the next press** (down/up alternation per input source).
3. **Inside the launch zone** (touch/mouse); keyboard/gamepad use the bound launch key.
4. **Inside the window**, as validated by the server (§6).
5. **Minimum interval 83.3 ms** after the previous counted press (= cap **12 presses/s**, max 60 counted presses).
6. One input source per player at a time (switching source mid-window allowed, intervals still apply).

## 4. RPS model
### 4.1 Current (confirmed) reference
5 presses → 50 RPS. Literal linear reading: `RPS = 10·n`.

### 4.2 Recommended model (CHG-01, ADR-015)
```
RPS(n) = RPS_min + (RPS_max − RPS_min) · (1 − e^(−n / k))
RPS_min = 20, RPS_max = 150, k = −5 / ln(1 − (50−20)/(150−20)) = 19.06   ⇒ RPS(5) = 50.0 exactly
```
| Presses n (per 5 s) | 0 | 1 | 3 | **5** | 10 | 15 | 20 | 25 | 30 | 40 | 45 | 50 | 60 (cap) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Recommended curve RPS | 20.0 | 26.6 | 38.9 | **50.0** | 73.1 | 90.8 | 104.5 | 115.0 | 123.1 | 134.1 | 137.7 | 140.6 | 144.4 |
| Linear 10·n | 0 | 10 | 30 | **50** | 100 | 150 | 200 | 250 | 300 | 400 | 450 | 500 | 600 |

- **Minimum 20 RPS** = auto-launch for a player who presses nothing (answers AFK case OQ-GP-06, proposal): they still play but start weak.
- **Effective maximum 144.4 RPS** (cap 60 presses). 150 is the asymptote.
- Typical human range (assumption, to measure in spike S-5): 5–9 presses/s → 25–45 presses → **115–138 RPS** (≈ ±9% around the middle). Skill matters, extremes are compressed.
- Top attributes **do not** change launch RPS (keeps launch readable and fair); attributes act afterwards (decay, clashes). Alternative "TIP modifies RPS_max ±5%" listed as OQ-LN-03.

## 5. Device fairness [P]
| Risk | Mitigation |
|---|---|
| Keyboard auto-repeat | Echo events ignored; edge + release required |
| Mechanical keyboards / mice faster than touch | 12 Hz cap + saturating curve; telemetry by input type to compare distributions (target: median RPS per input type within 5%) |
| Touch sampling 60–240 Hz | ≥ 5 samples per 83 ms at 60 Hz → no effect |
| Gamepad turbo buttons | Cap + regularity detection (§7) |
| Small phone screens | Launch zone ≥ 30% of screen width, thumb-reachable, both-hand option |
| Accessibility (motor impairments) | Open question OQ-LN-02: optional "assisted launch" only in unranked/friendly rooms |
Per-device calibration was rejected (players could fake device type; unequal rules).

## 6. Server validation [P]
1. During WAITING_FOR_PLAYERS/READY the client and server exchange ≥ 5 ping samples → clock offset `Δ` (median) and RTT.
2. Server broadcasts `windowStartServerMs = W0`. Client stamps presses with its monotonic clock and sends `C2S_LaunchPressBatch {seq[], tClientMs[]}` every 100 ms (reliable).
3. For each press: `t = tClient + Δ`. Accept if:
   - `W0 ≤ t ≤ W0 + 5000`;
   - batch arrived by `W0 + 5000 + 300 ms` (grace);
   - `t ≤ arrivalServerMs + 20` (no future stamps);
   - `t ≥ arrivalServerMs − (RTT/2 + 150 + 100)` (no back-dating beyond network plausibility);
   - interval to previous accepted ≥ 83.3 ms; sequence strictly increasing.
4. Server computes `n`, `launch_rps = RPS(n)` and sends `S2C_LaunchResult {userId, presses, launchRps}` to everyone at RELEASE. The client's local counter is cosmetic only.

## 7. Anti-automation [P]
- Hard cap (above) bounds the benefit of any macro to the human maximum.
- **Regularity flag:** if ≥ 20 presses and the coefficient of variation of intervals < 0.03 (threshold to calibrate on real data), record `LAUNCH_REGULARITY_FLAG` in match events. MVP: **no automatic penalty**; repeated flags go to moderator review.
- Modified clients cannot inflate counts beyond the cap and cannot backdate (§6).
- Never trust client-reported `presses` totals.

## 8. Tests (excerpt)
TC-L01 5 valid presses → 50.0 RPS · TC-L02 key repeat → 1 press · TC-L03 presses at 20 Hz → max 12/s counted · TC-L04 press stamped after window → rejected · TC-L05 back-dated 1 s → rejected · TC-L06 zero presses → 20 RPS · TC-L07 300 ms RTT player loses no in-window presses.
