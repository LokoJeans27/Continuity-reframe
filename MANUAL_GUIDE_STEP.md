# Manual image reference step

1. Inspect decoded source frames and frame_manifest.json. Labels assume constant frame rate. Use multiple moments, including the initial pose and the full gesture.
2. Select a camera brief and decide field of view and occlusions BEFORE listing visible objects. Do not relocate an object to force it into frame. Unknown hidden space remains an uncertainty.
3. Complete a new scene sheet: subject, camera, visible/partial objects with frame evidence, omitted objects and timed actions.
4. Supply selected frames to ChatGPT or another image tool manually. Request one compatible initial frame with sufficient gesture margin. No image-generation adapter is included.
5. Inspect anatomy, pose, contacts, background perspective, object positions and gesture margins. A different actor orientation alone does not prove a new camera. Reject invalid guides and retain the failed files for comparison.
6. Save a new guide image and reviewed scene sheet. Only then build and execute H3. Review output beside source and guide. Keep source-audio and native-audio results distinct.

Visibility and review flags are human editorial assertions, not automated scene understanding. Free-text fields can still introduce an invalid object and must be reviewed.
