# Narrated walkthrough

[Watch or download the English tutorial](https://github.com/LokoJeans27/Continuity-reframe/raw/refs/heads/main/docs/media/continuity-reframe-tutorial-en.mp4) · [English subtitles](media/continuity-reframe-tutorial-en.srt)

This viewing asset shows recorded interaction with the actual browser camera selector and local CLI: choosing a view, typing the camera instruction, reviewing the manual guide, building, submitting, waiting and collecting. It is not an executable input video or a standalone guide for generation. Follow [QUICKSTART](QUICKSTART.md) with your own authorized media.

The image guide is prepared externally and transferred manually. The selector describes a camera intention, not an exact reconstruction of the room. Scene and guide review flags must be set only after human review. This video does not demonstrate importing a graph in the ComfyUI canvas or an automatic ChatGPT integration.

This recording predates the new camera-intent studio and selector redesign. It demonstrates the underlying manual-guide/CLI sequence, not the current 3D proxy interface. See [the synthetic viewer example](../examples/camera_intent/README.md) for that separate prototype.

## What was recorded

- Windows PC with RTX 5070 Ti 16 GB; separate ComfyUI 0.34.3 environment, Python 3.13.12 and PyTorch 2.13.0+cu130, using existing weights and FFmpeg.
- Short pilot: 90 frames at 24 fps, 800 x 480, max reference size, 20 steps, seed 18840101. This is different from the default 124-frame QUICKSTART.
- Measured submission-complete to collection-complete: 450.04 seconds. Comparison happened afterward. A 442-second portion of the recorded wait is accelerated 44.2 times.
- Private filesystem locations are hidden by the recording wrapper. The visible terminal records real local work. Added frame holds are labelled; explanatory cards are not simulated players.
- The workflow saved an original-audio output. This tutorial replaces preview audio with English narration and music. It does not claim exact acting, identity or geometry preservation.

Generated H3 result frames are omitted from this new public tutorial. Review your output locally and compare gesture timing, face consistency and background perspective. The new result/review cards explicitly explain this omission; they do not show a new render result.

## Voice, assets and license limits

The English narration was synthesized locally with Chatterbox V2 from the owner's specifically authorized first voice reference. It is synthetic narration, not a newly recorded performance. The reference recording is not distributed. Automated transcription was checked and problematic takes were regenerated; this is not a perceptual certification of accent or voice identity. Subtitle phrase timings are approximate rather than word-aligned.

Music and motion graphics were authored for this tutorial. Source footage and the manually prepared image guide are owner-authorized demo material; no third-party scene clips are included. Code licensing does not grant permission to clone the speaker or reuse their likeness. No model weights, voice references, executables or credentials are included.

[Chatterbox's upstream MIT license](https://github.com/resemble-ai/chatterbox/blob/master/LICENSE) applies to that external component; its built-in audio watermark was retained. [MiniMax H3's model license](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE), including its territorial restrictions on works and outputs, remains separate from this repository's MIT code license. Publishing this tutorial does not establish worldwide eligibility to run H3 or publish its outputs.

See [technical validation](../evidence/validation/TUTORIAL.json) for the delivered file's measured properties and checks. No paid API or new service was used.
