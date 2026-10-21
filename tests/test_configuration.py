import json
from pathlib import Path
import tempfile
import unittest

from src.posterys.configuration import DEFAULT_CONFIG, load_config


class ConfigurationTests(unittest.TestCase):
    def load_values(self, values):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            path.write_text(json.dumps(values), encoding="utf-8")
            return load_config(path)

    def test_example_matches_legacy_defaults(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(load_config(root / "config/prototype.example.json"), DEFAULT_CONFIG)
        self.assertEqual(load_config(), DEFAULT_CONFIG)

    def test_partial_config_preserves_remaining_defaults(self):
        self.assertEqual(self.load_values({"camera_index": 1}), dict(DEFAULT_CONFIG, camera_index=1))

    def test_invalid_values_are_rejected(self):
        for values in ([], {"typo": 1}, {"camera_index": -1}, {"camera_index": True},
                       {"min_detection_confidence": 2}, {"min_tracking_confidence": float("nan")},
                       {"min_tracking_confidence": "0.5"}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                self.load_values(values)
