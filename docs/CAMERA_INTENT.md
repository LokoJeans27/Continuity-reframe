# Camera-intent studio: local experimental prototype

This optional viewer orbits an **already prepared** depth-derived Gaussian proxy. Maya-style Alt+left drag orbits, Alt+middle drag pans, and Alt+right drag dollies. Trackpad modes, keyboard shortcuts and independent optical zoom are available; see [navigation controls](CAMERA_NAVIGATION.md). Sliders remain available. Pan moves both the camera and aim target, and export records both. Front, lateral and overhead shortcuts generate visible, editable instructions for manual image-guide creation. Coordinates are source-image axes, not anatomical left/right; positive elevation assumes vertical. At elevation90 the optical axis points down in those assumed axes. Gravity, focal length, metric scale and hidden geometry are not calibrated.

For a ready-to-open, nonpersonal demonstration, use the [synthetic example](../examples/camera_intent/README.md). It includes an artificial JPEG/proxy pair and a self-contained HTML. It is not an example of reconstructing a real video; no real-scene proxy/frame pair is bundled.

The repository deliberately contains no personal frame or splat payload. The template itself is not directly runnable until packaged with local inputs. Replace the placeholder paths below with your own files; quote paths containing spaces:

```sh
python ui/camera_intent/build_studio.py --data /path/to/proxy.json --frame /path/to/frame.jpg --out /path/to/private-studio.html
```

Open the resulting HTML locally in a WebGL-capable browser. The output must not exist. Python standard library only; no installation or network call is performed. The resulting file embeds your frame and proxy: keep it private unless you intend to share that media.

`proxy.json` requires `count` (1..100000), positive `target_depth`, and `buffer`: base64 little-endian float32 records, eight values per Gaussian: `x,y,z,r,g,b,sigma,opacity`. RGB and opacity are in0..1; sigma is positive. Projection assumes a640x360 reference with fx=fy=576 before zoom. The source frame should match that16:9 view. This is a specific prototype interchange format, **not** a generic PLY/splat importer. Automatic video-to-depth/proxy conversion is not implemented here. Use an appropriately licensed external generator and review its coordinate convention.

Export JSON records camera position, target, basis, projection, editable prompt and the original frame. Proxy capture is optional and explicitly orientation-only. Neither export nor the GUI contacts ChatGPT or H3. Attach the original and prompt manually; include the proxy capture only if useful. Review the generated guide before using the existing H3 workflow. The intent JSON is not a reviewed H3 scene sheet and cannot be passed directly as `--scene`. Its full prompt is for the external image tool, not for pasting verbatim into H3. Record the chosen target-view description in the scene camera field and complete the review separately; [CURRENT_WORKFLOW](CURRENT_WORKFLOW.md) gives the exact handoff.

Manual edits survive slider changes; regeneration requires confirmation. Exports indicate whether text matches current controls and keep review flags false. Extreme views reveal holes and stretched texture; those are missing evidence, not reliable surfaces. This viewer is static and does not reconstruct motion.

Tests: `node tests/js/test_camera_geometry.cjs`, `node tests/js/test_camera_intent_dom.cjs`, `python -B tests/python/test_studio_builder.py`, and `python -B tests/python/test_synthetic_example.py`. The earlier private prototype was exercised in Edge; the sanitized packaging, synthetic fixture and UI logic have automated tests, not a new end-to-end browser/GPU validation.


The current synthetic fixture uses 57,600 samples with a smaller footprint. Backing resolution follows display pixel ratio up to 2×; a footprint control exposes the sharpness/holes tradeoff. These changes address known sampling and resolution limits, but no new perceptual sharpness assessment in a real browser has yet been completed.
