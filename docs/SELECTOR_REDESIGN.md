# Published camera-selector redesign

Open `ui/camera_picker.html` directly in a browser. It is self-contained: no installation, web fonts, network service or new package is required. This redesign is published in the experimental repository. It remains an intention editor, not a scene reconstruction. The separate [camera-intent studio](CAMERA_INTENT.md) can orbit an externally supplied proxy; its synthetic example is not a real-scene reconstruction.

The interface adds visual shot presets, performer-relative side controls, separate azimuth/elevation/framing controls, an optional local reference frame and a conceptual schematic. It does not transform the reference image, reconstruct geometry or generate a guide. Guide creation and continuity review remain external/manual.

Loading a sheet restores recorded numeric controls and separate notes. Legacy sheets without parameters reset controls to their recorded preset or the front defaults; those defaults are not inferred from their camera prose. Their camera instruction remains intact. Legacy notes embedded in camera prose are not parsed or discarded. A modified draft requires confirmation before loading another scene. Invalid loads preserve the current draft. Loading a new scene clears its previous local reference image.

Changing controls recomputes the preset label; nonmatching values become Custom. Generated instructions now retain each preset's specific visibility/pose guidance. Manual text is never silently regenerated. Exports preserve unrelated scene fields, store separate `camera_notes`, retain the existing camera instruction/parameter fields, and reset review approvals and object visibility. A custom view exports `camera_choice: "custom"`; the rendering CLI consumes the camera instruction, not a fixed preset lookup. Reference-image bytes and paths are not exported.

Run existing preservation regressions and the new scene round-trip regression:

```sh
node tests/js/test_manual_text.cjs
node tests/js/test_current_controls.cjs
node tests/js/test_scene_roundtrip.cjs
```

Actual installed Edge tests covered file loading, local image display/clear, JSON download, keyboard Enter/arrow interaction, accessible slider names, labels, and 1440/390 px layouts. Sampled text contrast ratios were above 4.5:1. These checks do not constitute a full WCAG certification or a screen-reader user test. No H3 generation was needed for this interface-only revision.

Design reference: [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md), consulted as design guidance only; no external code executed or packages installed.
