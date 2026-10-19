# Posterys documentation

Updated: 19 October 2026.
Status: supervisor-review draft.

## Main project report

[Open the consolidated project report in Google Docs](https://docs.google.com/document/d/1ozC7s9Gv_CD32tUh_pMsK2LaQbnglrGmf8uyfv52y80/edit)

The consolidated report contains:

- Project proposal, objectives and scope.
- User research and relevance evidence.
- Literature review and publication analysis.
- Existing-system and technology comparisons.
- Functional and non-functional requirements.
- Architecture and diagrams.
- Prototype description and UX mockups.
- Verification and evaluation plan.
- Responsibilities, milestones and risks.
- Supervisor feedback section, awaiting review.

These materials are maintained in the consolidated report rather than duplicated in separate Markdown files. The supervisor and committee must have access to the linked document.

## Repository documentation

| Material                    | Location                                                | Status                                                                           |
| --------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Architecture                | [Architecture draft](architecture-draft.md)             | Proposed system structure; integrated implementation is planned.                 |
| Requirements                | [Requirements and acceptance criteria](requirements.md) | Initial specification for team and supervisor review.                            |
| Functional prototype        | [Prototype description](prototype-notes.md)             | Describes the current local Python webcam application and its limitations.       |
| Verification and evaluation | [Evaluation plan](evaluation-plan.md)                   | Defines planned checks, metrics, measurement conditions and comparison baseline. |
| UX design                   | [Mockups and scenario mapping](ux/README.md)            | Five static interface designs; usability evaluation remains pending.             |

## UX mockups

The image files are stored in `docs/ux/mockups/`.

| File                                                                          | Scenario                          | Report location         |
| ----------------------------------------------------------------------------- | --------------------------------- | ----------------------- |
| [01-web-monitoring.png](ux/mockups/01-web-monitoring.png)                     | Seated monitoring                 | Section 8.2.1, Figure 4 |
| [02-web-media-analysis.png](ux/mockups/02-web-media-analysis.png)             | Full-body assessment              | Section 8.2.2, Figure 5 |
| [03-web-results.png](ux/mockups/03-web-results.png)                           | Assessment results                | Section 8.2.3, Figure 6 |
| [04-desktop-background.png](ux/mockups/04-desktop-background.png)             | Desktop background monitoring     | Section 8.2.4, Figure 7 |
| [05-desktop-history-reminder.png](ux/mockups/05-desktop-history-reminder.png) | Reminders, history and statistics | Section 8.2.5, Figure 8 |

The mockups illustrate planned interactions. Displayed measurements, times and statistics are examples, not experimental results.

Requirement mapping and scenario descriptions are provided in [ux/README.md](ux/README.md).

## Development and verification status

| Category               | Current status                                                                                                                |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Implemented            | Local Python webcam prototype with reference capture, head/shoulder feedback, tracking-quality states and exit controls.      |
| Reported verification  | Successful Windows operation and nine passing synthetic core tests reported by the team.                                      |
| Designed               | Five static web/desktop mockups and a draft target architecture.                                                              |
| Planned implementation | Integrated web/desktop clients, API, database, full-body assessment, background reminders, persistent history and PDF export. |
| Pending evaluation     | Recorded manual camera checks, usability walkthroughs, native macOS validation and accuracy/performance measurements.         |

GOOD POSTURE means that supported measurements are within the thresholds of a user-selected reference. It does not establish that the reference position is medically healthy.

The prototype does not directly measure muscle tension or establish clinical effectiveness.

## Submission checklist

Before submission:

- Confirm that the supervisor and committee can access the report and repository.
- Insert all five mockup images into their marked report locations.
- Check the final mockup exports against the design-review checklist in ux/README.md.
- Resolve the repeated P03 interview identifier and confirm participant uniqueness.
- Record actual manual prototype checks and demonstration screenshots.
- Record individual contributions and peer reviews.
- Obtain supervisor feedback and document the resulting decisions.
- Create the pre-defense-1 Git tag on the exact reviewed submission commit.

A complete integrated application is not required at this stage. Prepared documents and mockups do not replace actual implementation, verification or review evidence.
