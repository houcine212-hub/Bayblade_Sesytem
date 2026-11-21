# Authentication & Role/Permission Model

| Document ID | DOC-SEC-002 | Status | [P] — role names TBD (OQ-AC-05) |
|---|---|---|---|

## 1. Authentication [P]
- **Confirmed:** e-mail + password; unique display name; third-party authentication postponed (check App Store rules on sign-in options before the later iOS release).
- Passwords hashed with Laravel `Hash` (Argon2id driver proposed, bcrypt acceptable); e-mail verification required before ranked/social features [P]; password reset by signed single-use link.
- Access token: Laravel **Sanctum** personal access token (opaque, stored hashed), 15-min expiry, abilities scoped. Refresh token: opaque 256-bit, stored hashed in `auth_session`, 30 days, rotated each use (reuse → revoke family).
- Suspended accounts: login returns 403 ACCOUNT_SUSPENDED with end time.
- Tokens stored on device in the app's user data folder; acceptable for a game (not banking); revisit for platform keychain later.

## 2. Roles
Global roles (table `user_role`): **MODERATOR, ADMIN, ORGANIZER**. PLAYER is implicit for every ACTIVE account. **TEAM_LEADER** is derived from `team_membership.role` (scoped to one team). **Owner** = ADMIN held by the game owner; at least one ADMIN must always exist.

## 3. Permission matrix (proposed)
| Action | Player | Team Leader (own team) | Organizer | Moderator | Admin |
|---|---|---|---|---|---|
| Play, rooms, loadouts, own profile | ✔ | ✔ | ✔ | ✔ | ✔ |
| Create team | ✔ (eligibility TBD) | — | ✔ | ✔ | ✔ |
| Invite/remove members, edit team, transfer, dissolve | — | ✔ | — | — | ✔ (moderation only) |
| Report / block | ✔ | ✔ | ✔ | ✔ | ✔ |
| View report queue, apply WARN/MUTE/SUSPEND/RENAME | — | — | — | ✔ | ✔ |
| BAN (permanent) | — | — | — | — (propose to admin) | ✔ |
| Apply for organizer | ✔ (rank threshold TBD) | ✔ | — | ✔ | — |
| Approve/revoke organizer | — | — | — | — | ✔ (BR-006) |
| Create tournament (post-MVP) | — | — | ✔ | — | ✔ |
| Grant/revoke roles | — | — | — | — | ✔ |
| View audit log | — | — | — | own actions | ✔ |

Every ✔ is checked in the Backend handler (BR-007); the client only hides buttons for convenience.

## 4. Organizer approval workflow (FR-121/122)
`PENDING → APPROVED | REJECTED`, `APPROVED → REVOKED`. Approval adds ORGANIZER role and writes `audit_log(action=ORGANIZER_APPROVED)` in the same transaction.
