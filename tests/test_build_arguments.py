"""Argument data served by the site must come from the current build."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


class ArgumentBuildTest(unittest.TestCase):
    def test_built_packet_is_copied_after_regeneration(self):
        script = Path(__file__).resolve().parents[1] / "site" / "build.py"
        spec = importlib.util.spec_from_file_location("ipvv_site_build_test", script)
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        with tempfile.TemporaryDirectory() as directory:
            build.ROOT = Path(directory) / "site"
            build.DIST = build.ROOT / "dist"
            build.PATALA = Path(directory) / "patalacheckpoints"
            build.TF = lambda *_args, **_kwargs: "html"
            build.work_sidenav = lambda *_args: ""
            build.arg_essay_links = lambda *_args: ""
            source = build.ROOT / "data" / "translations"
            source.mkdir(parents=True)
            (source / "testwork.json").write_text(json.dumps([{
                "chunk": "test-p01-v01", "gate": "PASS", "sanskrit": "fresh source",
                "l2": "A translation."}]), encoding="utf-8")
            old_packets = build.ROOT / "data" / "arguments"
            old_packets.mkdir(parents=True)
            (old_packets / "testwork-test-p01-v01.json").write_text(
                json.dumps({"sanskrit": "stale source"}), encoding="utf-8")

            self.assertEqual(build.build_arguments(), 1)
            new_file = old_packets / "testwork-test-p01-v01.json"
            served_file = build.DIST / "data" / "arguments" / new_file.name
            self.assertEqual(json.loads(served_file.read_text())["sanskrit"], "fresh source")
            self.assertEqual(served_file.read_bytes(), new_file.read_bytes())


if __name__ == "__main__":
    unittest.main()
