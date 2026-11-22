# G0 Approval-with-Changes Review (for the owner)

| Document ID | DOC-G0R-001 | Version | 0.4.1 (2026-11-22) | Status | **Accepted by the owner (M1 only), 2026-11-22. No M1 test has been run.** |
|---|---|---|---|---|---|---|---|

## 1. Recommendation
Accept **G0 with changes** for the documentation baseline v0.4.1, authorising **M1 technical spikes only** (`../08-planning/M1-spike-checklist.md`). Do not start M2 features, deploy, or merge PR #1.

## 2. What was decided
- **Owner-confirmed:** D-01 linear launch (10 RPS per accepted press), D-02 READY cue 1.5 s + 5.0 s window, D-03 zero presses = 20 RPS.
- **Owner, after review (2026-11-22):** OQ-LN-08 → `RPS = max(20, 10 × n)`; OQ-CB-12 → D-17 threshold = 7-press (70-RPS) difference; G0 accepted with changes for M1 only.
- **Delegated:** D-04…D-18 (sheet `G0-decision-sheet.md`), all integrated into SRS, specs, ADRs, ERD, protocol, UML, tests, risks, roadmap and the analysis bundle (`v0.4-G0-decision-changelog.md`).

## 3. What the re-run analysis shows (1-v-1 model, v0.4.1, `tools/analysis/`) — not validation
| Item | Result |
|---|---|
| Type win rates vs other types | Attack 55.9%, Defense 53.4%, Stamina 48.8%, Balance 42.0% (AC-1 fail) |
| Favoured matchups | A>S 86.3%, S>D 80.8%, D>A 79.5% (AC-2 fail; D>A now inside the band) |
| Finishes | BURST 33.8% (M-1 pass), OVER 20.0%, SPIN 39.9%, time limit 5.7%; M-2 pass |
| Durations | cells 8.5–109.8 s (AC-4 fail), overall 53.3 s |
| D-17 | 30-RPS wording failed; amended 7-press criterion: Attack 12.6, Balance 17.3, **Stamina 9.9** points at g = 0.20 |
| Launch fairness FC-1 | passes only if the real median is 35 presses (47.1% / 51.0%); 32 vs 35 presses → 91.0% (Stamina mirror) |
| Magic (AC-7), FFA (AC-8) | not measured |
| Full-lock guarantee | holds (damage 49 for N up to 10⁶) |

## 4. Owner questions — status
1. **OQ-LN-08 — decided:** `RPS = max(20, 10 × n)`; the inversion is removed.
2. **OQ-CB-12 — decided:** threshold = 7-press (70-RPS) difference. Model result: passes except Stamina at g = 0.20 (9.9 points, borderline fail).
3. **OQ-LN-09 — still open:** the linear launch makes small press gaps decisive; players below ~7 presses/s are strongly disadvantaged.

## 5. Technical risks carried into M1
350 RPS as an authoritative scalar (RK-30); linear launch sensitivity (RK-27); macro ceiling (RK-23); custom Reverb client and refresh tokens (RK-26); server resources on one VPS (TR-05/06); Balance weakness (RK-16).

## 6. Owner acceptance
> **Accepted with changes — M1 technical spikes only.** Recorded on 2026-11-22 from the owner's answer in conversation (the assistant does not sign on the owner's behalf). Next: S-5 launch input study per `../08-planning/M1-spike-checklist.md`.
