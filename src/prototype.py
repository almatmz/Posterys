import math
from statistics import median
import time


WINDOW = "Posterys - Posture Prototype"
WIDTH, HEIGHT = 960, 660

EXIT_RECT = (800, 590, 940, 640)

GREEN = (80, 210, 90)
RED = (80, 80, 240)
YELLOW = (50, 210, 245)
WHITE = (235, 235, 235)


def angle_difference(value, reference):
    return (value - reference + 90.0) % 180.0 - 90.0


def measure(landmarks, width, height):
    """Измеряем положение носа и плеч в координатах изображения."""
    if landmarks is None or len(landmarks) < 13 or min(width, height) <= 0:
        return None

    points = []

    # Нос, левое плечо, правое плечо.
    for index in (0, 11, 12):
        point = landmarks[index]

        if not all(
            math.isfinite(value)
            for value in (point.x, point.y, point.visibility)
        ):
            return None

        if not (
            0 <= point.x <= 1
            and 0 <= point.y <= 1
            and 0.6 <= point.visibility <= 1
        ):
            return None

        points.append((point.x * width, point.y * height))

    head, left, right = points
    shoulder_span = math.dist(left, right)

    if shoulder_span < 0.12 * width:
        return None

    middle_x = (left[0] + right[0]) / 2
    middle_y = (left[1] + right[1]) / 2

    angle = math.degrees(
        math.atan2(right[1] - left[1], right[0] - left[0])
    )

    return (
        angle_difference(angle, 0),
        (head[0] - middle_x) / shoulder_span,
        (middle_y - head[1]) / shoulder_span,
    )


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


def main():
    import cv2
    import mediapipe as mp
    import numpy as np

    if not hasattr(mp, "solutions"):
        raise RuntimeError(
            "This prototype requires mediapipe==0.10.21"
        )

    detector = PostureDetector()
    running = True

    def on_mouse(event, x, y, flags, param):
        nonlocal running

        x1, y1, x2, y2 = EXIT_RECT

        if (
            event == cv2.EVENT_LBUTTONDOWN
            and x1 <= x <= x2
            and y1 <= y <= y2
        ):
            running = False

    def text(image, value, x, y, scale=0.65, color=WHITE):
        cv2.putText(
            image,
            value,
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            scale,
            color,
            2,
            cv2.LINE_AA,
        )

    cap = cv2.VideoCapture(0)

    try:
        cv2.namedWindow(WINDOW, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(WINDOW, on_mouse)

        with mp.solutions.pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as pose:
            while running:
                canvas = np.full(
                    (HEIGHT, WIDTH, 3),
                    (28, 28, 32),
                    dtype=np.uint8,
                )

                frame = None

                if cap.isOpened():
                    success, captured = cap.read()

                    if success and captured is not None and captured.size:
                        frame = cv2.flip(captured, 1)

                features = None
                landmarks = None

                if frame is not None:
                    height, width = frame.shape[:2]

                    result = pose.process(
                        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    )

                    if result.pose_landmarks:
                        landmarks = result.pose_landmarks.landmark
                        features = measure(landmarks, width, height)

                label, color, hint = detector.update(
                    features, time.monotonic()
                )

                if frame is None:
                    label = "CAMERA UNAVAILABLE"
                    hint = "Close other camera apps and restart."

                elif features is not None:
                    dots = [
                        (
                            int(landmarks[i].x * width),
                            int(landmarks[i].y * height),
                        )
                        for i in (0, 11, 12)
                    ]

                    cv2.line(frame, dots[1], dots[2], color, 3)

                    for point in dots:
                        cv2.circle(frame, point, 7, color, -1)

                if frame is not None:
                    scale = min(920 / width, 460 / height)

                    preview_width = max(1, round(width * scale))
                    preview_height = max(1, round(height * scale))

                    preview = cv2.resize(
                        frame, (preview_width, preview_height)
                    )

                    x = 20 + (920 - preview_width) // 2
                    y = 65 + (460 - preview_height) // 2

                    canvas[
                        y:y + preview_height,
                        x:x + preview_width,
                    ] = preview

                text(
                    canvas,
                    "POSTERYS | Posture prototype",
                    20, 38, 0.9,
                )

                text(canvas, label, 20, 568, 1.0, color)
                text(canvas, hint, 20, 607, 0.6)

                cv2.rectangle(
                    canvas,
                    EXIT_RECT[:2],
                    EXIT_RECT[2:],
                    (65, 65, 185),
                    -1,
                )

                text(canvas, "EXIT", 839, 623, 0.8)

                cv2.imshow(WINDOW, canvas)

                key = cv2.waitKey(20) & 0xFF

                if key in (27, ord("q"), ord("Q")):
                    break

                try:
                    if cv2.getWindowProperty(
                        WINDOW, cv2.WND_PROP_VISIBLE
                    ) < 1:
                        break
                except cv2.error:
                    break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()