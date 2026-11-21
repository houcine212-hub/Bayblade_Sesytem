# MVP Readiness Acceptance Criteria

| Document ID | DOC-QA-003 | Status | [P] — to approve with MVP scope |
|---|---|---|---|

The public MVP may launch only when:
1. All MVP-Core and MVP-Social requirements have passing acceptance tests (traceability matrix complete).
2. All blocking gameplay questions (OQ-GP-01, 02, 04, 05, 06, 15, 16, 17, 18) are decided and implemented.
3. Load tests L-100 and M-20 pass the criteria in `load-test-plan.md` on the production-sized VPS.
4. TC-008/TC-009 (server/backend failure) pass.
5. External port scan shows only 443/tcp, the UDP match range, and restricted SSH.
6. Backup + restore test completed within RTO; restore-to-new-VPS rehearsal done.
7. Monitoring dashboards and alerts active; operational owner named.
8. Privacy notice, data retention and account deletion implemented; legal review done for target markets.
9. Store requirements met for each launch platform (signing, policies, age rating).
10. Moderation tooling usable; at least one moderator trained.
11. No open Critical/High security findings.
12. Documentation synchronised with implementation (ADRs updated to Accepted/Superseded).
