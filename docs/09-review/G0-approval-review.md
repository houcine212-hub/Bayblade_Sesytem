# G0 Approval-with-Changes Review (for the owner)

| Document ID | DOC-G0R-001 | Version | 0.4 (2026-11-22) | Status | **Proposed — awaiting owner acceptance. No M1 test has been run.** |
|---|---|---|---|---|---|---|---|

## 1. Recommendation
Accept **G0 with changes** for the documentation baseline v0.4, authorising **M1 technical spikes only** (`../08-planning/M1-spike-checklist.md`). Do not start M2 features, deploy, or merge PR #1.

## 2. What was decided
- **Owner-confirmed:** D-01 linear launch (10 RPS per accepted press), D-02 READY cue 1.5 s + 5.0 s window, D-03 zero presses = 20 RPS.
- **Delegated:** D-04…D-18 (sheet `G0-decision-sheet.md`), all integrated into SRS, specs, ADRs, ERD, protocol, UML, tests, risks, roadmap and the analysis bundle (`v0.4-G0-decision-changelog.md`).

## 3. What the re-run analysis shows (1-v-1 model, v0.4, `tools/analysis/`) — not validation
| Item | Result |
|---|---|
| Type win rates vs other types | Attack 55.9%, Defense 53.4%, Stamina 48.8%, Balance 42.0% (AC-1 fail) |
| Favoured matchups | A>S 86.3%, S>D 80.8%, D>A 79.5% (AC-2 fail; D>A now inside the band) |
| Finishes | BURST 33.8% (M-1 pass), OVER 20.0%, SPIN 39.9%, time limit 5.7%; M-2 pass |
| Durations | cells 8.5–109.8 s (AC-4 fail), overall 53.3 s |
| D-17 as written | **fails** under linear launch (6.3 / 2.8 / 3.9 points at g ≈ 0.17 / 0.18 / 0.14) |
| Launch fairness FC-1 | passes only if the real median is 35 presses (47.1% / 51.0%); 32 vs 35 presses → 91.0% (Stamina mirror) |
| Magic (AC-7), FFA (AC-8) | not measured |
| Full-lock guarantee | holds (damage 49 for N up to 10⁶) |

## 4. Issues the owner should decide before or during M1
1. **OQ-LN-08 — zero/one-tap inversion** created by D-01 + D-03 (0 presses beats 1 press 98.6% / 99.6%). Recommended: R1 `RPS = max(20, 10 × n)`. Rules unchanged until you decide.
2. **OQ-CB-12 — D-17 threshold:** 30 RPS is only ~9% of a typical launch under the linear rule. Recommended: restate relatively (≈ 7 presses / r ≥ 0.2).
3. **OQ-LN-09 — accessibility:** the linear launch makes small press gaps decisive; players below ~7 presses/s are strongly disadvantaged.

## 5. Technical risks carried into M1
350 RPS as an authoritative scalar (RK-30); linear launch sensitivity (RK-27); macro ceiling (RK-23); custom Reverb client and refresh tokens (RK-26); server resources on one VPS (TR-05/06); Balance weakness (RK-16).

## 6. Owner acceptance
> ☐ Accept G0 with changes (v0.4) and authorise M1 spikes only ☐ Request changes — Name / date: ________ (to be completed by the owner)
