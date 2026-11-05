# Synthetic camera-intent viewer example

**This is an artificial software fixture, not a reconstruction of a real scene.** It contains two analytic depth planes with a checkerboard and orange rectangle. It uses no personal image, model, external service or generated H3 output.

After cloning/downloading the repository, open `examples/camera_intent/ready/studio.html` locally in a WebGL-capable browser. GitHub's file page shows source rather than running HTML: download the repository or the HTML file first. The HTML is self-contained, so no server is needed. Use Alt+left drag to orbit, Alt+middle to pan, Alt+right to dolly, or select a trackpad drag mode. Wheel dollies; Shift+wheel changes optical zoom. See [all controls and axis conventions](../../docs/CAMERA_NAVIGATION.md). At extreme angles the planes become edge-on or reveal missing surfaces; that is an expected limitation of this fixture.

Included files:

- [frame.jpg](ready/frame.jpg): valid 640×360 JPEG with synthetic labels and shapes.
- [proxy.json](ready/proxy.json): 57,600 Gaussian records, little-endian float32, with known synthetic geometry.
- [studio.html](ready/studio.html): packaged viewer containing those two inputs.

To reproduce all three files, run from the repository root using the existing CLI Python with NumPy/OpenCV:

```sh
python -B examples/camera_intent/make_synthetic_example.py --out-dir ../continuity-synthetic-demo-new
```

The destination must not already exist. To package the bundled inputs independently (Python standard library only):

```sh
python -B ui/camera_intent/build_studio.py --data examples/camera_intent/ready/proxy.json --frame examples/camera_intent/ready/frame.jpg --out ../continuity-synthetic-viewer-new.html
```

Both commands were executed with new destinations. Tests decode the JPEG, validate Gaussian values/count, check front projection against the source, compare the packaged inputs with the standalone files, and exercise prompt/export logic. The frame was visually inspected. A new actual-browser/WebGL visual acceptance remains pending; DOM tests use a renderer stub.

This example only exercises the viewer and camera-intent handoff. There is **no real-scene proxy/frame pair**, no video and no compatible H3 guide bundled here. For your own scene, create the depth/proxy externally, then create the image guide manually in an authorized image tool. The kit does not automatically reconstruct a video, fill hidden surfaces or generate guides. See [camera-intent instructions](../../docs/CAMERA_INTENT.md).
