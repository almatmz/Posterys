# Posterys — Initial Requirements Specification

**Version:** 0.1
**Date:** 19 October 2026
**Status:** Draft for team and supervisor review

## 1. Purpose

Posterys is a proposed integrated web and desktop system for preliminary posture analysis and preventive feedback.

The system has two main assessment scenarios:

1. Seated upper-body monitoring during computer work.
2. Guided full-body assessment through a live camera or uploaded photographs and videos.

Desktop applications target Windows and macOS. Background monitoring and native reminders are desktop-only features.

This document describes the intended product. It does not claim that all requirements are already implemented.

For the first pre-defence on 24 October, the team provides an initial specification alongside the other required analysis, design, prototype and planning materials.

## 2. Priorities and requirement sources

### Priorities

- **Must:** required for the minimum intended final product.
- **Should:** important planned functionality whose scheduling may be adjusted through a documented scope decision.
- **Could:** optional future functionality.

### Sources

- **S1 — Project scope:** agreed web, desktop, seated monitoring and full-body assessment scenarios.
- **S2 — User interviews:** preliminary evidence concerning privacy, reminders, understandable feedback and reliability. Participant identifiers and the consolidated findings still require verification.
- **S3 — Prototype:** local Python implementation and nine passing core tests reported on Windows.
- **S4 — Engineering proposal:** initial design decisions and candidate technical targets requiring evaluation.

Interview preferences are not treated as universal preferences. Synthetic tests do not establish clinical accuracy or cross-platform compatibility.

## 3. Functional requirements

| ID    | Requirement                                           | Priority | Acceptance criteria                                                                                                                                                                                                                                                                                                                                                                                                                        | Source     |
| ----- | ----------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| FR-01 | Control camera monitoring.                            | Must     | Users can start and stop a session and identify when the camera is active. Permission denial produces an explanation. Stop or Exit ends analysis and releases camera access within 2 seconds under documented test conditions.                                                                                                                                                                                                             | S1, S2, S4 |
| FR-02 | Establish a reference position for seated monitoring. | Must     | Setup explains camera placement and framing. The initial configuration requires at least 3 seconds and 15 stable valid observations. Invalid or unstable observations interrupt reference capture. Users can renew the reference after moving the camera. The interface explains that the reference is user-selected.                                                                                                                      | S1, S3     |
| FR-03 | Analyse seated head and shoulder position.            | Must     | Web and desktop foreground monitoring compare valid measurements with the reference. Crossing documented thresholds produces a deviation state; returning within them restores the reference state. Measurements and thresholds are documented.                                                                                                                                                                                            | S1, S3     |
| FR-04 | Display feedback and tracking quality.                | Must     | Text and colour distinguish reference setup, within-reference posture, detected deviation and insufficient data. Required landmarks are displayed. Unreliable landmarks produce NO DATA, and camera failure produces a camera-unavailable message. Invalid observations do not retain a previous green assessment.                                                                                                                         | S1, S2, S3 |
| FR-05 | Monitor posture in the desktop background.            | Must     | Users explicitly enable background monitoring and select a sampling interval N. Checks continue while the main window is hidden. Windows tray or macOS menu-bar controls allow users to pause, stop or exit. Pause/Stop prevents further checks and releases camera access.                                                                                                                                                                | S1, S2     |
| FR-06 | Send configurable desktop reminders.                  | Must     | Users can enable or mute reminders and configure deviation duration T and repeat interval C. Valid consecutive samples indicating a sustained deviation trigger one notification when OS settings permit. Brief deviations and invalid tracking do not trigger reminders. Notifications are not repeated before C elapses. Test configuration: N=1 second, T=10 seconds and C=60 seconds; these are test settings, not medical thresholds. | S1, S2, S4 |
| FR-07 | Provide guided live full-body assessment.             | Must     | Web and desktop interfaces explain the required view and framing. Users explicitly start server processing. Suitable observations produce supported measurements. Missing required landmarks produce guidance and unavailable measurements. Stop ends capture and further frame submission.                                                                                                                                                | S1, S2     |
| FR-08 | Analyse uploaded photographs and videos.              | Must     | Supported inputs include JPEG/PNG images and documented MP4 codecs. File-size and duration limits are displayed and enforced. Boundary, unsupported, oversized and corrupted inputs are tested. Video results identify sampled-frame timestamps. Failed processing is not reported as a successful assessment.                                                                                                                             | S1, S4     |
| FR-09 | Explain assessment results.                           | Must     | Results show the assessment view, landmark overlay, available measurements, units or ratio definitions, quality warnings and explanations. Missing measurements are marked unavailable. GOOD/BAD prototype labels are explained as comparisons with a reference. Results do not claim a medical diagnosis or direct measurement of muscle tension.                                                                                         | S1, S2     |
| FR-10 | Provide accounts for saved remote history.            | Must     | Users can register, sign in and sign out. Unauthenticated requests cannot access protected sessions. One account cannot access another account's sessions. Local desktop seated monitoring remains available without a remote account after installation.                                                                                                                                                                                  | S1, S2, S4 |
| FR-11 | Provide history and daily/weekly statistics.          | Should   | With storage consent, users can list and open saved sessions. Statistics identify the period and timezone and separate valid assessed time from unknown time. A fixture containing 8 minutes within reference, 2 minutes of deviation and 3 unknown minutes produces 20% deviation over 10 valid minutes; unknown time is reported separately.                                                                                             | S1, S2, S4 |
| FR-12 | Provide preventive information.                       | Should   | Recommendations identify their applicable situation, explanation and information source. Insufficient tracking produces camera/framing guidance. Content provides general preventive information rather than treatment prescribed from a landmark result.                                                                                                                                                                                  | S1, S2     |
| FR-13 | Export PDF assessment reports.                        | Should   | Reports contain the session date, selected measurements and definitions, quality warnings and limitations. Values match the interface. Reports open on Windows and macOS. Photographs are included only with separate image-use consent.                                                                                                                                                                                                   | S1, S2     |
| FR-14 | Control transmission and storage.                     | Must     | Seated/background camera frames remain local. Users are informed before explicitly requesting server-based full-body processing. Storage and synchronisation have explicit controls. Network and storage checks confirm that disabled options cause no corresponding upload or persistent session record. Temporary media follow a documented cleanup policy.                                                                              | S1, S2, S4 |
| FR-15 | Inspect and delete saved data.                        | Must     | Users can view and delete their own saved session measurements. Deleted sessions no longer appear in normal history/API queries. Other users' records remain unchanged. Revoking storage consent prevents future saves. Cache and temporary-media handling are documented and tested.                                                                                                                                                      | S2, S4     |

## 4. Non-functional requirements

Numerical targets below are initial engineering proposals, not measured results or clinically validated limits.

Evaluation records must identify hardware, software versions and test conditions. Any revised target must have a documented rationale.

| ID     | Requirement                                     | Priority | Acceptance criteria                                                                                                                                                                                                                                                                                                                             | Source     |
| ------ | ----------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| NFR-01 | Platform compatibility.                         | Must     | Supported OS, runtime and CPU combinations are documented. Installation and core manual scenarios are checked on Windows x86-64 and the advertised macOS 13+ Intel/Apple Silicon combinations. Web scenarios are checked in documented Chromium browser versions on Windows and macOS. Untested combinations remain marked pending.             | S1, S4     |
| NFR-02 | Responsive seated foreground analysis.          | Must     | Candidate target: at 640×480 input, at least 5 processed observations per second and p95 frame-receipt-to-feedback latency of no more than 500 ms during a 60-second steady-state test on declared reference hardware. Record CPU/RAM usage, dropped frames and unknown observations. Background mode follows its configured sampling interval. | S2, S4     |
| NFR-03 | Stability and failure handling.                 | Must     | A 30-minute local monitoring test completes without an uncaught crash. Separate tests cover denied/busy camera access, lost tracking and unavailable server. Failures produce clear states, preserve usable Stop/Exit controls and do not retain stale valid assessments. Server failure does not block local desktop monitoring.               | S2, S4     |
| NFR-04 | Offline local processing and data minimisation. | Must     | After installation with required model assets present, local desktop reference capture, feedback and exit work without network access. Inspection finds no persistent raw seated images/videos or automatic transmission of them. Storage and synchronisation settings match observed network/storage behaviour.                                | S2, S4     |
| NFR-05 | Protection of accounts and records.             | Must     | An externally deployed API uses HTTPS. Secrets and credentials are excluded from source control and logs. Passwords are stored using a suitable password-hashing mechanism. Tests with unauthenticated requests and two accounts verify ownership checks for reading and deleting sessions. Upload limits are enforced server-side.             | S2, S4     |
| NFR-06 | Understandable and accessible controls.         | Must     | Every monitoring state has a readable text label. Colour is not the only indication. Pause/Stop or Exit is reachable within two actions from an active monitoring view. Relevant controls are checked with mouse and keyboard on supported desktop platforms.                                                                                   | S2, S4     |
| NFR-07 | Reproducible setup and testing.                 | Must     | A fresh environment can follow the README, install declared dependencies and execute the core test suite. Record the tested revision, OS, architecture, runtime/dependency versions and outcomes. Camera checks are recorded separately from synthetic-data tests.                                                                              | S3, S4     |
| NFR-08 | Consistent measurements and reporting.          | Must     | Saved results identify timestamps, assessment view, quality state, measurement definitions and pipeline version. Fixtures produce consistent values in results, history, statistics and PDF outputs. Unknown observations are excluded from valid posture-duration calculations.                                                                | S1, S2, S4 |

The NFR-02 performance target applies to seated foreground monitoring. Full-body processing benchmarks and upload limits must be defined in the evaluation plan before accepting those features.

## 5. Traceability to the architecture

| Scenario                         | Requirements                        | Intended components                                                   |
| -------------------------------- | ----------------------------------- | --------------------------------------------------------------------- |
| Seated foreground monitoring     | FR-01–FR-04, NFR-02, NFR-06         | Shared UI, Camera and Media Access, Local Posture Engine              |
| Desktop background monitoring    | FR-05, FR-06, NFR-03, NFR-04        | Desktop Agent, Local Posture Engine, OS integration                   |
| Full-body live/upload assessment | FR-07–FR-09, NFR-01, NFR-03, NFR-05 | Shared UI, Camera and Media Access, HTTP API, Full-body CV Pipeline   |
| Accounts, history and reports    | FR-10–FR-13, NFR-05, NFR-08         | HTTP API, Application Services, PostgreSQL                            |
| Consent and deletion             | FR-14, FR-15, NFR-04, NFR-05        | Shared UI, capture/consent controls, Application Services, PostgreSQL |
| Setup and verification           | NFR-01, NFR-07                      | README, dependencies, tests and evaluation records                    |

Architecture sources:

- [System Context](../diagrams/system_context_diagram.puml)
- [Use Cases](../diagrams/use_case_diagram.puml)
- [Draft Component Diagram](../diagrams/component_diagram.puml)

## 6. Current implementation coverage

| Area                      | Current status                                                                                                                                                                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| FR-01–FR-04               | Partially covered by the standalone Python prototype: camera capture, automatic reference, selected 2D measurements, status/quality feedback and exit. Renewing the reference currently requires restarting. Web integration and full acceptance testing remain pending. |
| FR-05–FR-15               | Planned functionality. Corresponding product acceptance tests have not been executed.                                                                                                                                                                                    |
| Core logic tests          | Nine synthetic-input tests have passed, with successful Windows unittest output reported by the team. These tests cover selected algorithm behaviour rather than the complete specification.                                                                             |
| Non-functional evaluation | Native macOS execution, fresh-environment installation, performance measurements, endurance, account isolation and usability validation remain pending.                                                                                                                  |

## 7. Scope boundaries and open decisions

The initial baseline excludes:

- Native mobile applications.
- Footprint assessment.
- Clinical diagnosis.
- Direct measurement of muscle tension.
- Proof of long-term clinical effectiveness.

The following require further review:

- Draft hybrid architecture and final model choices.
- Reminder defaults.
- Upload limits and supported video codecs.
- Reference hardware and proposed performance targets.
- Changes arising from the interview synthesis, literature review and technology comparison.

Requirement changes must retain their IDs or document replacements and update the corresponding acceptance criteria.
