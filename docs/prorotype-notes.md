# Posterys — Current Prototype Description

**Version:** 0.1
**Date:** 19 October 2026
**Implementation:** [src/prototype.py](../src/prototype.py)

## 1. Purpose

Demonstrate a local webcam workflow:

1. Detect selected upper-body landmarks.
2. Establish a reference position.
3. Compare current measurements with the reference.
4. Display feedback.
5. Release the camera on exit.

The prototype is a standalone Python application.

The integrated web/desktop product is described separately in the [architecture draft](architecture-draft.md).

## 2. Inputs and quality checks

Input is a live stream from camera device 0. The preview is horizontally mirrored.

MediaPipe Pose supplies landmarks. Analysis uses:

- Nose: index 0.
- Left shoulder: index 11.
- Right shoulder: index 12.

Each required point must:

- Have finite image coordinates.
- Be inside the frame.
- Have visibility between 0.6 and 1.

The distance between shoulders must be at least 12% of image width.

Rejected observations produce NO DATA.

Visibility is a model output, not a measured probability of correct posture.

## 3. Measurements

Normalised landmark coordinates are converted into image pixels before calculating geometry.

Let:

- L and R be shoulder positions.
- H be the nose position.
- M = (L + R) / 2 be the shoulder midpoint.
- S be the pixel distance between shoulders.

| Measurement            | Calculation / meaning                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| Shoulder angle         | atan2(R.y − L.y, R.x − L.x), converted to degrees and normalised for an unoriented shoulder line. |
| Horizontal head offset | (H.x − M.x) / S.                                                                                  |
| Vertical head gap      | (M.y − H.y) / S. This is an image-space ratio, not anatomical neck length.                        |

Shoulder-span normalisation reduces sensitivity to uniform image-plane scale.

Perspective changes, camera rotation and landmark errors can still affect measurements.

## 4. Reference and classification

Reference capture requires:

- At least 3 seconds.
- At least 15 stable valid observations.

Permitted measurement ranges during setup:

| Measurement            | Stability range      |
| ---------------------- | -------------------- |
| Shoulder angle         | 3 degrees.           |
| Horizontal head offset | 0.06 shoulder spans. |
| Vertical head gap      | 0.08 shoulder spans. |

Instability, missing observations or gaps longer than 1 second restart candidate reference capture.

The reference uses medians, with angle wrapping handled separately.

The user deliberately selects the intended starting position. The system does not verify that this position is healthy.

After setup, time-based exponential smoothing uses a 0.2-second time constant.

The smoothed measurements are compared with the reference:

| Measurement                   | Experimental deviation threshold  |
| ----------------------------- | --------------------------------- |
| Shoulder angle change         | Greater than 6 degrees.           |
| Horizontal head-offset change | Greater than 0.12 shoulder spans. |
| Vertical head-gap change      | Greater than 0.15 shoulder spans. |

Any exceeded threshold produces BAD POSTURE.

The explanation reports the first exceeded condition in the table order.

Otherwise, valid observations produce GOOD POSTURE.

These thresholds are engineering settings awaiting evaluation, not clinically validated boundaries.

## 5. Outputs and controls

| Output             | Meaning                                                     |
| ------------------ | ----------------------------------------------------------- |
| SIT STRAIGHT       | Initial reference capture is in progress.                   |
| GOOD POSTURE       | Supported measurements are within the reference thresholds. |
| BAD POSTURE        | At least one supported measurement exceeds its threshold.   |
| NO DATA            | Required landmark observations are unavailable or rejected. |
| CAMERA UNAVAILABLE | Camera opening or frame acquisition failed.                 |

The interface displays text/colour feedback, a reason or setup hint, and valid nose/shoulder markers.

Available exit controls:

- Clickable EXIT button.
- Q or q.
- Esc.
- Window close control.

Cleanup releases camera access and closes OpenCV windows.

After tracking loss, smoothing is reset but an established reference remains.

Renewing the reference requires restarting the prototype, including after moving the camera.

## 6. Scope and data handling

Frames are processed in memory. The application code contains no recording or upload calls.

This version implements visible feedback and exit.

Planned features include:

- Desktop background operation.
- Native reminders.
- Web/server integration.
- Full-body assessment.
- Persistent history.
- PDF reports.

Frontal 2D head/shoulder changes do not establish spinal curvature, anatomical forward-head angles, direct muscle tension or medical diagnoses.

Clinical effectiveness and recognition accuracy have not been established.

## 7. Verification evidence

The team supplied Windows output showing nine passing [core tests](../tests/test_prototype.py) using synthetic inputs.

Successful Windows operation was also reported.

The following remain pending:

- Recorded manual test cases.
- Native macOS validation.
- Camera-quality evaluation.
- Performance measurements.

Procedures and proposed targets are in the [evaluation plan](evaluation-plan.md).

Setup and execution commands are provided in the [project README](../README.md).
