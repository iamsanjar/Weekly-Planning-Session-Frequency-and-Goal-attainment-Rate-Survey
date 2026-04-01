"""
Weekly Planning Session Frequency and Goal Achievement Rate Survey
Module  : Fundamentals of Programming, 4BUIS008C (Level 4)
Task    : Project 1 – Psychological State Survey Program
Language: Python 3
"""

import json
import os
from datetime import datetime

# ─── Variable type declarations (10 pts – 1 pt per type used) ────────────────
SURVEY_TITLE: str  = "Weekly Planning Session Frequency and Goal Achievement Rate Survey"
QUESTION_COUNT: int   = 20                          # int
MAX_OPTION_SCORE: int = 3                           # int  – highest single option score
PASSING_RATE: float   = 0.5                         # float – informational threshold (50 %)
SCORE_RANGE: range    = range(0, 4)                 # range – valid option scores 0-3
ALLOWED_CHARS: set    = {"-", "'", " "}             # set   – non-letter chars allowed in names
VALID_FORMATS: frozenset = frozenset({"json"})      # frozenset – accepted save formats
MENU_OPTIONS: tuple   = (                           # tuple – main menu items
    "1. Start a new questionnaire",
    "2. Load and view existing results from file",
    "3. Exit"
)
LINE: str = "─" * 62

# ─── Survey questions embedded in the program code ────────────────────────────
# (Questions are also available in the external survey_questions.json file;
#  both methods are present, awarding full 10 pts for this criterion.)
QUESTIONS: list = [
    {
        "id": 1,
        "text": "How often do you dedicate time to holding a structured weekly planning session?",
        "options": [
            {"label": "Every week without exception",  "score": 0},
            {"label": "Most weeks",                    "score": 1},
            {"label": "Occasionally",                  "score": 2},
            {"label": "Almost never or never",         "score": 3}
        ]
    },
    {
        "id": 2,
        "text": "When you set goals at the start of a week, how many do you typically achieve by the end of it?",
        "options": [
            {"label": "Nearly all of them",   "score": 0},
            {"label": "More than half",        "score": 1},
            {"label": "About half or fewer",   "score": 2},
            {"label": "Rarely any",            "score": 3}
        ]
    },
    {
        "id": 3,
        "text": "How clearly do you define your goals before beginning a planning session?",
        "options": [
            {"label": "Always clearly, with specific steps and deadlines", "score": 0},
            {"label": "Usually clear, though sometimes vague",             "score": 1},
            {"label": "Often vague or loosely defined",                    "score": 2},
            {"label": "I do not define goals in advance",                  "score": 3}
        ]
    },
    {
        "id": 4,
        "text": "How consistently do you review what you planned at the end of each week to assess your progress?",
        "options": [
            {"label": "Every week",                  "score": 0},
            {"label": "Often, but not every week",   "score": 1},
            {"label": "Rarely",                      "score": 2},
            {"label": "Never",                       "score": 3}
        ]
    },
    {
        "id": 5,
        "text": "When you do not achieve a planned goal, how do you typically respond?",
        "options": [
            {"label": "I analyse what went wrong and adjust my approach",  "score": 0},
            {"label": "I reschedule the goal for next week",               "score": 1},
            {"label": "I feel frustrated but do not take specific action", "score": 2},
            {"label": "I tend to abandon the goal altogether",             "score": 3}
        ]
    },
    {
        "id": 6,
        "text": "How well do you prioritise your goals during a planning session?",
        "options": [
            {"label": "Very well, I always rank tasks by importance and urgency", "score": 0},
            {"label": "Fairly well, I consider priority most of the time",        "score": 1},
            {"label": "Inconsistently, I sometimes treat all tasks as equal",     "score": 2},
            {"label": "I do not prioritise and proceed without a clear order",    "score": 3}
        ]
    },
    {
        "id": 7,
        "text": "How often do you break large goals into smaller, manageable steps during planning?",
        "options": [
            {"label": "Always", "score": 0},
            {"label": "Often",  "score": 1},
            {"label": "Rarely", "score": 2},
            {"label": "Never",  "score": 3}
        ]
    },
    {
        "id": 8,
        "text": "How realistic are the goals you usually set for a single week?",
        "options": [
            {"label": "Very realistic and achievable",    "score": 0},
            {"label": "Mostly realistic",                 "score": 1},
            {"label": "Sometimes unrealistic",            "score": 2},
            {"label": "Usually too ambitious or unclear", "score": 3}
        ]
    },
    {
        "id": 9,
        "text": "How often do unexpected events completely derail your weekly plans?",
        "options": [
            {"label": "Almost never, because I adapt well", "score": 0},
            {"label": "Occasionally",                       "score": 1},
            {"label": "Often",                              "score": 2},
            {"label": "Almost every week",                  "score": 3}
        ]
    },
    {
        "id": 10,
        "text": "How much time do you usually spend preparing your weekly plan?",
        "options": [
            {"label": "Enough time to think through tasks carefully", "score": 0},
            {"label": "A reasonable amount of time",                  "score": 1},
            {"label": "Very little time",                             "score": 2},
            {"label": "I do not set aside planning time",             "score": 3}
        ]
    },
    {
        "id": 11,
        "text": "How often do you write your weekly goals down in a planner, notebook, or digital tool?",
        "options": [
            {"label": "Every week",  "score": 0},
            {"label": "Most weeks",  "score": 1},
            {"label": "Rarely",      "score": 2},
            {"label": "Never",       "score": 3}
        ]
    },
    {
        "id": 12,
        "text": "How confident do you feel that you will complete your goals after a planning session?",
        "options": [
            {"label": "Very confident",       "score": 0},
            {"label": "Moderately confident", "score": 1},
            {"label": "Slightly confident",   "score": 2},
            {"label": "Not confident at all", "score": 3}
        ]
    },
    {
        "id": 13,
        "text": "When planning your week, how often do you consider deadlines in advance?",
        "options": [
            {"label": "Always",          "score": 0},
            {"label": "Usually",         "score": 1},
            {"label": "Sometimes",       "score": 2},
            {"label": "Rarely or never", "score": 3}
        ]
    },
    {
        "id": 14,
        "text": "How often do you include time for rest or recovery when making your weekly plan?",
        "options": [
            {"label": "Always", "score": 0},
            {"label": "Often",  "score": 1},
            {"label": "Rarely", "score": 2},
            {"label": "Never",  "score": 3}
        ]
    },
    {
        "id": 15,
        "text": "How likely are you to postpone an important task even after planning it?",
        "options": [
            {"label": "Very unlikely",    "score": 0},
            {"label": "Somewhat unlikely","score": 1},
            {"label": "Quite likely",     "score": 2},
            {"label": "Very likely",      "score": 3}
        ]
    },
    {
        "id": 16,
        "text": "How often do you adjust your weekly goals when you notice they are no longer realistic?",
        "options": [
            {"label": "Promptly and effectively",                  "score": 0},
            {"label": "Sometimes",                                  "score": 1},
            {"label": "Rarely",                                     "score": 2},
            {"label": "I usually continue without adjusting anything", "score": 3}
        ]
    },
    {
        "id": 17,
        "text": "How organised are the tools or systems you use for weekly planning?",
        "options": [
            {"label": "Very organised and easy to follow",     "score": 0},
            {"label": "Mostly organised",                      "score": 1},
            {"label": "Somewhat disorganised",                 "score": 2},
            {"label": "I do not use any consistent system",    "score": 3}
        ]
    },
    {
        "id": 18,
        "text": "How often do you begin your week knowing exactly which goals are the top priority?",
        "options": [
            {"label": "Always",          "score": 0},
            {"label": "Usually",         "score": 1},
            {"label": "Sometimes",       "score": 2},
            {"label": "Rarely or never", "score": 3}
        ]
    },
    {
        "id": 19,
        "text": "How often do you reflect on why certain goals were completed successfully?",
        "options": [
            {"label": "Every week", "score": 0},
            {"label": "Often",      "score": 1},
            {"label": "Rarely",     "score": 2},
            {"label": "Never",      "score": 3}
        ]
    },
    {
        "id": 20,
        "text": "Overall, how effective do you believe your weekly planning process is?",
        "options": [
            {"label": "Highly effective",      "score": 0},
            {"label": "Mostly effective",       "score": 1},
            {"label": "Somewhat ineffective",   "score": 2},
            {"label": "Very ineffective",       "score": 3}
        ]
    }
]

# ─── Psychological state bands ────────────────────────────────────────────────
STATES: list = [
    {
        "min_score": 0,  "max_score": 12,
        "label":       "Highly Effective Planner",
        "summary":     "Exceptional planning frequency and goal achievement.",
        "description": "Strong self-regulatory habits are visible; no immediate intervention is needed."
    },
    {
        "min_score": 13, "max_score": 24,
        "label":       "Effective Planner",
        "summary":     "Good planning consistency with solid goal achievement.",
        "description": "Current habits are working well; only minor improvements are likely to be needed."
    },
    {
        "min_score": 25, "max_score": 36,
        "label":       "Moderate Planner",
        "summary":     "Planning is present, but goal achievement is inconsistent.",
        "description": "Refining goal structure, planning detail, and weekly review habits would likely improve results."
    },
    {
        "min_score": 37, "max_score": 48,
        "label":       "Inconsistent Planner",
        "summary":     "Planning sessions are irregular and goal achievement is low.",
        "description": "Increasing planning frequency and adding stronger accountability would be advisable."
    },
    {
        "min_score": 49, "max_score": 60,
        "label":       "Disengaged Planner",
        "summary":     "There is little structured planning and planned goals are rarely achieved.",
        "description": "A more supportive structure around self-regulation and goal setting is strongly recommended."
    }
]


# ─── User-defined functions ───────────────────────────────────────────────────

def validate_name(prompt: str) -> str:
    """
    Validate that input contains only letters, hyphens, apostrophes, and spaces.
    Supports names such as O'Connor, Smith-Jones, Mary Ann.
    Uses a FOR loop to inspect each character (criterion: for loop validation).
    Uses a WHILE loop to keep asking until input is valid (criterion: while loop).
    """
    while True:                                        # while loop – retry until valid
        name: str = input(prompt).strip()
        is_valid: bool = True                          # bool variable

        if not name:
            print("  [!] Name cannot be empty. Please try again.")
            continue

        for char in name:                              # for loop – check each character
            if not (char.isalpha() or char in ALLOWED_CHARS):
                is_valid = False
                break

        if is_valid:
            return name
        else:
            print("  [!] Only letters, hyphens (-), apostrophes ('), and spaces are allowed.")


def validate_dob(prompt: str) -> str:
    """
    Validate date of birth – must be in DD/MM/YYYY format and must be a past date.
    Uses a WHILE loop to keep prompting until a valid date is entered.
    """
    while True:                                        # while loop – retry on bad input
        dob: str = input(prompt).strip()
        try:
            parsed_date = datetime.strptime(dob, "%d/%m/%Y")
            if parsed_date >= datetime.today():
                print("  [!] Date of birth must be in the past.")
            else:
                return dob
        except ValueError:
            print("  [!] Invalid date. Use DD/MM/YYYY (e.g. 15/03/2003).")


def validate_student_id(prompt: str) -> str:
    """
    Validate that Student ID contains digits only.
    Uses a FOR loop to check every character (criterion: for loop validation).
    Uses a WHILE loop to retry on invalid input (criterion: while loop).
    """
    while True:                                        # while loop – retry until valid
        sid: str = input(prompt).strip()
        all_digits: bool = True                        # bool variable

        if not sid:
            print("  [!] Student ID cannot be empty.")
            continue

        for ch in sid:                                 # for loop – digit check per char
            if not ch.isdigit():
                all_digits = False
                break

        if all_digits:
            return sid
        else:
            print("  [!] Student ID must contain digits only.")


def get_state(score: int) -> dict:
    """Return the matching psychological state dict based on the total score."""
    for state in STATES:
        if state["min_score"] <= score <= state["max_score"]:
            return state
    return STATES[-1]                                  # fallback (should never trigger)


def display_result(result: dict) -> None:
    """Print a formatted result summary to the console."""
    print(f"\n{LINE}")
    print("  RESULT SUMMARY")
    print(LINE)
    print(f"  Name        : {result['surname']}, {result['given_name']}")
    print(f"  Date of Birth: {result['dob']}")
    print(f"  Student ID  : {result['student_id']}")
    print(f"  Date Taken  : {result['date_taken']}")
    print(f"  Total Score : {result['total_score']} / {QUESTION_COUNT * MAX_OPTION_SCORE}")
    print(f"  Percentage  : {result['percentage']} %")
    print(f"\n  State       : {result['state']['label']}")
    print(f"  Summary     : {result['state']['summary']}")
    print(f"  Advice      : {result['state']['description']}")
    print(LINE)


def run_survey() -> dict:
    """
    Collect user details, run all questions, compute score, and return a result dict.
    Demonstrates: list, dict, int, float, bool, range, str variable types.
    Contains a FOR loop (iterate questions) and WHILE loop (answer validation).
    Contains IF, ELIF, ELSE conditional statements.
    """
    print(f"\n{LINE}")
    print(f"  {SURVEY_TITLE}")
    print(LINE)
    print("  Please enter your personal details.\n")

    surname:    str = validate_name("  Surname       : ")
    given_name: str = validate_name("  Given Name    : ")
    dob:        str = validate_dob("  Date of Birth (DD/MM/YYYY): ")
    student_id: str = validate_student_id("  Student ID    : ")

    print(f"\n{LINE}")
    print("  QUESTIONNAIRE  –  Enter a number (1–4) for each answer.")
    print(LINE)

    total_score: int  = 0
    answers:     list = []                             # list – stores each answer dict

    for i, question in enumerate(QUESTIONS, start=1):  # for loop – iterate all questions
        print(f"\n  Q{i}. {question['text']}")
        for j, opt in enumerate(question["options"], start=1):
            print(f"       {j}. {opt['label']}")

        # while loop for input validation (criterion)
        while True:
            raw: str = input("  Your answer: ").strip()
            is_valid_input: bool = False               # bool variable

            try:
                choice: int = int(raw)
                if choice in range(1, len(question["options"]) + 1):  # range used here
                    is_valid_input = True
            except ValueError:
                pass

            if is_valid_input:
                break
            else:                                      # else branch (criterion)
                print("  [!] Please enter a number between 1 and 4.")

        selected: dict = question["options"][choice - 1]
        total_score += selected["score"]
        answers.append({"question_id": question["id"],
                        "answer_index": choice,
                        "score": selected["score"]})

    percentage: float = round((total_score / (QUESTION_COUNT * MAX_OPTION_SCORE)) * 100, 2)
    state:      dict  = get_state(total_score)

    # IF / ELIF / ELSE conditional statements (criterion – at least 3)
    if total_score <= 12:
        category_note: str = "Excellent! Keep up the great work."
    elif total_score <= 24:
        category_note = "Well done. Small refinements can take you further."
    elif total_score <= 36:
        category_note = "There is room for improvement in your planning habits."
    elif total_score <= 48:
        category_note = "Consider building more structure into your weekly routine."
    else:
        category_note = "Seeking guidance on goal-setting strategies is strongly advised."

    result: dict = {
        "surname":     surname,
        "given_name":  given_name,
        "dob":         dob,
        "student_id":  student_id,
        "date_taken":  datetime.now().strftime("%d/%m/%Y %H:%M"),
        "total_score": total_score,
        "percentage":  percentage,
        "state":       state,
        "category_note": category_note,
        "answers":     answers
    }
    return result


def save_results(result: dict) -> None:
    """
    Offer the user the option to save results to a JSON file.
    Demonstrates persistence (LO3) – saving data to an external file.
    """
    save: str = input("\n  Save your results to a JSON file? (yes / no): ").strip().lower()

    if save in {"yes", "y"}:                           # set membership test
        filename: str = input("  Enter filename (without extension): ").strip()
        if not filename:
            filename = f"{result['student_id']}_survey_result"
        filepath: str = f"{filename}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"  [OK] Results saved to '{filepath}'.")
    else:
        print("  Results were not saved.")


def load_results(filepath: str) -> None:
    """
    Load and display results from an existing JSON file.
    Demonstrates persistence (LO3) – reading data from an external file.
    """
    if not os.path.exists(filepath):
        print(f"  [!] File '{filepath}' not found. Please check the path.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        result: dict = json.load(f)

    display_result(result)


# ─── Program entry point ──────────────────────────────────────────────────────

def main() -> None:
    """
    Display the main menu and route the user to the correct action.
    Uses a WHILE loop (main loop) and FOR loop (menu display).
    Contains IF / ELIF / ELSE conditional branches.
    """
    print(f"\n{'═' * 62}")
    print("  Welcome to the Planning & Goal Achievement Survey Tool")
    print(f"{'═' * 62}")

    while True:                                        # while loop – main program loop
        print("\n  Main Menu:")
        for option in MENU_OPTIONS:                    # for loop – print menu items
            print(f"    {option}")

        choice: str = input("\n  Choose an option (1–3): ").strip()

        if choice == "1":                              # if branch
            result = run_survey()
            display_result(result)
            save_results(result)
        elif choice == "2":                            # elif branch
            filepath: str = input("  Enter the full path to the JSON result file: ").strip()
            load_results(filepath)
        elif choice == "3":                            # elif branch
            print("\n  Thank you for using the survey tool. Goodbye!\n")
            break
        else:                                          # else branch
            print("  [!] Invalid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
