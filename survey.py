import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Weekly Planning Session Frequency and Goal Achievement Rate Survey",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

SURVEY_TITLE: str = "Weekly Planning Session Frequency and Goal Achievement Rate Survey"
MAX_OPTION_SCORE: int = 3
PASSING_RATE: float = 0.5
SCORE_RANGE: range = range(0, 4)
ALLOWED_CHARS: set = {"-", "'", " "}
VALID_FORMATS: frozenset = frozenset({"json"})
MENU_OPTIONS: tuple = (
    "🆕 Start a New Questionnaire",
    "📂 Load Existing Results"
)
QUESTIONS_FILE: str = "survey_questions.json"

EMBEDDED_QUESTIONS: list = [
    {
        "id": 1,
        "text": "How often do you dedicate time to holding a structured weekly planning session?",
        "options": [
            {"label": "Every week without exception", "score": 0},
            {"label": "Most weeks", "score": 1},
            {"label": "Occasionally", "score": 2},
            {"label": "Almost never or never", "score": 3}
        ]
    },
    {
        "id": 2,
        "text": "When you set goals at the start of a week, how many do you typically achieve by the end of it?",
        "options": [
            {"label": "Nearly all of them", "score": 0},
            {"label": "More than half", "score": 1},
            {"label": "About half or fewer", "score": 2},
            {"label": "Rarely any", "score": 3}
        ]
    },
    {
        "id": 3,
        "text": "How clearly do you define your goals before beginning a planning session?",
        "options": [
            {"label": "Always clearly, with specific steps and deadlines", "score": 0},
            {"label": "Usually clear, though sometimes vague", "score": 1},
            {"label": "Often vague or loosely defined", "score": 2},
            {"label": "I do not define goals in advance", "score": 3}
        ]
    },
    {
        "id": 4,
        "text": "How consistently do you review what you planned at the end of each week to assess your progress?",
        "options": [
            {"label": "Every week", "score": 0},
            {"label": "Often, but not every week", "score": 1},
            {"label": "Rarely", "score": 2},
            {"label": "Never", "score": 3}
        ]
    },
    {
        "id": 5,
        "text": "When you do not achieve a planned goal, how do you typically respond?",
        "options": [
            {"label": "I analyse what went wrong and adjust my approach", "score": 0},
            {"label": "I reschedule the goal for next week", "score": 1},
            {"label": "I feel frustrated but do not take specific action", "score": 2},
            {"label": "I tend to abandon the goal altogether", "score": 3}
        ]
    },
    {
        "id": 6,
        "text": "How well do you prioritise your goals during a planning session?",
        "options": [
            {"label": "Very well, I always rank tasks by importance and urgency", "score": 0},
            {"label": "Fairly well, I consider priority most of the time", "score": 1},
            {"label": "Inconsistently, I sometimes treat all tasks as equally important", "score": 2},
            {"label": "I do not prioritise and proceed without a clear order", "score": 3}
        ]
    },
    {
        "id": 7,
        "text": "How often do you break large goals into smaller, manageable steps during planning?",
        "options": [
            {"label": "Always", "score": 0},
            {"label": "Often", "score": 1},
            {"label": "Rarely", "score": 2},
            {"label": "Never", "score": 3}
        ]
    },
    {
        "id": 8,
        "text": "How realistic are the goals you usually set for a single week?",
        "options": [
            {"label": "Very realistic and achievable", "score": 0},
            {"label": "Mostly realistic", "score": 1},
            {"label": "Sometimes unrealistic", "score": 2},
            {"label": "Usually too ambitious or unclear", "score": 3}
        ]
    },
    {
        "id": 9,
        "text": "How often do unexpected events completely derail your weekly plans?",
        "options": [
            {"label": "Almost never because I adapt well", "score": 0},
            {"label": "Occasionally", "score": 1},
            {"label": "Often", "score": 2},
            {"label": "Almost every week", "score": 3}
        ]
    },
    {
        "id": 10,
        "text": "How much time do you usually spend preparing your weekly plan?",
        "options": [
            {"label": "Enough time to think through tasks carefully", "score": 0},
            {"label": "A reasonable amount of time", "score": 1},
            {"label": "Very little time", "score": 2},
            {"label": "I do not set aside planning time", "score": 3}
        ]
    },
    {
        "id": 11,
        "text": "How often do you write your weekly goals down in a planner, notebook, or digital tool?",
        "options": [
            {"label": "Every week", "score": 0},
            {"label": "Most weeks", "score": 1},
            {"label": "Rarely", "score": 2},
            {"label": "Never", "score": 3}
        ]
    },
    {
        "id": 12,
        "text": "How confident do you feel that you will complete your goals after a planning session?",
        "options": [
            {"label": "Very confident", "score": 0},
            {"label": "Moderately confident", "score": 1},
            {"label": "Slightly confident", "score": 2},
            {"label": "Not confident at all", "score": 3}
        ]
    },
    {
        "id": 13,
        "text": "When planning your week, how often do you consider deadlines in advance?",
        "options": [
            {"label": "Always", "score": 0},
            {"label": "Usually", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Rarely or never", "score": 3}
        ]
    },
    {
        "id": 14,
        "text": "How often do you include time for rest or recovery when making your weekly plan?",
        "options": [
            {"label": "Always", "score": 0},
            {"label": "Often", "score": 1},
            {"label": "Rarely", "score": 2},
            {"label": "Never", "score": 3}
        ]
    },
    {
        "id": 15,
        "text": "How likely are you to postpone an important task even after planning it?",
        "options": [
            {"label": "Very unlikely", "score": 0},
            {"label": "Somewhat unlikely", "score": 1},
            {"label": "Quite likely", "score": 2},
            {"label": "Very likely", "score": 3}
        ]
    },
    {
        "id": 16,
        "text": "How often do you adjust your weekly goals when you notice they are no longer realistic?",
        "options": [
            {"label": "Promptly and effectively", "score": 0},
            {"label": "Sometimes", "score": 1},
            {"label": "Rarely", "score": 2},
            {"label": "I usually continue without adjusting anything", "score": 3}
        ]
    },
    {
        "id": 17,
        "text": "How organized are the tools or systems you use for weekly planning?",
        "options": [
            {"label": "Very organized and easy to follow", "score": 0},
            {"label": "Mostly organized", "score": 1},
            {"label": "Somewhat disorganized", "score": 2},
            {"label": "I do not use any consistent system", "score": 3}
        ]
    },
    {
        "id": 18,
        "text": "How often do you begin your week knowing exactly which goals are the top priority?",
        "options": [
            {"label": "Always", "score": 0},
            {"label": "Usually", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Rarely or never", "score": 3}
        ]
    },
    {
        "id": 19,
        "text": "How often do you reflect on why certain goals were completed successfully?",
        "options": [
            {"label": "Every week", "score": 0},
            {"label": "Often", "score": 1},
            {"label": "Rarely", "score": 2},
            {"label": "Never", "score": 3}
        ]
    },
    {
        "id": 20,
        "text": "Overall, how effective do you believe your weekly planning process is?",
        "options": [
            {"label": "Highly effective", "score": 0},
            {"label": "Mostly effective", "score": 1},
            {"label": "Somewhat ineffective", "score": 2},
            {"label": "Very ineffective", "score": 3}
        ]
    }
]

EMBEDDED_STATES: list = [
    {
        "min_score": 0,
        "max_score": 12,
        "label": "Highly Effective Planner",
        "summary": "Exceptional planning frequency and goal achievement.",
        "description": "Strong self-regulatory habits are visible in the answers, so no immediate intervention is needed."
    },
    {
        "min_score": 13,
        "max_score": 24,
        "label": "Effective Planner",
        "summary": "Good planning consistency with solid goal achievement.",
        "description": "Current habits are working well, and only minor improvements are likely to be needed."
    },
    {
        "min_score": 25,
        "max_score": 36,
        "label": "Moderate Planner",
        "summary": "Planning is present, but goal achievement is inconsistent.",
        "description": "Refining goal structure, planning detail, and weekly review habits would likely improve results."
    },
    {
        "min_score": 37,
        "max_score": 48,
        "label": "Inconsistent Planner",
        "summary": "Planning sessions are irregular and goal achievement is low.",
        "description": "Increasing planning frequency and adding stronger accountability would be advisable."
    },
    {
        "min_score": 49,
        "max_score": 60,
        "label": "Disengaged Planner",
        "summary": "There is little structured planning and planned goals are rarely achieved.",
        "description": "A more supportive structure around self-regulation and goal setting is strongly recommended."
    }
]

def validate_question_structure(questions: list) -> bool:
    if not isinstance(questions, list) or len(questions) == 0:
        return False

    for question in questions:
        if not isinstance(question, dict):
            return False
        if "id" not in question or "text" not in question or "options" not in question:
            return False
        if not isinstance(question["options"], list) or len(question["options"]) == 0:
            return False
        for option in question["options"]:
            if not isinstance(option, dict):
                return False
            if "label" not in option or "score" not in option:
                return False
    return True

def validate_state_structure(states: list) -> bool:
    if not isinstance(states, list) or len(states) == 0:
        return False

    for state in states:
        if not isinstance(state, dict):
            return False
        required_keys = {"min_score", "max_score", "label", "summary", "description"}
        if not required_keys.issubset(state.keys()):
            return False
    return True

def load_survey_data(file_path: str) -> tuple:
    questions: list = EMBEDDED_QUESTIONS
    states: list = EMBEDDED_STATES

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                file_questions = data.get("questions")
                file_states = data.get("states")

                if validate_question_structure(file_questions):
                    questions = file_questions

                if validate_state_structure(file_states):
                    states = file_states

        except json.JSONDecodeError:
            st.warning("The JSON file could not be decoded. Embedded survey data will be used.")
        except Exception:
            st.warning("The JSON file could not be read. Embedded survey data will be used.")
    else:
        st.info("External survey file not found. Embedded survey data will be used.")

    return questions, states

QUESTIONS, STATES = load_survey_data(QUESTIONS_FILE)
QUESTION_COUNT: int = len(QUESTIONS)

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

    if total_score <= 12:
        note: str = "Your weekly planning habits appear highly effective."
    elif total_score <= 24:
        note = "Your planning habits are generally strong, with room for small improvements."
    elif total_score <= 36:
        note = "Your planning process is moderate and may benefit from more structure and consistency."
    elif total_score <= 48:
        note = "Your weekly planning appears inconsistent and may be affecting your ability to achieve goals."
    else:
        note = "Your current planning habits show major gaps, and a stronger planning routine is strongly recommended."

    return {
        "survey_title": SURVEY_TITLE,
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

def render_loaded_result(result: dict) -> None:
    state_info: dict = result.get("state", {})
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
    st.subheader(state_info.get("label", "Unknown"))
    st.write(f"**Summary:** {state_info.get('summary', '')}")
    st.write(f"**Advice:** {state_info.get('description', '')}")
    if result.get("category_note"):
        st.info(f"💡 {result['category_note']}")

if "page" not in st.session_state:
    st.session_state.page = "menu"

def page_menu() -> None:
    st.title("📋 " + SURVEY_TITLE)
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
    st.title("📋 " + SURVEY_TITLE)
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
            for error in errors:
                st.error(error)
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
    st.title("📋 " + SURVEY_TITLE)
    st.progress(0.55)
    st.caption(f"Step 2 of 3 – Questionnaire · Answer all {QUESTION_COUNT} questions")
    st.divider()

    with st.form("survey_form"):
        selected_labels: dict = {}

        for i, question in enumerate(QUESTIONS):
            labels: list = [option["label"] for option in question["options"]]
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
                for option in question["options"]:
                    if option["label"] == chosen:
                        answers.append({
                            "question_id": question["id"],
                            "answer_label": chosen,
                            "score": option["score"]
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

    st.title("📋 " + SURVEY_TITLE)
    st.progress(1.0)
    st.caption("Step 3 of 3 – Your Results")
    st.divider()

    state_info: dict = result["state"]

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
    st.subheader(state_info["label"])
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

    if st.button("🔄 Take Survey Again", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def page_load() -> None:
    st.title("📋 " + SURVEY_TITLE)
    st.subheader("Load Existing Results")
    st.caption("Upload a JSON file that was previously downloaded from this survey.")
    st.divider()

    uploaded = st.file_uploader("Choose a JSON file", type=["json"])

    if uploaded is not None:
        try:
            result: dict = json.load(uploaded)
            st.success("✅ File loaded successfully!")
            st.divider()
            render_loaded_result(result)
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
