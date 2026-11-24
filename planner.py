"""Deterministic schedule generation and validation for Tymora."""
from datetime import date, timedelta

DIFFICULTY = {"Easy": 1, "Medium": 2, "Hard": 3}
PREPARATION = {"Good": 1, "Medium": 2, "Weak": 3}

def priority(subject, today):
    days_left = max((subject["exam_date"] - today).days, 0)
    return 5 / (days_left + 1) + 0.8 * DIFFICULTY.get(subject.get("difficulty", "Medium"), 2) + 1.2 * PREPARATION.get(subject.get("preparation", "Medium"), 2)

def validate_inputs(subjects, daily_hours, session_minutes):
    errors = []
    if not subjects: errors.append("Add at least one subject.")
    if not 0.5 <= daily_hours <= 16: errors.append("Daily study time must be between 0.5 and 16 hours.")
    if session_minutes not in (25, 30, 45, 50, 60, 90, 120): errors.append("Choose a supported session length.")
    names = set()
    for i, s in enumerate(subjects, 1):
        name = str(s.get("name", "")).strip()
        if not name: errors.append(f"Subject {i}: name is required.")
        elif name.lower() in names: errors.append(f"Subject {i}: subject names must be unique.")
        names.add(name.lower())
        if s.get("exam_date") is None: errors.append(f"Subject {i}: exam date is required.")
        elif s["exam_date"] < date.today(): errors.append(f"Subject {i}: exam date cannot be in the past.")
    return errors

def generate_schedule(subjects, daily_hours, session_minutes=50, start_date=None):
    start = start_date or date.today()
    active = [s for s in subjects if s.get("exam_date") and s["exam_date"] >= start]
    if not active: return []
    last_exam = max(s["exam_date"] for s in active)
    cap = int(daily_hours * 60)
    slot = max(25, min(session_minutes, cap))
    result, current = [], start
    while current <= last_exam:
        ranked = sorted([s for s in active if s["exam_date"] >= current],
                        key=lambda s: priority(s, current), reverse=True)
        remaining, cursor = cap, 0
        while remaining >= 25 and ranked and cursor < len(ranked) * 4:
            s = ranked[cursor % len(ranked)]
            duration = min(slot, remaining)
            task = ("Focused study", "Practice questions", "Revision")[(current.toordinal() + cursor) % 3]
            if (s["exam_date"] - current).days <= 2:
                task = "Final revision and practice"
            result.append({"Date": current.isoformat(), "Subject": s["name"], "Task": task,
                           "Duration (minutes)": duration, "Exam date": s["exam_date"].isoformat(),
                           "Priority": round(priority(s, current), 2)})
            remaining -= duration
            cursor += 1
        current += timedelta(days=1)
    return result

def validate_schedule(schedule, daily_hours):
    errors, totals = [], {}
    cap = int(daily_hours * 60)
    for item in schedule:
        day, duration = item["Date"], int(item["Duration (minutes)"])
        totals[day] = totals.get(day, 0) + duration
        if duration <= 0: errors.append(f"{day}: duration must be positive.")
        if date.fromisoformat(day) > date.fromisoformat(item["Exam date"]):
            errors.append(f"{day}: {item['Subject']} is scheduled after its exam.")
    for day, total in totals.items():
        if total > cap: errors.append(f"{day}: {total} minutes exceeds the {cap}-minute daily limit.")
    return errors
