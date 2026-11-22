# Product Scope

| Document ID | DOC-SCO-001 | Status | Draft — scope boundaries are [P] until approved at Gate G0 |
|---|---|---|---|

## 1. Scope tiers
| Tier | Meaning |
|---|---|
| **MVP-Core** | Required for the first playable online release (internal alpha → public MVP) |
| **MVP-Social** | Small social layer required for public MVP |
| **Post-MVP** | Planned, explicitly scheduled after MVP |
| **Excluded** | Not allowed in MVP by the user |

## 2. Feature scope (recommended)
| Feature | Tier | Basis |
|---|---|---|
| Shared account, login, sessions | MVP-Core | [C] need, [P] tier |
| Player profile (view) | MVP-Core | [C] |
| Starter top + basic loadout selection | MVP-Core | [C] K1 / [A] A-04 |
| Create room, room code, join by code, ready | MVP-Core | [C] |
| ≤5 competitors per match | MVP-Core | [C] |
| FFA, ring-out, last-top-wins | MVP-Core | [C] |
| Launch mechanic — 5 s rapid press | MVP-Core | [C] v0.2 |
| 360° joystick steering + Skill button | MVP-Core | [C] v0.2 |
| Attributes ATK/DEF/STA/MAG, derived Energy, types, opponent-relative combat, Burst Finish | MVP-Core | [C] v0.2 concepts / [P] formulas |
| Server-authoritative match & result | MVP-Core | [C] |
| Spectating (eliminated players + room spectators) | MVP-Core | [C] eliminated / [P] room spectators |
| Match history | MVP-Core | [C] |
| Monitoring & error logging | MVP-Core | [C] |
| Client version compatibility gate | MVP-Core | [P] |
| Competitive record (W/L, placements) | MVP-Social | [P] |
| Rank / rating | MVP-Social (simple) or Post-MVP (rated) | [TBD] OQ-AC-04 |
| Block + report + minimal moderation tools | MVP-Social | [C] design needed / [P] tier |
| Basic teams (create, invite, leave, leader) | MVP-Social (recommended last item; can slip) | [P] |
| Organizer application + admin approval | Post-MVP (data model ready in MVP) | [C] concept |
| Tournaments | Post-MVP | [C] concept |
| Exploration vertical slice | Post-MVP (milestone M5) | **[C] v0.2: postponed beyond Battle MVP** |
| Team Battle mode | Post-MVP | [TBD] rules |
| Loot/chests economy | Post-MVP | [C] postponed |
| Proximity voice chat | Post-MVP | [C] later |
| Voice commands for tops | Post-MVP | [C] later |
| Virtual-item stakes | Post-MVP, only after explicit approval | [C] |
| Real-money wagering | **Excluded** | [C] |
| Facebook/Messenger integration | Excluded (links only, if approved) | [C] no API confirmed |
| Web-browser client | Not in scope | [A] A-08 |

## 3. Why exploration is recommended post-MVP [P]
Exploration needs a first-person controller, a world level, chest/loot rules, a *second* networked
mode (shared world presence), a challenge protocol and an arena transition. It roughly doubles the
networking surface and depends on the battle loop being fun first. Shipping battle-first lets us
test with real players earlier. The data model (items, inventory, sources) is designed now so
exploration can add loot without redesign.
