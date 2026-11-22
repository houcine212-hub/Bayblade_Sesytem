# ADR-008: Cross-platform build, compatibility matrix & update policy
- **Status:** Proposed · **Date:** 2026-11-21
## 1. Strategy
One Godot project; export presets per platform; CI builds Linux server + Windows/Linux/Android clients on Linux runners; macOS/iOS builds require a macOS machine with Xcode (Apple requirement) [S8].
## 2. Compatibility matrix (draft — minimum versions TBD OQ-PL-01)
| Platform | Input | Renderer [P] | Distribution (TBD) | Release constraints |
|---|---|---|---|---|
| Windows | KB+M (gamepad later) | Forward+ / Mobile renderer (high/low presets) | Own site / itch.io / Steam | Code-signing recommended to avoid SmartScreen warnings |
| Linux | KB+M | Forward+ / Compatibility | Own site / itch.io / Steam | Few extra constraints |
| macOS | KB+M | Forward+ (Metal via MoltenVK or native Metal per version — verify) | Own site / Steam / Mac App Store | Signing + notarization (Apple developer account) |
| Android | Touch | Mobile renderer | Google Play (closed testing → production) | Target-API requirements of Google Play; Gradle build / keystore [S9] |
| iOS | Touch | Mobile renderer | App Store / TestFlight | macOS + Xcode; paid Apple developer programme; App Review; login-method rules (OQ-AC-01) |
| Server | — | headless (no rendering) | VPS | Dedicated server export of the same project [S10] |
## 3. Parity rules
Same rules/protocol on all platforms; quality presets differ only visually. Launch input fairness across touch vs keyboard is a **game design issue** (OQ-GP-02) — prefer timing-based mechanics over raw press-rate.
## 4. Mobile-specific
Safe areas, aspect ratios 16:9–21:9 and tablets, thermal throttling (cap 30/60 FPS options), app backgrounding = disconnect (SQ-08), network switching Wi-Fi↔cellular.
## 5. Update / version policy (Brief §M-14)
- `protocolVersion` must match exactly between client and Match Server; Backend groups rooms by protocolVersion.
- `minClientVersion` per platform in `GET /meta/client-policy`; below → 426 + store link.
- Rollout: start new Match Server pool on new version alongside old, let old pool drain (`Drain` message), then bump minimum client version. Store review delays (iOS) mean **two protocol versions may need to run simultaneously** for days.
## Revisit when
First platforms are chosen (OQ-PL-02); web build requested.
