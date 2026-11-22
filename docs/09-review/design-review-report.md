# Design Review Report — Gate G0 (package v0.4; sections 1–5 record the v0.3.1 audit pass)

| Document ID | DOC-REV-001 | Version | 0.4 (G0 decisions integrated, 2026-11-22) | Status | G0 decisions recorded (owner D-01…D-03, delegated D-04…D-18); **approval with changes proposed — see `G0-approval-review.md`**; no M1 test run |
|---|---|---|---|---|---|---|---|

Related: `G0-approval-review.md` (current owner review), `G0-decision-sheet.md` (D-01…D-18 outcomes), `v0.4-G0-decision-changelog.md` (decision → artefact traceability), `v0.3.1-audit-correction-log.md`. Sections 1–5 below describe the v0.3.1 audit pass (historical); v0.4 numbers are in DOC-BAL-001.

## 1. What changed in v0.3.1
| Area | Change |
|---|---|
| Launch (C-01) | Median-rate press cap, FC-1, ranked gate FR-186, honest anti-cheat limits |
| Formulas (C-02…C-04) | Units and normalisation; contact events; canonical burst equation; full-lock guarantee with proof |
| Reproducibility (C-05) | `tools/analysis/` bundle; all balance numbers regenerated from it; re-run byte-identical |
| Balance (H-01…H-05) | Seat-averaged criteria, AC-8 FFA, AC-9 launch; Burst metric populations; D-17; Magic provisional; TIP-only type source; zero-total guard |
| Data/API/security (D-01…D-06) | ERD and dictionary aligned; JWT key removed; versions and examples updated |
| Drift (§6) and UML (§7) | stale references fixed; actor hierarchy; titles; re-rendered |
| New requirements | FR-186, FR-225, FR-226, NFR-074 (all [P]) |

## 2. Validation results
| Check | Result |
|---|---|
| PlantUML `-checkonly` | **21/21 pass** (PlantUML 1.2020.02 + Graphviz) |
| PlantUML render to SVG | **21/21 rendered**, no embedded error text |
| Visual inspection | use-case, state-bey-combat, ERD (full width) inspected after changes |
| Mermaid render (roadmap) | rendered (mermaid-cli 11.x) |
| Static lint | 21/21 (structural only; not counted as rendering) |
| Cross-references | all relative references resolve |
| Traceability | **210** requirement IDs mapped, 0 unmapped |
| Analysis reproducibility | `python3 tools/analysis/run_all.py` re-run → results byte-identical (Python 3.13.18, numpy 2.5.3) |
| Full-lock guarantee | proved (DOC-BURST-001 §2.3); analysis check N up to 10⁶ → damage 49, L ≥ 51 |
| Combat acceptance (1-v-1 model) | AC-1 **fail**, AC-2 **fail**, AC-3 pass under D-10 proposal, AC-4 **fail** (cells) / pass (overall), AC-5 pass, AC-6 pass under D-17 (b), AC-7 not measurable, AC-8 not measurable, AC-9 passes only with the median cap |

## 3. What this means for Gate G0
Architecture, requirements, data model, interfaces, official-source research, formula structure and the analysis method are ready for a decision. **Combat values are not balanced** and are proposed only as spike S-1 starting values with AC-1…AC-9 as exit criteria. **Ranked play is gated** (FR-186) until launch fairness is demonstrated with real data.

## 4. Remaining items
| ID | Item |
|---|---|
| R-3 | Confirm Regulation Vol.11 (latest, image-based PDF) did not change finish rules from the 6th edition |
| R-4 | Spikes S-1…S-6 after approval |
| R-5 | AC-1, AC-2, AC-4 (S-1) |
| R-6 | Real skills to evaluate Magic (AC-7) and FFA bots (AC-8) |
| R-7 | Split dense ERD/component/domain diagrams into per-area views (implementation phase) |
| R-8 | Measure real touch press distributions (S-5) → final cap value, FC-1 |
| R-9 | Spin-race launch sensitivity F-11 (OQ-CB-10) |

## 5. Approval statement — superseded
The v0.3.1 approval quote that stood here is **historical and must not be signed**. The current owner acceptance is in `G0-approval-review.md` §6 (package v0.4, M1 spikes only).

## 6. v0.4 independent audit (2026-11-22)
Verdict: approve with changes **for M1 technical experiments only**, subject to owner acceptance; not ready for M2, ranked play, deployment or merging. It reproduced all 11 analysis CSV files byte-for-byte (numpy 2.3.5) and confirmed 210/210 traced requirements. Open items: OQ-LN-08, OQ-CB-12, launch fairness/accessibility (S-5), unmet AC-1/2/4/6, unmeasured AC-7/8, unproven stack integration. Its two editorial findings (this section 5; the sequence-diagram count in README) are fixed.
