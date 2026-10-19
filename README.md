# Posterys

**Diploma topic:** Development of an Integrated Software System for Primary Comprehensive Body Posture Analysis and Muscle Strain Prevention Based on Computer Vision.

## Problem, users and expected outcomes

Initial interviews describe prolonged seated work, forgotten breaks, and difficulty noticing posture changes while concentrating. They also identify concerns about camera privacy, inaccurate feedback, and intrusive reminders. These findings inform the requirements; recognition accuracy and preventive benefits remain to be evaluated.

**Target users:** university students and people performing prolonged computer-based work, including IT and office workers.

**Aim:** develop an integrated web and desktop system for preliminary camera-based posture feedback and preventive reminders.

**Expected outcomes:** shared web/desktop workflows, seated and full-body analysis, understandable results with quality warnings, consent-controlled history and reports, and documented evaluation of detection quality, performance and usability.

## Team and responsibilities

| Member                      | Group   | Planned feature ownership                                                                                     |
| --------------------------- | ------- | ------------------------------------------------------------------------------------------------------------- |
| Muzdybay Almat Amanzholuly  | SE-2413 | Seated monitoring: CV rules, backend integration, client workflow and tests.                                  |
| Samatova Zhanel Samatovna   | SE-2419 | Full-body assessment: CV pipeline, backend APIs, client workflow and tests.                                   |
| Diana Sabulla Ziyadullakyzy | SE-2401 | Background monitoring and analytics: CV quality/timing rules, backend statistics, desktop workflow and tests. |

All members contribute to computer vision, backend development, client integration, testing and documentation. Feature ownership identifies a coordinator; it does not restrict a member to one technical layer.

Contributions must be recorded through each member's own Git account and reviewed by another team member.

**Supervisor:** Нәдіров Нұртас Қонысұлы.

## Scope

**Planned scope:**

- Seated posture feedback through a webcam.
- Guided full-body assessment through live camera input or uploaded photographs/videos.
- Reference calibration and landmark quality checks.
- Desktop background monitoring and configurable reminders.
- History, statistics, preventive information and PDF reports.
- Privacy and storage controls.
- Desktop applications targeting Windows and macOS, alongside browser-based workflows.

**Outside the initial scope:**

- Native mobile applications.
- Footprint analysis.
- Clinical diagnosis.
- Direct measurement of muscle tension.
- Proof of long-term clinical effectiveness.

## Current development status

- A local Python webcam prototype is implemented; the team has reported successful operation on Windows.
- It automatically captures a stable reference, displays GOOD POSTURE / BAD POSTURE relative to it, and shows NO DATA when landmarks are unreliable.
- EXIT, Esc, Q and the window close control finish the session and release the camera.
- The prototype processes camera frames locally without recording or uploading them.
- Three editable PlantUML diagrams and their image exports have been prepared. The component diagram is a draft hybrid proposal.
- React/Electron clients, FastAPI integration, background operation, database storage, full-body assessment and PDF reports are planned.
- macOS execution, formal camera evaluation and the remaining submission materials are pending. See the documentation index.

GOOD POSTURE means within the chosen reference thresholds. The prototype does not verify that the reference is healthy. The thresholds are experimental and measure selected 2D head/shoulder changes.

## Technologies

**Current prototype:**

- Python.
- MediaPipe Pose 0.10.21.
- OpenCV.
- NumPy.
- Standard-library unittest.

Dependency versions are recorded in requirements.txt. The prototype uses the legacy mp.solutions.pose API.

**Draft target stack:**

- React for shared web/desktop interfaces.
- Electron for the desktop application and system integration.
- Local MediaPipe inference for seated monitoring.
- Python/FastAPI for user-requested full-body analysis and application services.
- PostgreSQL for structured storage.

Target choices must be justified in the technology comparison before being treated as final.

## Platforms and prerequisites

Use 64-bit CPython 3.10 for the commands below, Git, and an accessible webcam.

Create a virtual environment separately on each computer.

| Platform | Installation target                            | Verification status                                                      |
| -------- | ---------------------------------------------- | ------------------------------------------------------------------------ |
| Windows  | x86-64; Python 3.10                            | Existing prototype run reported by the team; formal test record pending. |
| macOS    | macOS 13+; Intel or Apple Silicon; Python 3.10 | Instructions provided; native installation and camera test pending.      |

The macOS 13+ target follows the published wheels for the pinned OpenCV version. Package availability does not establish that the application has been tested on that platform.

## Setup and execution

Download the project into a new directory:

```text
git clone https://github.com/almatmz/Posterys.git
cd Posterys
```

### Windows - PowerShell

```powershell
py -3.10 -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe .\src\prototype.py
```

### macOS - Terminal

Install Python 3.10 first, then run:

```bash
python3.10 -m venv venv
./venv/bin/python -m pip install --upgrade pip
./venv/bin/python -m pip install -r requirements.txt
./venv/bin/python src/prototype.py
```

Allow camera access when requested.

On macOS, camera permissions are managed in:

System Settings > Privacy & Security > Camera

Allow access for the application used to launch the prototype.

Keep the camera fixed, use sufficient light, and include the face and both shoulders. Sit upright and hold still for approximately three seconds during automatic setup.

Unstable or missing observations restart setup. Restart the application to capture a different reference.

## Testing

Run the core tests from the project root.

### Windows

```powershell
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

### macOS

```bash
./venv/bin/python -m pip check
./venv/bin/python -m unittest discover -s tests -v
```

Automated tests use synthetic landmarks and check reference capture, quality gating, image scale/aspect handling, and status changes.

They do not establish real-camera accuracy or native GUI compatibility.

### Manual checks on each target platform

1. Complete setup while sitting upright; expect GOOD POSTURE.
2. Tilt the shoulders or move the head relative to the reference; check for BAD POSTURE and recovery when returning.
3. Cover the camera or move required landmarks out of view; expect NO DATA.
4. In separate runs, exit using EXIT, Esc and the window close control; confirm the process ends and releases the camera.

Record the OS, CPU architecture, Python version, camera/setup conditions, expected and actual outcomes, and defects.

A formal evaluation plan must define labelled data, metrics, measurement conditions and a baseline.

## Documentation and project tracking

- [Documentation index and submission status](docs/README.md)
- [System Context source](diagrams/system_context_diagram.puml)
- [Use Case source](diagrams/use_case_diagram.puml)
- [Draft Component source](diagrams/component_diagram.puml)
- [GitHub Issues - task tracking](https://github.com/almatmz/Posterys/issues)

YouTrack is not required according to the instructor's clarification. GitHub Issues will track assigned, prioritised tasks with acceptance criteria and deadlines.

Use feature branches and pull requests, commit completed work progressively, and obtain another team member's review before merging into main.

Create the pre-defense-1 tag only after the submission is ready and its exact commit is identified.

Record supervisor review notes and follow-up decisions as they are received.
