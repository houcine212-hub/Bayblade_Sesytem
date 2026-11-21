# Requirements Traceability Matrix

| Document ID | DOC-RTM-001 | Status | [P] — generated from SRS v0.1; keep in sync |
|---|---|---|---|

Columns: Use case (UC) · Diagram (`02-uml`) · Data (`03-data`) · API / protocol (`04-interfaces`) · Test (`07-quality-operations`).

| Req | Status | Use case | Diagram | Data | API / Protocol | Test |
|---|---|---|---|---|---|---|
| FR-001 | C | UC-02 | context | user_account | API-02 | E2E cross-device login |
| FR-002 | C need / TBD method | UC-01 | SQ-01 | user_account, player_profile | API-01 | TC-0xx (after OQ-AC-01) |
| FR-003 | C need / P mechanism | UC-02 | SQ-01 | auth_session | API-02..04 | Auth integration |
| FR-004 | TBD | UC-01 | — | user_account | API-05 | TBD |
| FR-005 | P (privacy, J6) | UC-03 | — | all personal tables (§5 lifecycle) | API-13 | Privacy tests |
| FR-006 | P | UC-02 | SQ-01 | — | API-02, API-06 | TC-012 |
| FR-010 | C | UC-03 | domain-model | player_profile | API-10..12 | Profile API tests |
| FR-011 | P | UC-03 | domain-model | player_profile | API-10..12 | Profile API tests |
| FR-012 | P | UC-03 | domain-model | player_profile | API-10..12 | Profile API tests |
| FR-020 | C (E3 separation) / P (format) | UC-04 | component (Content Data) | item_definition | API-20 | Content schema validation |
| FR-021 | C | UC-04 | SQ-01 | inventory_item | API-21 | Starter grant test |
| FR-022 | C | UC-04 | SQ-02 | loadout, loadout_slot | API-22, API-33 | Ownership validation |
| FR-023 | A (A-04) | UC-04 | SQ-01 | inventory_item | API-21 | Starter grant test |
| FR-024 | P | UC-08 | SQ-03 | match_participant.loadout_snapshot_json | INT-01 AssignMatch | TC-014 |
| FR-025 | TBD (OQ-GP-03, OQ-GP-11) | — | — | item_definition (future) | — | TBD |
| FR-030 | C (create) / A (host, A-02) | UC-05 | SQ-02, state-room | room, room_member | API-30 | Room tests |
| FR-031 | C | UC-05 | SQ-02, state-room | room, room_member | API-30 | Room tests |
| FR-032 | C | UC-06 | SQ-02 | room.active_code | API-31 | TC-015 |
| FR-033 | C | UC-06 | SQ-02, state-room | room_member, match_participant.slot | API-31, API-34 | TC-001 |
| FR-034 | C (<5) / A (min 2, A-01) | UC-08 | SQ-03, activity | room | API-36 | Start validation tests |
| FR-035 | C | UC-07 | SQ-02 | room_member.is_ready | API-33 | Ready flow test |
| FR-036 | A (A-02) | UC-08 | SQ-03, activity | room | API-36 | Start validation tests |
| FR-037 | C concept / TBD capacity | UC-06, UC-11 | SQ-06 | room_member.role | API-31, API-34 | Spectator capacity (TBD) |
| FR-038 | P / TBD | UC-05 | state-room | room | API-35 | TBD rules |
| FR-039 | TBD (OQ-GP-08, OQ-GP-14) | UC-05 | state-room | room | API-35 | TBD rules |
| FR-040 | P | UC-04 | SQ-02 | loadout, loadout_slot | API-22, API-33 | Ownership validation |
| FR-050 | P | UC-08 | SQ-03, state-match | game_match | API-36, INT-01 | Allocation tests |
| FR-051 | P | UC-08 | SQ-03 | (memory: ticket hashes) | INT-01 TicketGrant, C2S_Hello | TC-002 |
| FR-052 | C (exists) / TBD | UC-09 | SQ-04, state-match | match_participant.launch_summary_json | C2S_LaunchInput | Launch unit tests (after OQ-GP-01/02) |
| FR-053 | C concept / TBD | UC-09 | SQ-04, state-match | match_participant.launch_summary_json | C2S_LaunchInput | Launch unit tests (after OQ-GP-01/02) |
| FR-054 | C | UC-09 | SQ-04 | item_definition.stats_json | — | Formula unit tests |
| FR-055 | C (O-7) / P (method) | UC-10 | SQ-04, component | (memory) | S2C_Snapshot | Simulation golden tests |
| FR-056 | C | UC-10 | SQ-05, state-match | match_participant.placement, elimination_reason | S2C_Eliminated | TC-003 |
| FR-057 | C | UC-10 | SQ-05, state-match | match_participant.placement, elimination_reason | S2C_Eliminated | TC-003 |
| FR-058 | C | UC-11 | SQ-06 | — | S2C_RoleChanged | TC-004 |
| FR-059 | C (C3) | UC-09, UC-10, UC-12 | SQ-04..07 | — | S2C_* events | E2E UX review |
| FR-060 | TBD (G-02, OQ-GP-15) | UC-10 | SQ-05, state-match | game_match.end_reason | TBD | TBD after decision |
| FR-061 | TBD (G-01, OQ-GP-16) | UC-10 | SQ-05, state-match | game_match.end_reason | TBD | TBD after decision |
| FR-062 | TBD (OQ-GP-04) | UC-10 | SQ-05, state-match | game_match.end_reason | TBD | TBD after decision |
| FR-063 | TBD (OQ-GP-05) | UC-13 | SQ-08 | match_participant.connection_outcome | API-40, API-41 | TC-007 |
| FR-064 | TBD rule / P mechanism | UC-13 | SQ-08 | match_participant.connection_outcome | API-40, API-41 | TC-007 |
| FR-065 | TBD (OQ-GP-06) | UC-10 | SQ-05, state-match | game_match.end_reason | TBD | TBD after decision |
| FR-066 | TBD (OQ-GP-17) | UC-10 | SQ-05, state-match | game_match.end_reason | TBD | TBD after decision |
| FR-067 | TBD (OQ-GP-04) | UC-10 | SQ-05, state-match | game_match.end_reason | TBD | TBD after decision |
| FR-068 | TBD rule / P default | UC-10 | SQ-08, state-match | game_match.status=ABORTED | INT-01 heartbeat | TC-008 |
| FR-069 | TBD (OQ-GP-18) | UC-10 | SQ-05, state-match | game_match.end_reason | TBD | TBD after decision |
| FR-070 | P | UC-12 | SQ-07 | game_match, match_participant, match_event | INT-02 | TC-005, TC-009 |
| FR-071 | C | UC-12 | SQ-07 | — | (no client endpoint) | TC-006 |
| FR-080 | C | UC-10 | state-match | game_match.mode | AssignMatch.mode | Mode tests |
| FR-081 | C concept / A (A-03) | UC-08 | — | game_match.stake_type | — | Schema check |
| FR-082 | TBD | — | domain-model (MatchSide) | match_participant.side_id | — | Post-MVP |
| FR-083 | C (gate) | — | — | game_match.stake_type=NONE | — | Schema check |
| FR-084 | C | — | — | game_match.stake_type=NONE | — | Schema check |
| FR-090 | C concept / P enforcement | UC-11 | SQ-06 | — | C2S handlers role check | TC-004 |
| FR-091 | TBD (OQ-GP-07) | UC-11 | SQ-06 | — | API-41 | TBD |
| FR-100 | C | UC-12 | SQ-07 | game_match, match_participant | API-42, API-43 | History tests |
| FR-101 | C | UC-12 | SQ-07 | game_match, match_participant | API-42, API-43 | History tests |
| FR-102 | P | UC-23 | SQ-07 | competitive_record | API-44 | Record update tests (rules TBD) |
| FR-103 | C concept / TBD | UC-23 | SQ-07 | competitive_record | API-44 | Record update tests (rules TBD) |
| FR-104 | P | UC-23 | SQ-07 | competitive_record | API-44 | Record update tests (rules TBD) |
| FR-110 | C concept / TBD rules | UC-17 | domain-model | team, team_membership, team_invitation | API-50..54 | Team tests |
| FR-111 | C | UC-17 | domain-model | team, team_membership, team_invitation | API-50..54 | Team tests |
| FR-112 | C (investigate) / P | UC-17 | domain-model | team, team_membership, team_invitation | API-50..54 | Team tests |
| FR-113 | C (investigate) / P | UC-17 | domain-model | team, team_membership, team_invitation | API-50..54 | Team tests |
| FR-114 | C (investigate) / P | UC-17 | domain-model | team, team_membership, team_invitation | API-50..54 | Team tests |
| FR-115 | TBD (OQ-AC-03) | UC-17 | domain-model | team, team_membership, team_invitation | API-50..54 | Team tests |
| FR-116 | TBD ("if approved") | UC-17 | — | (future) | — | Post-MVP |
| FR-120 | C | UC-20 | use-case | tournament (post) | — | Post-MVP |
| FR-121 | C concept / TBD | UC-18, UC-19 | use-case | organizer_application, user_role, audit_log | API-80, API-81 | TC-011 |
| FR-122 | C / P audit | UC-18, UC-19 | use-case | organizer_application, user_role, audit_log | API-80, API-81 | TC-011 |
| FR-123 | TBD (OQ-AC-06) | UC-20 | use-case | tournament (post) | — | Post-MVP |
| FR-130 | P | UC-14 | — | user_block | API-60 | TC-013 |
| FR-131 | C (design) | UC-15 | — | report | API-61 | TC-013 |
| FR-132 | P | UC-16 | — | moderation_action, audit_log | API-70..72 | Moderation tests |
| FR-133 | P | UC-16 | — | moderation_action, audit_log | API-70..72 | Moderation tests |
| FR-134 | P | UC-16 | — | — | — | TBD |
| FR-135 | TBD (OQ-AC-07) | UC-16 | — | — | — | TBD |
| FR-140 | C (vision) | UC-21, UC-22 | use-case | inventory_item.source, game_match.room_id NULL | — | Post-MVP |
| FR-141 | C (vision) | UC-21, UC-22 | use-case | inventory_item.source, game_match.room_id NULL | — | Post-MVP |
| FR-142 | C (vision) | UC-21, UC-22 | use-case | inventory_item.source, game_match.room_id NULL | — | Post-MVP |
| FR-150 | C (not authoritative) / P links | — | context | — | API-06 | UI check |
| FR-151 | C (later) | — | — | — | — | Post-MVP |
| FR-152 | C (later, excluded from MVP) | — | — | — | — | Post-MVP |
| FR-160 | C families / TBD order | all | deployment | — | X-Platform header | Cross-platform matrix |
| FR-161 | C | all | deployment | — | X-Platform header | Cross-platform matrix |
| FR-162 | C | all | deployment | — | X-Platform header | Cross-platform matrix |
| FR-163 | P (evaluate) | all | deployment | — | X-Platform header | Cross-platform matrix |
| FR-164 | P | all | deployment | — | X-Platform header | Cross-platform matrix |
| BR-001 | C | UC-06, UC-08 | SQ-02, SQ-03, state-room | match_participant.slot CHECK | API-31, INT-01 | TC-001 |
| BR-002 | C | UC-10, UC-11 | SQ-05, SQ-06 | match_participant | S2C_Eliminated | TC-003, TC-004 |
| BR-003 | C | UC-10, UC-11 | SQ-05, SQ-06 | match_participant | S2C_Eliminated | TC-003, TC-004 |
| BR-004 | C | UC-10, UC-11 | SQ-05, SQ-06 | match_participant | S2C_Eliminated | TC-003, TC-004 |
| BR-005 | C | UC-12 | SQ-07 | — | INT-02 | TC-006 |
| BR-006 | C | UC-19 | — | organizer_application | API-81 | TC-011 |
| BR-007 | C | all | — | user_role | all | AuthZ matrix tests |
| BR-008 | C | — | — | game_match.stake_type | — | Schema check |
| BR-009 | C | — | — | game_match.stake_type | — | Schema check |
| BR-010 | C | — | — | — | — | Scope review |
| BR-011 | C | — | context | — | — | Scope review |
| BR-012 | A (A-01) | UC-08 | SQ-03 | — | API-36 | Start validation |
| BR-013 | P | UC-10 | SQ-08 | game_match.status | — | TC-008 |
| BR-014 | P | UC-08 | SQ-03 | game_match.protocol_version | C2S_Hello | TC-002 |
| NFR-001 | C target | — | deployment | — | — | L-10..L-100 |
| NFR-002 | C | UC-06 | SQ-02, SQ-03 | slot CHECK | API-31, INT-01 | TC-001 |
| NFR-003 | C intent / P mechanism | — | deployment | — | INT-01 | M-churn |
| NFR-004 | C | — | deployment | — | — | L-10..L-100 |
| NFR-005 | C | — | deployment | — | — | M-20 |
| NFR-006 | P (benchmark) | UC-10 | SQ-04 | — | S2C_Snapshot | Spike S-2, impairment tests |
| NFR-007 | P (spike) | UC-10 | SQ-04 | — | S2C_Snapshot | Spike S-2, impairment tests |
| NFR-008 | P (estimate in protocol doc) | UC-10 | SQ-04 | — | S2C_Snapshot | Spike S-2, impairment tests |
| NFR-009 | P | UC-08 | SQ-03 | — | API-36 | Load metric |
| NFR-010 | P | — | — | — | all | Load metric |
| NFR-020 | C | — | component (Quality Settings) | — | — | Device matrix, spike S-4 |
| NFR-021 | C (define later) | — | component (Quality Settings) | — | — | Device matrix, spike S-4 |
| NFR-022 | P | — | component (Quality Settings) | — | — | Device matrix, spike S-4 |
| NFR-030 | P | — | deployment | — | — | TC-008 |
| NFR-031 | P | — | SQ-07, SQ-08 | — | INT-02 retry | TC-009 |
| NFR-032 | P | — | deployment | backups | — | Restore test |
| NFR-033 | P | — | deployment | — | — | Kill-process test |
| NFR-040 | C | — | component | — | — | Repo/CI review |
| NFR-041 | C | — | component | — | — | Repo/CI review |
| NFR-042 | C | — | component | — | — | Repo/CI review |
| NFR-043 | C | — | component | — | — | Repo/CI review |
| NFR-044 | C intent / P format | — | component | — | — | Repo/CI review |
| NFR-050 | C | — | deployment | — | — | Cross-platform matrix |
| NFR-051 | C | — | deployment | — | — | Cross-platform matrix |
| NFR-060 | C | UC-03 | — | data dictionary §5 | API-13 | Privacy review |
| NFR-061 | C | UC-03 | — | data dictionary §5 | API-13 | Privacy review |
| SEC-001 | C | — | context, deployment | — | — | TC-010 |
| SEC-002 | C | UC-12 | SQ-07 | — | INT-02 | TC-006 |
| SEC-003 | C | all | — | user_role | all | AuthZ tests |
| SEC-004 | P | UC-01, UC-02 | SQ-01 | user_account.password_hash | API-01..03 | Security tests |
| SEC-005 | P | UC-01, UC-02 | SQ-01 | user_account.password_hash | API-01..03 | Security tests |
| SEC-006 | P | UC-08 | SQ-03 | — | INT-01, C2S_Hello | TC-002 |
| SEC-007 | C (analyse) / P | — | — | — | all | Fuzz + rate-limit tests |
| SEC-008 | C (analyse) / P | — | — | — | all | Fuzz + rate-limit tests |
| SEC-009 | C | — | — | — | — | Secret scanning in CI |
| SEC-010 | C (analyse) / P | UC-16, UC-19 | — | audit_log | API-72 | Audit tests |
| SEC-011 | P | UC-06 | SQ-02 | room.active_code | API-31 | TC-015 |
| SEC-012 | P | — | SQ-03, SQ-07 | — | INT-01, INT-02 | Service auth tests |
| SEC-013 | TBD | UC-09 | SQ-04 | — | C2S_LaunchInput | TBD |
| SEC-014 | P | — | — | — | protocol §7 | Flood test |
| OPS-001 | C | — | deployment | — | — | Ops checklist |
| OPS-002 | P | — | deployment | — | — | Ops checklist |
| OPS-003 | P | — | deployment | — | — | Ops checklist |
| OPS-004 | C (backups) / P (tests) | — | deployment | backups | — | Restore test |
| OPS-005 | C | — | deployment | — | — | TC-010 port scan |
| OPS-006 | P | — | — | migrations | — | Deploy rehearsal |
| OPS-007 | C | — | — | — | — | Load test report |
