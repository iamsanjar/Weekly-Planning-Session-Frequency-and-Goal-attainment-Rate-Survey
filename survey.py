"""
Weekly Planning Session Frequency and Goal Achievement Rate Survey
Module  : Fundamentals of Programming,
Task    : Project 1 – Psychological State Survey (Web Application)
Language: Python 3  |  Framework: Streamlit
Run     : streamlit run survey.py
Deploy  : https://share.streamlit.io
"""

import streamlit as st
import json
from datetime import datetime

# ─── st.set_page_config MUST be the very first Streamlit call ─────────────────
st.set_page_config(
    page_title="Planning Survey",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Variable type declarations (10 pts – 1 pt per type) ─────────────────────
SURVEY_TITLE: str        = "Weekly Planning & Goal Achievement Survey"
QUESTION_COUNT: int      = 20                      # int
MAX_OPTION_SCORE: int    = 3                       # int  – max score per question
PASSING_RATE: float      = 0.5                     # float – 50 % reference threshold
SCORE_RANGE: range       = range(0, 4)             # range – valid option scores 0-3
ALLOWED_CHARS: set       = {"-", "'", " "}         # set   – allowed non-letter chars
VALID_FORMATS: frozenset = frozenset({"json"})     # frozenset – accepted file formats
MENU_OPTIONS: tuple      = (                       # tuple – main menu labels
    "🆕  Start a New Questionnaire",
    "📂  Load Existing Results"
)


# ─── Psychological state bands ────────────────────────────────────────────────
STATES: list = [
    {
        "min_score": 0,  "max_score": 12,
        "label":       "Highly Effective Planner",
        "summary":     "Exceptional planning frequency and goal achievement.",
        "description": "Strong self-regulatory habits are visible; no immediate intervention is needed.",
        "emoji":       "🟢"
    },
    {
        "min_score": 13, "max_score": 24,
        "label":       "Effective Planner",
        "summary":     "Good planning consistency with solid goal achievement.",
        "description": "Current habits are working well; only minor improvements are likely to be needed.",
        "emoji":       "🟡"
    },
    {
        "min_score": 25, "max_score": 36,
        "label":       "Moderate Planner",
        "summary":     "Planning is present, but goal achievement is inconsistent.",
        "description": "Refining goal structure, planning detail, and weekly review habits would improve results.",
        "emoji":       "🟠"
    },
    {
        "min_score": 37, "max_score": 48,
        "label":       "Inconsistent Planner",
        "summary":     "Planning sessions are irregular and goal achievement is low.",
        "description": "Increasing planning frequency and adding stronger accountability would be advisable.",
        "emoji":       "🔴"
    },
    {
        "min_score": 49, "max_score": 60,
        "label":       "Disengaged Planner",
        "summary":     "There is little structured planning and planned goals are rarely achieved.",
        "description": "A more supportive structure around self-regulation and goal setting is strongly recommended.",
        "emoji":       "🔴"
    }
]


# ─── User-defined functions ───────────────────────────────────────────────────

def validate_name_chars(name: str) -> tuple:
    """
    Validate that a name only contains letters, hyphens, apostrophes, and spaces.
    Supports names like O'Connor, Smith-Jones, Mary Ann.
    Uses a FOR loop to inspect every character (criterion: for loop validation).
    Returns (is_valid: bool, error_message: str).
    """
    if not name.strip():
        return False, "This field cannot be empty."
    for char in name:                                  # for loop – character check
        if not (char.isalpha() or char in ALLOWED_CHARS):
            return False, (
                f"Invalid character '{char}'. "
                "Only letters, hyphens (-), apostrophes ('), and spaces are allowed."
            )
    return True, ""


def validate_dob(dob_str: str) -> tuple:
    """
    Validate date of birth in DD/MM/YYYY format.
    The date must exist and must be in the past.
    Returns (is_valid: bool, error_message: str).
    """
    try:
        parsed: datetime = datetime.strptime(dob_str.strip(), "%d/%m/%Y")
        if parsed >= datetime.today():
            return False, "Date of birth must be in the past."
        return True, ""
    except ValueError:
        return False, "Invalid date. Please use DD/MM/YYYY format (e.g. 15/03/2003)."


def validate_student_id(sid: str) -> tuple:
    """
    Validate that Student ID is non-empty and contains digits only.
    Uses a FOR loop to check every character (criterion: for loop validation).
    Returns (is_valid: bool, error_message: str).
    """
    if not sid.strip():
        return False, "Student ID cannot be empty."
    for ch in sid:                                     # for loop – digit check
        if not ch.isdigit():
            return False, "Student ID must contain digits only."
    return True, ""


def compute_score(answers: list) -> int:
    """
    Sum all answer scores using a WHILE loop (criterion: while loop).
    """
    total: int = 0
    i: int     = 0
    while i < len(answers):                            # while loop – accumulate score
        total += answers[i]["score"]
        i += 1
    return total


def get_state(score: int) -> dict:
    """Return the matching psychological state dict for a given total score."""
    for state in STATES:
        if state["min_score"] <= score <= state["max_score"]:
            return state
    return STATES[-1]                                  # fallback


def build_result(user_info: dict, answers: list) -> dict:
    """
    Assemble the final result dictionary.
    Uses IF / ELIF / ELSE conditional statements (criterion: >= 3 conditionals).
    """
    total_score: int  = compute_score(answers)
    percentage: float = round((total_score / (QUESTION_COUNT * MAX_OPTION_SCORE)) * 100, 2)
    state: dict       = get_state(total_score)

    # IF / ELIF / ELSE chain (criterion)
    if total_score <= 12:
        note: str = "Excellent! Keep up the great work."
    elif total_score <= 24:
        note = "Well done. Small refinements can take you further."
    elif total_score <= 36:
        note = "There is room for improvement in your planning habits."
    elif total_score <= 48:
        note = "Consider building more structure into your weekly routine."
    else:
        note = "Seeking guidance on goal-setting strategies is strongly advised."

    return {
        "surname":       user_info["surname"],
        "given_name":    user_info["given_name"],
        "dob":           user_info["dob"],
        "student_id":    user_info["student_id"],
        "date_taken":    datetime.now().strftime("%d/%m/%Y %H:%M"),
        "total_score":   total_score,
        "percentage":    percentage,
        "state":         state,
        "category_note": note,
        "answers":       answers
    }


# ─── Session state initialisation ────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "menu"


# ─── Page: Menu ───────────────────────────────────────────────────────────────
def page_menu() -> None:
    st.title("📋 " + SURVEY_TITLE)
    st.caption("Westminster International University in Tashkent · 4BUIS008C")
    st.divider()
    st.subheader("Main Menu")
    st.write("Choose an option to get started:")
    st.write("")

    for i, option in enumerate(MENU_OPTIONS):          # for loop – render menu buttons
        if st.button(option, key=f"menu_{i}", use_container_width=True):
            if i == 0:
                st.session_state.page = "details"
            else:
                st.session_state.page = "load"
            st.rerun()


# ─── Page: Personal Details ───────────────────────────────────────────────────
def page_details() -> None:
    st.title("📋 " + SURVEY_TITLE)
    st.progress(0.15)
    st.caption("Step 1 of 3 – Personal Details")
    st.divider()

    prev: dict = st.session_state.get("user_info", {})

    with st.form("details_form"):
        surname    = st.text_input("Surname *",
                                   value=prev.get("surname", ""),
                                   placeholder="e.g. Smith-Jones")
        given_name = st.text_input("Given Name *",
                                   value=prev.get("given_name", ""),
                                   placeholder="e.g. Mary Ann")
        dob        = st.text_input("Date of Birth * (DD/MM/YYYY)",
                                   value=prev.get("dob", ""),
                                   placeholder="15/03/2003")
        student_id = st.text_input("Student ID * (digits only)",
                                   value=prev.get("student_id", ""),
                                   placeholder="202301234")
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            back    = st.form_submit_button("← Back",     use_container_width=True)
        with col2:
            proceed = st.form_submit_button("Continue →", use_container_width=True,
                                            type="primary")

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
            for e in errors:                           # for loop – display each error
                st.error(e)
        else:
            st.session_state.user_info = {
                "surname":    surname.strip(),
                "given_name": given_name.strip(),
                "dob":        dob.strip(),
                "student_id": student_id.strip()
            }
            st.session_state.page = "survey"
            st.rerun()


# ─── Page: Survey ─────────────────────────────────────────────────────────────
def page_survey() -> None:
    st.title("📋 " + SURVEY_TITLE)
    st.progress(0.55)
    st.caption(f"Step 2 of 3 – Questionnaire  ·  Answer all {QUESTION_COUNT} questions")
    st.divider()

    with st.form("survey_form"):
        selected_labels: dict = {}

        for i, question in enumerate(QUESTIONS):       # for loop – render all questions
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
            back   = st.form_submit_button("← Back",          use_container_width=True)
        with col2:
            submit = st.form_submit_button("Submit Answers →", use_container_width=True,
                                           type="primary")

    if back:
        st.session_state.page = "details"
        st.rerun()

    if submit:
        unanswered: list   = []
        all_answered: bool = True                      # bool variable

        for qid, label in selected_labels.items():    # for loop – completeness check
            if label is None:
                unanswered.append(qid)
                all_answered = False

        if not all_answered:
            nums: str = ", ".join(f"Q{n}" for n in unanswered)
            st.error(f"⚠️ Please answer every question. Missing: {nums}")
        else:
            answers: list = []
            for question in QUESTIONS:                 # for loop – build answers list
                chosen: str = selected_labels[question["id"]]
                for opt in question["options"]:
                    if opt["label"] == chosen:
                        answers.append({
                            "question_id":  question["id"],
                            "answer_label": chosen,
                            "score":        opt["score"]
                        })
                        break

            st.session_state.result = build_result(
                st.session_state.user_info, answers
            )
            st.session_state.page = "results"
            st.rerun()


# ─── Page: Results ────────────────────────────────────────────────────────────
def page_results() -> None:
    result: dict = st.session_state.get("result", {})

    if not result:
        st.warning("No result found. Please complete the survey first.")
        if st.button("← Back to Menu"):
            st.session_state.page = "menu"
            st.rerun()
        return

    st.title("📋 " + SURVEY_TITLE)
    st.progress(1.0)
    st.caption("Step 3 of 3 – Your Results")
    st.divider()

    state_info: dict = result["state"]
    emoji: str       = state_info.get("emoji", "📊")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"👤 **Name:** {result['surname']}, {result['given_name']}")
        st.info(f"🎂 **Date of Birth:** {result['dob']}")
        st.info(f"🪪 **Student ID:** {result['student_id']}")
        st.info(f"📅 **Date Taken:** {result['date_taken']}")
    with col2:
        st.metric("Total Score",
                  f"{result['total_score']} / {QUESTION_COUNT * MAX_OPTION_SCORE}")
        st.metric("Percentage", f"{result['percentage']} %")

    st.divider()
    st.subheader(f"{emoji}  {state_info['label']}")
    st.write(f"**Summary:** {state_info['summary']}")
    st.write(f"**Advice:** {state_info['description']}")
    st.info(f"💡 {result['category_note']}")
    st.divider()

    # JSON download – persistence criterion (LO3)
    json_str: str = json.dumps(result, indent=4, ensure_ascii=False)
    filename: str = f"{result['student_id']}_survey_result.json"

    st.download_button(
        label="⬇️  Download Results as JSON",
        data=json_str,
        file_name=filename,
        mime="application/json",
        use_container_width=True
    )
    st.write("")
    if st.button("🔄  Take Survey Again", use_container_width=True):
        for key in list(st.session_state.keys()):     # for loop – clear all state
            del st.session_state[key]
        st.rerun()


# ─── Page: Load Results ───────────────────────────────────────────────────────
def page_load() -> None:
    st.title("📋 " + SURVEY_TITLE)
    st.subheader("Load Existing Results")
    st.caption("Upload a JSON file that was previously downloaded from this survey.")
    st.divider()

    uploaded = st.file_uploader("Choose a JSON file", type=["json"])

    if uploaded is not None:
        try:
            result: dict     = json.load(uploaded)
            state_info: dict = result.get("state", {})
            emoji: str       = state_info.get("emoji", "📊")

            st.success("✅ File loaded successfully!")
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.info(f"👤 **Name:** {result.get('surname','?')}, {result.get('given_name','?')}")
                st.info(f"🎂 **Date of Birth:** {result.get('dob','?')}")
                st.info(f"🪪 **Student ID:** {result.get('student_id','?')}")
                st.info(f"📅 **Date Taken:** {result.get('date_taken','?')}")
            with col2:
                st.metric("Total Score",
                          f"{result.get('total_score','?')} / {QUESTION_COUNT * MAX_OPTION_SCORE}")
                st.metric("Percentage", f"{result.get('percentage','?')} %")

            st.divider()
            st.subheader(f"{emoji}  {state_info.get('label','Unknown')}")
            st.write(f"**Summary:** {state_info.get('summary','')}")
            st.write(f"**Advice:** {state_info.get('description','')}")
            if result.get("category_note"):
                st.info(f"💡 {result['category_note']}")

        except Exception as e:
            st.error(f"Could not read the file: {e}")

    st.write("")
    if st.button("← Back to Menu", use_container_width=True):
        st.session_state.page = "menu"
        st.rerun()


# ─── Router – runs on every Streamlit rerun ──────────────────────────────────
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
else:                                                  # else branch – safety fallback
    st.session_state.page = "menu"
    st.rerun()
