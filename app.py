
import streamlit as st
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime

st.set_page_config(page_title="Brainyscout Skill Gap Tracker", layout="wide")

# Inject custom CSS to enhance the UI aesthetics
st.markdown(
    """
    <style>
        /* Overall background color for the app */
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

# Role selection in sidebar
selected_role = st.sidebar.selectbox("Select Role", list(roles.keys()))
all_skills = list(roles[selected_role]["skills"].keys())

# Initialise session state for completed skills when the role changes
if "completed_skills" not in st.session_state or st.session_state.get("role") != selected_role:
    st.session_state["completed_skills"] = []
    st.session_state["role"] = selected_role

# Multiselect to predefine completed/known skills; uses session state as default
initial_known = st.session_state.get("completed_skills", [])
known_skills_sidebar = st.sidebar.multiselect(
    "Select Known Skills", options=all_skills, default=initial_known
)

# Synchronise session state with sidebar selection if it changes
if set(known_skills_sidebar) != set(st.session_state["completed_skills"]):
    st.session_state["completed_skills"] = known_skills_sidebar

# Determine missing skills based on current completed skills
missing_skills_list = [s for s in all_skills if s not in st.session_state["completed_skills"]]

# -----------------------------------------------------------------------------
# Define dashboard tabs
tab_skill_checker, tab_learning_plan, tab_progress, tab_analytics = st.tabs(
    ["Skill Checker", "Learning Plan", "Progress Tracker", "Analytics"]
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

# -----------------------------------------------------------------------------
# Footer branding
st.markdown("---")
st.markdown(
    '<div style="text-align: center;">Powered by Brainyscout</div>',
    unsafe_allow_html=True
)
