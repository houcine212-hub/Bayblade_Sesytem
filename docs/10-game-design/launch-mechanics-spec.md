# Launch Mechanics Specification — 5-Second Rapid Press

| Document ID | DOC-LAUNCH-001 | Version | 0.4 (G0 decisions integrated) | Status | D-01…D-03 **owner-confirmed**; D-04 **decided under owner delegation** — all pending M1 verification (S-5, S-1) |
|---|---|---|---|---|---|---|---|

v0.4 changes: the saturating curve (CHG-01) is **replaced** by the owner's linear rule (D-01); READY cue confirmed (D-02); zero presses = 20 RPS confirmed (D-03); counted-press cap 35 → max **350 RPS** (D-04). All numbers from `tools/analysis/results/e5_launch.csv` (v0.4 config). The previous 129.3 / 144.42 RPS maxima no longer apply.

## 1. Confirmed mechanic
Before each battle: a 5-second launch window; a dedicated launch zone; players press repeatedly as fast as possible; the number of successful presses determines the initial rotation; 5 presses = 50 RPS; no hold-to-charge [C].

## 2. Timeline — D-02 (owner-confirmed)
| Phase (server clock) | Duration | Presses accepted? |
|---|---|---|
| READY cue ("3-2-1") | **1.5 s** | **No** |
| **LAUNCH_WINDOW** | **exactly 5.000 s**, half-open `[W0, W0 + 5000 ms)` | Yes |
| RELEASE | 0.5 s | No |

## 3. Successful (accepted) press — D-04 (delegated)
1. Edge-triggered (touch-begin, mouse-down, key-down without echo — Godot 4.7 `InputEvent.is_echo()`, gamepad button-down).
2. Released before the next press (per input source).
3. Inside the launch zone (touch/mouse) or bound key/button — **client-side check only** (§8).
4. Inside the window, validated by the authoritative server (§7).
5. **Interval floor:** at least **1000/7 ms ≈ 142.857 ms** after the previous accepted press. Implementation rule: compare in integer microseconds — accept if `t − t_prev ≥ 142 857 µs`.
6. **Hard cap:** at most **`n_max = 35`** accepted presses. With the half-open window a 36th press could only fall at exactly 5000 ms, which is excluded; the explicit cap covers any timing edge.
7. Strictly increasing sequence numbers.

## 4. RPS rule — D-01 and D-03 (owner-confirmed)
```
n = min(accepted_press_count, 35)
RPS(n) = 20            if n = 0       (D-03: automatic launch, deliberate exception, no automatic elimination)
RPS(n) = 10 × n        if n ≥ 1       (D-01: strictly linear; no exponential, saturating or rescaled formula)
```
| n | 0 | 1 | 2 | 3 | 5 | 10 | 15 | 20 | 25 | 28 | 30 | 32 | **35 (cap)** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RPS | **20** | **10** | 20 | 30 | **50** | 100 | 150 | 200 | 250 | 280 | 300 | 320 | **350** |
Minimum RPS of a pressing player: 10 (n = 1). Maximum: **350** (n = 35). The value shown to players is the value used by the server — **no hidden conversion** to another scale.

### 4.1 ⚠ Zero-tap / one-tap paradox — flagged for owner decision (OQ-LN-08)
Under D-01 + D-03, **0 presses gives 20 RPS but 1 press gives 10 RPS**, and 2 presses equals 0 presses. Measured (v0.4 model): a 0-press Bey beats a 1-press Bey **98.6%** (Attack mirror) / **99.6%** (Stamina mirror). A player who can press only once is better off not pressing. The rules are kept **exactly as confirmed**; resolution options for the owner:
| Option | Rule | Effect | Changes a confirmed decision? |
|---|---|---|---|
| R0 | keep as is | paradox remains; tiny practical impact (both lose ≥ 98.9% vs a median player) | no |
| **R1 (recommended)** | `RPS = max(20, 10 × n)` | no inversion; identical for n = 0 and n ≥ 2; n = 1 becomes 20 | yes — D-01 for n = 1 |
| R2 | zero presses = 10 RPS | no inversion; linear everywhere | yes — D-03 |
| R3 | zero presses = 0 RPS → immediate SPIN finish | no inversion; harsh for AFK | yes — D-03 |

### 4.2 Spin as an authoritative gameplay quantity
350 RPS at the 60 Hz server tick is 5.83 revolutions per tick. Spin is therefore simulated as an **authoritative scalar state** (`spin_rps`) that drives decay, stability, burst threshold and outcomes; the 3D body is **not** rotated physically at that rate, and clients render a visually capped/blurred spin decoupled from the value. This is a **design approach to prototype in S-1**, not a proven result (DOC-CMB-001 §2.4).

## 5. Fairness — D-04 (delegated)
### 5.1 Criterion FC-1 (NFR-074, kept)
A player who always reaches the cap must not win more than 60% of equal-build 1-v-1 mirrors (Attack, Stamina) against a player at the **measured median** touch press count.

### 5.2 Measured (v0.4 model, linear launch, N = 4,000; P(capped presser wins) Attack / Stamina mirror)
| Opponent presses (RPS) | 20 (200) | 25 (250) | 28 (280) | 30 (300) | 32 (320) | **35 (350)** |
|---|---|---|---|---|---|---|
| Capped presser (35 → 350) | 83.3% / 99.3% | 81.2% / 99.1% | 78.0% / 98.8% | 73.8% / 97.8% | 65.8% / 91.0% | **47.1% / 51.0%** |
FC-1 passes **only if the real median is 35 presses**. If the measured median is lower, the cap must follow it; caps above the median fail: 40 vs 35 → 71.4% / 97.1%; 50 vs 35 → 80.5% / 98.9%; 60 vs 35 → 81.9% / 99.2%.
**Linear launch makes small press differences decisive:** 3 presses fewer than the cap (32) already loses 91% of Stamina mirrors. See risk RK-27 / finding F-11.

### 5.3 Accessibility risk of the median cap (D-04 requirement)
Players physically unable to sustain ~7 presses/s (motor impairments, older devices, one-handed play) are strongly disadvantaged: at 25 presses they lose 81% / 99% of mirrors. Options for owner decision (OQ-LN-09): assisted launch in friendly rooms only (OQ-LN-02); per-player calibration is **not** acceptable for ranked play (device/ability cannot be verified). Ranked stays gated anyway (§6).

### 5.4 Device fairness
Android touchscreen vs keyboard vs gamepad distributions must be **measured in S-5** (median and spread per input type, NFR-073). The cap (35) is provisional until then; FC-1, S-1 physics and balance must be re-run with the measured distributions.

## 6. Ranked gate — FR-186 (kept)
Ranked/rating-changing modes stay **disabled** until FC-1 passes with S-5 data and S-1 physics. Friendly code rooms function normally.

## 7. Server validation
1. ≥ 5 ping samples during WAITING/READY → clock offset Δ, RTT.
2. `C2S_LaunchPressBatch {seq[], tClientMs[]}` every 100 ms (reliable).
3. Accept a press if `W0 ≤ tClient + Δ < W0 + 5000`, batch arrived by `W0 + 5300`, not future-dated (> arrival + 20 ms), not back-dated (< arrival − (RTT/2 + 250 ms)), interval ≥ 142 857 µs, count < 35.
4. Server computes `launch_rps` per §4 and broadcasts `S2C_LaunchResult {userId, presses, launchRps}`.
**Server validation cannot prove that a physical human pressed.** It only bounds when claimed presses occurred.

## 8. Anti-cheat — residual limitations
| Measure | Prevents | Does not prevent |
|---|---|---|
| Interval floor + cap 35 | more than 35 presses | a macro always reaching 35 (= 350 RPS) |
| Edge + release | key-repeat abuse | macros emitting down/up pairs |
| Timestamp bounds | gross back/future-dating | small shifts within tolerance |
| Server-side counting | inflated totals | — |
| Launch-zone check | — | client-side only |
| Regularity flag | naive macros (flag for review only) | jittered macros; **no automated punishment from regularity alone** |
| Ranked gate | competitive damage | — |

## 9. Tests
TC-L01 0 presses → 20 RPS · TC-L02 1 → 10, 5 → 50, 15 → 150, 25 → 250, 35 → 350 · TC-L03 36th press rejected; interval 142 856 µs rejected, 142 857 µs accepted · TC-L04 press at exactly W0 + 5000 rejected · TC-L05 back-dated 1 s rejected · TC-L06 key repeat → 1 press · TC-L07 300 ms RTT → no valid press lost · TC-L08 READY-phase presses not counted · TC-L09 displayed RPS equals server RPS (no rescaling) · TC-034 FC-1 from S-5 data.
