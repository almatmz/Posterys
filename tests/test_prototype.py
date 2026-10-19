import math
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.prototype import PostureDetector, angle_difference, measure


BASE = (0.0, 0.0, 0.5)


def make_landmarks():
    points = [
        SimpleNamespace(x=0.5, y=0.5, visibility=1.0)
        for _ in range(33)
    ]

    points[0] = SimpleNamespace(
        x=0.5, y=0.25, visibility=1.0
    )
    points[11] = SimpleNamespace(
        x=0.3, y=0.6, visibility=1.0
    )
    points[12] = SimpleNamespace(
        x=0.7, y=0.6, visibility=1.0
    )

    return points


def calibrate(detector):
    for frame in range(16):
        detector.update(BASE, frame / 5)


class PrototypeTests(unittest.TestCase):
    def test_scale_and_translation_preserve_measurements(self):
        points = make_landmarks()
        before = measure(points, 1000, 500)

        for point in points:
            point.x = 0.5 + 0.5 * (point.x - 0.5)
            point.y = 0.6 + 0.5 * (point.y - 0.5)

        after = measure(points, 1000, 500)

        self.assertIsNotNone(before)
        self.assertIsNotNone(after)

        for actual, expected in zip(after, before):
            self.assertAlmostEqual(actual, expected)

    def test_angle_accounts_for_image_aspect_ratio(self):
        points = make_landmarks()
        points[12].y += 0.1

        features = measure(points, 1000, 500)

        self.assertAlmostEqual(
            features[0],
            math.degrees(math.atan2(50, 400)),
        )

    def test_missing_or_invisible_landmarks_are_rejected(self):
        self.assertIsNone(measure(None, 1000, 500))

        for index in (0, 11, 12):
            with self.subTest(index=index):
                points = make_landmarks()
                points[index].visibility = 0

                self.assertIsNone(
                    measure(points, 1000, 500)
                )

    def test_invalid_coordinates_and_tiny_shoulders_are_rejected(self):
        for value in (float("nan"), float("inf"), -1, 2):
            with self.subTest(value=value):
                points = make_landmarks()
                points[0].x = value

                self.assertIsNone(
                    measure(points, 1000, 500)
                )

        points = make_landmarks()
        points[12].x = points[11].x + 0.01

        self.assertIsNone(measure(points, 1000, 500))

    def test_reference_requires_three_seconds(self):
        detector = PostureDetector()

        for frame in range(15):
            label = detector.update(BASE, frame / 5)[0]
            self.assertTrue(
                label.startswith("SIT STRAIGHT")
            )

        self.assertEqual(
            detector.update(BASE, 3)[0],
            "GOOD POSTURE",
        )

    def test_deviation_and_return_change_status(self):
        deviations = (
            (12, 0, 0.5),
            (0, 0.3, 0.5),
            (0, 0, 0.8),
        )

        for changed in deviations:
            with self.subTest(changed=changed):
                detector = PostureDetector()
                calibrate(detector)

                for frame in range(5):
                    label = detector.update(
                        changed, 3.2 + frame / 5
                    )[0]

                self.assertEqual(label, "BAD POSTURE")

                for frame in range(5):
                    label = detector.update(
                        BASE, 4.2 + frame / 5
                    )[0]

                self.assertEqual(label, "GOOD POSTURE")

    def test_missing_data_does_not_retain_green_status(self):
        detector = PostureDetector()
        calibrate(detector)

        self.assertEqual(
            detector.update(None, 3.1)[0],
            "NO DATA",
        )

        self.assertEqual(
            detector.update((15, 0, 0.5), 3.2)[0],
            "BAD POSTURE",
        )

    def test_unstable_pose_or_long_gap_prevents_reference(self):
        detector = PostureDetector()

        for frame in range(30):
            detector.update(
                (10 if frame % 2 else 0, 0, 0.5),
                frame / 5,
            )

        self.assertIsNone(detector.reference)

        detector = PostureDetector()
        detector.update(BASE, 0)

        self.assertEqual(
            detector.update(BASE, 10)[0],
            "SIT STRAIGHT: 3.0s",
        )

        self.assertIsNone(detector.reference)

    def test_shoulder_angle_uses_shortest_line_difference(self):
        self.assertAlmostEqual(
            angle_difference(-89, 89), 2
        )


if __name__ == "__main__":
    unittest.main()