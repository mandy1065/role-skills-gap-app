
import streamlit as st
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime

# Import comprehensive interview question data for each role. This module
# provides 50 behavioural and 50 technical interview questions per role.
from interview_questions_data import interview_questions

st.set_page_config(page_title="Brainyscout Skill Gap Tracker", layout="wide")

# Inject custom CSS to enhance the UI aesthetics
st.markdown(
    """
    <style>
        /* Ensure consistent light theme across devices */
        html, body, [data-testid="stApp"] {
            background-color: #f5f7fa !important;
            color: #264653 !important;
        }
        /* Overall background color for the app's main container */
        .reportview-container {
            background-color: #f5f7fa;
        }
        /* Style the sidebar: white card with rounded corners */
        .sidebar .sidebar-content {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 8px;
        }
        /* Style the main content container */
        .block-container {
            background-color: #ffffff;
            padding: 2rem 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        /* Style header text */
        h1 {
            color: #264653;
        }
        /* Style subheader text */
        h2, h3 {
            color: #2a9d8f;
        }
        /* Style tables generated via markdown */
        table {
            width: 100% !important;
        }
        th, td {
            padding: 0.5rem;
        }
        /* Style buttons */
        button[kind="primary"] {
            background-color: #2a9d8f;
            color: #ffffff;
        }
        button[kind="secondary"] {
            background-color: #e9c46a;
            color: #264653;
        }
        /* Ensure link color is visible in dark or light mode */
        a, a:visited {
            color: #1e90ff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Google Sheets Integration
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/13W17_W3rSIvWCSuYDLo-RX__y365UA7SECB5vOTZ9xs/edit?usp=sharing").sheet1

# Role → Skills → Course links
roles = {
    "QA Analyst": {
        "skills": {
            "Test case design": "https://www.coursera.org/learn/software-testing",
            "Manual testing": "https://www.udemy.com/course/manual-software-testing/",
            "Bug reporting (JIRA)": "https://www.udemy.com/course/jira-tutorial-a-complete-guide-for-beginners/",
            "SQL for data validation": "https://www.coursera.org/learn/sql-for-data-science",
            "Functional testing": "https://www.udemy.com/course/software-testing/",
            "Regression testing": "https://www.linkedin.com/learning/",
            "SDLC knowledge": "https://www.youtube.com/watch?v=xtPYTfLJZBM",
            "Communication skills": "https://www.coursera.org/learn/business-communication"
        }
    },
    "QA Automation Engineer": {
        "skills": {
            "Python": "https://www.coursera.org/specializations/python",
            "Selenium/WebDriver": "https://www.udemy.com/course/selenium-real-time-examplesinterview-questions/",
            "API Testing (Postman)": "https://www.coursera.org/learn/postman-api",
            "TestNG/PyTest": "https://www.udemy.com/course/pytest-tutorial/",
            "CI/CD with Jenkins": "https://www.coursera.org/learn/continuous-integration",
            "Version Control (Git)": "https://www.codecademy.com/learn/learn-git",
            "BDD (Cucumber/Gherkin)": "https://www.udemy.com/course/bdd-with-selenium-webdriver-and-cucumber/",
            "Framework Design": "https://www.udemy.com/course/test-automation-frameworks/"
        }
    },
    "Software Developer": {
        "skills": {
            "Data Structures & Algorithms": "https://www.coursera.org/specializations/data-structures-algorithms",
            "OOP (Java/Python/C#)": "https://www.coursera.org/learn/python-object-oriented-programming",
            "HTML/CSS/JavaScript": "https://www.freecodecamp.org/learn/",
            "SQL/NoSQL": "https://lagunita.stanford.edu/courses/DB/2014/SelfPaced/about",
            "REST APIs": "https://www.udacity.com/course/api-development-and-documentation--ud805",
            "Git/GitHub": "https://www.youtube.com/watch?v=RGOj5yH7evk",
            "Unit Testing": "https://www.coursera.org/learn/automated-software-testing",
            "Agile Development": "https://www.coursera.org/learn/agile-atlassian-jira"
        }
    },
    "Data Engineer": {
        "skills": {
            "SQL & NoSQL": "https://mode.com/sql-tutorial/",
            "ETL pipelines": "https://www.udemy.com/course/etl-and-data-pipelines-with-python/",
            "Python/Scala": "https://www.coursera.org/learn/python-data-analysis",
            "Big Data (Spark, Hadoop)": "https://www.coursera.org/learn/intro-to-apache-spark",
            "Data Warehousing": "https://www.coursera.org/learn/dwh",
            "Cloud (AWS/GCP/Azure)": "https://www.coursera.org/professional-certificates/data-engineering-gcp",
            "Apache Airflow": "https://www.udemy.com/course/the-complete-hands-on-course-to-master-apache-airflow/",
            "Data Modeling": "https://www.coursera.org/learn/data-modeling"
        }
    },
    "Data Analyst": {
        "skills": {
            "SQL": "https://www.udemy.com/course/sql-for-data-analytics/",
            "Excel & Google Sheets": "https://www.coursera.org/specializations/excel",
            "Tableau/Power BI": "https://www.coursera.org/learn/visual-analytics-tableau",
            "Python (Pandas, Numpy)": "https://www.coursera.org/learn/data-analysis-with-python",
            "A/B Testing": "https://www.udacity.com/course/ab-testing--ud257",
            "Statistics": "https://online.stanford.edu/courses/sohs-ystatslearningstatisticallearning",
            "Business Communication": "https://www.coursera.org/learn/business-writing"
        }
    },
    "Product Manager": {
        "skills": {
            "Strategic thinking": "https://www.coursera.org/learn/strategic-management",
            "Market research": "https://www.coursera.org/learn/market-research",
            "User-centric design": "https://www.coursera.org/specializations/interaction-design",
            "Technical documentation": "https://www.udemy.com/course/technical-writing/",
            "Data analysis": "https://www.coursera.org/learn/data-analysis-with-python",
            "Agile product development": "https://www.coursera.org/learn/agile-development"
        }
    },
    "Project Manager": {
        "skills": {
            "Project planning": "https://www.coursera.org/learn/project-management-principles",
            "Agile methodology": "https://www.coursera.org/learn/agile-project-management",
            "Risk management": "https://www.coursera.org/learn/project-risk-management",
            "Team communication": "https://www.coursera.org/learn/communication-in-the-21st-century-workplace",
            "Budgeting and cost control": "https://www.udemy.com/course/project-budgeting-cost-control/",
            "Project scheduling tools": "https://www.coursera.org/learn/project-management-tools"
        }
    }
}

# -----------------------------------------------------------------------------
# Interview practice questions and sample answers.  Behavioural questions use
# the STAR (Situation, Task, Action, Result) method to structure answers.
# Technical questions cover general topics across roles.  Users can practise
# answering these questions, view a sample guideline, and receive simple
# feedback based on answer length and structure.
# The old placeholder interview_questions dictionary has been removed. The
# comprehensive per-role interview question data is imported from
# interview_questions_data.

# -----------------------------------------------------------------------------
# Main page title and description
st.title("Brainyscout Skill Gap Tracker")
st.markdown(
    "Select your role, mark the skills you already have, and explore your "
    "personalised learning plan."
)

# -----------------------------------------------------------------------------
# Sidebar for user inputs
st.sidebar.title("Your Profile")
st.sidebar.markdown(
    "Use the options below to enter your email, choose your role, and select "
    "the skills you already possess."
)

# Email input
email = st.sidebar.text_input("Enter your email:", "")

# -----------------------------------------------------------------------------
# If the user has not provided an email address yet, halt the application after
# displaying a prompt.  This ensures that users first enter their email
# before they start exploring roles or selecting skills.  Preventing the rest
# of the app from running until an email is entered also prevents accidental
# writes to the Google Sheet without a user identifier.
if not email:
    st.sidebar.warning("Please enter your email to continue.")
    # Use st.stop() to gracefully stop further execution until an email is
    # provided.  None of the downstream UI (role selector, skills, tabs)
    # will render until the user supplies an email.
    st.stop()

# Role selection in sidebar.  Use a placeholder option so that no role is
# pre-selected by default.  The list begins with a prompt followed by
# all available roles.  When the placeholder is chosen, the rest of the
# application will not proceed until the user selects a real role.
role_options = ["Select Role"] + list(roles.keys())
selected_role = st.sidebar.selectbox("Select Role", role_options, index=0)

# If the user has not selected a real role yet (i.e. the placeholder is
# selected), prompt them and stop execution.  This prevents any skills or
# analytics from showing until a role is chosen.
if selected_role == "Select Role":
    st.sidebar.warning("Please select a role to continue.")
    st.stop()

all_skills = list(roles[selected_role]["skills"].keys())

# Initialise session state for completed skills when the role changes
if "completed_skills" not in st.session_state or st.session_state.get("role") != selected_role:
    st.session_state["completed_skills"] = []
    st.session_state["role"] = selected_role

# -----------------------------------------------------------------------------
# Replace the multiselect for known skills with individual checkboxes.  A list
# accumulates the skills that the user marks as known.  This makes it easier
# for users to see all skills at once rather than opening a dropdown.  The
# selections are stored in ``st.session_state['completed_skills']`` so the rest
# of the app (progress tracker, analytics, etc.) stays in sync.

# Build a list of known skills based on checkbox selections in the sidebar.
checkbox_known_skills: list[str] = []
for skill in all_skills:
    # Use a unique key per role and skill to preserve individual checkbox state
    chk_key = f"sidebar_known_{selected_role}_{skill}"
    checked = st.sidebar.checkbox(
        label=skill,
        value=(skill in st.session_state.get("completed_skills", [])),
        key=chk_key
    )
    if checked:
        checkbox_known_skills.append(skill)

# Update session state when the selections differ
if set(checkbox_known_skills) != set(st.session_state.get("completed_skills", [])):
    st.session_state["completed_skills"] = checkbox_known_skills

# Determine missing skills based on current completed skills
missing_skills_list = [s for s in all_skills if s not in st.session_state["completed_skills"]]

# -----------------------------------------------------------------------------
# Automatically record the user's selections to Google Sheets if they have
# provided an email address.  This allows progress to persist without
# requiring the user to explicitly click "Save Progress".  Each record
# includes a timestamp, the user's email, their selected role, the skills
# they have marked as known/completed and the skills still missing.  This
# will create multiple rows over time but gives a historical view of how
# the user's knowledge evolves.
if email:
    # Only record a row if a real role has been selected.  Because the
    # placeholder "Select Role" causes an early stop above, this code is
    # only reached when the user has chosen a valid role.  Recording the
    # timestamped progress on each run provides a historical log of
    # selections.
    try:
        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            email,
            selected_role,
            ", ".join(st.session_state["completed_skills"]),
            ", ".join(missing_skills_list)
        ])
    except Exception:
        # Silently ignore errors to avoid interrupting the UI.  This could
        # happen if the sheet is temporarily unavailable.  The progress
        # tracker will still attempt to save changes when the user clicks
        # "Save Progress".
        pass

# -----------------------------------------------------------------------------
# Define dashboard tabs including Interview Practice
tab_skill_checker, tab_learning_plan, tab_progress, tab_analytics, tab_interview = st.tabs(
    ["Skill Checker", "Learning Plan", "Progress Tracker", "Analytics", "Interview Practice"]
)

# ----------------------- Skill Checker Tab ------------------------------
with tab_skill_checker:
    st.subheader("Missing Skills & Recommended Courses")
    if missing_skills_list:
        # Build a list for missing skills and courses
        for skill in missing_skills_list:
            link = roles[selected_role]["skills"][skill]
            st.markdown(f"- **{skill}** -> [Course Link]({link})")
    else:
        st.success("You have all the skills for this role!")

# ----------------------- Learning Plan Tab -----------------------------
with tab_learning_plan:
    st.subheader("Full Learning Plan for Selected Role")
    # Construct a markdown table of all skills and their courses for the role
    lp_rows = ""
    for skill, link in roles[selected_role]["skills"].items():
        lp_rows += f"| {skill} | [Link]({link}) |\n"
    lp_table = "| Skill | Course |\n| --- | --- |\n" + lp_rows
    st.markdown(lp_table, unsafe_allow_html=True)

    # Personalised learning path based on missing skills
    st.subheader("Personalised Learning Path")
    if missing_skills_list:
        path_rows = ""
        for idx, skill in enumerate(missing_skills_list, start=1):
            link = roles[selected_role]["skills"][skill]
            path_rows += f"| Step {idx} | {skill} | [Link]({link}) |\n"
        path_table = "| Step | Skill | Course |\n| --- | --- | --- |\n" + path_rows
        st.markdown(path_table, unsafe_allow_html=True)
    else:
        st.success("No missing skills – you're all set!")

# ----------------------- Progress Tracker Tab ---------------------------
with tab_progress:
    st.subheader("Skill Progress Tracker")
    st.markdown(
        "Use the checkboxes below to mark skills as completed. "
        "Click **Save Progress** to record your changes."
    )
    # Collect new completed skills based on checkboxes
    new_completed = []
    for skill in all_skills:
        checked = st.checkbox(
            label=skill,
            value=(skill in st.session_state["completed_skills"]),
            key=f"prog_{selected_role}_{skill}"
        )
        if checked:
            new_completed.append(skill)
    # Save progress button
    if st.button("Save Progress"):
        # Update session state
        st.session_state["completed_skills"] = new_completed
        # Recalculate missing skills after update
        missing_skills_list = [s for s in all_skills if s not in new_completed]
        # Append progress to Google Sheets if email is provided
        if email:
            sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                email,
                selected_role,
                ", ".join(new_completed),
                ", ".join(missing_skills_list)
            ])
        st.success("Progress saved.")
    # Display completed vs pending skills as a table
    progress_rows = ""
    for skill in all_skills:
        status = "Completed" if skill in st.session_state["completed_skills"] else "Pending"
        progress_rows += f"| {skill} | {status} |\n"
    progress_table = "| Skill | Status |\n| --- | --- |\n" + progress_rows
    st.markdown(progress_table, unsafe_allow_html=True)
    # Display summary counts
    st.markdown(
        f"**Summary:** {len(st.session_state['completed_skills'])} completed, "
        f"{len([s for s in all_skills if s not in st.session_state['completed_skills']])} pending"
    )

# ----------------------- Analytics Tab --------------------------------
with tab_analytics:
    st.subheader("Learning Analytics")
    st.markdown(
        "Visualise your progress: compare the number of completed skills "
        "with those still pending."
    )
    # Prepare data for bar chart
    completed_count = len(st.session_state.get("completed_skills", []))
    pending_count = len(all_skills) - completed_count
    analytics_df = pd.DataFrame({
        "Status": ["Completed", "Pending"],
        "Count": [completed_count, pending_count]
    }).set_index("Status")
    st.bar_chart(analytics_df)

# ----------------------- Interview Practice Tab ---------------------------
with tab_interview:
    st.subheader("Interview Practice")
    st.markdown(
        "Select a type of question (behavioural or technical), practise your "
        "answer, and receive instant feedback. Behavioural answers should be "
        "structured using the STAR method (Situation, Task, Action, Result) as "
        "recommended for interview responses【892174856631884†L139-L159】."
    )

    # Allow the user to choose behavioural or technical questions
    # Allow the user to choose between behavioural and technical questions.
    # Categories are consistent across roles and align with the imported data structure.
    categories = ["Behavioral", "Technical"]
    category = st.selectbox("Interview Question Type", categories)
    # Retrieve the list of question dictionaries for the selected role and category
    questions = interview_questions[selected_role][category]
    question_texts = [q["question"] for q in questions]
    selected_question = st.selectbox("Select a question to practise", question_texts)
    # Retrieve the selected question and sample answer
    question_obj = next(q for q in questions if q["question"] == selected_question)
    st.markdown(f"**Question:** {selected_question}")
    st.markdown(f"**Sample Answer (Guideline):** {question_obj['answer']}")

    # Text area for the user's answer
    user_answer = st.text_area("Your Answer", "", height=150)

    # Container for feedback messages
    if st.button("Submit Answer"):
        # Basic evaluation criteria: length and use of STAR keywords for behavioural questions
        feedback_messages = []
        word_count = len(user_answer.split())
        if word_count < 50:
            feedback_messages.append("Your answer seems short; try elaborating more.")
        # Check for STAR method keywords in behavioural answers
        if category == "Behavioral":
            star_keywords = ["situation", "task", "action", "result"]
            star_used = any(k in user_answer.lower() for k in star_keywords)
            if not star_used:
                feedback_messages.append(
                    "Consider using the STAR structure: describe the Situation, "
                    "Task, Action and Result explicitly."
                )
        if not feedback_messages:
            feedback_messages.append("Great job! Your answer covers the key points.")
        # Display feedback
        for msg in feedback_messages:
            st.success(msg)
        # Save the user's answer in session state for progress tracking
        # Save the user's answer in session state for progress tracking
        st.session_state.setdefault("interview_answers", {})
        # Ensure answers are stored per role
        st.session_state["interview_answers"].setdefault(selected_role, {})
        st.session_state["interview_answers"][selected_role][selected_question] = user_answer

    # Display progress summary for interview practice
    # Compute progress for the selected role. Total questions is the sum of behavioural
    # and technical questions for that role.
    total_questions = len(interview_questions[selected_role]["Behavioral"]) + len(interview_questions[selected_role]["Technical"])
    answered_count = len(st.session_state.get("interview_answers", {}).get(selected_role, {}))
    st.markdown(f"You have answered {answered_count} out of {total_questions} interview questions for the {selected_role} role.")
    # Simple bar chart to visualise interview practice progress
    interview_prog_df = pd.DataFrame({
        "Status": ["Answered", "Unanswered"],
        "Count": [answered_count, total_questions - answered_count]
    }).set_index("Status")
    st.bar_chart(interview_prog_df)


# -----------------------------------------------------------------------------
# Footer branding
st.markdown("---")
st.markdown(
    '<div style="text-align: center;">Powered by Brainyscout</div>',
    unsafe_allow_html=True
)
