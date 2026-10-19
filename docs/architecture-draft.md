# Posterys — Architecture Description

**Version:** 0.1
**Date:** 19 October 2026
**Status:** Draft hybrid architecture; production integration pending

## 1. Scope and implementation status

The proposed system combines shared web/desktop interfaces, local seated-posture processing and server-based full-body assessment.

Desktop targets are Windows and macOS.

The existing implementation is a standalone Python/OpenCV/MediaPipe prototype. It captures a camera stream, establishes a reference, displays selected upper-body deviations and releases the camera on exit.

React clients, backend services, database storage, background monitoring and PDF reporting are planned.

React, Electron, FastAPI, PostgreSQL and the production CV runtimes remain draft choices requiring technology comparison and integration checks.

## 2. Architecture views

- [System Context](../diagrams/system_context_diagram.puml): users, external camera/OS and the overall system boundary.
- [Use Cases](../diagrams/use_case_diagram.puml): planned user scenarios and desktop-only background operation.
- [Component Diagram](../diagrams/component_diagram.puml): client, backend and storage responsibilities.

Component arrows represent calls/dependencies. Returned results are omitted. The arrows do not show a chronological sequence of every camera frame.

## 3. Component responsibilities

| Component               | Responsibility                                                                                                                                                                      |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shared User Interface   | Proposed React screens for camera controls, feedback, media selection, results, history and settings in web/desktop clients.                                                        |
| Camera and Media Access | Permissions, camera lifecycle and selected files. Coordinates capture ownership between foreground and background modes.                                                            |
| Local Posture Engine    | Seated landmark inference, quality checks, reference capture and reference-relative measurements/feedback. Production client integration is separate from the Python demonstration. |
| Desktop Agent           | Proposed Electron tray/menu-bar operation, periodic local checks and native reminders. Desktop only.                                                                                |
| HTTP API                | Proposed FastAPI boundary for explicit full-body requests, accounts, optional metric synchronisation, saved results and reports. Validates requests and enforces access/limits.     |
| Full-body CV Pipeline   | Selected-model inference, landmark quality checks and view-appropriate measurements. Returns results, unavailable metrics and explanations.                                         |
| Application Services    | Accounts, consent settings, saved sessions, statistics, preventive information, PDF generation and deletion.                                                                        |
| PostgreSQL              | Proposed persistent storage for accounts, settings and consented structured measurements.                                                                                           |

The camera and operating system are external dependencies.

Camera permission and native-notification availability depend on the platform and user settings.

## 4. Main data flows

### 4.1 Seated foreground monitoring

1. The user starts monitoring and grants camera access.
2. Camera and Media Access supplies frames to the Local Posture Engine.
3. The engine checks required landmarks and establishes a stable reference.
4. Supported head/shoulder measurements are compared with the reference.
5. The interface displays setup, within-reference, deviation or insufficient-data feedback.
6. Stopping ends processing and releases camera access.

Camera frames remain local.

Optional consented measurement synchronisation uses the API.

Local desktop monitoring does not require a remote account or an available server after installation with required assets.

The reference is user-selected. Frontal 2D observations do not directly measure muscle strain or establish spinal diagnoses.

### 4.2 Desktop background monitoring

The user explicitly enables background mode.

The Desktop Agent requests checks from the same Local Posture Engine at interval N while the main window is hidden.

Valid sustained deviations may produce native reminders according to configured duration and repeat limits.

Invalid tracking does not trigger posture reminders.

Pause/Stop ends checks and releases camera access. Capture ownership is transferred when switching monitoring modes.

The web version provides foreground monitoring. Browser background monitoring is outside this proposal.

### 4.3 Full-body assessment

1. The user selects live full-body assessment or a photo/video file.
2. The interface explains framing and server processing before the user requests analysis.
3. The API validates the request and invokes the Full-body CV Pipeline.
4. The pipeline returns supported measurements, landmarks, quality warnings and explanations.
5. The API returns results to the client.
6. With storage consent, the API passes structured results to Application Services for persistence.

Media limits must be enforced server-side.

Unsupported or inadequately visible measurements remain unavailable.

Raw media are temporary processing inputs under a documented cleanup policy. Indefinite raw-media storage is outside this design.

### 4.4 History, statistics and reports

An authenticated user requests their own saved sessions through the API.

Application Services verifies ownership and reads PostgreSQL.

Statistics separate assessed time from unknown time.

PDF output uses the same values and definitions as the interface.

Deletion follows the same ownership checks.

Revoking future storage consent prevents subsequent session saves. Existing records remain available for explicit deletion.

## 5. Data handling and failure behaviour

| Data / condition                   | Intended handling                                                                                                             |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Seated camera frames               | Local processing memory; no automatic server upload or raw-media recording.                                                   |
| Full-body frames or selected media | Explicit server request; temporary processing and cleanup on completion, failure or cancellation under a documented policy.   |
| Measurements and history           | Persistent storage/synchronisation under corresponding user controls. Include timestamps, view, quality and pipeline version. |
| Accounts and settings              | Protected remote records; credentials/secrets excluded from public source and application logs.                               |
| Invalid tracking                   | NO DATA/unavailable measurements; no stale valid assessment or posture reminder.                                              |
| Camera unavailable                 | Explain the state and preserve usable exit/stop controls.                                                                     |
| Server unavailable                 | Show a full-body/history error; local desktop seated monitoring remains independent.                                          |

Access control, HTTPS deployment, cleanup and privacy behaviour require implementation and testing.

The diagram does not establish that these requirements have passed validation.

## 6. Requirement traceability

| Requirements | Responsible architecture area                                         |
| ------------ | --------------------------------------------------------------------- |
| FR-01–FR-04  | Shared UI, Camera and Media Access, Local Posture Engine.             |
| FR-05, FR-06 | Desktop Agent, Local Posture Engine, OS integration.                  |
| FR-07–FR-09  | Shared UI, HTTP API, Full-body CV Pipeline.                           |
| FR-10–FR-13  | HTTP API, Application Services, PostgreSQL.                           |
| FR-14, FR-15 | Capture/consent controls, HTTP API, Application Services, PostgreSQL. |

Detailed acceptance criteria:

- [Requirements](requirements.md)

Platform, reliability, performance, privacy and reporting checks:

- [Evaluation plan](evaluation-plan.md)

## 7. Open architectural decisions

- Final local CV runtime and full-body pose model.
- Supported landmarks, assessment views and measurement definitions.
- API contracts and storage schema.
- Media limits and temporary-file cleanup policy.
- Desktop packaging and native permissions/notifications on Windows and macOS.
- Background scheduling, inference/UI isolation and measured hardware requirements.

Resolve these through technology comparison and integration experiments.

Update related requirements, diagrams and evaluation cases together.
