from datetime import date, timedelta
import pandas as pd
import streamlit as st
from planner import generate_schedule, validate_inputs, validate_schedule
from prompt_templates import build_integrated_prompt

st.set_page_config(page_title="Tymora | Smart Study Planner", page_icon="📚", layout="wide")
st.title("📚 Tymora — Smart Study Planner")
st.caption("A prompt-engineering prototype for turning exam goals into a practical day-wise plan.")

with st.sidebar:
    st.header("Planning settings")
    daily_hours = st.slider("Available study hours per day", 1.0, 12.0, 4.0, 0.5)
    session_minutes = st.select_slider("Preferred session length", options=[25, 30, 45, 50, 60, 90, 120], value=50)
    st.info("The local planner works without an API key.")
    api_key = st.text_input("Gemini API key (optional)", type="password")
    use_gemini = st.checkbox("Enable Gemini experiment", value=False, disabled=not api_key)

st.subheader("1. Add your subjects")
st.write("Enter one row per subject.")
if "rows" not in st.session_state:
    st.session_state.rows = [
        {"Subject": "Data Structures", "Exam date": date.today()+timedelta(days=10), "Difficulty": "Medium", "Preparation": "Medium"},
        {"Subject": "Operating Systems", "Exam date": date.today()+timedelta(days=13), "Difficulty": "Hard", "Preparation": "Weak"},
        {"Subject": "Computer Networks", "Exam date": date.today()+timedelta(days=16), "Difficulty": "Medium", "Preparation": "Good"},
    ]
edited = st.data_editor(pd.DataFrame(st.session_state.rows), num_rows="dynamic", use_container_width=True,
    column_config={
        "Exam date": st.column_config.DateColumn("Exam date", min_value=date.today(), format="DD MMM YYYY"),
        "Difficulty": st.column_config.SelectboxColumn("Difficulty", options=["Easy","Medium","Hard"], required=True),
        "Preparation": st.column_config.SelectboxColumn("Preparation", options=["Good","Medium","Weak"], required=True),
    })

if st.button("Generate my study plan", type="primary", use_container_width=True):
    subjects = []
    for _, row in edited.iterrows():
        if pd.isna(row.get("Subject")) or not str(row.get("Subject","")).strip():
            continue
        d = row.get("Exam date")
        if pd.isna(d): d = None
        elif hasattr(d, "date"): d = d.date()
        subjects.append({"name":str(row["Subject"]).strip(),"exam_date":d,
                         "difficulty":str(row.get("Difficulty","Medium")),
                         "preparation":str(row.get("Preparation","Medium"))})
    errors = validate_inputs(subjects, daily_hours, int(session_minutes))
    if errors:
        for e in errors: st.error(e)
    else:
        schedule = generate_schedule(subjects, daily_hours, int(session_minutes))
        violations = validate_schedule(schedule, daily_hours)
        if violations:
            for e in violations: st.error(e)
        elif not schedule:
            st.warning("No sessions could be generated for these dates.")
        else:
            st.session_state.schedule = schedule
            st.session_state.subjects = subjects
            st.success("Your study plan is ready. Review it and adjust your inputs if needed.")

if "schedule" in st.session_state:
    st.divider()
    st.subheader("2. Your day-wise study plan")
    df = pd.DataFrame(st.session_state.schedule)
    st.dataframe(df, use_container_width=True, hide_index=True)
    totals = df.groupby("Date")["Duration (minutes)"].sum().reset_index()
    totals["Study hours"] = (totals["Duration (minutes)"]/60).round(2)
    st.markdown("Daily study-time check")
    st.dataframe(totals, use_container_width=True, hide_index=True)
    st.download_button("Download timetable as CSV", df.to_csv(index=False).encode("utf-8"),
                       "tymora_study_plan.csv", "text/csv")
    student_input = "\n".join(f"- {s['name']}: exam {s['exam_date']}, difficulty {s['difficulty']}, preparation {s['preparation']}" for s in st.session_state.subjects)
    student_input += f"\n- Available time: {daily_hours} hours/day; session: {session_minutes} minutes."
    prompt = build_integrated_prompt(student_input)
    with st.expander("View integrated V3 prompt"):
        st.code(prompt, language="text")
    if use_gemini and api_key and st.button("Generate an AI draft with Gemini"):
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.markdown("Gemini draft — review before use")
            st.write(response.text or "The model returned an empty response.")
        except Exception as exc:
            st.error(f"Gemini request failed: {exc}")

st.divider()
st.caption("Tymora is an academic prototype. Review the timetable against personal commitments.")
