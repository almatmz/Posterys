"""Reference capture, temporal smoothing and feedback classification."""
import math
from statistics import median

from .measurements import angle_difference
from .ui import GREEN, RED, YELLOW


class PostureDetector:
    # Экспериментальные пороги относительно начального положения.
    LIMITS = (6.0, 0.12, 0.15)
    STABILITY = (3.0, 0.06, 0.08)

    def __init__(self):
        self.reference = None
        self.samples = []
        self.smoothed = None
        self.last_seen = None

    def update(self, current, now):
        if current is None:
            self.samples.clear()
            self.smoothed = None
            self.last_seen = None

            return (
                "NO DATA",
                YELLOW,
                "More light; keep face and both shoulders visible.",
            )

        dt = 0 if self.last_seen is None else now - self.last_seen

        if dt > 1:
            self.samples.clear()
            self.smoothed = None

        self.last_seen = now

        # Автоматически запоминаем исходное положение.
        if self.reference is None:
            self.samples.append((now, current))
            first = self.samples[0][1]

            values = [
                (angle_difference(value[0], first[0]), value[1], value[2])
                for _, value in self.samples
            ]

            stable = all(
                max(value[i] for value in values)
                - min(value[i] for value in values) <= limit
                for i, limit in enumerate(self.STABILITY)
            )

            if not stable:
                self.samples = [(now, current)]

            elapsed = now - self.samples[0][0]

            if elapsed < 3 or len(self.samples) < 15:
                return (
                    f"SIT STRAIGHT: {max(0, 3 - elapsed):.1f}s",
                    YELLOW,
                    "Face the camera and hold still for setup.",
                )

            first = self.samples[0][1]

            self.reference = (
                first[0] + median(
                    angle_difference(value[0], first[0])
                    for _, value in self.samples
                ),
                median(value[1] for _, value in self.samples),
                median(value[2] for _, value in self.samples),
            )

            self.samples.clear()

        # Сглаживание уменьшает дрожание результата.
        if self.smoothed is None:
            self.smoothed = current
        else:
            alpha = 1 - math.exp(-dt / 0.2)
            previous = self.smoothed

            self.smoothed = (
                previous[0] + alpha * angle_difference(
                    current[0], previous[0]
                ),
                previous[1] + alpha * (current[1] - previous[1]),
                previous[2] + alpha * (current[2] - previous[2]),
            )

        differences = (
            abs(angle_difference(
                self.smoothed[0], self.reference[0]
            )),
            abs(self.smoothed[1] - self.reference[1]),
            abs(self.smoothed[2] - self.reference[2]),
        )

        reasons = (
            "Shoulders tilted.",
            "Head shifted sideways.",
            "Head position changed vertically.",
        )

        for difference, limit, reason in zip(
            differences, self.LIMITS, reasons
        ):
            if difference > limit:
                return "BAD POSTURE", RED, reason

        return "GOOD POSTURE", GREEN, "Close to your starting position."
