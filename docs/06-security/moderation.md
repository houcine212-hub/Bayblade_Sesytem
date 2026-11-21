# Abuse, Reporting & Moderation Design (MVP-sized)

| Document ID | DOC-SEC-003 | Status | [P] |
|---|---|---|---|

## 1. Player tools
- **Block** (FR-130): blocked user cannot invite you to teams or (if chat exists) message you; you can still meet in public rooms only if room visibility allows (TBD).
- **Report** (FR-131): from profile, room list, or post-match screen; reason ∈ {CHEATING, HARASSMENT, OFFENSIVE_NAME, OTHER} + optional 1000-char text + automatic match reference. Rate limit: e.g. 10 reports/day/user.

## 2. Moderator workflow
Queue sorted by age and number of reports per target → view report, target history, related match summary → action {WARN, MUTE, SUSPEND(duration), RENAME, propose BAN} → report status ACTIONED/DISMISSED → audit entry. The user sees the sanction (`account.sanctioned` event / login error).

## 3. Tooling for MVP
A minimal **web admin page** or protected API used via a simple internal tool [P]; no in-game moderator UI needed.

## 4. Appeals
MVP: manual, via an official contact address listed in-game; moderator records outcome as `LIFT` action. Formal workflow post-MVP (FR-134).

## 5. Out of scope for MVP
Automated chat filtering beyond a name blocklist, voice moderation (voice is post-MVP), automated cheat detection.

## 6. Voice features (future) — required assessment before introduction
Platform microphone permissions (Android/iOS), consent & age requirements, recording/retention policy, reporting of voice abuse, latency and bandwidth, accessibility alternative for voice commands (buttons must remain), speech-recognition privacy (on-device vs cloud).
