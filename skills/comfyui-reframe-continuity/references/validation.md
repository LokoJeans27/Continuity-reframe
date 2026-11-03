# Minimal validation and stopping rules

## Test the helper

Run `python scripts/sample_video.py --help`. Then run it on a short synthetic or authorized clip into a new directory. Check the manifest's source hash, duration, stream metadata, selected frame indices/timestamps, PNG count and optional extracted audio. The helper must refuse to overwrite existing output files. None of this validates generative video quality.

Run `python scripts/test_sample_video.py` for the bundled local regression tests. They create temporary synthetic video/audio, test constant and variable frame rates, window/explicit sampling, audio extraction, and non-overwrite/error handling. They require ffmpeg with `libx264`, plus ffprobe. No models, network calls, or paid inference are involved.

Example: `python scripts/sample_video.py source.mp4 --out run01/evidence --samples 8 --extract-audio`. The optional WAV contains the **full first audio stream**, decoded as float32 without requested resampling, not only the selected window. Its timeline starts at zero; use the source offset in the manifest when synchronizing. It is not a compressed bitstream copy. Keep the original media as the authority.

For variable-frame-rate material, use actual presentation timestamps, not frame index divided by nominal fps. Inspect any source rotation/HDR/color conversion: this helper produces analysis PNGs, not a color-managed mastering deliverable.

## Smallest meaningful video experiment

Choose one short, rights-cleared continuous event that exposes a continuity risk, such as a hand approaching a prop or two people exchanging looks. Use a licensed/authorized inference environment and an agreed generation budget.

1. **Control:** original first frame + source video, with no requested camera change. This tests basic reference/actuation handling.
2. **Reframe:** inspected new-view first frame + the same source video and semantic record + frame-zero guide.
3. **If budget permits:** same reframe without the scene-specific semantic constraints, keeping settings/seed constant. This tests whether the extra analysis helps instead of merely asserting it.

Keep model, sampling preset, seed, source interval, output size and duration the same wherever possible. A single seed is a smoke test, not a general performance claim. Do not describe a test as passed when only a prompt/graph was prepared.

## Score separately

Use pass / partial / fail / unverified with concrete timestamps and notes:

- Target camera and background perspective agree; no return to the source angle.
- Identities and clothing persist.
- Prop count, ownership, contact and anatomical handedness remain plausible.
- Eyelines target the intended subjects, including when those subjects are off-screen.
- Occlusion follows the new view; hidden objects are not dragged into visibility.
- Event order and phases survive; record the timestamp difference at each landmark.
- Duration and source-audio offsets are measured. Audio is not duplicated or silently retimed.
- Lip motion is reviewed separately and described as approximate/failed/unverified as appropriate.
- Frame zero, mid-action, and end remain coherent in playback, not only as attractive stills.

Do not use raw pixel similarity between different views as a semantic-continuity score. Do not declare exact camera position, geometry or lip sync from this checklist.

## Demonstrate reuse

Before calling the process generalizable, test at least a second materially different shot. Useful cases are a front/behind occlusion, a hand-to-hand exchange, moving source camera, or a viewpoint revealing an unseen wall. A failed case is useful evidence: record the failure and narrow supported claims.

## Failure diagnosis

| Observation | Next useful check |
| --- | --- |
| First image already has wrong hand/contact | Source evidence and image prompt, before another video run |
| Starts correctly, drifts to source camera | Actual guide wiring, image/video role conflict, clip conditioning |
| Action is early/late or missing | fps normalization, rounded frame count, reference truncation, event coverage |
| Important prop appears through a person | Target visibility record and generated occlusion |
| Output sounds different | Was original audio remuxed, or merely used as a reference? |
| Original audio matches but face does not | Motion/lip-sync failure; do not claim audio reuse fixes it |
| Larger viewpoint invents layout | Unobserved-region uncertainty; reduce angle or obtain evidence |

Stop at the agreed acceptable sample, a material license/capability blocker, or the agreed test budget. Preserve the best and failed outputs with settings. Any expansion to paid inference, model installation, external uploads or distribution needs the corresponding user authority.
