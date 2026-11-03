#!/usr/bin/env python3
"""Extract timestamped evidence frames; never infer scene content or overwrite files."""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
import shutil
import statistics
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, capture_output=True, text=True)


def probe(path: Path, frames: bool = False) -> dict:
    command = ["ffprobe", "-v", "error"]
    if frames:
        command += ["-select_streams", "v:0", "-show_frames", "-show_entries",
                    "frame=best_effort_timestamp_time,duration_time,pkt_duration_time"]
    else:
        command += ["-show_streams", "-show_format"]
    return json.loads(run(command + ["-of", "json", str(path)]).stdout)


def finite_positive(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be finite and greater than zero")
    return number


def nearest_index(times: list[float], target: float) -> int:
    position = bisect.bisect_left(times, target)
    candidates = [i for i in (position - 1, position) if 0 <= i < len(times)]
    return min(candidates, key=lambda i: (abs(times[i] - target), i))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", required=True, type=Path,
                        help="new, non-existing output directory; never overwritten")
    parser.add_argument("--start", type=float, default=0.0,
                        help="seconds from first displayed video frame (default: 0)")
    parser.add_argument("--duration", type=finite_positive,
                        help="sampling window duration; does not trim the source")
    parser.add_argument("--samples", type=int, default=8, help="2–48 even samples")
    parser.add_argument("--times", help="comma-separated source-relative seconds; overrides --samples")
    parser.add_argument("--max-width", type=int, default=1280,
                        help="analysis PNG maximum width, never upscale (default: 1280)")
    parser.add_argument("--extract-audio", action="store_true",
                        help="decode full first audio stream to float32 WAV; not trimmed to sample window")
    args = parser.parse_args()
    if not math.isfinite(args.start) or args.start < 0:
        parser.error("--start must be finite and nonnegative")
    if not 2 <= args.samples <= 48 or not 64 <= args.max_width <= 8192:
        parser.error("--samples must be 2–48 and --max-width 64–8192")
    source = args.source.expanduser().resolve(strict=True)
    if not source.is_file():
        parser.error("source must be a local file")
    destination = args.out.expanduser().resolve()
    if destination.exists():
        parser.error("output directory already exists; choose a new directory")
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            parser.error(f"{binary} is missing; no software is installed automatically")

    metadata = probe(source)
    video = next((s for s in metadata["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in metadata["streams"] if s["codec_type"] == "audio"), None)
    if video is None:
        parser.error("source has no video stream")
    if video.get("disposition", {}).get("attached_pic"):
        parser.error("the first video stream is cover art; prepare a source with the intended video first")
    raw_frames = probe(source, frames=True).get("frames", [])
    if not raw_frames or any("best_effort_timestamp_time" not in f for f in raw_frames):
        parser.error("missing frame presentation timestamps; cannot establish reliable sampling")
    pts = [float(f["best_effort_timestamp_time"]) for f in raw_frames]
    if not all(math.isfinite(t) for t in pts) or any(b < a for a, b in zip(pts, pts[1:])):
        parser.error("non-finite or non-monotonic frame timestamps; inspect source before sampling")
    times = [t - pts[0] for t in pts]
    intervals = [b - a for a, b in zip(times, times[1:]) if b > a]
    median_interval = statistics.median(intervals) if intervals else 0.0
    end = args.start + args.duration if args.duration else math.inf
    eligible = [i for i, t in enumerate(times) if args.start <= t < end]
    if not eligible:
        parser.error("sampling window contains no displayed frames")
    eligible_times = [times[i] for i in eligible]
    if args.times:
        try:
            targets = [float(t.strip()) for t in args.times.split(",")]
        except ValueError:
            parser.error("--times must contain comma-separated numeric seconds")
        if not 1 <= len(targets) <= 48 or any(
            not math.isfinite(t) or t < args.start or t >= end or t > times[-1]
            for t in targets
        ):
            parser.error("provide 1–48 times inside the sampling window and source frame range")
    else:
        lo, hi = eligible_times[0], eligible_times[-1]
        targets = [lo + (hi - lo) * i / (args.samples - 1) for i in range(args.samples)]
    selected_for_target = [eligible[nearest_index(eligible_times, t)] for t in targets]
    selected = sorted(set(selected_for_target))
    destination.mkdir(parents=True, exist_ok=False)
    commands = []
    expression = "+".join(f"eq(n\\,{i})" for i in selected)
    filters = f"select={expression},scale=w=min(iw\\,{args.max_width}):h=-1"
    command = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n",
               "-i", str(source), "-map", "0:v:0", "-an", "-vf", filters,
               "-fps_mode", "passthrough", "-frames:v", str(len(selected)),
               "-start_number", "0", str(destination / "sample_%03d.png")]
    run(command)
    commands.append(command)
    names = {index: f"sample_{position:03d}.png" for position, index in enumerate(selected)}
    if any(not (destination / name).is_file() for name in names.values()):
        raise RuntimeError("ffmpeg did not produce every expected sample")

    audio_result = None
    if args.extract_audio and audio is not None:
        audio_path = destination / "full_source_audio.wav"
        command = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n",
                   "-i", str(source), "-map", "0:a:0", "-vn", "-c:a", "pcm_f32le",
                   str(audio_path)]
        run(command)
        commands.append(command)
        audio_result = {"file": audio_path.name, "mode": "full_first_audio_stream_decoded_float32",
                        "not_trimmed_to_sampling_window": True,
                        "note": "No sample-rate or channel changes requested. Original timestamps are not carried by WAV; use source stream offsets. This is decoded audio, not a bitstream copy.",
                        "output_metadata": probe(audio_path)}

    digest = hashlib.sha256()
    with source.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    samples = [{"file": names[i], "source_frame_index_zero_based": i,
                "source_pts_seconds": pts[i], "source_relative_seconds": times[i],
                "window_relative_seconds": times[i] - args.start} for i in selected]
    manifest = {
        "schema_version": 1, "source_filename": source.name, "source_sha256": digest.hexdigest(),
        "source_probe": metadata, "first_video_pts_seconds": pts[0],
        "decoded_video_frames": len(pts), "sample_window": {
            "start_seconds": args.start, "duration_seconds": args.duration,
            "time_basis": "seconds_from_first_displayed_video_frame"},
        "timing": {"median_positive_frame_interval_seconds": median_interval,
                   "nonuniform_frame_intervals": bool(intervals) and any(
                       abs(d - median_interval) > 0.0001 for d in intervals),
                   "duplicate_pts_count": sum(a == b for a, b in zip(pts, pts[1:])),
                   "last_frame_relative_seconds": times[-1]},
        "samples": samples,
        "requested_samples": [{"requested_source_relative_seconds": target,
                               "selected_file": names[index],
                               "actual_source_relative_seconds": times[index],
                               "sampling_error_seconds": times[index] - target}
                              for target, index in zip(targets, selected_for_target)],
        "audio": {"source_has_audio": audio is not None, "extraction": audio_result,
                  "source_audio_start_seconds": audio.get("start_time") if audio else None,
                  "alignment_verified": False},
        "limits": ["No semantic, cut, identity, or audio-content analysis performed.",
                   "PNG previews use ffmpeg autorotation and may not preserve mastering color/HDR.",
                   "No fps normalization or H3 inference performed.",
                   "Frame indexing follows the first decoded video stream.",
                   "Full source was scanned; prefer shot-sized files for speed."],
        "commands": commands,
        "ffmpeg_version": run(["ffmpeg", "-version"]).stdout.splitlines()[0],
        "ffprobe_version": run(["ffprobe", "-version"]).stdout.splitlines()[0],
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(destination), "samples": len(samples),
                      "audio_extracted": audio_result is not None}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError):
            print(error.stderr, file=sys.stderr)
        print("Source was not modified. Partial output, if any, remains for inspection.", file=sys.stderr)
        sys.exit(1)
