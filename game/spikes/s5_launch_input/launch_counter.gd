## S-5 launch press counter — pure logic, no engine input dependencies.
## Implements DOC-LAUNCH-001 §3 (accepted press) and §4 (RPS rule, owner decision OQ-LN-08).
## Throw-away M1 spike code: the Match Server validator will be written separately (M2).
class_name LaunchCounter
extends RefCounted

const WINDOW_US: int = 5_000_000        # half-open window [W0, W0 + 5 s)
const MIN_INTERVAL_US: int = 142_857    # 1000/7 ms, integer microseconds (D-04)
const MAX_PRESSES: int = 35             # provisional cap (D-04), re-selected after S-5
const MIN_RPS: int = 20                 # floor (D-03 / OQ-LN-08)
const RPS_PER_PRESS: int = 10           # D-01

enum Verdict { ACCEPTED, BEFORE_WINDOW, AFTER_WINDOW, TOO_SOON, CAP_REACHED, NOT_EDGE, OUTSIDE_ZONE }

const VERDICT_NAMES: PackedStringArray = [
	"ACCEPTED", "BEFORE_WINDOW", "AFTER_WINDOW", "TOO_SOON", "CAP_REACHED", "NOT_EDGE", "OUTSIDE_ZONE",
]

var accepted: int = 0
var _last_accepted_us: int = -1


## RPS for n accepted presses: max(20, 10 × min(n, 35)).
static func launch_rps(n: int) -> int:
	var c: int = clampi(n, 0, MAX_PRESSES)
	return maxi(MIN_RPS, RPS_PER_PRESS * c)


func reset() -> void:
	accepted = 0
	_last_accepted_us = -1


## Offer a press that already passed the edge/release and zone checks.
## t_us is measured from W0 (window start) in integer microseconds.
func offer(t_us: int) -> Verdict:
	if t_us < 0:
		return Verdict.BEFORE_WINDOW
	if t_us >= WINDOW_US:
		return Verdict.AFTER_WINDOW
	if accepted >= MAX_PRESSES:
		return Verdict.CAP_REACHED
	if _last_accepted_us >= 0 and t_us - _last_accepted_us < MIN_INTERVAL_US:
		return Verdict.TOO_SOON
	accepted += 1
	_last_accepted_us = t_us
	return Verdict.ACCEPTED


func rps() -> int:
	return launch_rps(accepted)
