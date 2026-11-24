# Tymora Test Plan

## Objectives
Verify input validation, day-wise schedule generation, daily time limits, exam-date correctness, and readable output.

## Test dimensions
- Missing names, duplicate names, missing dates, past dates, and invalid study hours.
- Prioritization of nearer exams, hard topics, and weak preparation.
- Positive durations, daily cap, and no sessions after an exam.
- Schedule table, prompt preview, and CSV export.
- V1/V2/V3 prompt comparison on identical inputs.

## Automated checks
Run `python -m unittest discover -s tests -v`.

## Manual evaluation
Record whether the nearest exam is prioritized, weak/hard subjects receive attention, daily minutes stay within the limit, revision/practice appear, no session falls after an exam, and the result is understandable.

No performance score is claimed in advance.
