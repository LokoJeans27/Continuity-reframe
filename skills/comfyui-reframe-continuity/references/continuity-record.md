# Scene record and prompt brief

Use a small JSON/YAML record or equivalent legible notes. The schema is a guide, not a reason to invent values. Keep stable IDs across samples, prompts, and evaluation. Distinguish scene/world relations, person-local anatomical directions, and image/screen coordinates.

## Minimum record

```yaml
source:
  asset: source.mp4
  sha256: record_from_file
  shot: shot_01
  interval_seconds: [0.0, 4.0]
  time_basis: seconds_from_first_displayed_video_frame
  video: {fps: measured, variable_frame_rate: unknown, frame_count: measured}
  audio: {present: measured, source_offset_seconds: measured_or_unknown}
target:
  camera_location: behind_A_and_to_A_anatomical_left
  look_toward: B_face
  height: approximately_A_eye_level
  framing: medium_over_shoulder
  camera_motion: fixed
  may_change: [camera_view, screen_positions, occlusion, background_perspective]
  must_preserve: [identities, clothing, physical_actions, object_ownership, event_order]
subjects:
  - id: A
    distinguishing_features: only_visible_supported_details
  - id: B
    distinguishing_features: only_visible_supported_details
facts:
  - relation: A_holds_cup_in_anatomical_right_hand
    status: observed
    evidence: [{source_time_seconds: 0.8, sample_file: sample_02.png}]
    confidence: high
    note: never_equate_anatomical_right_with_screen_right
  - relation: cupboard_continues_behind_A
    status: inferred
    evidence: []
    confidence: low
    alternative: unseen_wall_may_be_plain
unknowns: [back_of_cupboard, detail_of_A_left_hand_when_occluded]
events:
  - id: pass_cup
    source_interval_seconds: [1.2, 2.6]
    actor: A
    action: extends_right_hand_toward_B
    recipient: B
    object: cup
    phases: [approach, contact, transfer, release]
    verified_phases: [approach, contact]
    uncertain_phases: [transfer, release]
target_visibility:
  - entity: cup
    at_time_seconds: 0.0
    prediction: occluded_by_A_torso
    basis: target_camera_plus_observed_hand_position
    confidence: medium
    instruction: do_not_move_cup_into_view
```

Replace all descriptive placeholders with actual evidence or explicit `unknown`. Never reuse this illustrative action as a fact about another source. If a hand cannot be resolved, preserve the visible relation and mark handedness unknown rather than guessing.

## What to inspect

- **Identity:** count, distinguishing visible features, costume/accessory continuity. Do not infer real-world identity.
- **Space:** subject positions relative to landmarks, facing direction, depth/overlap, surface contact, light direction. Avoid unsupported metric distances.
- **Props:** identity, owner, location, orientation, hand/contact, changing state, onset of visibility. One object briefly hidden is not two objects.
- **Eyelines:** observer, target, eye/head/body alignment, evidence before and after turns. Do not force everyone to look at the new camera.
- **Motion:** action sequence and phases, starts/stops, touch/release, gaze shifts, locomotion. Use source timestamps. Distinguish object motion, camera motion, and cuts.
- **Audio:** whether present, dialogue/sound timing actually heard, the selected original track, start offset. A silent frame cannot establish what was spoken.
- **Uncertainty:** unseen regions, ambiguous mirror/reflection, truncated limbs, off-screen speakers, motion between sparse samples.

## Image-generation brief

Write in the generator's effective language while keeping any visible text unchanged:

“Create the initial frame of the same event from [target camera]. [Frame A] is time zero; [frames B–D] provide evidence of [specific identities/layout/props], not later poses to copy. Preserve [observed invariants]. From this viewpoint [visibility/overlap predictions]. The background must have [plausible perspective changes], with no unsupported detailed reconstruction of [unknown regions]. At time zero [precise action phase, hand, contact, eyeline]. Allow [known occlusions]. Do not reposition objects merely to display them.”

Do not use contradictory catchalls such as “keep everything exactly the same” while requesting a camera move. Say what remains physically the same and what should look different on screen.
