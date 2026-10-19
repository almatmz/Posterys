# Posterys — Verification and Evaluation Plan

**Version:** 0.1
**Date:** 19 October 2026
**Status:** Initial plan; manual results and measurements pending

## 1. Purpose and evaluation stages

Evaluate whether Posterys implements its requirements and provides understandable preliminary feedback about selected visible posture changes.

### First pre-defence

- Provide this evaluation plan.
- Retain the existing automated tests and their actual results.
- Check the current local webcam prototype.
- Collect real demonstration screenshots.
- Record limitations and unresolved defects.

### Later implementation

- Execute a labelled-data benchmark.
- Compare the current algorithm with a baseline.
- Measure performance.
- Validate web, background, full-body and remote-history features when implemented.

The current prototype compares selected 2D head/shoulder measurements with a user-selected reference. GOOD POSTURE means within experimental reference thresholds. This evaluation does not establish a healthy reference, a diagnosis, direct muscle tension or clinical benefit.

Related materials:

- [Requirements](requirements.md)
- [Prototype](../src/prototype.py)
- [Automated tests](../tests/test_prototype.py)

## 2. Test conditions

For each executed test, record:

- Test ID, date and tester.
- Source revision or dated source snapshot.
- Operating system and version.
- CPU, CPU architecture and RAM.
- Camera model and actual resolution.
- Python and dependency versions.
- Camera placement, approximate distance and lighting.
- Visible body area.
- Reference procedure and thresholds.
- Expected result, actual result and evidence.

Use a fixed frontal camera with the face and both shoulders visible. Establish a new reference after moving the camera.

Keep conditions identical when comparing algorithms. Record Windows and macOS results separately.

## 3. Existing automated tests

The team supplied Windows unittest output showing:

**9 tests passed.**

These tests use synthetic landmarks and timestamps. They do not access a real camera or exercise native GUI controls.

Covered behaviour:

- Measurement behaviour under scale and translation.
- Image aspect-ratio handling.
- Missing and low-visibility landmarks.
- Invalid coordinates and insufficient shoulder span.
- Reference timing.
- Deviation and return transitions.
- Loss of tracking.
- Unstable reference setup and observation gaps.
- Shoulder-angle wrapping.

### Windows command

Run from the project root:

    .\venv\Scripts\python.exe -m unittest discover -s tests -v

### macOS command

Run from the project root:

    ./venv/bin/python -m unittest discover -s tests -v

The macOS command is an instruction, not evidence of an executed macOS test.

These tests partially support FR-02–FR-04. They do not establish camera accuracy, complete product acceptance or cross-platform compatibility.

## 4. Manual checks for the current prototype

Every case remains pending until its actual outcome is recorded.

| ID   | Procedure                                                                                                        | Expected result                                                                                                                                                                          | Requirement                   |
| ---- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| M-01 | Launch with camera access and hold the chosen reference position.                                                | Setup continues until at least 3 seconds and 15 stable valid observations are obtained; then GOOD POSTURE appears.                                                                       | FR-01–FR-04, partial          |
| M-02 | After setup, change shoulder tilt, horizontal head position and vertical head position separately; then return.  | Changes exceeding documented thresholds produce BAD POSTURE with an explanation. Returning restores GOOD POSTURE after smoothing settles. Record missed or unstable transitions.         | FR-03, FR-04                  |
| M-03 | Leave the frame or obstruct required landmarks, then restore visibility.                                         | Rejected observations produce NO DATA instead of stale green feedback. Analysis resumes when observations become valid. Record cases where the model incorrectly accepts an obstruction. | FR-04, NFR-03                 |
| M-04 | Move during initial setup or interrupt tracking, then hold still.                                                | Movements exceeding stability limits or invalid observations interrupt setup. A reference is established only after a new stable interval satisfies both requirements.                   | FR-02                         |
| M-05 | In separate runs, exit using EXIT, Q, Esc and the window close control.                                          | Every supported exit ends the process and releases camera access. Check the proposed 2-second release target.                                                                            | FR-01, NFR-06, partial        |
| M-06 | Launch with camera access genuinely unavailable or denied.                                                       | CAMERA UNAVAILABLE appears when capture fails; exit remains usable. A busy-camera case applies only when the OS prevents shared capture.                                                 | FR-01, FR-04, NFR-03, partial |
| M-07 | After installing dependencies and required model assets, disable networking and repeat setup, feedback and exit. | Local monitoring still works. Availability is recorded separately from network/storage inspection.                                                                                       | NFR-04, partial               |
| M-08 | Run local monitoring for 30 minutes, including tracking loss and recovery.                                       | No uncaught crash or persistent stale assessment. Exit remains usable. Record resource use and capture stalls.                                                                           | NFR-03, partial               |

Full acceptance of FR-01–FR-04 remains pending. The prototype starts capture on launch, and renewing the reference requires restarting. Web integration and final session controls are separate implementation work.

## 5. Planned labelled-data pilot

### Pilot design

Proposed exploratory dataset:

- 3 consenting adult volunteers.
- 2 lighting conditions.
- 5 scenarios.
- 2 repetitions.
- 10 seconds per segment, excluding reference setup.

Total: 60 proposed segments.

Scenarios:

1. Reference-like position.
2. Shoulder tilt.
3. Horizontal head shift.
4. Vertical head shift.
5. Unavailable view or obstructed required body parts.

After reference setup, each segment contains:

- 2 seconds near reference.
- 5 seconds in the selected scenario.
- 3 seconds returning near reference.

The reference-only scenario remains near reference throughout. Annotators record actual transition times.

Keep camera geometry fixed within each comparison. Do not require participants to hold uncomfortable positions.

This is a feasibility pilot, not a representative population study. Report the actual participant and segment counts.

The current prototype does not record video or export benchmark logs. Separately consented recordings and a benchmark capture/logging process are planned work.

### Independent annotation

Two team members independently label predetermined evaluation times:

- **REFERENCE:** visibly close to the established reference.
- **DEVIATION:** visible change in a supported head/shoulder relationship.
- **UNKNOWN:** required body parts are absent, obstructed or not assessable.

Annotators must not see model predictions or calculate labels from the tested thresholds.

Resolve disagreements and record their count before scoring. Flag ambiguous samples and decide how to handle them before inspecting predictions.

Labels describe visible reference-relative changes, not medical conditions.

### Development and evaluation separation

For the three-person pilot:

- Use one participant for development and tuning.
- Keep two participants for held-out evaluation.
- Assign these groups before tuning.
- Freeze thresholds before the held-out run.
- Disclose any later tuning.

Do not randomly distribute neighbouring frames between development and evaluation.

Use one predetermined sample per second for classification scores. Use full timestamped predictions for transition measurements.

Report counts by participant and segment. Adjacent samples are not independent participants.

A smaller single-person study must be described as an exploratory session-based check rather than evaluation on unseen users.

## 6. Baseline comparison and quality metrics

### Compared methods

**B0 — Unsmoothed baseline**

Same pose landmarks, quality checks, reference procedure, measurements and thresholds, but classify each valid observation without temporal smoothing.

**P1 — Current method**

The same pipeline with the prototype's existing temporal smoothing.

Replay identical timestamped observations into both methods. Reset and calibrate both identically.

This comparison evaluates smoothing's effect on false transitions and response delay. It does not compare pose-estimation models or independently establish the benefit of calibration.

The baseline harness and comparison remain unimplemented.

### Metrics

| Metric                                 | Definition                                                                                                                                                        |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Three-state confusion matrix           | Compare REFERENCE/DEVIATION/UNKNOWN labels with GOOD POSTURE/BAD POSTURE/NO DATA predictions after setup.                                                         |
| Deviation precision                    | TP / (TP + FP): correctly detected deviations divided by all BAD POSTURE predictions. False BAD predictions on UNKNOWN inputs count as false positives.           |
| Deviation recall                       | TP / (TP + FN): detected deviations divided by all labelled deviations. NO DATA on a labelled deviation counts as a miss.                                         |
| Deviation F1                           | 2 × precision × recall / (precision + recall). Report undefined results as N/A with counts.                                                                       |
| Valid-input coverage                   | Proportion of REFERENCE/DEVIATION-labelled observations receiving a GOOD/BAD assessment.                                                                          |
| Incorrect assessment of UNKNOWN inputs | Proportion of UNKNOWN-labelled observations receiving GOOD or BAD instead of NO DATA.                                                                             |
| Transition delay                       | Time from an annotated visible change until the matching state remains for 1 second. Report detection and return delays separately, including missed transitions. |
| False transitions                      | Incorrect transitions per minute during labelled stable-reference segments.                                                                                       |

Report results for B0 and P1 per participant and overall, including denominators and failure examples.

Do not claim that P1 performs better unless the measurements support that conclusion.

Classification scores have not yet been measured. Acceptance targets require pilot evidence and must be fixed before the subsequent held-out acceptance evaluation.

## 7. Performance evaluation

### Seated foreground monitoring

Use documented reference hardware and a 640×480 input.

Exclude model loading and reference setup. Measure a 60-second steady-state interval.

Candidate targets from NFR-02:

- At least 5 processed observations per second.
- p95 application processing/presentation-submission latency of no more than 500 ms.

Timestamp immediately after frame receipt and when submitting the updated preview to the GUI.

This is an application-side proxy for rendered feedback. It excludes camera exposure, OS buffering and physical display latency.

Record:

- Processed observations.
- Failed camera reads.
- Invalid observations.
- Measurable dropped frames.
- CPU and RAM usage.
- Runtime and model versions.

Report unavailable measurements explicitly. Measure the 30-minute stability scenario separately.

Performance instrumentation remains planned work; no measured performance results are currently claimed.

## 8. Later product verification

| Area                             | Planned verification                                                                                                                                                                                                                                                                                              | Requirements                         |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Desktop background and reminders | Test hidden-window operation, sampling, pause/stop, notifications, mute, invalid tracking and repeat suppression on Windows/macOS. Use N=1 s, T=10 s and C=60 s as a test fixture.                                                                                                                                | FR-05, FR-06; NFR-01, NFR-03, NFR-06 |
| Full-body live and upload        | Test framing instructions, explicit server requests, stop, unavailable measurements, explanations and supported media. Include oversized, boundary, corrupted and unsupported inputs. Fix limits, codecs and processing-time budgets before acceptance. Record resolution, duration, network and server hardware. | FR-07–FR-09; NFR-01, NFR-03, NFR-05  |
| Accounts and privacy             | Use unauthenticated requests and two accounts to verify ownership checks. Inspect consent changes, network traffic, stored records, temporary files and cleanup. Check HTTPS, credential handling and server-side limits.                                                                                         | FR-10, FR-14, FR-15; NFR-04, NFR-05  |
| History, statistics and PDF      | Verify consistent values, timestamps, timezone, measurement definitions and pipeline version. A fixture with 8 minutes reference, 2 deviation and 3 unknown must report 20% deviation over 10 valid minutes, with unknown time separate. Check image-use consent.                                                 | FR-11, FR-13; NFR-08                 |
| Recommendations and usability    | Review information sources and applicability. Ask pilot users to identify the state, stop monitoring and explain a warning. Record task completion, assistance and errors. Check keyboard/mouse controls and text/colour feedback.                                                                                | FR-09, FR-12; NFR-06                 |
| Platforms and reproducibility    | Check fresh installation and documented scenarios on every advertised Windows/macOS architecture and browser version. Identify untested combinations explicitly.                                                                                                                                                  | NFR-01, NFR-07                       |

## 9. Evidence and result records

For each executed test, complete:

| Field                                | Entry           |
| ------------------------------------ | --------------- |
| Run/test ID, date and tester         | To be completed |
| Source snapshot and environment      | To be completed |
| Requirement and procedure            | To be completed |
| Expected result                      | To be completed |
| Actual result and measurements       | Not measured    |
| Status                               | Not run         |
| Evidence and defect/retest reference | To be completed |

Available statuses:

- Pass.
- Fail.
- Blocked.
- Not run.

Explain any not-applicable case.

Capture real GOOD POSTURE, BAD POSTURE and NO DATA demonstrations. Use the tester's own image or obtain permission. Public evidence should remove identifying details while preserving the actual displayed result.

Benchmark recordings must follow the agreed consent and retention conditions.

## 10. Current evidence summary

- Nine synthetic core tests passed in the supplied Windows output.
- The user reported successful local prototype operation on Windows.
- Individual manual cases still require recorded results.
- Native macOS execution remains pending.
- Labelled-data scores, baseline comparison, latency and endurance measurements remain pending.
- Future product features have not completed acceptance testing.

Before the first pre-defence, prioritise documented manual checks and real demonstration evidence.

Record macOS results if a target machine is available. Otherwise, retain its pending status and assign the validation task.

This plan alone does not establish measured accuracy, cross-platform compatibility or clinical effectiveness.
