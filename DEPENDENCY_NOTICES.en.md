# Dependencies and attribution

This is a private review candidate. No model weights, binaries, private videos, credentials or personal paths are bundled. Project-authored code is MIT licensed; see LICENSE. Upstream components and weights retain their own terms.

The local validation environment used Python 3.13.12, NumPy 2.4.6, OpenCV 5.0.0, FFmpeg/ffprobe 8.1.1, ComfyUI 0.34.3 and frontend 1.49.6 on RTX 5070 Ti 16 GB. These are observed versions, not a universal lockfile. The CLI requires numpy and cv2 plus ffmpeg/ffprobe on PATH. It does not start or install ComfyUI.

Credits and upstream terms reused from the reviewed publication draft:

| Component | Role and terms |
| --- | --- |
| Python Software Foundation and contributors | Interpreter: https://docs.python.org/3/license.html |
| NumPy developers | Array processing: https://numpy.org/doc/stable/license.html |
| OpenCV contributors | Image/video processing: https://opencv.org/license/ |
| FFmpeg project | Media conversion: https://ffmpeg.org/legal.html . Actual binary terms depend on build options; libx264 can affect GPL obligations. No FFmpeg binary is distributed. |
| Comfy-Org and contributors | External local runtime: https://github.com/Comfy-Org/ComfyUI/blob/master/LICENSE (GPLv3). Integration documentation: https://docs.comfy.org/tutorials/video/minimax/minimax-h3 |
| MiniMax | H3 Community License: https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE . Applicable territory excludes USA, EU, UK and Republic of Korea; distribution/use/commercial conditions also apply. This package does not establish permission or contest eligibility. |
| Qwen team and contributors | Encoder lineage: https://github.com/QwenLM/Qwen3-VL/blob/main/LICENSE . This does not establish the provenance/terms of each converted H3 encoder artifact. |

Exact installed filenames are listed in workflow.template.api.json. Ref2VA NVFP4 is the tested diffusion variant; FL2VA is not a substitute. Matching published artifact URLs, pinned revisions and local SHA256 values are now recorded in MODEL_PROVENANCE.md and WEIGHT_PROVENANCE.json. Exact conversion processes and redistribution eligibility remain unverified; byte matching is not a rights grant. No weights are redistributed or automatically downloaded.

This clean package includes no example video or guide. Use your own authorized media. ChatGPT/FLUX are external manual providers subject to their respective terms, not bundled adapters. No GUI toolkit is required for this CLI; the separate offline preparation GUI is not integrated here.
