## S-5 Launch Input Study — capture prototype (DOC-M1-001 steps 5.1–5.2).
## Records every press/release edge with a microsecond timestamp, applies the
## DOC-LAUNCH-001 counting rules and writes one CSV per trial to user://s5/.
## Throw-away spike: no networking, no server validation, no gameplay.
extends Control

const READY_US: int = 1_500_000   # D-02 READY cue, presses not accepted
const RELEASE_US: int = 500_000
const KEY_BIND: Key = KEY_SPACE
const JOY_BIND: JoyButton = JOY_BUTTON_A
const OUT_DIR := "user://s5"
const CSV_HEADER := "participant,device_label,input_class,trial,seq,source_id,edge,t_us_from_w0,frame,verdict,accepted_count,os,model"

enum Phase { SETUP, READY, WINDOW, RELEASE, RESULT }

var phase: Phase = Phase.SETUP
var counter := LaunchCounter.new()
var edges := EdgeTracker.new()
var w0_us: int = 0
var trial: int = 0
var rows: PackedStringArray = []
var raw_presses: int = 0
var seq: int = 0

@onready var zone: ColorRect = %Zone
@onready var status: Label = %Status
@onready var participant: LineEdit = %Participant
@onready var device_label: LineEdit = %DeviceLabel
@onready var input_class: OptionButton = %InputClass
@onready var start_button: Button = %Start
@onready var setup_box: Control = %Setup


func _ready() -> void:
	for c in ["touch", "keyboard", "mouse", "gamepad"]:
		input_class.add_item(c)
	start_button.pressed.connect(_on_start)
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	status.text = "S-5 launch input study. Enter participant + device, then Start."


func _on_start() -> void:
	if participant.text.strip_edges() == "":
		status.text = "Participant ID required."
		return
	trial += 1
	counter.reset()
	edges.reset()
	rows.clear()
	raw_presses = 0
	seq = 0
	setup_box.visible = false
	get_viewport().gui_release_focus()   # Space must not re-trigger the Start button
	w0_us = Time.get_ticks_usec() + READY_US
	phase = Phase.READY


func _process(_delta: float) -> void:
	if phase == Phase.SETUP or phase == Phase.RESULT:
		return
	var t := Time.get_ticks_usec() - w0_us
	if t < 0:
		phase = Phase.READY
		status.text = "READY… %d" % ceili(-t / 500_000.0)
	elif t < LaunchCounter.WINDOW_US:
		phase = Phase.WINDOW
		status.text = "PRESS!  %.1f s   accepted %d   →  %d RPS" % [(LaunchCounter.WINDOW_US - t) / 1e6, counter.accepted, counter.rps()]
	elif t < LaunchCounter.WINDOW_US + RELEASE_US:
		phase = Phase.RELEASE
		status.text = "RELEASE"
	else:
		_finish()


func _input(event: InputEvent) -> void:
	if phase == Phase.SETUP or phase == Phase.RESULT:
		return
	var t := Time.get_ticks_usec() - w0_us   # timestamp at event delivery (frame-quantised, see report)
	get_viewport().set_input_as_handled()
	if event is InputEventScreenTouch:
		_edge("touch:%d" % event.index, event.pressed, false, t, _in_zone(event.position))
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		_edge("mouse:left", event.pressed, false, t, _in_zone(event.position))
	elif event is InputEventKey and event.keycode == KEY_BIND:
		_edge("key:space", event.pressed, event.is_echo(), t, true)
	elif event is InputEventJoypadButton and event.button_index == JOY_BIND:
		_edge("joy%d:a" % event.device, event.pressed, false, t, true)


func _in_zone(pos: Vector2) -> bool:
	return zone.get_global_rect().has_point(pos)   # client-side only (DOC-LAUNCH-001 §8)


func _edge(source_id: String, pressed: bool, is_echo: bool, t: int, in_zone: bool) -> void:
	seq += 1
	if not pressed:
		edges.release(source_id)
		_row(source_id, "up", t, "")
		return
	var verdict: String
	if not edges.press(source_id, is_echo):
		verdict = "NOT_EDGE"
	else:
		raw_presses += 1
		if not in_zone:
			verdict = "OUTSIDE_ZONE"
		else:
			verdict = LaunchCounter.VERDICT_NAMES[counter.offer(t)]
	_row(source_id, "down", t, verdict)


func _row(source_id: String, edge: String, t: int, verdict: String) -> void:
	var f := [participant.text.strip_edges().replace(",", "_"), device_label.text.strip_edges().replace(",", "_"),
		input_class.get_item_text(input_class.selected), trial, seq, source_id, edge, t,
		Engine.get_process_frames(), verdict, counter.accepted, OS.get_name(), OS.get_model_name().replace(",", "_")]
	rows.append(",".join(f.map(func(v): return str(v))))


func _finish() -> void:
	phase = Phase.RESULT
	var stamp := Time.get_datetime_string_from_system(true).replace(":", "-")
	var path := "%s/%s_%s_t%d_%s.csv" % [OUT_DIR, participant.text.strip_edges().replace(",", "_"),
		input_class.get_item_text(input_class.selected), trial, stamp]
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file:
		file.store_line(CSV_HEADER)
		for r in rows:
			file.store_line(r)
		file.close()
	status.text = "Trial %d: %d raw presses, %d accepted → %d RPS\nSaved %s" % [
		trial, raw_presses, counter.accepted, counter.rps(), ProjectSettings.globalize_path(path) if file else "(write failed)"]
	setup_box.visible = true
