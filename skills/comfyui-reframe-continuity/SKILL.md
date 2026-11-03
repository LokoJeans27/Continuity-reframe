---
name: comfyui-reframe-continuity
description: Analyze a source video and plan or test a new camera viewpoint while preserving semantic shot continuity, then prepare an edited first-frame image and a ComfyUI MiniMax H3 Ref2VA workflow. Use for reference-guided reframing, shot matching, eyelines, props, handedness, and action timing, not calibrated 3D reconstruction or guaranteed motion transfer.
---

# Reframe video with semantic continuity

Turn an existing shot into a *plausible new view of the same event*. Preserve who does what, with which hand and object, to whom, and when. Do not solve every scene by building a new 3D set.

This is a reusable procedure, not a vision model, image generator, video model, or permission grant. It adds no capabilities to the host assistant. Read [portability.md](references/portability.md) when adapting it to Codex, Claude, or another assistant.

## Establish what can actually run

- Identify the source file, shot/time range, desired viewpoint, output aspect ratio, required audio treatment, and available local ComfyUI environment. Ask only for missing details that block the task; otherwise declare reasonable assumptions.
- Check whether the host can inspect image pixels, play or sample video, hear audio, generate/edit images, run files, and operate ComfyUI. Distinguish unavailable from untested. An installed model name is not proof that it works.
- Select an available image-generator adapter: manual ChatGPT, local FLUX 3 Image Klein, or another verified provider. Read [image-adapters.md](references/image-adapters.md). If none is available, deliver the precise image brief and wait for the user-provided image. Do not silently switch providers, spend paid API credits, install models, or upload private source material.
- Check the actual MiniMax H3 license before downloading, running, or distributing H3-based assets. Its published community license checked on 2026-11-03 excludes the EU, UK, US, and South Korea. Unknown location or license coverage is a gate for H3 execution, not a reason to stop model-independent analysis. Read [h3-comfyui.md](references/h3-comfyui.md).

## 1. Inspect the event, not just frame zero

Probe source dimensions, duration, frame rate/time base, rotation, and audio. Detect cuts or explicitly bound the task to one continuous shot. For multiple shots, create separate continuity records rather than treating a cut as object motion.

Start with 6–12 time-stamped samples across the chosen shot, including its first and last usable frames. Add close samples around contact, occlusion, object exchange, eyeline changes, and the start/apex/end of important gestures. Inspect the actual pixels. Sparse samples do not establish everything that happens between them.

`scripts/sample_video.py` extracts a small, time-stamped PNG sample set and a manifest using Python, ffprobe, and ffmpeg. Run `--help` first. It preserves the source, does not perform visual analysis, and does not create a 24 fps H3 reference. Use a shot-sized input for efficiency. Review `manifest.json` before relying on frame/time correspondence.

Record scene evidence using [continuity-record.md](references/continuity-record.md). Separate:

- **Observed:** directly visible or audible, with frame/time evidence.
- **Inferred:** a plausible relation, confidence, and alternatives.
- **Unknown:** hidden surfaces, uncertain anatomy, or events not inspected.
- **Requested change:** the user's intended camera or creative modification.

Do not present an inference about an unseen room wall as an observation.

## 2. Design the new camera and visibility

Define the viewpoint relative to named subjects and landmarks: camera location, look direction, height, shot size, and whether it remains fixed or moves. Degrees are meaningful only with a declared axis and reference. A new camera is not a mirror of the old frame.

For each important subject/prop, predict visible, partly occluded, outside frame, or uncertain. Preserve its physical existence without forcing it into the image. A cup that stays behind a person need not become visible merely because it matters to the story.

Reproject the *relationships*, not old screen positions. Anatomical right/left stays attached to the person; screen right/left can reverse. Check eyelines, the action axis, entry/exit direction, overlap order, contact points, and where the background should fall from the new viewpoint. When crossing the action axis is intentional, acknowledge the changed screen direction.

Change background perspective coherently with the camera. Do not paste a rotated character over an unchanged background. Newly revealed areas are hypotheses; use restrained, compatible detail, or choose a less revealing angle when accuracy matters. Do not label this a measured camera solve or recoverable ground-truth geometry.

## 3. Prepare and inspect the new first frame

Give the available image generator the original first frame and only the other sampled frames needed for identity, clothing, object, or layout evidence. Explain which frame represents time zero. Later frames are evidence, not permission to advance the action in the starting image.

The image brief must specify:

1. The requested camera and background perspective.
2. Stable identities, clothing, body orientation, and the exact initial action state.
3. Object ownership, anatomical hands, contact, eyelines, and permitted occlusions.
4. What may be newly inferred and what must not be invented or exposed.

Inspect the generated pixels against the continuity record before spending video inference time. Repair an incorrect initial pose, identity, prop, or viewpoint here. A video prompt is not a reliable repair for a contradictory starting image. Save the source references, image prompt, resulting image, and whether the user reviewed it.

## 4. Build the reference-guided video test

Read [h3-comfyui.md](references/h3-comfyui.md) for the verified native-node recipe and license/source links. Check the installed node schema and template rather than guessing socket names or importing a fabricated graph.

Separate the conditioning roles:

- New image: target camera, frame-zero composition, and background appearance.
- Original video: subject identity, physical action, expressions, event sequence, and intended timing.
- Continuity record: semantic constraints and uncertainty.
- Original audio: preserved externally for the comparison unless another treatment was requested.

Use MiniMax **Ref2VA**, not the FL2VA checkpoint, with the original video as a video reference. Anchor the new image at output frame 0 with the available guide node. Also provide it as an image reference if the text prompt names it. Do not hard-guide the whole original-view video while asking for a different camera.

Record source trimming/resampling, asset-to-reference label mapping, model and node versions, seed, canvas, frame count, sampler settings, elapsed time, and hardware. Never claim a prompt or saved graph was successfully executed unless the output exists and was inspected.

## 5. Compare, diagnose, and deliver

Start with one short event rather than a long montage. Use [validation.md](references/validation.md) for the minimal comparison and reuse tests. Compare frame zero, event landmarks, occlusion transitions, and the end, then inspect playback. Assess identity, camera/background, physical continuity, action timing, and audio separately.

Preserve the original audio externally after matching duration and offsets. A reference-audio prompt does not prove waveform preservation, and original audio on a generated face does not prove lip sync. Never silently stretch time to hide a mismatch. If an output is longer/shorter, disclose the difference and choose an explicit trim/pad/retime policy with the user when it changes the performance.

If exact geometry, identical motion, or identical lip sync is a hard acceptance condition, explain that this generative method cannot guarantee it and ask whether an approximate test is acceptable before inference. Continue evidence gathering while that decision is pending.

Fix the earliest failed stage: wrong scene understanding → evidence/record; wrong initial image → image edit; good start but later drift → reference/timing/conditioning experiment. Change one important variable per comparison. Agree a useful test budget and stopping condition; do not generate indefinitely or spend paid credits without approval.

Deliver the usable image/video/comparison and the reusable record, prompts, workflow export, and run manifest that actually exist. State which steps were manual, which were tested, and which remain untested. Describe the result as reference-guided generative reframing with semantic continuity checks. Do not promise exact geometry, novel-view truth, identical motion, pixel-exact frame anchors, or guaranteed lip sync.
