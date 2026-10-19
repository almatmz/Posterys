# Posterys — Project Plan, Responsibilities and Risks

**Version:** 0.1
**Date:** 19 October 2026
**Status:** Proposed plan for team review

## 1. Delivery stages

The first pre-defence on 24 October requires research, analysis, design, prototype and planning materials.

The complete integrated web/desktop application belongs to the later implementation stage.

Implemented features, planned features and completed tests must remain clearly distinguishable.

The instructor waived YouTrack. This document provides the initial work plan. GitHub Issues is the proposed tracker when repository preparation resumes.

Related documents:

- [Requirements](requirements.md)
- [Evaluation plan](evaluation-plan.md)
- [Documentation status](README.md)

## 2. Team responsibilities

All three members contribute to:

- Computer vision and measurement logic.
- Backend services and API integration.
- Web and desktop interfaces.
- Testing and evaluation.
- Technical documentation.

Coordination identifies responsibility for a feature's progress and integration. Work within each feature is shared according to estimated effort and available capacity.

| Member                      | Group   | Proposed coordination area                                                                                    | Initial peer reviewer       |
| --------------------------- | ------- | ------------------------------------------------------------------------------------------------------------- | --------------------------- |
| Muzdybay Almat Amanzholuly  | SE-2413 | Seated monitoring: CV rules, backend integration, client workflow and tests.                                  | Samatova Zhanel Samatovna   |
| Samatova Zhanel Samatovna   | SE-2419 | Full-body assessment: CV pipeline, backend APIs, client workflow and tests.                                   | Diana Sabulla Ziyadullakyzy |
| Diana Sabulla Ziyadullakyzy | SE-2401 | Background monitoring and analytics: CV quality/timing rules, backend statistics, desktop workflow and tests. | Muzdybay Almat Amanzholuly  |

Review assignments may rotate. The team reviews workload regularly to maintain balanced contributions.

These assignments describe planned responsibilities. Actual contributions and completed reviews are recorded when performed.

**Supervisor:** Нәдіров Нұртас Қонысұлы.

Supervisor feedback is provided by the supervisor and documented after receipt.

## 3. Proposed schedule before 24 October

The following dates are internal planning targets.

| Target date   | Work package                                                                                 | Completion evidence                                                                                                   |
| ------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 19–20 October | Consolidate requirements, evaluation plan and project plan.                                  | Consistent drafts containing priorities, acceptance criteria, risks and pending checks.                               |
| 20–21 October | Complete architecture explanation and key workflow mockups.                                  | Editable diagrams, readable exports and workflow designs linked to requirements.                                      |
| 21–22 October | Integrate proposal, interview synthesis, literature and comparison materials when available. | Required materials with traceable sources and conclusions; affected requirements updated.                             |
| 22–23 October | Perform deferred prototype checks and collect demonstration evidence.                        | Actual manual outcomes, screenshots and recorded defects; accurate macOS validation status.                           |
| 23 October    | Assemble the Word submission and reconcile documentation.                                    | Consistent names, scope, figures, references and implementation statuses; supervisor feedback included when received. |
| By 24 October | Publish the prepared repository and verify submission access.                                | Accessible repository URL, required project materials and a submission revision/tag matching the report.              |

All members participate. Individual work items receive an owner and reviewer before execution.

Incomplete mandatory materials remain open submission risks. Their actual status must be documented and discussed with the supervisor.

The formal labelled-data benchmark remains planned for later evaluation.

## 4. Later implementation milestones

Dates and estimates will be set after reviewing scope and technology decisions.

| Milestone                              | Deliverable                                                                                                                             | Requirement links                          |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| P1 — Shared foundations                | API/data contracts, consent flow, remote account access and client structure; account-independent local desktop monitoring.             | FR-10, FR-14; NFR-04, NFR-05               |
| P2 — Integrated seated monitoring      | Camera controls, reference capture, quality checks and foreground feedback in web/desktop clients; target-platform installation checks. | FR-01–FR-04; NFR-01–NFR-03, NFR-06, NFR-07 |
| P3 — Background monitoring             | Desktop tray/menu-bar operation, sampling and configurable native reminders.                                                            | FR-05, FR-06; NFR-03, NFR-04               |
| P4 — Full-body assessment              | Guided live assessment, media uploads, supported measurements and explanations.                                                         | FR-07–FR-09; NFR-03, NFR-05                |
| P5 — History, reporting and evaluation | Consent-controlled records and deletion, statistics, preventive information, PDF reports, benchmark and integrated acceptance tests.    | FR-11–FR-15; NFR-05–NFR-08                 |

## 5. Risk register

Likelihood and impact are initial qualitative estimates.

| ID   | Risk                                                                              | Likelihood / impact | Response                                                                                                                                     | Coordinator |
| ---- | --------------------------------------------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| R-01 | Lighting, occlusion or framing produces unreliable landmarks.                     | High / High         | Apply quality gates, show NO DATA, explain camera placement and evaluate failure cases. Unknown observations must not count as good posture. | Almat       |
| R-02 | An unsuitable reference or camera movement makes feedback misleading.             | Medium / High       | Explain reference selection, provide renewal in the final product and require recalibration after camera movement.                           | Almat       |
| R-03 | macOS behaviour differs or a target machine is unavailable.                       | Medium / High       | Arrange native testing, check camera/exit/packaging and keep untested configurations explicitly pending.                                     | Diana       |
| R-04 | Browser CV integration requires more work than the Python demonstration suggests. | Medium / High       | Validate the proposed browser runtime through a small integration experiment before finalising the stack.                                    | Zhanel      |
| R-05 | Camera frames or uploaded media are handled contrary to user choices.             | Medium / High       | Keep seated frames local; require explicit server requests; verify consent, access control, cleanup and deletion.                            | Diana       |
| R-06 | Research or comparison materials arrive late or contradict design decisions.      | Medium / High       | Track dependencies, review traceability and update affected requirements and diagrams before submission.                                     | All members |
| R-07 | Scope and integration exceed available effort.                                    | High / High         | Prioritise Must requirements, deliver complete feature slices, review workload and document scope changes.                                   | All members |
| R-08 | Noisy measurements or smoothing cause false feedback or delayed response.         | Medium / High       | Compare against the unsmoothed baseline and measure false transitions, missed changes and response delay.                                    | Zhanel      |

## 6. Dependencies and open tasks

| Dependency / task                                                  | Needed for                                              | Current status                                                                  |
| ------------------------------------------------------------------ | ------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Verified proposal, interview synthesis, literature and comparisons | Final scope and justified technology decisions.         | Completion/integration pending.                                                 |
| Key workflow mockups and architecture explanation                  | Complete design documentation.                          | Pending.                                                                        |
| Native Windows/macOS camera environments                           | Platform and GUI validation.                            | Windows operation reported; recorded cases and native macOS validation pending. |
| Manual checks and real screenshots                                 | Demonstration evidence and accurate evaluation results. | Deferred; still pending.                                                        |
| Consented benchmark data and logging harness                       | Algorithm comparison and measured quality/performance.  | Planned for later evaluation.                                                   |
| Repository preparation and access checks                           | GitHub submission and traceable collaboration.          | Deferred until material preparation; publication/access pending.                |
| Supervisor feedback                                                | Review evidence and follow-up decisions.                | Awaiting supervisor input.                                                      |

## 7. Work-item and review process

Each assigned work item records:

- Owner and peer reviewer.
- Priority.
- Related requirement.
- Expected output.
- Acceptance criteria.
- Target date.
- Current status.

Use these statuses:

- Planned.
- In progress.
- In review.
- Done.
- Blocked.

A prepared document does not imply that the feature it describes has been implemented or tested.

When repository work resumes, record actual contributions through individual accounts and review completed changes.

Before closing an implemented feature:

1. Check its acceptance criteria.
2. Run relevant tests.
3. Record actual outcomes and unresolved defects.
4. Update related documentation.
5. Obtain peer review.

Record supervisor comments, the team's response and evidence of any resulting changes.
