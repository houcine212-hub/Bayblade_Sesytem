## Headless unit tests for the S-5 launch counter.
## Run: godot --headless --path game --script res://tests/test_launch_counter.gd
extends SceneTree

var failures: int = 0
var checks: int = 0


func check(cond: bool, name: String) -> void:
	checks += 1
	if not cond:
		failures += 1
		printerr("FAIL: ", name)


func _init() -> void:
	# TC-016 / TC-038 / TC-L01 / TC-L02 — RPS = max(20, 10 × n) (OQ-LN-08)
	var expected := {0: 20, 1: 20, 2: 20, 3: 30, 5: 50, 10: 100, 15: 150, 25: 250, 35: 350, 36: 350, -1: 20}
	for n in expected:
		check(LaunchCounter.launch_rps(n) == expected[n], "launch_rps(%d) == %d" % [n, expected[n]])

	# TC-L03 interval floor in integer µs: 142 856 rejected, 142 857 accepted
	var c := LaunchCounter.new()
	check(c.offer(0) == LaunchCounter.Verdict.ACCEPTED, "press at W0 accepted")
	check(c.offer(142_856) == LaunchCounter.Verdict.TOO_SOON, "142 856 µs rejected")
	check(c.offer(142_857) == LaunchCounter.Verdict.ACCEPTED, "142 857 µs accepted")
	check(c.accepted == 2, "two accepted")

	# TC-L04 half-open window; TC-L08 READY-phase presses not counted
	c.reset()
	check(c.offer(-1) == LaunchCounter.Verdict.BEFORE_WINDOW, "READY-phase press rejected")
	check(c.offer(5_000_000) == LaunchCounter.Verdict.AFTER_WINDOW, "press at W0 + 5000 ms rejected")
	check(c.offer(4_999_999) == LaunchCounter.Verdict.ACCEPTED, "press at W0 + 4999.999 ms accepted")

	# TC-032 cap: 35 presses at the floor fit in the window, a 36th is rejected
	c.reset()
	var t: int = 0
	for i in 35:
		check(c.offer(t) == LaunchCounter.Verdict.ACCEPTED, "press %d at floor accepted" % (i + 1))
		t += LaunchCounter.MIN_INTERVAL_US
	check(c.accepted == 35 and c.rps() == 350, "35 presses -> 350 RPS")
	# 35 × 142 857 µs = 4 999 995 µs < 5 000 000: in integer µs a 36th press at the floor is
	# still inside the window, so the explicit cap (not the window) must reject it.
	check(t == 4_999_995, "36th press at floor lands at 4 999 995 µs (inside window)")
	check(c.offer(t) == LaunchCounter.Verdict.CAP_REACHED, "36th press rejected by cap")

	# Mashing faster than the floor is clipped, never inflated
	c.reset()
	for i in 5000:
		c.offer(i * 1_000)    # 1000 presses/s for 5 s (macro-like)
	check(c.accepted == 35, "1000/s mashing -> 35 accepted (got %d)" % c.accepted)
	c.reset()
	for i in 200:
		c.offer(i * 25_000)   # 40 presses/s: only every 6th press (150 ms) clears the floor
	check(c.accepted == 34, "40/s mashing -> 34 accepted (got %d)" % c.accepted)

	# TC-L06 key repeat / held key -> one press; release required per source
	var e := EdgeTracker.new()
	check(e.press("key:space"), "first down is an edge")
	check(not e.press("key:space", true), "echo is not an edge")
	check(not e.press("key:space"), "held key without release is not an edge")
	e.release("key:space")
	check(e.press("key:space"), "down after release is an edge")
	check(e.press("touch:1"), "independent source has its own edge state")

	print("S-5 counter tests: %d checks, %d failures" % [checks, failures])
	quit(1 if failures > 0 else 0)
