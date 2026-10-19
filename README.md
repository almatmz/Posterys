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

All members contribute to computer vision, backend development, client integration, testing and documentation. Feature ownership identifies a coordinator; it does not restrict a member to one technical layer. Contributions must be recorded through each member's own Git account and reviewed by another team member.

**Supervisor:** Нәдіров Нұртас Қонысұлы.

## Scope

**Planned scope:** seated live feedback; guided full-body live and photo/video assessment; reference calibration and quality checks; desktop background monitoring and configurable reminders; history, statistics, preventive information and PDF reports; privacy and storage controls. Desktop targets are Windows and macOS; web workflows use a browser.

**Outside the initial scope:** native mobile apps, footprint analysis, clinical diagnosis, direct measurement of muscle tension, and proof of long-term clinical effectiveness.

## Current development status

- A local Python webcam prototype is implemented; the team has reported successful operation on Windows.
- It automatically captures a stable reference, displays GOOD POSTURE / BAD POSTURE relative to it, and shows NO DATA when landmarks are unreliable.
- EXIT, Esc, Q and the window close control finish the session and release the camera.
- The prototype processes camera frames locally without recording or uploading them.
- Three editable PlantUML diagrams and their image exports have been prepared. The component diagram is a draft hybrid proposal.
- Five static UI mockups cover seated monitoring, full-body assessment, results, background operation and history/reminders. See [UX mockups](docs/ux/README.md). Usability evaluation is pending.
- React/Electron clients, FastAPI integration, background operation, database storage, full-body assessment and PDF reports are planned.
- macOS execution, formal camera evaluation and the remaining submission materials are pending. See the documentation index.

GOOD POSTURE means within the chosen reference thresholds; the prototype does not verify that the reference is healthy. The thresholds are experimental and measure selected 2D head/shoulder changes.

## Technologies

**Current prototype:** Python, MediaPipe Pose 0.10.21, OpenCV, NumPy and standard-library unittest. Dependency versions are recorded in requirements.txt; the prototype uses the legacy mp.solutions.pose API.

**Draft target stack:** React, Electron, local MediaPipe inference for seated monitoring, Python/FastAPI for user-requested full-body analysis, and PostgreSQL. Alternatives and rationale are documented in the technology comparison; this target stack is not yet the implemented integrated product.

## Platforms and prerequisites

Use 64-bit CPython 3.10 for the commands below, Git, and an accessible webcam. Create a virtual environment separately on each computer.

| Platform | Installation target                            | Verification status                                                      |
| -------- | ---------------------------------------------- | ------------------------------------------------------------------------ |
| Windows  | x86-64; Python 3.10                            | Existing prototype run reported by the team; formal test record pending. |
| macOS    | macOS 13+; Intel or Apple Silicon; Python 3.10 | Instructions provided; native installation and camera test pending.      |

The macOS 13+ target follows the published wheels for the pinned OpenCV version. Package availability does not establish that the application has been tested on that platform.

## Setup and execution

If the repository has been published and your account has access, clone it into a new directory. Repository contents and access have not been verified for this README package:

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

Allow camera access when requested. On macOS, camera permissions are managed in System Settings > Privacy & Security > Camera for the application used to launch the prototype.

Keep the camera fixed, use sufficient light, and include the face and both shoulders. Sit upright and hold still for approximately three seconds during automatic setup. Unstable or missing observations restart setup. Restart the application to capture a different reference.

## Testing

Run the core tests from the project root.

Windows:

```powershell
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

macOS:

```bash
./venv/bin/python -m pip check
./venv/bin/python -m unittest discover -s tests -v
```

Automated tests use synthetic landmarks and check reference capture, quality gating, image scale/aspect handling, and status changes. They do not establish real-camera accuracy or native GUI compatibility.

Manual checks on each target platform:

1. Complete setup while sitting upright; expect GOOD POSTURE.
2. Tilt the shoulders or move the head relative to the reference; check for BAD POSTURE and recovery when returning.
3. Cover the camera or move required landmarks out of view; expect NO DATA.
4. In separate runs, exit using EXIT, Esc and the window close control; confirm the process ends and releases the camera.

Record the OS, CPU architecture, Python version, camera/setup conditions, expected and actual outcomes, and defects. A formal evaluation plan must define labelled data, metrics, measurement conditions and a baseline.

## Documentation and project tracking

- [Documentation index and submission status](docs/README.md)
- [UX mockups and requirement mapping](docs/ux/README.md)
- [Supervisor review report — Google Docs](https://docs.google.com/document/d/1ozC7s9Gv_CD32tUh_pMsK2LaQbnglrGmf8uyfv52y80/edit)
- [System Context source](diagrams/system_context_diagram.puml)
- [Use Case source](diagrams/use_case_diagram.puml)
- [Draft Component source](diagrams/component_diagram.puml)
- [GitHub Issues - task tracking](https://github.com/almatmz/Posterys/issues)

This README package contains documentation only. It does not include source code, dependencies, diagrams or PNG exports; copy these README files into the existing project.
