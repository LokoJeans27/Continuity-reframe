# MiniMax H3 in ComfyUI

Verified against public primary sources on **2026-11-03**. These are a known recipe and constraints, not a guarantee that the user's installed build has identical nodes. This package contains no model weights or upstream implementation.

## License gate

The [MiniMax H3 Community License](https://huggingface.co/MiniMaxAI/MiniMax-H3/raw/main/LICENSE), dated August 2, 2026, excludes the **European Union, United Kingdom, Republic of Korea, and United States of America**. Its restrictions address use and distribution of H3 works and outputs, not just downloading weights. Section II offers a route to a separate license. A different server location or omitting weights is not evidence of permission.

Check the applicable person/entity, deployment and intended distribution against the actual license. For excluded/uncertain coverage, pause H3 execution and distribution pending appropriate authorization; continue source analysis and generic image planning. Do not infer location from language. Commercial conditions include separate authorization above US$20 million annual revenue and UI attribution. This summary is not legal advice and does not replace the current agreement or an applicable separate contract.

## Verify the environment

Inspect a known-good exported native Ref2VA workflow, installed node definitions, and model paths. Prefer native nodes already present. Missing nodes are a capability/setup issue, not a reason to install an unreviewed custom pack automatically.

Record the ComfyUI version/commit and exact checkpoint filename, model revision/hash if available, video/audio VAEs, text encoder, and any LoRA. Do not mix FL2VA and Ref2VA model families. Follow the existing tested sampler preset first; compare acceleration only after a baseline works.

The [official Ref2VA model documentation](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/README.md) describes video/audio references of 2–15 seconds, with up to three of each and 15 seconds total per category, plus up to nine images. Implementation acceptance of a smaller/larger input is not evidence of trained quality.

## Reference preparation

1. Select one continuous source event. Preserve the unmodified original.
2. Decode/resample a reference copy to **24 fps** without changing playback speed. Do not relabel 25 or 30 fps frames as 24 fps. Record dropped/duplicated frames and audio offset. H3's native frame-batch input does not carry the original file's fps automatically.
3. Check the installed H3 frame grid and the *actual* generated/reference lengths. The checked code uses `17k+5` frames; 124 frames at 24 fps last about 5.167 seconds, not exactly five. Output length rounds upward; reference truncation can round downward. Choose coverage consciously and compare the covered interval.
4. Preserve audio separately for final remuxing/comparison. A soundtrack attached to a video reference and a standalone audio reference are distinct inputs; do not accidentally duplicate one track.

Reference resizing/cropping can alter framing. Inspect the exact image and frame batch that enter the model, not only their original files. Keep the target first-frame image at the intended canvas/aspect ratio.

Example of a coverage trap: four seconds at 24 fps is 96 frames, between valid lengths 90 (3.75 s) and 107 (about 4.458 s). A 96-frame reference can be truncated to 90 while a requested 96-frame output rounds up to 107 in the checked implementation. Do not silently lose the final action or squeeze 107 generated frames into four seconds. Select a compatible source interval, explicitly account for coverage, and verify the installed behavior.

## Wiring recipe, not a fabricated workflow

Adapt the official template in the actual installed UI/schema:

1. Load the **Ref2VA** checkpoint and its matching encoders/VAEs.
2. Decode the prepared source clip into a 24 fps IMAGE batch. Send it to a video-reference input of `MiniMaxH3ReferenceToVideo`.
3. Send the new first-frame image to its first image-reference input. Set the target canvas and length there; connect the video VAE so visual references are encoded beyond text-encoder conditioning.
4. Pass the returned positive conditioning and latent into `MiniMaxH3AddGuide`. Supply that same new image, video VAE, and `frame_idx = 0`. The guide's updated positive conditioning goes to the sampler/guider; use the reference node's latent.
5. Continue the verified sampler and decoding/export path from the template. Preserve the generated raw output for diagnosis before remuxing original audio.

If a guide is absent, report the missing anchor and do not describe image-reference-only generation as equivalent. A frame anchor is a conditioning constraint, not a proof of pixel-exact reconstruction. Do not add two competing images at frame zero. Do not put the whole original-view video in the target guide input: that can constrain the camera you intend to change.

The [official multiframe guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3-multiframe) explains that guide-only images do not get text-encoder reference labels. Supplying the image as a reference as well lets the prompt name it. Download/inspect the [official workflow template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_multiframe_reference.json) rather than inventing node IDs.

## Prompt compilation

Follow the [official Ref2VA prompt guide](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/ref-en.txt) when a full rewrite is useful. Its sections are `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, and `non_diegetic_music`. Write model instructions in English, preserving spoken language and visible text where relevant.

Map actual socket order to `<Picture N>`, `<Video N>`, and `<Audio N>` explicitly. Do not name an audio label for a soundtrack that was never enabled/connected. Assign a stable `<Subject N>` to each person or important object, and state separately which source supplies appearance, action, timing, and target camera. Retention markers express requested roles, not measured success.

Example intent, to compile using the actual scene record:

“The target is a new view of the event in <Video 1>. <Picture 1> defines its opening composition and camera. The video supplies [subjects] and [observed action phases/timestamps]. Keep those physical actions and relationships from the new view, rather than reproducing the original screen positions or camera. [Object] remains [hand/owner/contact] even when hidden. Keep a continuous shot and [specified camera motion].”

Only use audio-copy language when the delivery process actually reuses the signal. Generated audio conditioned by a reference is not a waveform copy.

## Technical primary sources

- [Native node implementation](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_minimax_h3.py): schemas, reference ordering, frame handling and guide semantics. Re-check the user's version.
- [Native workflow documentation](https://docs.comfy.org/tutorials/video/minimax/minimax-h3-native): current templates and conditioning guidance.
- [MiniMax's H3 overview](https://design.minimax.io/h3): supported deployment paths and model overview.

Do not claim access to an API, cloud credits, a subscription's image-generation quota, or a local GPU through this skill. Any such access must exist independently and be authorized.
