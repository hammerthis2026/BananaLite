# Banana Lite

A performance-focused experimental Android fork of [Banana Native](https://git.eden-emu.dev/moceure/BananaNative) for compatible ARM64 devices, with particular attention to older GPUs and memory-constrained phones.

## Project status

**v0.2 — device-tested prototype.** Donkey Kong Bananza is playable on the initial test device. The previously reported purple screen no longer appears in that test. Tester-reported performance is typically around 20 FPS, reaching 30 FPS in some areas. These are informal observations, not controlled benchmarks.

**v0.3 — experimental development.** Changes have been committed but are not yet validated on a device.

## Features and performance profiles

- Distinct Banana Lite icon and dark branding.
- Per-game performance presets and rendering recovery controls.
- Optional save backups and frame generation status indicators.
- Experimental lower-resolution options and upscaling.
- Runtime log sharing and existing custom game cover support.

| Profile | v0.3 intended resolution | FPS cap |
| --- | --- | --- |
| Ultra Lite | 360p | 30 |
| Balanced | 540p | 30 |
| Performance | 720p | 60 |
| Custom | Adjustable | Adjustable |

FPS caps are not performance guarantees. Feature availability and compatibility vary by device and build.

## Known issues

- Black character materials during some animations, including banana collection.
- Missing or incorrectly rendered textures and geometry.
- Pixelated graphics and inconsistent frame times.
- LSFG may remain unavailable even with a DLL present.
- In-app updates are not yet operational end to end.

## Roadmap

### v0.3
- Investigate and correct black materials and missing geometry.
- Improve image clarity and native performance without sacrificing rendering accuracy.
- Improve LSFG diagnostics and compatibility.
- Make diagnostic log export easier.
- Complete the library, cover art presentation, settings and theme redesign.

### v0.4
- Automatic versioned builds and release publishing.
- Permanent APK signing and tested save-preserving upgrades.
- In-app update checking, download progress, release notes and installation confirmation.

## Download and testing

Check [GitHub Actions](https://github.com/hammerthis2026/BananaLite/actions/workflows/android.yml) for experimental build artifacts. Select a successful run, download its artifact ZIP and extract the APK. To build manually, use Run workflow with Ubuntu 24.04; macOS alternatives are available.

Back up saves before installing. Signing compatibility between experimental builds is not guaranteed. See [release instructions](docs/RELEASING.md).

## Initial test device

Snapdragon 732G, Adreno 618, 6 GB RAM, Turnip. This is a test configuration, not a hardware requirement.

## Upstream and licensing

Based on Banana Native. The build workflow fetches a pinned upstream revision and applies Banana Lite patches. Original upstream licensing and redistribution obligations apply. Do not upload proprietary game files, keys or DLLs.


## v0.4 development targets

- Distinct library, settings and game-details UI; automatic embedded game artwork with fallback placeholder.
- Explicit play, game settings and update actions; hardware-aware presets.
- Battery-independent app performance policy, respecting Android thermal and power limits.
- In-app release updates with signing compatibility checks.
- Investigate black materials and DK textures; validate real LSFG output on supported devices.

These are planned changes, not implemented features. v0.3 user testing reported approximately 20 FPS on Snapdragon 732G at 12% battery.
