# Design Review Report — Gate G0 (package v0.3)

| Document ID | DOC-REV-001 | Version | 0.3 (final correction pass, 2026-11-21) | Status | **Gate G0 NOT approved** — every item below that is not marked [C] is a proposal awaiting the user's decision |
|---|---|---|---|---|---|---|---|

Decision sheet for approval: `G0-decision-sheet.md`.

## 1. Correction pass results (user request of 2026-11-21)
| # | Request | What was done | Where |
|---|---|---|---|
| 1 | Recalculate RPS/Energy scenarios; define g and r; fix ADR-013 contradiction; actual numbers | g, r, w, S defined normatively; S1–S9 recalculated to 4 decimals (values unchanged, labels corrected); spec-consistent Monte Carlo model replaced the deterministic one; seven contradictions (C1–C7) documented with measured numbers; ADR-013 rewritten with measurable criteria AC-1…AC-7 | DOC-BAL-001 §1–6, DOC-CMB-001 §2–3, ADR-013 |
| 2 | Official vs original; verify Takara Tomy references | Official pages downloaded and read directly (Start Dash Guide, Regulation 6th ed., History, Hasbro Parents Guide, FURYU XONE). Corrections: official type is **determined by the Bit**; the "click together" quote was **not on** the cited page (removed); simultaneous finishes = draw + restart; opposite-spin effects are official; 3-player battles official | DOC-RES-001 §1–5, DOC-CLS-001 §1–2 |
| 3 | Review Energy formula and 0.8 weight | 0.8 had no derivation; equal-budget tests at weights 0–1.0: moving Magic into physical attributes wins 78.9–91.5%; recommendation changed to plain mean (CHG-07) | DOC-STAT-001 §4.5 |
| 4 | Launch zero/max/fairness/anti-cheat | 0 presses → 20.00 RPS (wins 0.1–3.5%); max 60 presses (half-open window + explicit cap); max 144.42 RPS; device-fairness and anti-cheat limitations with measured macro advantage (68.6–93.3%); cap options measured | DOC-LAUNCH-001 §4–7, ADR-015 |
| 5 | Official Burst vs Lock Integrity; primary vs secondary | Burst spec split into official facts (§1) and our model (§2); BURST primary [C]; OVER secondary [C]; SPIN secondary-required [P]; XTREME optional [P]; Burst share measured 35.0% → decision CHG-09 | DOC-BURST-001, ADR-014 |
| 6 | Review Laravel 13 + Reverb + Godot | Facts verified on laravel.com (13.x) and docs.godotengine.org/en/4.7; corrections (Sanctum tokens never expire by default → custom refresh; Echo is JavaScript → custom Godot client; Reverb scaling uses Redis; secondary "database driver" claim removed); comparison robust under three weightings; 10 technical risks | ADR-012 §7 |
| 7 | Render and validate UML | **Rendered**: 21/21 PlantUML files pass `-checkonly` and render to SVG (PlantUML 1.2020.02 + Graphviz); Mermaid roadmap renders (mermaid-cli 11.x); 4 diagrams inspected visually. Static lint reported separately | `../02-uml/README.md` |
| 8 | Update review report, keep proposals marked | This report, decision sheet, CHG-07…12, register v0.3 | — |

## 2. Validation results
| Check | Result |
|---|---|
| PlantUML syntax check (`-checkonly`) | **21/21 pass** (PlantUML 1.2020.02) |
| PlantUML render to SVG | **21/21 rendered**, no error text in output; visual inspection of 4 renders |
| Mermaid render | 1/1 rendered (mermaid-cli 11.x, headless Chromium) |
| Static lint | 21/21 pass (structural only; not counted as rendering) |
| Cross-references | all relative document references resolve |
| Traceability | 206 requirement IDs mapped, 0 unmapped |
| Official Beyblade facts | verified directly in 5 official documents (DOC-RES-001 §1.1); remaining INDEX/SEC items labelled |
| Godot 4.7 API names | verified in the 4.7 documentation (DOC-RES-001 T-03) |
| Laravel 13 facts | verified in the 13.x documentation (T-04, T-05, T-08…T-10) |
| Combat model vs acceptance criteria | **not met**: AC-1, AC-2, AC-4, AC-7 fail; AC-5, AC-6 pass; AC-3 depends on CHG-09 (DOC-BAL-001 §5.3) |

## 3. What this means for Gate G0
The **architecture, requirements, data, interfaces and official-source research** are ready for approval. The **combat numbers are not balanced** and must not be approved as final; the proposal is to approve the *equations and the starting coefficient set* as the input to spike S-1, with AC-1…AC-7 as that spike's exit criteria. This is why the decision sheet separates "approve structure" from "approve values".

## 4. Remaining items (not blocking G0 if accepted as spike work)
| ID | Item |
|---|---|
| R-1 | ~~Render PlantUML~~ done in v0.3 |
| R-2 | ~~Re-verify Godot API names~~ done in v0.3 |
| R-3 | Confirm that Regulation **Vol.11** (latest, image-based PDF) did not change finish rules from the 6th edition |
| R-4 | Spikes S-1…S-6 after approval (no implementation before) |
| R-5 | Combat acceptance criteria AC-1, AC-2, AC-4, AC-7 (spike S-1) |
| R-6 | Real skill model to evaluate Magic (AC-7) |

## 5. Decisions required
See `G0-decision-sheet.md` (D-01 … D-16).

## 6. Approval statement (to be completed by the user)
> I approve design package v0.3 with the decisions recorded in the G0 decision sheet [with changes: …] and authorise Milestone M1 (technical spikes only). — Name, date
