# Use and reuse across assistants

This folder is an **export-only package**. Preparing or reading it does not install it, modify user settings, or enable an external service.

## Capability adapter

Before executing, fill a short capability record:

| Need | Capability to verify | If missing |
| --- | --- | --- |
| Visual analysis | Host can inspect actual image pixels | Ask for a capable host or supply an evidence worksheet, not invented observations |
| Temporal analysis | Video playback or ffmpeg sampling | Work from supplied time-stamped frames and disclose gaps |
| Image generation | Available image editor/generator plus accessible references | Produce the brief for a manual handoff |
| Video inference | Authorized working ComfyUI and eligible model use | Deliver plan/graph recipe; do not claim a render |
| Original audio | Audio stream tools and listening where needed | Preserve file separately; mark sound review untested |
| Deliverables | Local writable files and supported attachment/export | Return readable text and specify missing delivery route |

“Vision supported” and “image generation supported” are different. A model that can describe images may not create them. A local visual model is optional, must be tested independently, and is not supplied here. The text encoder inside H3 is not automatically an assistant-accessible scene analyzer.

## Host-specific adaptation

- **Codex:** `SKILL.md` and relative supporting files are the portable core. `agents/openai.yaml` is optional UI metadata. Invoke explicitly with `$comfyui-reframe-continuity` when the host exposes it, or ask the assistant to read this folder. For project-scoped installation, use the host's current supported skill location and permission flow. No global install is required for a one-off read.
- **Claude Code:** the same core follows the Agent Skills form. Current documentation supports project-local `.claude/skills/<name>/SKILL.md` and `/comfyui-reframe-continuity` invocation. Optional OpenAI UI metadata can be ignored. Copying into a project remains an explicit installation step, not something this package already did.
- **Other assistants:** load `SKILL.md` as instructions and the linked references as needed. Map file access, visual inspection, image generation, ComfyUI control, and media export to real tools. If the host cannot follow relative links, attach those references too. Do not imitate missing tools with claimed outcomes.

Re-check platform documentation before installation because paths and UX change: [OpenAI skills documentation](https://developers.openai.com/codex/skills/) and [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

## Reuse without locking it to one scene

For each shot save a separate scene record, source hash, sampled-frame manifest, target-camera description, first-frame image and prompt, H3 prompt/reference mapping, exact workflow export, run settings, output and QA notes. Keep source files immutable and outputs in a new run directory.

Reuse the procedure and verified environment preset; replace the subjects, events, camera, visibility predictions, and evidence. Do not reuse a previous room layout, the cup example, or one lucky seed as universal truth. Keep creative assumptions in the scene record, not hardcoded into the skill.

No server calls, credentials, model downloads, or paid services are embedded in the supplied helper. The helper needs only Python 3, ffprobe, and ffmpeg; check those binaries first. Installation of missing software follows the host's normal approval rules.
