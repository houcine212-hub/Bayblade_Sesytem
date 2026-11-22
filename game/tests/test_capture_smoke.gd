## Headless smoke test: loads the S-5 capture scene, simulates a trial with synthetic
## key events and checks the CSV output. Timing is simulated by shifting w0_us.
## Run: godot --headless --path game --script res://tests/test_capture_smoke.gd
extends SceneTree


func _initialize() -> void:
	_run.call_deferred()


func _key(pressed: bool, echo: bool = false) -> InputEventKey:
	var k := InputEventKey.new()
	k.keycode = KEY_SPACE
	k.pressed = pressed
	k.echo = echo
	return k


func _run() -> void:
	var ok := true
	var scene: Node = load("res://spikes/s5_launch_input/s5_capture.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.participant.text = "SMOKE"
	scene._on_start()
	# READY phase: press must not count (TC-L08)
	scene._input(_key(true)); scene._input(_key(false))
	# Enter the window and press 3 times, 200 ms apart, plus one echo and one held repeat
	var base := Time.get_ticks_usec()
	for i in 3:
		scene.w0_us = Time.get_ticks_usec() - (100_000 + i * 200_000)
		scene._input(_key(true))
		scene._input(_key(true, true))   # echo -> NOT_EDGE
		scene._input(_key(false))
	if scene.counter.accepted != 3:
		ok = false; printerr("FAIL accepted=%d (expected 3)" % scene.counter.accepted)
	# Jump past window + release and let _process finish the trial
	scene.w0_us = Time.get_ticks_usec() - 6_000_000
	await process_frame
	await process_frame
	if scene.phase != scene.Phase.RESULT:
		ok = false; printerr("FAIL phase not RESULT")
	var files := DirAccess.get_files_at("user://s5")
	var csv := ""
	for f in files:
		if f.begins_with("SMOKE_"):
			csv = "user://s5/" + f
	if csv == "":
		ok = false; printerr("FAIL no CSV written")
	else:
		var lines := FileAccess.get_file_as_string(csv).strip_edges().split("\n")
		var verdicts := {}
		for l in lines.slice(1):
			var v := l.split(",")[9]
			verdicts[v] = verdicts.get(v, 0) + 1
		print("CSV ", ProjectSettings.globalize_path(csv), " rows=", lines.size() - 1, " verdicts=", verdicts)
		if verdicts.get("ACCEPTED", 0) != 3 or verdicts.get("BEFORE_WINDOW", 0) != 1 or verdicts.get("NOT_EDGE", 0) != 3:
			ok = false; printerr("FAIL verdict counts")
		DirAccess.remove_absolute(csv)
	print("S-5 capture smoke test: ", "PASS" if ok else "FAIL")
	quit(0 if ok else 1)
