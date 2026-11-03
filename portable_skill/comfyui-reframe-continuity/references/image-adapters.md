# Interchangeable first-frame generators

Keep semantic analysis and the continuity record independent of the image provider. Every adapter consumes the same source evidence and target-camera brief, and returns an inspectable image plus provenance. An adapter declaration is a contract, not an implemented integration.

## Common contract

```yaml
adapter:
  provider: selected_by_user_or_verified_available
  mode: manual_or_local_or_authorized_api
  model_id: exact_or_unknown
  revision: exact_or_unknown
  installed_and_tested: false
  reference_images: ordered_files_with_roles_and_times
  reference_limit: verified_for_this_implementation
  target_canvas: width_height
  prompt: continuity_brief
  preprocessing: none_or_recorded
  seed: value_or_unavailable
  cost: local_or_included_or_explicitly_approved_budget
  license: verified_source_and_applicable_terms
result:
  image: verified_local_or_attached_file
  actual_canvas: measured
  actual_prompt: submitted_prompt_and_expansion_if_available
  manual_steps: recorded
  continuity_review: pending_or_actual_result
```

Pass references in deliberate order, identify time zero, and respect the actual input limit. More frames are not automatically better. If a provider accepts only one image, use a reduced evidence set or an explicitly labeled contact sheet only when supported; report the reduced conditioning rather than claiming multi-reference equivalence.

## Manual ChatGPT image step

Supply the selected images and continuity brief through the existing available ChatGPT image tool or a manual user handoff. Retrieve the resulting image through a supported attachment/file route, inspect it, and feed that file into ComfyUI.

This is not an end-to-end local pipeline. A ChatGPT subscription or available UI generator is not a generic ComfyUI API credential or proof of programmatic quota access. Do not promise automatic consumption of the user's image allowance, scrape session credentials, or substitute a billed API without approval. Record the manual transfer honestly.

## Local FLUX 3 Image Klein

Verified on **2026-11-03**. Match the exact model family: FLUX 3 Image Klein, its base variant, and FLUX.2 Klein are not interchangeable names. The [official inference repository](https://github.com/black-forest-labs/flux-3-image-klein) documents editing with up to **10 reference images**, distilled and base checkpoints, and a required prompt-upsampled caption path. Inspect the actual ComfyUI template/model card, installed nodes, quantization and hardware before execution.

Use the official prompt upsampler, or a supported precomputed equivalent following its current system prompts. Preserve both the original continuity brief and expanded caption; inspect expansion for invented props, changed hands, camera reversions or prematurely advanced actions. On constrained GPUs, use a tested sequential/offload setup rather than assuming the upsampler, image model and H3 fit simultaneously.

The weights use the [FLUX Kommunity License v1.0](https://huggingface.co/black-forest-labs/flux-3-image-klein/blob/main/LICENSE.md), not an unrestricted open-source license. It conditionally permits commercial output generation for qualifying users below US$5 million aggregate gross annualized revenue, subject to its requirements, including filtering or review and applicable AI disclosure. Other uses may need a separate license. Check actual terms and eligibility; do not treat the inference code's Apache-2.0 license as the weight license.

Use the [official ComfyUI model distribution](https://huggingface.co/black-forest-labs/flux-3-image-klein-comfy) for current files and instructions. Downloads, license acceptance and installation require the host's normal authorization. This package neither downloads nor tests FLUX weights.

## Future provider

Verify its actual editing/multi-reference support, prompt conventions, canvas constraints, output-file route, version, license, data transmission and cost. Map those facts into the common contract, then run a small first-frame test on the same semantic record. Keep H3's accepted-image input unchanged. Do not claim equivalent quality, identity preservation or multi-view consistency from matching the interface alone.
