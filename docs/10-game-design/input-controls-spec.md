# Input & Controls Specification — Joystick, Skill Button, Launch Zone

| Document ID | DOC-CTRL-001 | Version | 0.2 | Status | Joystick & skill button [C]; mappings & physics [P] |
|---|---|---|---|---|---|---|---|

## 1. Confirmed
- Every player has a **360° analog directional joystick** during battle to steer direction and trajectory; works on touch, keyboard/mouse and controllers; responsive and correctly synchronised.
- A **Skill button** on the **opposite side** of the joystick activates the Bey's special ability.
- Precedent: the official licensed game BEYBLADE X XONE gives players in-battle commands ("Active Move … to perform an Attack or Counter", O-5, verified); Hasbro digital-control tops (R-18, search index only). Physical tops are not steerable; 360° steering is a deliberate game-design addition [C].

## 2. Control vector
`u = (x, y)`, `|u| ≤ 1`, arena plane, camera-relative. Sent quantised as two int8 values (−127…127) → 254² directions/magnitudes.

## 3. Device mappings [P]
| Device | Direction | Skill | Launch |
|---|---|---|---|
| Mobile (default right-handed) | Floating virtual joystick, **left** half of screen, radial dead-zone 10% | Button **right** side, ≥ 12 mm | Large launch zone, right/centre |
| Mobile left-handed | Mirrored layout (option) | Left side | Mirrored |
| Gamepad | Left stick, radial dead-zone 0.15, response curve `m' = ((m−0.15)/0.85)^1.3` | South/R1 (remappable) | South button |
| Keyboard only | WASD/arrows → 8 directions, ramp 0→1 over 120 ms for pseudo-analog | Space / J | Space / K (rebindable) |
| Mouse + keyboard (default desktop) | **Mouse vector mode:** direction from own top (screen) to cursor, magnitude = distance / 150 px (clamped) → true analog | Right mouse / Space | Left click in zone or Space |
Keyboard-only is digital; it is acceptable because steering force is capped identically for all devices.

## 4. Steering physics (server-authoritative) [P]
```
F_ctrl = F_max · u · mobility · Stab(spin) · (1 − stagger)
v_cap  = v_max · (0.6 + 0.4·mobility)
spin cost per second += c_ctrl · |u| · mobility   (reduced by STA through decay formula)
```
- Steering cannot exceed `v_cap`; it shapes trajectory, it does not override collisions.
- **Stagger:** after a hit with normalised impact N, control authority × (1 − 0.5·min(1, N)) for 0.3 s.
- Stamina/Defense builds (low mobility) steer less → they rely on positioning; Attack builds steer hard but pay spin.

## 5. Network synchronisation [P] (details in `../04-interfaces/multiplayer-protocol.md`)
- Client sends `C2S_ControlInput {seq, tick, x, y}` at 30 Hz on an unreliable-sequenced channel; each packet repeats the last 3 inputs (loss tolerance).
- **Client-side prediction for the player's own top** (movement only) with server reconciliation; other tops interpolated (~100 ms buffer). Collisions, spin, burst are never predicted as final — shown when the server confirms.
- Target: own-input-to-visual response ≤ 100 ms on device (NFR-011) regardless of RTT, via prediction.
- Server clamps `|u| ≤ 1`, drops inputs > 60/s, ignores spectators.

## 6. Skill button behaviour
Pressing sends `C2S_SkillActivate {seq}`; client plays a short "requested" feedback; effect and VFX start on `S2C_SkillEvent` (≈ RTT). Rules in `skills-spec.md`.
