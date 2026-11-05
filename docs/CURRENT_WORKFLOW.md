# Current workflow: what the new viewer replaces, and what it does not

There is one supported H3 generation sequence:

**prepare video/frames → describe target view and review scene → create image guide externally → review guide → build → submit → collect → compare.**

The new viewer is an optional way to choose the target view. It does **not** replace the scene sheet, image-guide step or H3 CLI. The earlier text selector remains functional and useful when no proxy exists; it has not been removed or silently redirected to an incompatible format. You do not need to use both camera helpers.

| Component | Actual input/output | Current role |
|---|---|---|
| `cinema.py prepare` | Authorized video with audio → prepared clip, sampled frames and `scene.template.json` | Required preparation |
| `ui/camera_picker.html` | Scene sheet → new scene sheet with camera instruction, review flags false and visibility reset | Working text/preset helper; no geometry |
| `ui/camera_intent/build_studio.py` and generated HTML | External proxy JSON + JPEG → offline orbit viewer; exports `camera-intent.v1` package/prompt | Optional visual planning; no depth estimation |
| External image tool | Original frame + manual camera prompt (+ optional proxy screenshot) → image guide | External/manual; no provider adapter |
| Reviewed scene sheet | Subject, camera description, object evidence/visibility and timed acting; human review flags | Required by H3 build; neither camera helper completes this review |
| `cinema.py build/submit/collect/compare` | Reviewed scene + guide + prepared clip → H3 result and comparison | Existing local generation path |

## If you choose the new viewer

1. Follow QUICKSTART through `prepare`. Inspect the original frames and gesture.
2. Create a proxy externally using the matching original frame and an appropriately licensed tool. This repository has no real-video-to-proxy converter. The bundled synthetic example is only a viewer test.
3. Package the proxy/frame, orbit the viewer, and export the intent. Use its image-creation prompt in your external image tool, with the original frame attached manually.
4. Create a new scene sheet from `scene.template.json`. In `camera`, write the target-view description and framing chosen in the viewer. **Do not paste the whole image-creation prompt as an H3 instruction, and do not use the camera-intent JSON as the scene sheet.** Complete subject, object visibility/evidence and timed acting using actual source frames. No automatic intent-to-scene importer exists.
5. Review the generated guide and scene; set the boolean review flags only then. Resume QUICKSTART at `build` using that scene and guide. Do not run the text selector afterward unless deliberately changing the camera; another camera choice requires a new review.

Viewer axes are source-image-relative, whereas the older selector uses its documented semantic/performance-relative conventions. Numeric values must not be copied between them as if calibrated or automatically equivalent. Both describe intention; neither guarantees hidden geometry or exact image-model camera control.

## Compatibility and remaining gaps

The root `camera_picker.html` is only a compatibility redirect to `ui/camera_picker.html`. Root Python commands still forward to `src/continuity_reframe`. `choose_camera.py` and the optional ComfyUI camera-text node remain manual text helpers. None is an old video pipeline that the viewer replaces.

A unified viewer-to-reviewed-scene UI, automatic real-video proxy creation and automatic image-guide generation are not implemented. Until those integrations exist, removing the scene/guide instructions would make the published workflow incomplete. The recorded tutorial predates this viewer and demonstrates the retained manual-guide/CLI sequence, not the new visual planning step.
