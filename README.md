# Tymora — Smart Study Planner

Tymora turns a student's subjects, exam dates, topic difficulty, preparation level, and available study time into a day-wise study plan.

## Team
- Project C20: AI-Based Timetable and Study Plan Generator
- Team: Tymora
- Team leader: Abhijeet (S24CSEU1419)
- Members: Namrata Sharma, Dipansu Kumar, Yash Singh Pundir

## Features
- Subject and exam-date inputs
- Prioritization by urgency, difficulty, and preparation level
- Focused study, practice, and revision sessions
- Daily time-limit validation
- Prompt preview and CSV export
- Optional Gemini API experiment; local planner works without an API key

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Use Python 3.10+. Add a Gemini API key in the sidebar only if you want to test the optional LLM feature.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Structure
- `app.py`: Streamlit interface
- `planner.py`: schedule generation and validation
- `prompt_templates.py`: V1/V2/V3 prompts
- `prompts/`: prompt documentation
- `tests/`: automated checks
- `test_cases/`: sample evaluation inputs
- `docs/`: technical overview

## Prototype status
The input flow, heuristic schedule generation, constraint checks, prompt construction, and CSV export are implemented. Gemini integration is optional and must be tested with a valid key before claiming AI-generated results. Use fictional data; no student identifiers are required.
