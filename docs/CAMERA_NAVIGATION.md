# Camera-intent navigation and sharpness

These controls are Maya-style shortcuts, not an exact Maya/Blender navigation implementation. They apply to the camera-intent viewer, not the older text selector or ComfyUI canvas.

| Input | Action |
|---|---|
| Alt + left drag | Orbit around the current target |
| Alt + middle drag; middle drag; Shift + drag | Pan; the scene at the target depth follows the pointer |
| Alt + right drag; Ctrl + drag | Dolly; right moves closer, left moves farther |
| Plain drag | Selected Orbit / Pan / Dolly mode; useful on a trackpad |
| Wheel | Dolly toward/away; wheel up moves closer |
| Shift + wheel | Optical zoom; changes field of view without moving camera |
| Arrow keys | Orbit |
| Shift + arrows | Pan |
| + / − or the close/far buttons | Dolly |
| F or Reset camera | Restore original eye/target, orbit distance and optical zoom |

The default orbit direction was reversed relative to the previous viewer: drag right decreases azimuth; drag down increases elevation. Separate horizontal/vertical inversion checkboxes reverse only orbit. Pan stays screen-relative and does not unexpectedly change direction at lateral or overhead angles. Physical orbit has parallax: not every surface can follow the pointer equally, especially when the estimated pivot differs from the subject depth.

Coordinates retain the existing proxy convention: +X is source-image right, +Y is source-image down, +Z goes away from the source camera. Navigation up is −Y, an assumed scene vertical rather than calibrated gravity. Positive azimuth places the eye toward source-image right; positive elevation places it above the target. At exact overhead, azimuth rotates the framing around the vertical axis. No roll control or arbitrary gravity correction is implemented.

Pan translates both eye and target along camera right/down axes. Orbit then uses that shifted target. Dolly changes eye-to-target distance while leaving target and focal length fixed; optical zoom changes focal length only. Export keeps `position`, `target`, `target_offset`, `orbit_radius`, basis and projection, plus navigation preferences. The generated image prompt includes eye/target and pan values in explicitly arbitrary proxy units. Manual prompts remain untouched when navigating and report a mismatch with current controls until regenerated. There is no automatic intent-to-scene/H3 conversion.

## Why the example could look soft

The previous artificial fixture sampled every4 pixels (14,400 points), with a Gaussian sigma equivalent to2.4 source pixels. The canvas also used CSS dimensions for its backing buffer. These are code-level sources of softness/coarse sampling, not a perceptual diagnosis of the user's particular screen.

The updated fixture samples every2 pixels (57,600 points), reduces sigma to1.1 source pixels and increases opacity from0.9 to0.98. The backing buffer uses device pixel ratio, capped at2 for cost. The Gaussian-size control scales footprint from0.5× to1.5× without changing camera or source data. Smaller sizes can reveal holes; larger sizes smooth them while blending details. The source JPEG is still640×360, so no setting recovers missing detail at large display sizes or extreme views.

All points are sorted by depth on each render. More samples and high-DPI rendering can cost frame time; interactive performance and subjective sharpness on the actual browser are not certified. The example remains synthetic planes, not a real-scene reconstruction.

## Checks

Automated tests cover orbit directions and independent inversion, Alt button mappings, pan at front/lateral/oblique/overhead views, separate dolly/FOV behavior, keyboard/trackpad controls, exported eye/target and2× backing resolution. They use a DOM/WebGL stub and do not establish real-browser rendering or pointer-event behavior. A real-browser check is attempted separately when computer control is available; no success is implied here.
