# Quickstart: use an existing ComfyUI installation

**Before starting:** provide a continuous video with an audio stream and at least approximately 5.167 seconds for the default124-frame clip at24fps. Have a working ComfyUI installation, four H3 weights, Python with NumPy/OpenCV and FFmpeg/ffprobe. Start the local server before doctor. A separately installed package/server test is documented in docs/ALTERNATIVE_INSTALL.md; it reused existing weights, driver and FFmpeg.

This guide is for someone who already has a working local ComfyUI installation and can run commands in a terminal. It is not an automated from-zero installer. Owner-authorized illustrative demo stills are included in docs/images, and a narrated viewing tutorial is available in docs/media (see TUTORIAL.md). No executable example videos, standalone generation guides or model weights are bundled. Use your own authorized video and check model-license eligibility before downloading or running weights. The first successful setup will require manual file placement and scene/guide review.

**Historical GPU version warning:** the exact recorded PyTorch nightly is no longer found in the checked official index. The newly installed CLI passed its tests, and one complete H3 run succeeded on an independently installed alternative Torch/CUDA stack with existing weights, driver and FFmpeg. Read the installation-status section in README.md before choosing versions.

## 1. Check the two environments

**Video server:** existing ComfyUI with native MiniMax H3 nodes, matching GPU-capable PyTorch, four model files below and enough RAM/VRAM. The tested server used Windows, RTX 5070 Ti 16 GB, approximately 64 GB RAM, ComfyUI 0.34.3, PyTorch 2.14.0.dev20260705+cu130 and SageAttention 2.2.0. These versions describe a working existing environment; this package does not install or recreate it. Exact commits and launch differences are in evidence/provenance/RUNTIME_PROVENANCE.json. Do not upgrade/downgrade an existing installation merely to match a number here.

**Kit commands:** Python with NumPy and OpenCV, plus FFmpeg and ffprobe on PATH. The tested CLI used Python 3.13.12, NumPy 2.4.6 and opencv-python 5.0.0.93. Open a terminal in the repository root (the folder containing cinema.py). In all kit commands below, `python` means the interpreter with these dependencies; replace it with your actual interpreter command if needed. For example, in PowerShell an executable path containing spaces is invoked as `& "PATH_TO_PYTHON_EXE"`.

```text
python --version
python -c "import numpy, cv2; print(numpy.__version__, cv2.__version__)"
ffmpeg -version
ffprobe -version
```

FFmpeg must support libx264, AAC, PNG decoding/encoding and WAV. The tested build was 8.1.1. Check with `ffmpeg -encoders`; if a binary is missing, obtain it through your normal approved installation process and ensure both commands are on PATH. No binary is installed by this kit.

If Python imports fail, use a separate CLI virtual environment or your already managed environment. For a **new, isolated** Python 3.13 environment, the package versions used here can be installed with `python -m pip install numpy==2.4.6 opencv-python==5.0.0.93` after activating that environment. These exact NumPy/OpenCV versions were installed successfully in a new CPython 3.13.12 environment and passed the CLI tests. This verifies the CLI dependency installation, not a new GPU server or FFmpeg installation. Do not run it against your ComfyUI Python blindly; do not replace its Torch/CUDA packages. Node.js is needed only for the JavaScript regression tests, not for inference or opening the selector.

## 2. Place the four H3 model files

docs/MODEL_PROVENANCE.md contains pinned, hash-matched published artifact links. evidence/provenance/WEIGHT_PROVENANCE.json contains exact byte counts and SHA256. Obtain weights only after accepting applicable terms through the distributor's normal flow. This guide does not bypass access gates or download anything automatically.

| ComfyUI model subdirectory | Filename expected by this kit |
| --- | --- |
| models/diffusion_models | minimax_h3_ref2va_pruned_nvfp4.safetensors |
| models/text_encoders | qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors |
| models/vae | minimax_h3_video_vae_fp16.safetensors |
| models/vae | minimax_h3_audio_vae_fp32.safetensors |

The verified Abiray diffusion artifact uses `MiniMax_H3_Ref2VA_pruned_nvfp4.safetensors` capitalization. If needed, make a separately named copy with the kit's expected lowercase name; do not overwrite or rename an existing model. The three companion H3 files match Comfy-Org. Do not substitute FL2VA or a same-named conversion with a different hash. On Windows, `Get-FileHash -Algorithm SHA256 MODEL_FILE` verifies an existing file without changing it. Model folders may instead be configured through ComfyUI's existing extra-model-paths configuration; the server must list the expected filenames.

No FLUX weights are required to run H3 with a guide you already have. The separately tested FLUX image environment is documented in README.md; its output was transferred manually, not invoked by this kit.

## 3. Start or reuse the local server

If ComfyUI is already running, reuse it and its actual input/output directories. Do not launch a second GPU server or restart a busy queue. If it is stopped, use its existing working launcher. A standard source installation can be started **from its ComfyUI folder** with its own Python environment:

```text
python main.py --listen 127.0.0.1 --port 8188 --disable-auto-launch --cache-none
```

For Windows portable installations, the supplied launcher normally selects the embedded Python correctly. Adapt its existing command rather than using an unrelated system Python. The tested H3 runtime additionally used `--reserve-vram 3 --vram-headroom 2 --use-sage-attention`; only use SageAttention if that existing installation supports it. Memory/runtime behavior elsewhere is unverified.

Stock ComfyUI may clean its temporary directory. If preserving every old temporary file matters, use `--temp-directory NEW_EMPTY_TEMP_DIRECTORY` pointing to a newly created empty directory, never a prior run folder. The trial's in-memory cleanup suppression/audit hook is documented evidence and is not installed by this kit.

Open `http://127.0.0.1:8188` to confirm the server responds. Record the server's real input and output folders; when custom flags are used, do not assume they are the default `ComfyUI/input` and `ComfyUI/output`. The kit permits only local HTTP servers. If your port differs, use that same URL in both doctor and build.

Back in the **kit folder**, run:

```text
python -B cinema.py doctor --server http://127.0.0.1:8188 --out doctor-new.json
```

Expected: `missing_nodes` is empty and all four models have `listed: true`. Doctor was checked against the existing server and the separately installed alternative server; both listed all required nodes and models. If it fails, read the newly written report: missing models require correct paths/names; missing native H3 nodes require a compatible ComfyUI environment. Do not submit until resolved. Doctor is a dependency check, not a fresh-install certification or a hash check.

## 4. Prepare one clip and a reviewed guide

Choose a continuous source video with an audio stream. Constant-frame-rate input is the documented path; variable-frame-rate and rotation-metadata mapping need separate validation. Use a source longer than the selected interval. The normal example below selects 124 frames at 24 fps, about 5.167 seconds. The measured 90-frame/3.75-second pilots used `--frames 90 --pilot-short`; they are short experimental runs, not a claim that all durations are trained equally well.

```text
python -B cinema.py prepare --video YOUR_VIDEO.mp4 --out project-new --frames 124
```

This creates `project-new/source.mp4`, audio.wav, project.json, sampled frames, a frame manifest, a contact sheet and scene.template.json. Inspect the actual frames and gesture timing.

Open `ui/camera_picker.html` in a local browser. Load `project-new/scene.template.json`, select a view, adjust controls and edit the instruction. Download a new scene sheet. Move that downloaded JSON into the kit folder as `scene-reviewed.json` using a new filename. Fill subject, camera, object visibility/evidence and timed acting entries; replace illustrative placeholders. Do not demand an object that should be outside the new field of view.

Optional proxy route: see [CAMERA_INTENT.md](CAMERA_INTENT.md) and the [synthetic viewer example](../examples/camera_intent/README.md). For your own scene, depth/proxy creation must happen externally; this kit does not reconstruct your video. Export camera intent, then write its target-view description in the scene sheet; do not paste the entire image-creation prompt into H3. See [the current workflow](CURRENT_WORKFLOW.md) for this manual handoff and why the viewer has not replaced the scene editor/review steps. The camera-intent JSON is not a valid replacement for scene-reviewed.json. The synthetic example only exercises the viewer and cannot serve as an H3 source-video example.

Create the first-frame guide manually in ChatGPT, FLUX or another authorized tool. Save it as `guide.png` in the kit folder. Inspect posture, anatomy, props, room perspective and hand margin against the original frames. Only after review set both JSON fields `reviewed` and `guide_reviewed` to the boolean `true`, without quotation marks. They record a human review, not an automatic guarantee.

## 5. Build, generate and collect

Replace `COMFY_INPUT` and `COMFY_OUTPUT` below with the actual server folders. Quote paths containing spaces. Keep all output names new.

```text
python -B cinema.py build --project project-new --scene scene-reviewed.json --guide guide.png --comfy-input COMFY_INPUT --out run-new --server http://127.0.0.1:8188 --width 800 --height 480 --ref-image-size max
python -B cinema.py submit --run run-new
python -B cinema.py collect --run run-new --comfy-output COMFY_OUTPUT --wait 50
```

Build stages uniquely named inputs and writes workflow.api.json, workflow.visual.json, run.json and prompt.txt. Review them before submit. Submit must return a prompt ID. While collect reports PENDING, repeat **collect only**. After a lost submission connection, inspect server queue/history and submission_intent.json; never resubmit blindly.

Only proceed to compare after collect prints COLLECTED; PENDING exits successfully but is not completion. When complete, run-new contains native_audio.mp4, original_audio.mp4 and result.json. If collection stopped after one file, repeat collect: identical existing files are reused; different files or symlink destinations are preserved and rejected. Inspect such a conflict rather than deleting or overwriting it.

```text
python -B cinema.py compare --run run-new
```

Expected: `run-new/comparison/comparison.mp4` with SOURCE / MANUAL GUIDE / H3 RESULT and verification.json. The comparison preserves the prepared AAC track, not a bit-identical copy of the entire original recording. Check acting, identity, background, cropped hands and lip sync manually. Higher resolution is not guaranteed to improve all of them. Existing output folders are never reused by prepare/build/compare; use fresh names for another experiment.

## 6. Optional controls inside ComfyUI

The core path above works without the custom camera node. The HTML selector already contributes the camera instruction to the scene and H3 prompt. If you also want the ComfyUI node, copy the new `custom_nodes/h3_camera_brief` folder into that installation's custom_nodes folder without replacing an existing folder, then restart only when idle. No pip dependency is needed for this node. Restricted launchers must whitelist it. Follow README.md's `attach_camera.py` example and build with a matching reviewed guide; controls never create an image automatically.

For canvas editing, import the **built workflow.visual.json**, not the API graph or placeholder template. Refresh model/media lists. Browser/canvas interaction has not been visually accepted in this environment; API inference and offline selector logic were tested. A one-click clean installation is not claimed.

## Troubleshooting and publication limits

| Symptom | Next step |
| --- | --- |
| ImportError for numpy/cv2 | Select the intended CLI interpreter; check step1. |
| Connection refused | Start/reuse the server; match doctor/build URL and port. |
| Models not listed | Correct model folder, filename and configured search paths; refresh/restart when idle. |
| Review error | Complete the scene; use literal JSON true after review. |
| Queue busy | Wait for the existing job; do not start a second inference server. |
| OOM or runtime failure | Preserve history and outputs; inspect compatibility and reduce size for a separately named test. No automatic retry. |
| Existing file/folder error | Choose a fresh destination; preserve the earlier attempt. |

Project-authored code is MIT licensed. Public example rights and applicable model licenses remain separate. No private media, weights, credentials or personal paths are included. Official API2K is documented as a future option only; this kit has not made paid API calls or implemented that adapter.

## Storage and optional FLUX access

The four H3 weights total approximately34.03GB (decimal); the three optional FLUX image weights add approximately11.02GB. Allow additional space for the Python/ComfyUI environments, download staging, temporary files and output videos. FLUX is not required when supplying an already created guide.

FLUX downloads may require Hugging Face login and explicit acceptance/access approval on the official repository. Anonymous download requests may return401 even when an artifact exists; that is not evidence of a hash mismatch. No credentials, access acceptance or automatic download are included. Follow the distributor's normal access flow only if you elect to use FLUX.

The H3 artifact's published capitalization differs from the expected lowercase filename in the table. Make a new correctly named copy from the downloaded original. On a case-insensitive filesystem, if the alternate capitalization already occupies the destination, do not overwrite it: use a fresh configured model-search directory and copy the expected name there. Verify the server lists the exact expected name before build. Existing originals remain untouched.
