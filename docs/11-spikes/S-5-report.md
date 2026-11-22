# S-5 Launch Input Study — Spike Report

| Document ID | SPK-S5-001 | Version | 0.1 (2026-11-22) | Status | **In progress: capture prototype built and unit-tested headless. No participant data has been collected, and no pass/fail result exists yet.** |
|---|---|---|---|---|---|---|---|

Scope: DOC-M1-001 §S-5. Throw-away prototype; not a game feature. No G0 decision has been changed.

## Environment
Godot 4.7.2-stable (official Linux build, headless) on the Linux cloud container. Renderer: Compatibility. No Android, Windows or real input device has been used yet.

## Artefacts
| Path | Purpose |
|---|---|
| `game/project.godot` | M1 spike project (created on this branch; `game/` did not exist) |
| `game/spikes/s5_launch_input/launch_counter.gd` | DOC-LAUNCH-001 §3–4 counting rules and `RPS = max(20, 10 × n)` |
| `game/spikes/s5_launch_input/edge_tracker.gd` | edge + release rule per input source; key echo rejected |
| `game/spikes/s5_launch_input/s5_capture.{gd,tscn}` | capture UI: READY 1.5 s → window 5 s → release 0.5 s; touch, mouse, keyboard (Space), gamepad (A); per-trial CSV in `user://s5/` |
| `game/tests/test_launch_counter.gd` | headless unit tests (TC-016, TC-038, TC-L01–L04, TC-L06, TC-L08, TC-032) |
| `game/tests/test_capture_smoke.gd` | headless scene smoke test (synthetic key events → CSV) |
| `tools/spikes/s5_summarize.py` | step 5.3: independent recount, median/p10/p90 per input class, NFR-073 check |

Run the tests:
```bash
godot --headless --path game --script res://tests/test_launch_counter.gd
godot --headless --path game --script res://tests/test_capture_smoke.gd
```

## Step status
| # | Step | Status |
|---|---|---|
| 5.1 | Input-capture prototype | **Built; desktop headless only.** Not yet exported or run on ≥ 3 Android phones, keyboard, mouse or gamepad hardware |
| 5.2 | Apply counting rules | **Implemented and tested** (63/63 unit checks, smoke test PASS) |
| 5.3 | Median and spread per input type | Tool ready, checked on synthetic data only. **No result**: needs ≥ 30 participants per input class |
| 5.4 | Re-select cap | Not started (needs 5.3) |
| 5.5 | Re-run `tools/analysis` with measured distributions → FC-1 | Not started |
| 5.6 | Regularity human vs macro | Not started (raw timestamps are already recorded) |
| 5.7 | Verify `max(20, 10 × n)` end-to-end | Counter level verified (0, 1, 2 → 20; 3 → 30; 35 → 350). End-to-end on devices pending |
| 5.8 | Accessibility sample (OQ-LN-09) | Not started |

## Findings so far
1. **Integer-µs edge of the cap.** 35 × 142 857 µs = 4 999 995 µs < 5 000 000 µs, so a 36th press at the interval floor lies *inside* the half-open window. The explicit cap of 35 is therefore what rejects it, as DOC-LAUNCH-001 §3.6 already requires. The sentence in that section ("a 36th press could only fall at exactly 5000 ms") holds only in exact arithmetic. This is a wording note for the owner; the rule is unchanged.
2. **Pressing faster does not help.** At 40 presses/s only presses ≥ 142.857 ms apart count (34 accepted in the test). A 1000/s macro gets exactly 35 (RK-23 is confirmed at logic level).
3. **Timestamp limitation.** Godot `InputEvent`s carry no hardware timestamp. The prototype stamps `Time.get_ticks_usec()` at event delivery, with agile event flushing enabled, so times are quantised to input-processing granularity (it also records the frame number). This must be quantified on real devices before the regularity analysis (5.6) is trusted.
4. Touch→mouse emulation is disabled so one tap is not counted twice on Android.

## Next actions
Export to Android (needs SDK and export templates, not available in this container), recruit participants (≥ 30 per input class, pseudonymous IDs, consent), run trials, then `python3 tools/spikes/s5_summarize.py <csv dir>`.
