
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup Google Sheets connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("13W17_W3rSIvWCSuYDLo-RX__y365UA7SECB5vOTZ9xs").sheet1

# Available roles and skills
role_skills = {{
    "QA Analyst": ["Test case design", "Manual testing", "Bug reporting", "SQL", "Functional testing", "Regression testing", "SDLC knowledge", "Communication"],
    "QA Automation Engineer": ["Python", "Selenium/WebDriver", "API Testing", "CI/CD", "BDD", "Git", "Framework Design"],
    "Software Developer": ["Data Structures", "OOP", "Web Dev", "Databases", "REST APIs", "Version Control", "Unit Testing", "Agile"],
    "Data Engineer": ["SQL", "ETL pipelines", "Python/Scala", "Big Data Tools", "Data Warehousing", "Airflow", "Data Modeling"],
    "Data Analyst": ["SQL", "Excel", "Tableau", "Python (Pandas/Numpy)", "A/B Testing", "Statistics", "Business Communication"],
    "Product Manager": ["Strategic thinking", "Market research", "User-centric design", "Technical writing", "Data analysis", "Agile product development"],
    "Project Manager": ["Project planning", "Agile methodology", "Risk management", "Team communication", "Budgeting", "Scheduling tools"]
}}

st.title("ðŸ” Brainyscout Skill Tracker")

# Login screen
st.sidebar.header("Login")
email = st.sidebar.text_input("Enter your email to begin", key="email")

if email:
    st.success("Welcome, {} ðŸ‘‹".format(email))
    role = st.selectbox("Select Your Role", list(role_skills.keys()))
    skills = role_skills[role]

    # Load existing data for the user if any
    records = sheet.get_all_records()
    user_data = next((row for row in records if row["email"] == email), None)

    known_skills = []
    completed_skills = []

    if user_data:
        if user_data["role"] == role:
            known_skills = user_data["known_skills"].split(",") if user_data["known_skills"] else []
            completed_skills = user_data["completed_skills"].split(",") if user_data["completed_skills"] else []

    st.markdown("### âœ… Select Known Skills")
    selected_known = st.multiselect("Skills you already know", skills, default=known_skills)

    st.markdown("### ðŸ Mark Completed Skills")
    selected_completed = st.multiselect("Skills you've completed learning", skills, default=completed_skills)

    # Show missing skills
    missing_skills = [s for s in skills if s not in selected_known]
    st.markdown("### âŒ Missing Skills")
    for s in missing_skills:
        st.markdown("- " + s)

    # Save to Google Sheets
    def save_to_sheet():
        existing_row = next((i for i, row in enumerate(records) if row["email"] == email), None)
        new_data = [email, role, ",".join(selected_known), ",".join(selected_completed), str(datetime.now())]

        if existing_row is not None:
            sheet.update(f"A{existing_row+2}:E{existing_row+2}", [new_data])
        else:
            sheet.append_row(new_data)

        st.success("âœ… Your progress has been saved!")

    if st.button("ðŸ’¾ Save Progress"):
        save_to_sheet()

    # Sidebar preview
    st.sidebar.markdown("### ðŸ” Dashboard")
    st.sidebar.markdown("**Role:** {}".format(role))
    st.sidebar.markdown("**Known:** {} skills".format(len(selected_known)))
    st.sidebar.markdown("**Completed:** {} skills".format(len(selected_completed)))
    st.sidebar.markdown("**Missing:** {} skills".format(len(missing_skills)))
