# Model artifacts and runtime provenance

Checked2026-11-03. No weights were copied, modified, uploaded or redistributed. Hashes below were computed by streaming each local file and compared with public repository metadata at pinned revisions. Saved executed workflows confirm the selected filenames. No file hash was captured inside the original model-load event, so this identifies the current files corresponding to those names, not a retrospective proof that bytes never changed.

| Pipeline | Local filename | Bytes | SHA256 | Matching published artifact |
| --- | --- | ---: | --- | --- |
| H3 | minimax_h3_ref2va_pruned_nvfp4.safetensors | 12528636866 | 3e1be702c95bc057c05a7d1867e8aeea33073dcf5743835f2f27f06a2f34c596 | [Pinned file](https://huggingface.co/Abiray/Minimax-H3-nvfp4-INT4-INT8-Convrot/blob/908eccad7e68751190d04c171956f163bfeed741/MiniMax_H3_Ref2VA_pruned_nvfp4.safetensors) |
| H3 | qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors | 15687142551 | 35a88d51044231fe332301d7a62aa81e3f2cba62febeb446e2c1e3e0ef76f2c6 | [Pinned file](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/54472221d27c695fca9621b0c3ed52f06c4af707/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors) |
| H3 | minimax_h3_video_vae_fp16.safetensors | 5207808496 | 7c1f131492e7eddacaac9069a61b81bdd39de5cc96561e677c5eab1cdce5e522 | [Pinned file](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/54472221d27c695fca9621b0c3ed52f06c4af707/vae/minimax_h3_video_vae_fp16.safetensors) |
| H3 | minimax_h3_audio_vae_fp32.safetensors | 605254808 | 8e505d95dd1561d47abd43d4238fd40d9bb1ae9e147ed0a4cba778d76ae4db48 | [Pinned file](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/54472221d27c695fca9621b0c3ed52f06c4af707/vae/minimax_h3_audio_vae_fp32.safetensors) |
| FLUX manual image experiment | flux3_image_klein_sd_int8_convrot.safetensors | 5827874779 | 847d8933548afd93df4af2cac2498e70891bf28d9dae06d695f536992e168fe2 | [Pinned file](https://huggingface.co/black-forest-labs/flux-3-image-klein-comfy/blob/5c9b714851dc072b04a23ef6d2d36421f5ccb3a0/diffusion_models/flux3_image_klein_sd_int8_convrot.safetensors) |
| FLUX manual image experiment | qwen3vl_4b_int8_convrot.safetensors | 4858559240 | 32de113cbf8282b02cbff0794b637b9d6676da09314a1db5a30bcea9bf4ee01c | [Pinned file](https://huggingface.co/black-forest-labs/flux-3-image-klein-comfy/blob/5c9b714851dc072b04a23ef6d2d36421f5ccb3a0/text_encoders/qwen3vl_4b_int8_convrot.safetensors) |
| FLUX manual image experiment | flux2-vae.safetensors | 336211292 | 868fe7b343cc8f3a19dbcfcafbc3d5f888802be3f89bd81b65b3621a066ce8f3 | [Pinned file](https://huggingface.co/black-forest-labs/flux-3-image-klein-comfy/blob/5c9b714851dc072b04a23ef6d2d36421f5ccb3a0/vae/flux2-vae.safetensors) |

## What this establishes

The H3 diffusion file matches the Abiray collection exactly, including66 bytes after the declared tensor region. It does not match the currently checked lilcheaty file, which has the same lowercase basename but different full-file bytes. Do not infer that quantizations with similar names are interchangeable. No trimming or repair was attempted. The encoder and both H3 VAEs match Comfy-Org artifacts; equivalent companion mirrors also exist. The diffusion and text-encoder headers lack file-level provenance metadata. VAE metadata contains model configuration, not a download receipt.

For FLUX, the earlier local verification manifest names the official black-forest-labs/flux-3-image-klein-comfy repository and revision5c9b714851dc072b04a23ef6d2d36421f5ccb3a0. The three fresh hashes also match its published metadata. A same-named Qwen encoder from another publisher was not assumed equivalent. Only the distilled image model, its encoder and VAE were used in this trial; base models and a prompt upsampler were not used.

## Remaining unknowns

The original H3 download transaction was not found in the bounded prior-project record search. The exact conversion scripts, calibration data and full upstream revision chain of every conversion were not independently recreated. Current installed package versions and git commits are recorded, but a fresh installation and deterministic rerun from those revisions were not performed. Current driver version is not proof of the driver version at every earlier render. A hash match does not resolve license applicability or redistribution rights.

## Sources and terms

- [Abiray conversion collection](https://huggingface.co/Abiray/Minimax-H3-nvfp4-INT4-INT8-Convrot): community collection; do not infer that repository hosting proves authorship of each conversion.
- [Comfy-Org H3](https://huggingface.co/Comfy-Org/MiniMax-H3): matching encoder and VAE artifacts.
- [Official FLUX distribution](https://huggingface.co/black-forest-labs/flux-3-image-klein-comfy): matching pinned image-model dependencies.
- [H3 license](https://huggingface.co/MiniMaxAI/MiniMax-H3/raw/main/LICENSE) and [FLUX weight license](https://huggingface.co/black-forest-labs/flux-3-image-klein/blob/main/LICENSE.md) remain separate from this project code. This provenance report grants no model rights. Project-authored code is MIT licensed separately in LICENSE.

The supplied package remains source/templates/documentation only. Machine names, user names, personal filesystem paths and private media are omitted. See evidence/provenance/RUNTIME_PROVENANCE.json for separate H3/FLUX environments and launch differences.
