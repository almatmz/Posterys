"""Image-space landmark validation and head/shoulder measurements."""
import math


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
