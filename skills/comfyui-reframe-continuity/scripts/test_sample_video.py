#!/usr/bin/env python3
"""Synthetic, local regression tests for sample_video.py. No model inference."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HELPER = Path(__file__).with_name("sample_video.py")


def command(args):
    return subprocess.run(args, capture_output=True, check=True)


def decoded_audio(path):
    return command(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0",
                    "-f", "f32le", "-"]).stdout


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe required")
class SampleVideoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from types import SimpleNamespace
        cls.temporary = SimpleNamespace(name=tempfile.mkdtemp(prefix="continuity-skill-test-"), cleanup=lambda: None) # Preserve fixtures; no deletion
        cls.root = Path(cls.temporary.name)
        cls.source = cls.root / "cfr.mp4"
        command(["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "lavfi", "-i",
                 "testsrc2=size=320x240:rate=25:duration=2", "-f", "lavfi", "-i",
                 "sine=frequency=440:sample_rate=48000:duration=2", "-c:v", "libx264",
                 "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(cls.source)])
        cls.source_digest = hashlib.sha256(cls.source.read_bytes()).hexdigest()
        cls.vfr = cls.root / "vfr.mp4"
        command(["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "lavfi", "-i",
                 "testsrc2=size=320x240:rate=25:duration=2", "-vf",
                 r"select=not(mod(n\,3))+gte(n\,25)", "-fps_mode", "vfr", "-c:v",
                 "libx264", "-pix_fmt", "yuv420p", str(cls.vfr)])

    @classmethod
    def tearDownClass(cls):
        assert hashlib.sha256(cls.source.read_bytes()).hexdigest() == cls.source_digest
        cls.temporary.cleanup()

    def sample(self, source, name, *args):
        output = self.root / name
        command([sys.executable, str(HELPER), str(source), "--out", str(output), *args])
        return output, json.loads((output / "manifest.json").read_text())

    def test_constant_rate_exact_indices(self):
        output, manifest = self.sample(self.source, "cfr_samples", "--samples", "6")
        self.assertEqual(manifest["decoded_video_frames"], 50)
        self.assertEqual([s["source_frame_index_zero_based"] for s in manifest["samples"]],
                         [0, 10, 20, 29, 39, 49])
        self.assertFalse(manifest["timing"]["nonuniform_frame_intervals"])
        self.assertEqual(len(list(output.glob("sample_*.png"))), 6)
        self.assertEqual(manifest["source_sha256"], self.source_digest)

    def test_variable_rate_and_window(self):
        _, manifest = self.sample(self.vfr, "vfr_samples", "--start", "0.24", "--duration",
                                  "1.3", "--times", "0.24,0.51,0.99,1.4", "--extract-audio")
        self.assertTrue(manifest["timing"]["nonuniform_frame_intervals"])
        self.assertEqual([s["source_relative_seconds"] for s in manifest["samples"]],
                         [0.24, 0.48, 1.0, 1.4])
        self.assertFalse(manifest["audio"]["source_has_audio"])
        self.assertIsNone(manifest["audio"]["extraction"])

    def test_decoded_audio_preservation(self):
        output, manifest = self.sample(self.source, "audio", "--extract-audio")
        self.assertEqual(decoded_audio(self.source), decoded_audio(output / "full_source_audio.wav"))
        self.assertFalse(manifest["audio"]["alignment_verified"])
        self.assertTrue(manifest["audio"]["extraction"]["not_trimmed_to_sampling_window"])

    def test_never_overwrites(self):
        output, _ = self.sample(self.source, "overwrite")
        before = (output / "manifest.json").read_bytes()
        result = subprocess.run([sys.executable, str(HELPER), str(self.source), "--out",
                                 str(output)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((output / "manifest.json").read_bytes(), before)

    def test_invalid_requests_have_no_output(self):
        for name, arguments in [("bad_range", ["--start", "99"]),
                                ("bad_time", ["--times", "nan"]),
                                ("bad_negative", ["--start", "-1"])]:
            with self.subTest(name=name):
                output = self.root / name
                result = subprocess.run([sys.executable, str(HELPER), str(self.source),
                                         "--out", str(output), *arguments], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
