## Edge + release rule (DOC-LAUNCH-001 §3.1–3.2): a press counts only on a down edge,
## and a source must be released before its next press counts. Key echo is never an edge.
class_name EdgeTracker
extends RefCounted

var _down: Dictionary = {}  # source_id -> true while held


func reset() -> void:
	_down.clear()


## Returns true if this down event is a valid edge for the source.
func press(source_id: String, is_echo: bool = false) -> bool:
	if is_echo or _down.get(source_id, false):
		return false
	_down[source_id] = true
	return true


func release(source_id: String) -> void:
	_down.erase(source_id)
