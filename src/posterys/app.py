"""Local camera acquisition, pose inference and interactive display."""
import time

from .configuration import DEFAULT_CONFIG
from .detector import PostureDetector
from .measurements import measure
from .ui import WINDOW, WIDTH, HEIGHT, EXIT_RECT, WHITE


def main(config=None):
    config = config or DEFAULT_CONFIG
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

    cap = cv2.VideoCapture(config["camera_index"])

    try:
        cv2.namedWindow(WINDOW, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(WINDOW, on_mouse)

        with mp.solutions.pose.Pose(
            min_detection_confidence=config["min_detection_confidence"],
            min_tracking_confidence=config["min_tracking_confidence"],
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
