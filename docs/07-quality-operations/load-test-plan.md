# Load & Concurrent-Match Test Plan

| Document ID | DOC-QA-002 | Status | [P] — **no capacity is claimed until these pass** |
|---|---|---|---|

## 1. Environment
Staging VPS identical to candidate production plan. Bot clients run on separate machines (not on the VPS) to avoid skewing CPU. Bots use the real protocol (headless Godot bot mode).

## 2. Population tests (NFR-004)
| Step | Connected users | Mix (example) | Duration |
|---|---|---|---|
| L-10 | 10 | 5 in 1 match, 5 in lobby/menus | 30 min |
| L-25 | 25 | 3 matches (15), 10 lobby | 30 min |
| L-50 | 50 | 7 matches (35), 15 lobby | 60 min |
| L-100 | 100 | 16 matches (80), 20 lobby/profile browsing | 60 min + 4 h soak |

## 3. Concurrent-match tests (NFR-005)
| Test | Matches | Notes |
|---|---|---|
| M-5 | 5 × 5 competitors | warm-up |
| M-10 | 10 × 5 | |
| M-20 | **20 × 5 (theoretical maximum at 100 CCU)** | + 2 spectators each in a variant |
| M-churn | continuous start/finish for 1 h | allocation, reset, memory leaks |

## 4. Impairment variants
RTT 50/150/250 ms, loss 0/2/5%, jitter 20 ms (netem on bot hosts).

## 5. Pass criteria (provisional — confirm with user)
| Metric | Target |
|---|---|
| Match Server tick time p99 | < 50% of tick budget (60 Hz → < 8.3 ms) |
| Snapshot send rate | ≥ 95% of configured rate |
| VPS CPU (sustained) | < 70% |
| RAM | < 80%, no growth over soak |
| API p95 | ≤ 300 ms; error rate < 0.5% |
| Join time p95 (Start → PRE_LAUNCH) | ≤ 5 s |
| Result persistence | 100% of completed matches persisted exactly once |
| Disconnect rate (no impairment) | < 1% |

## 6. Outputs
Per-test report: config, versions, graphs (CPU, RAM, net, tick time, API latency), pass/fail, and resulting VPS sizing recommendation (ADR-010).
