# Technical Overview — Tymora

## Problem
Students may have multiple subjects and exam dates but limited daily study time. Choosing what to study first and balancing learning, practice, and revision can be difficult.

## Proposed solution
Tymora collects planning details and builds a day-wise study schedule. Prompt versions make the planning rules explicit and allow comparison of baseline, improved, and integrated prompts.

## Architecture
1. Streamlit UI (`app.py`) collects subject, exam date, difficulty, preparation level, daily hours, and preferred session length.
2. Validation (`planner.py`) checks required fields, duplicate names, dates, and daily limits.
3. Priority planner ranks subjects using urgency, difficulty, and preparation level.
4. Prompt builder (`prompt_templates.py`) creates the integrated V3 prompt.
5. Optional Gemini integration sends the prompt only when the user supplies a key and enables it.
6. Output displays the timetable, daily totals, and CSV export.

## Technology
Python, Streamlit, Pandas, optional Google GenAI SDK, GitHub.

## Privacy and limitations
Use fictional test data. The prototype does not need personally identifying data. The local planner uses heuristic allocation; it does not understand detailed syllabi unless topic details are added. Gemini depends on a valid key, network access, and output review. Schedules are suggestions, not guarantees.

## Future improvements
Topic-level inputs, completion tracking, calendar export, consent-based saved profiles, quantitative prompt comparison, and improved optimization for uneven session allocation.
