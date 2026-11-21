# Glossary

| Term | Definition |
|---|---|
| **Attribute (primary)** | Attack, Defense, Stamina or Magic (0–100), computed from parts. |
| **Advantage S** | Pairwise value in (−1,1) combining Energy gap and current-spin gap (combat spec §3). |
| **Arena** | The bowl-shaped play area in which tops battle. Leaving it = ring-out. |
| **Balance type** | Primary type with near-equal ATK/DEF/STA shares. |
| **Burst Finish** | Elimination when Lock Integrity reaches 0 (components separate). Primary elimination. |
| **Backend (Backend API)** | HTTP(S)/WebSocket service owning accounts, profiles, inventory, rooms, history, teams, moderation. Only service that accesses MySQL. |
| **CCU** | Concurrent connected users (connected to Backend and/or a match). |
| **Competitor** | A room/match participant with a top in the battle. Max 5 per match. |
| **Content version** | Version identifier of balance/item data used by a match. |
| **Component property** | Non-attribute part value: mass, lock strength, mobility, friction, height, contact profile, spin direction. |
| **Elimination** | Removal of a competitor: BURST, OVER, XTREME or SPIN finish. |
| **Energy** | Derived overall power from the four attributes; not an attribute. |
| **FFA** | Free-for-All: every competitor for themselves. |
| **Friendly match** | Match without any stake. |
| **Host** | Room creator, allowed to start the match [A-02]. |
| **Item definition** | Catalogue entry describing a top or part and its stats. |
| **Inventory item** | A player-owned instance of an item definition. |
| **Launch** | The act that puts a top into the arena with an initial spin based on input + stats. |
| **Launch window** | The 5-second period in which successful presses are counted. |
| **Launch RPS** | Initial rotation from the launch curve (20–144.4 RPS). |
| **Lock Integrity** | 0–100 per-match burst gauge; damage accumulates from strong impacts. |
| **Magic** | Primary attribute governing skill charge, potency and skill resistance. |
| **Loadout** | A player's chosen top configuration for a match. |
| **Loadout snapshot** | Immutable copy of the loadout and stats used in a specific match. |
| **Match** | One battle instance from pre-launch to result. |
| **Match Server** | Headless Godot process that runs an authoritative match. |
| **Match ticket** | Short-lived signed token authorising one user to connect to one match in one role. |
| **MatchSide** [P] | In-match grouping for Team Battle; distinct from social Team. |
| **Orchestrator (Match Allocator)** | Backend module tracking Match Server instances and assigning matches. |
| **Organizer** | Player approved by Admin to create tournaments. |
| **Protocol version** | Integer identifying the client↔Match Server message format; must match exactly. |
| **Ring-out** | A top leaving the arena boundary. |
| **Room** | Pre-match gathering place identified by a room code; owned by Backend. |
| **Room code** | Shareable short code to join a room. |
| **RPO / RTO** | Recovery Point / Time Objective: max data loss / max downtime after failure. |
| **Snapshot** | Periodic server→client message with authoritative state of all tops. |
| **Spectator** | Participant that receives match state but sends no gameplay input. |
| **Spin (current)** | Remaining rotation in RPS during battle; not the Stamina attribute. |
| **Spin rate / RPS** | Rotations per second (1 RPS = 60 RPM). |
| **Skill gauge** | 0–100 charge needed to activate a skill. |
| **Stamina (attribute)** | Resistance to spin loss; static per build. |
| **Successful press** | A launch press meeting all counting rules (launch spec §3). |
| **Subtype** | Property-based specialisation (SMASH, UPPER, ANCHOR, ABSORB, ENDURANCE, EVASIVE, ADAPTIVE). |
| **Team** | Persistent social group with leader(s) and members. |
| **Tick** | One fixed step of the server simulation. |
| **VPS** | Virtual private server (candidate: Hostinger KVM). |
| **Warm pool** | Pre-started idle Match Server processes ready to take a match. |
