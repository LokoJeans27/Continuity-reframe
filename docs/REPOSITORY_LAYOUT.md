# Repository layout

Run commands from the repository root, where `cinema.py` is located.

| Folder | Contents |
| --- | --- |
| `src/continuity_reframe/` | Python implementation: preparation, build, collection, comparison and camera helpers |
| `ui/` | Browser camera selector and optional camera-intent template/builder |
| `examples/camera_intent/` | Synthetic frame, Gaussian proxy, ready-to-open viewer and reproducible generator; no real-scene reconstruction |
| `configs/` | Scene template, camera presets and isolated-install constraints |
| `workflows/` | ComfyUI API and visual workflow templates |
| `custom_nodes/h3_camera_brief/` | Optional ComfyUI camera-text node |
| `docs/` | Quickstart, installation, model/rights documentation and illustrative images |
| `evidence/` | Current inventory, provenance and validation records |
| `evidence/history/` | Previous inventory retained as historical evidence; not the current file index |
| `tests/python/` | Python contract and regression tests |
| `tests/js/` | Selector DOM tests and their historical fixture |
| `skills/` | Portable continuity-review skill and its sampler tests |

The root `cinema.py`, `choose_camera.py` and `attach_camera.py` preserve previous CLI commands. The root Python modules also retain import compatibility, including `visual.py`. Their implementations now live under `src/continuity_reframe/`; edit those implementations rather than duplicating code in the entry points.

Open `ui/camera_picker.html` for the selector. The old root `camera_picker.html` forwards there and provides a direct link. The redirect is a compatibility aid, not a new automatic image provider.

Configuration, templates and tests now use their folder paths. Generated project and run files keep their previous filenames and formats. Existing `run.json` files contain absolute local paths and are not made portable by moving this repository. Do not move an existing project/run folder without inspecting those paths.

The current inventory is [evidence/INVENTORY.json](../evidence/INVENTORY.json). The [reorganization map](../evidence/REORGANIZATION.json) records previous and current paths. Historical validation records describe their original layouts and test dates; they are preserved as evidence, not silently rewritten as new test results.

All original checkout files were retained during this reorganization. No private project/run files, models, caches or credentials are part of the repository.
