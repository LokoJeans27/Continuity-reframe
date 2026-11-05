# Recent local camera-intent pilot

Two manually generated image guides, moderate (requested25deg azimuth/15deg elevation) and overhead (requested90deg), were tested with the same authorized seated reference clip. Personal media, file identifiers, local paths and splat payloads are excluded from this repository.

Both local Ref2VA runs completed:800x480,90frames at24fps (3.75s short experimental pilot),20steps,seed18840101,reference size max. Machine:RTX5070Ti16GB;Python3.13.12;Torch2.13.0+cu130; existing isolated ComfyUI0.34.3 stack described elsewhere in this repo. No paid API.

| Guide | Server execution | Sampled total GPU memory peak |
|---|---:|---:|
| Moderate |486.474s|12353MiB|
| Overhead |448.260s|12517MiB|

Memory sampled every15s can miss peaks. Both runs are below the usual124-frame recommendation. These results do not establish optimal settings or cross-machine reproducibility.

Sampled visual review found recognizable torso sway and pointing in both. The moderate view changed initial lean, gaze and amplitude; overhead maintained a superior view but changed head orientation and the final hand shape. The overhead guide already inferred unseen floor and altered an object's support, and the video retained that defect. Exact identity, pose, anatomical trajectories and calibrated camera angles are not validated.

Sparse background tracking in limited top/right regions measured maximum median displacement below0.4px; this supports local image-space stability only. It does not validate scene geometry. Full video/audio decoding succeeded. Comparison audio packets matched the prepared AAC source, which was previously reencoded; exact lip synchronization was not tested. Original audio was used for delivery rather than generated audio.

This is evidence that the manual camera-intent → image-guide → local H3 chain executed, not proof of faithful unseen geometry. No personal media is required to run the automated code tests. Model terms and territorial restrictions remain applicable; see the dependency notices.
