# Design Change Proposals (changes to confirmed decisions)

| Document ID | DOC-CHG-001 | Status | **Each item awaits user decision** — nothing here is applied silently |
|---|---|---|---|

Format per Brief rule: existing decision → proposal → evidence → advantages → disadvantages → recommendation.

## CHG-01 Launch: linear "×10" vs saturating curve
| Field | Content |
|---|---|
| Existing (C) | Rapid presses in 5 s; **5 successful presses = 50 RPS** (reference example). Read literally: 10 RPS per press, linear. |
| Proposal | Keep rapid-press and the 5→50 anchor; use a **saturating curve** `RPS(n) = 20 + 130·(1 − e^(−n/19.06))` (min 20, max 150) plus a counted-press rate cap of 12 Hz. |
| Evidence | Official launchers measure launch strength (R-19) and stronger launches have diminishing physical returns (rip-cord/launcher limits); no source gives a formula (INT). Linear growth has no natural ceiling. |
| Advantages | Linear: 30 presses (6/s, normal human) = 300 RPS, 60 presses = 600 RPS → a 12× spread between players; macro/autoclicker gains are unbounded. Curve: 30 presses → 123 RPS, 60 → 144 RPS: skill still rewarded, extremes compressed, device differences shrink. |
| Disadvantages | Less intuitive than "1 press = 10 RPS"; very fast tappers gain less. |
| Recommendation | Adopt curve (ADR-015). Alternative kept: linear with hard cap at 15 presses (150 RPS) — simpler but flat above 15 presses (no reward for >3 presses/s), which removes most skill expression. |

## CHG-02 Attributes: keep four, add component properties (not attributes)
| Field | Content |
|---|---|
| Existing (C) | Primary attributes Attack, Defense, Stamina, Magic; Energy derived. |
| Proposal | **Keep the four unchanged.** Add **component properties** that are *not* attributes and *not* in Energy: `mass`, `lock_strength` (burst resistance), `mobility`, `height`, `contact_profile`, `spin_direction`. |
| Evidence | Official/near-official: burst rates vary by configuration (R-09), burst stopper (R-10), Bit determines movement and burst resistance, Ratchet height/CoG (R-12), weight from metal wheel (R-14). In real tops, burst resistance is a separate property from defensive shape (R-11). |
| Advantages | Allows "Defense type with weak lock" or "Attack with strong lock" builds — real strategic variety; avoids overloading DEF with three meanings. |
| Disadvantages | More numbers for players; UI must show them simply (icons/bars). |
| Recommendation | Adopt. Do **not** add a fifth attribute. |

## CHG-03 Magic: scope restricted to the skill system
| Field | Content |
|---|---|
| Existing (C) | Magic is a primary attribute contributing to Energy; influence on abilities to be investigated. |
| Proposal | Magic affects **only** skills: gauge charge rate (×0.85–1.15), skill potency (×0.80–1.20), and resistance to opponent skill effects. It never changes base collision physics. Energy weight 0.8 (others 1.0). Name stays "Magic" in UI (alternative "Spirit" offered). |
| Evidence | No official Beyblade attribute named Magic exists (INT). Official precedents for a *charge-then-unleash* special power: Hasbro app Avatar attacks (R-18), EVOBATTLE skills (R-17), XONE gauges (R-16); anime special moves. |
| Advantages | Prevents Magic from being a hidden fourth damage stat; gives a clear identity; bounded influence keeps physics readable. |
| Disadvantages | Players who expect "Magic = damage" must learn its role; weight 0.8 is a judgement. |
| Recommendation | Adopt; weight validated in playtests (ADR-013). |

## CHG-04 Elimination set: Burst primary + ring-out + spin finish
| Field | Content |
|---|---|
| Existing (C) | v0.1: ring-out eliminates (FFA), last top wins. v0.2: **Burst Finish is the primary elimination mechanic.** |
| Conflict | Both are confirmed; the brief does not say whether ring-out still eliminates, or what happens when a top stops spinning. |
| Proposal | Four finish types, all eliminate: **BURST** (primary, most common by design), **OVER** (ring-out into pocket/out of bounds — keeps v0.1 rule), **SPIN** (current spin < stop threshold), **XTREME** (ring-out via special zone, cosmetic/score distinction). |
| Evidence | Official finishes (R-05). Without SPIN finish a stopped top would stay "alive" forever (spin is a tracked variable). |
| Advantages | Faithful to established rules; Stamina types win by outlasting (SPIN), Attack by BURST/OVER — supports the type triangle. |
| Disadvantages | "Primary" becomes a tuning target (Burst share of finishes ≥ 40% target, NFR-070), not a guarantee. |
| Recommendation | Adopt; user to confirm whether XTREME zone exists in MVP arena (OQ-CB-03). |

## CHG-05 Supersede ADR-003 (backend stack)
Existing: TypeScript/Node proposed (never approved). Proposal: **PHP 8.x + Laravel 13 + Reverb** for Backend/API; Godot headless remains the real-time Match Server. Full objective comparison in ADR-012 (Laravel leads even when the "familiarity" criterion is removed). Recommendation: adopt ADR-012; ADR-003 → Superseded.

## CHG-06 Internal Backend ↔ Match Server channel
Existing (P): Match Server holds a WebSocket control channel to Backend. Proposal: **heartbeat-pull over HTTP** (1 Hz) carrying commands in the response, because PHP-FPM is stateless. Adds ≤ 1 s to allocation/reconnect. Recommendation: adopt (ADR-012 §5).
