# Design Review Report — Gate G0

| Document ID | DOC-REV-001 | Status | Awaiting user decisions |
|---|---|---|---|

## 1. Design-phase acceptance checklist (Brief §O)
| # | Criterion | Status | Where |
|---|---|---|---|
| 1 | Confirmed requirements in SRS with IDs | ✔ | SRS |
| 2 | Uncertain rules in open-questions register | ✔ | register |
| 3 | Five-player max consistent everywhere | ✔ | BR-001, NFR-002, SQ-02/03, state-room, ERD `slot` CHECK, API-31, TC-001, M-20 |
| 4 | 100 CCU = peak planning target | ✔ | NFR-001, gap §3, load plan |
| 5 | Client/Backend/MS/MySQL separated | ✔ | architecture §3, component |
| 6 | No client → MySQL | ✔ | SEC-001, deployment |
| 7 | Server-side official result | ✔ | BR-005, SQ-07 |
| 8 | Mobile + desktop with constraints | ✔ | ADR-008 |
| 9 | FFA correct; Team Battle TBD | ✔ | FR-056/057, FR-082 |
| 10 | Voice control excluded from MVP | ✔ | BR-010, FR-152 |
| 11 | Real-money wagering excluded | ✔ | BR-008, FR-084 |
| 12 | Single VPS documented as candidate | ✔ | ADR-010 |
| 13 | Editable UML/ERD consistent | ✔ (rendering not yet validated by a PlantUML renderer — see R-1) | 02-uml, 03-data |
| 14 | Traceability matrix | ✔ | 08-planning |
| 15 | ADRs / pending decisions | ✔ | 05-architecture/adr |
| 16 | MVP vs future separated | ✔ | MVP-scope |
| 17 | Review report | ✔ | this file |
| 18 | No production code/infrastructure created | ✔ | — |

## 2. Remaining items
| ID | Item |
|---|---|
| R-0 | No git repository exists; the package lives in an ephemeral environment. Create a repository and commit it. |
| R-1 | Diagrams were written by hand and not rendered with PlantUML in this session (no renderer installed, by design rule). Render once and fix any syntax errors. |
| R-2 | Godot documentation URLs marked "Re-verify" in the ADR sources must be checked against the pinned version. |

## 3. Decisions required from the user
**Blocking (needed to start M1 spikes):**
1. OQ-GP-16 in-battle control? 2. OQ-GP-15/18 spin-out/burst and time limit? 3. OQ-GP-01/02 launch semantics? 4. OQ-GP-12 exploration after MVP? 5. OQ-PL-02 first platforms? 6. OQ-AC-01 registration method? 7. OQ-TO-01 backend language?

**Approve or change the proposals:** ADR-001…011, MVP scope, `Team` vs `MatchSide` terminology, assumptions A-01…A-10.

**Needed before the build of each feature:** the other "H" items in the register.

## 4. Approval statement (to be completed by user)
> I approve the design package version 0.1 [with changes: …] and authorise Milestone M1 (technical spikes only). — Name, date
