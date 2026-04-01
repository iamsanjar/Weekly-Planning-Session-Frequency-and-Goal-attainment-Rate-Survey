import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Psychological State Survey",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

SURVEY_TITLE: str = "Psychological State Survey"
MAX_OPTION_SCORE: int = 4
PASSING_RATE: float = 0.5
SCORE_RANGE: range = range(0, 5)
ALLOWED_CHARS: set = {"-", "'", " "}
VALID_FORMATS: frozenset = frozenset({"json"})
MENU_OPTIONS: tuple = (
    "🆕 Start a New Questionnaire",
    "📂 Load Existing Results"
)
QUESTIONS_FILE: str = "survey_questions.json"

def load_questions(file_path: str) -> list:
    if not os.path.exists(file_path):
        st.error(f"Questions file '{file_path}' was not found.")
        st.stop()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            questions = data
        elif isinstance(data, dict) and "questions" in data:
            questions = data["questions"]
        else:
            st.error("Invalid JSON structure.")
            st.stop()

        if not isinstance(questions, list) or len(questions) == 0:
            st.error("The questions JSON file is empty or invalid.")
            st.stop()

        for q in questions:
            if not isinstance(q, dict):
                st.error("Each question must be an object.")
                st.stop()
            if "id" not in q or "text" not in q or "options" not in q:
                st.error("Each question must contain 'id', 'text', and 'options'.")
                st.stop()
            if not isinstance(q["options"], list) or len(q["options"]) == 0:
                st.error("Each question must have a non-empty options list.")
                st.stop()
            for opt in q["options"]:
                if not isinstance(opt, dict):
                    st.error("Each option must be an object.")
                    st.stop()
                if "label" not in opt or "score" not in opt:
                    st.error("Each option must contain 'label' and 'score'.")
                    st.stop()

        return questions

    except json.JSONDecodeError as e:
        st.error(f"JSON format error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Could not read questions file: {e}")
        st.stop()

QUESTIONS: list = load_questions(QUESTIONS_FILE)
QUESTION_COUNT: int = len(QUESTIONS)

STATES: list = [
    {
        "min_score": 0,
        "max_score": 15,
        "label": "Very Low Distress",
        "summary": "Your responses suggest a stable psychological state with low emotional distress.",
        "description": "You appear to manage emotions and daily pressures well. Continue maintaining healthy routines and self-care habits.",
        "emoji": "🟢"
    },
    {
        "min_score": 16,
        "max_score": 30,
        "label": "Low Distress",
        "summary": "Your responses show mild emotional strain, but overall coping appears effective.",
        "description": "There may be occasional stress or tension, but it is generally manageable. Continued self-awareness and balance are recommended.",
        "emoji": "🟡"
    },
    {
        "min_score": 31,
        "max_score": 45,
        "label": "Moderate Distress",
        "summary": "Your responses suggest a noticeable level of stress, anxiety, or emotional pressure.",
        "description": "You may benefit from improving rest, self-regulation, and support strategies before symptoms intensify.",
        "emoji": "🟠"
    },
    {
        "min_score": 46,
        "max_score": 60,
        "label": "High Distress",
        "summary": "Your responses indicate a high level of emotional strain and reduced psychological comfort.",
        "description": "It would be advisable to actively address stressors and seek support from trusted people or appropriate wellbeing resources.",
        "emoji": "🔴"
    },
    {
        "min_score": 61,
        "max_score": 75,
        "label": "Very High Distress",
        "summary": "Your responses suggest significant psychological stress or emotional difficulty.",
        "description": "You may be experiencing serious strain. Seeking timely support from a counsellor, psychologist, or mental health professional is strongly recommended.",
        "emoji": "🚨"
    }
]

def validate_name_chars(name: str) -> tuple:
    if not name.strip():
        return False, "This field cannot be empty."
    for char in name:
        if not (char.isalpha() or char in ALLOWED_CHARS):
            return False, f"Invalid character '{char}'. Only letters, hyphens (-), apostrophes ('), and spaces are allowed."
    return True, ""

def validate_dob(dob_str: str) -> tuple:
    try:
        parsed: datetime = datetime.strptime(dob_str.strip(), "%d/%m/%Y")
        if parsed >= datetime.today():
            return False, "Date of birth must be in the past."
        return True, ""
    except ValueError:
        return False, "Invalid date. Please use DD/MM/YYYY format (e.g. 15/03/2003)."

def validate_student_id(sid: str) -> tuple:
    if not sid.strip():
        return False, "Student ID cannot be empty."
    i: int = 0
    while i < len(sid):
        if not sid[i].isdigit():
            return False, "Student ID must contain digits only."
        i += 1
    return True, ""

def compute_score(answers: list) -> int:
    total: int = 0
    i: int = 0
    while i < len(answers):
        total += answers[i]["score"]
        i += 1
    return total

def get_state(score: int) -> dict:
    for state in STATES:
        if state["min_score"] <= score <= state["max_score"]:
            return state
    return STATES[-1]

def build_result(user_info: dict, answers: list) -> dict:
    total_score: int = compute_score(answers)
    percentage: float = round((total_score / (QUESTION_COUNT * MAX_OPTION_SCORE)) * 100, 2)
    state: dict = get_state(total_score)

    if total_score <= 15:
        note: str = "Your responses suggest a healthy overall psychological balance."
    elif total_score <= 30:
        note = "Your responses show mild strain, but your condition appears manageable."
    elif total_score <= 45:
        note = "Your responses suggest moderate emotional pressure that may need attention."
    elif total_score <= 60:
        note = "Your responses indicate high emotional strain and a need for stronger coping support."
    else:
        note = "Your responses suggest very high distress. Seeking professional support would be strongly advisable."

    return {
        "surname": user_info["surname"],
        "given_name": user_info["given_name"],
        "dob": user_info["dob"],
        "student_id": user_info["student_id"],
        "date_taken": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "total_score": total_score,
        "percentage": percentage,
        "state": state,
        "category_note": note,
        "answers": answers
    }

if "page" not in st.session_state:
    st.session_state.page = "menu"

def page_menu() -> None:
    st.title("🧠 " + SURVEY_TITLE)
    st.caption("Westminster International University in Tashkent · 4BUIS008C")
    st.divider()
    st.subheader("Main Menu")
    st.write("Choose an option to get started:")
    st.write("")

    for i, option in enumerate(MENU_OPTIONS):
        if st.button(option, key=f"menu_{i}", use_container_width=True):
            if i == 0:
                st.session_state.page = "details"
            else:
                st.session_state.page = "load"
            st.rerun()

def page_details() -> None:
    st.title("🧠 " + SURVEY_TITLE)
    st.progress(0.15)
    st.caption("Step 1 of 3 – Personal Details")
    st.divider()

    prev: dict = st.session_state.get("user_info", {})

    with st.form("details_form"):
        surname = st.text_input("Surname *", value=prev.get("surname", ""), placeholder="e.g. Smith-Jones")
        given_name = st.text_input("Given Name *", value=prev.get("given_name", ""), placeholder="e.g. Mary Ann")
        dob = st.text_input("Date of Birth * (DD/MM/YYYY)", value=prev.get("dob", ""), placeholder="15/03/2003")
        student_id = st.text_input("Student ID * (digits only)", value=prev.get("student_id", ""), placeholder="202301234")
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        with col2:
            proceed = st.form_submit_button("Continue →", use_container_width=True, type="primary")

    if back:
        st.session_state.page = "menu"
        st.rerun()

    if proceed:
        errors: list = []

        ok, err = validate_name_chars(surname)
        if not ok:
            errors.append(f"**Surname:** {err}")

        ok, err = validate_name_chars(given_name)
        if not ok:
            errors.append(f"**Given Name:** {err}")

        ok, err = validate_dob(dob)
        if not ok:
            errors.append(f"**Date of Birth:** {err}")

        ok, err = validate_student_id(student_id)
        if not ok:
            errors.append(f"**Student ID:** {err}")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.user_info = {
                "surname": surname.strip(),
                "given_name": given_name.strip(),
                "dob": dob.strip(),
                "student_id": student_id.strip()
            }
            st.session_state.page = "survey"
            st.rerun()

def page_survey() -> None:
    st.title("🧠 " + SURVEY_TITLE)
    st.progress(0.55)
    st.caption(f"Step 2 of 3 – Questionnaire · Answer all {QUESTION_COUNT} questions")
    st.divider()

    with st.form("survey_form"):
        selected_labels: dict = {}

        for i, question in enumerate(QUESTIONS):
            labels: list = [opt["label"] for opt in question["options"]]
            choice = st.radio(
                label=f"**Q{i + 1}.** {question['text']}",
                options=labels,
                index=None,
                key=f"q{question['id']}"
            )
            selected_labels[question["id"]] = choice
            st.write("")

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        with col2:
            submit = st.form_submit_button("Submit Answers →", use_container_width=True, type="primary")

    if back:
        st.session_state.page = "details"
        st.rerun()

    if submit:
        unanswered: list = []
        all_answered: bool = True

        for qid, label in selected_labels.items():
            if label is None:
                unanswered.append(qid)
                all_answered = False

        if not all_answered:
            nums: str = ", ".join(f"Q{n}" for n in unanswered)
            st.error(f"⚠️ Please answer every question. Missing: {nums}")
        else:
            answers: list = []
            for question in QUESTIONS:
                chosen: str = selected_labels[question["id"]]
                for opt in question["options"]:
                    if opt["label"] == chosen:
                        answers.append({
                            "question_id": question["id"],
                            "answer_label": chosen,
                            "score": opt["score"]
                        })
                        break

            st.session_state.result = build_result(st.session_state.user_info, answers)
            st.session_state.page = "results"
            st.rerun()

def page_results() -> None:
    result: dict = st.session_state.get("result", {})

    if not result:
        st.warning("No result found. Please complete the survey first.")
        if st.button("← Back to Menu"):
            st.session_state.page = "menu"
            st.rerun()
        return

    st.title("🧠 " + SURVEY_TITLE)
    st.progress(1.0)
    st.caption("Step 3 of 3 – Your Results")
    st.divider()

    state_info: dict = result["state"]
    emoji: str = state_info.get("emoji", "📊")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"👤 **Name:** {result['surname']}, {result['given_name']}")
        st.info(f"🎂 **Date of Birth:** {result['dob']}")
        st.info(f"🪪 **Student ID:** {result['student_id']}")
        st.info(f"📅 **Date Taken:** {result['date_taken']}")
    with col2:
        st.metric("Total Score", f"{result['total_score']} / {QUESTION_COUNT * MAX_OPTION_SCORE}")
        st.metric("Percentage", f"{result['percentage']} %")

    st.divider()
    st.subheader(f"{emoji} {state_info['label']}")
    st.write(f"**Summary:** {state_info['summary']}")
    st.write(f"**Advice:** {state_info['description']}")
    st.info(f"💡 {result['category_note']}")
    st.divider()

    json_str: str = json.dumps(result, indent=4, ensure_ascii=False)
    filename: str = f"{result['student_id']}_survey_result.json"

    st.download_button(
        label="⬇️ Download Results as JSON",
        data=json_str,
        file_name=filename,
        mime="application/json",
        use_container_width=True
    )

    st.write("")
    if st.button("🔄 Take Survey Again", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def page_load() -> None:
    st.title("🧠 " + SURVEY_TITLE)
    st.subheader("Load Existing Results")
    st.caption("Upload a JSON file that was previously downloaded from this survey.")
    st.divider()

    uploaded = st.file_uploader("Choose a JSON file", type=["json"])

    if uploaded is not None:
        try:
            result: dict = json.load(uploaded)
            state_info: dict = result.get("state", {})
            emoji: str = state_info.get("emoji", "📊")

            st.success("✅ File loaded successfully!")
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.info(f"👤 **Name:** {result.get('surname', '?')}, {result.get('given_name', '?')}")
                st.info(f"🎂 **Date of Birth:** {result.get('dob', '?')}")
                st.info(f"🪪 **Student ID:** {result.get('student_id', '?')}")
                st.info(f"📅 **Date Taken:** {result.get('date_taken', '?')}")
            with col2:
                st.metric("Total Score", f"{result.get('total_score', '?')} / {QUESTION_COUNT * MAX_OPTION_SCORE}")
                st.metric("Percentage", f"{result.get('percentage', '?')} %")

            st.divider()
            st.subheader(f"{emoji} {state_info.get('label', 'Unknown')}")
            st.write(f"**Summary:** {state_info.get('summary', '')}")
            st.write(f"**Advice:** {state_info.get('description', '')}")
            if result.get("category_note"):
                st.info(f"💡 {result['category_note']}")

        except Exception as e:
            st.error(f"Could not read the file: {e}")

    st.write("")
    if st.button("← Back to Menu", use_container_width=True):
        st.session_state.page = "menu"
        st.rerun()

current_page: str = st.session_state.page

if current_page == "menu":
    page_menu()
elif current_page == "details":
    page_details()
elif current_page == "survey":
    page_survey()
elif current_page == "results":
    page_results()
elif current_page == "load":
    page_load()
else:
    st.session_state.page = "menu"
    st.rerun()
