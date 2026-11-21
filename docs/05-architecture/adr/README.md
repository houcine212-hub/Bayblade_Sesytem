# Architecture Decision Records
| ADR | Title | Status |
|---|---|---|
| 001 | Godot version (4.7.x) | Proposed |
| 002 | GDScript, one project for client + server | Proposed |
| 003 | Backend: TypeScript/Node.js + Fastify | **Superseded by 012** |
| 004 | MySQL 8.4 LTS | Proposed |
| 005 | Server-authoritative custom simulation + local prediction (v0.2) | Proposed |
| 006 | One match per process, warm pool | Proposed |
| 007 | ENet/UDP transport | Proposed |
| 008 | Cross-platform build & update policy | Proposed |
| 009 | Ranking options | Open |
| 010 | Single-VPS deployment | Proposed |
| 011 | Rooms in Backend + push events (Reverb in v0.2) | Proposed |
| 012 | Backend: PHP + Laravel 13 + Reverb (heartbeat-pull internal channel); verified & risk-reviewed v0.3 | Proposed — user decision |
| 013 | Combat stats, Energy (plain mean, v0.3), RPS–Energy model, acceptance criteria AC-1…7 | Proposed (revised v0.3) |
| 014 | Burst Finish hybrid model (official facts separated) | Proposed (revised v0.3) |
| 015 | Launch curve, limits & anti-cheat limitations | Proposed (revised v0.3) |

## Sources cited in ADRs
| Ref | Source | Verified in this session? |
|---|---|---|
| S1 | Godot download archive — https://godotengine.org/download/archive/ | Yes (web search, 2026-11-21) |
| S2 | Godot 4.7.2 stable — https://godotengine.org/download/archive/4.7.2-stable/ | Yes |
| S3 | Godot release policy — https://docs.godotengine.org/en/stable/about/release_policy.html | Yes |
| S4 | High-level multiplayer — https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html | URL from docs structure; re-verify content for 4.7 |
| S5 | ENetMultiplayerPeer class — https://docs.godotengine.org/en/stable/classes/class_enetmultiplayerpeer.html | Re-verify |
| S6 | Hostinger managed VPS firewall — https://www.hostinger.com/support/8172641-how-to-use-a-managed-vps-firewall-at-hostinger/ | Yes |
| S7 | Hostinger UFW tutorial — https://www.hostinger.com/tutorials/how-to-configure-firewall-on-ubuntu-using-ufw/ | Yes |
| S8 | Exporting for iOS — https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_ios.html | Re-verify |
| S9 | Exporting for Android — https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html | Re-verify |
| S10 | Exporting for dedicated servers — https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_dedicated_servers.html | Re-verify |
| S11 | Hostinger: securing publicly accessible services on VPS — https://www.hostinger.com/support/securing-publicly-accessible-services-on-your-vps/ | Yes (search result) |
| S13 | Laravel Reverb docs — https://laravel.com/docs/master/reverb | Search index; re-verify |
| S14 | Godot 4.7 release page — https://godotengine.org/releases/4.7/ | Search index; read migration guide |
| S12 | MySQL 8.4 reference manual — https://dev.mysql.com/doc/refman/8.4/en/ | Re-verify |

"Re-verify" = cited from the official documentation site structure; the exact page content must be checked against the pinned Godot version before the ADR is accepted.
