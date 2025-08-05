
import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup Google Sheets connection using Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("13W17_W3rSIvWCSuYDLo-RX__y365UA7SECB5vOTZ9xs").sheet1

# Role and skill mapping
role_skills = {
    "QA Analyst": ["Test case design", "Manual testing", "Bug reporting", "SQL", "Functional testing", "Regression testing", "SDLC knowledge", "Communication"],
    "QA Automation Engineer": ["Python", "Selenium/WebDriver", "API Testing", "CI/CD", "BDD", "Git", "Framework Design"],
    "Software Developer": ["Data Structures", "OOP", "Web Dev", "Databases", "REST APIs", "Version Control", "Unit Testing", "Agile"],
    "Data Engineer": ["SQL", "ETL pipelines", "Python/Scala", "Big Data Tools", "Data Warehousing", "Airflow", "Data Modeling"],
    "Data Analyst": ["SQL", "Excel", "Tableau", "Python (Pandas/Numpy)", "A/B Testing", "Statistics", "Business Communication"],
    "Product Manager": ["Strategic thinking", "Market research", "User-centric design", "Technical writing", "Data analysis", "Agile product development"],
    "Project Manager": ["Project planning", "Agile methodology", "Risk management", "Team communication", "Budgeting", "Scheduling tools"]
}

st.title("Brainyscout Skill Tracker")

# Email-based login
st.sidebar.header("Login")
email = st.sidebar.text_input("Enter your email", key="email")

if email:
    st.success(f"Welcome, {email}")
    role = st.selectbox("Select Your Role", list(role_skills.keys()))
    skills = role_skills[role]

    # Load data
    records = sheet.get_all_records()
    user_data = next((row for row in records if row["email"] == email), None)

    known_skills = []
    completed_skills = []

    if user_data:
        if user_data["role"] == role:
            known_skills = user_data["known_skills"].split(",") if user_data["known_skills"] else []
            completed_skills = user_data["completed_skills"].split(",") if user_data["completed_skills"] else []

    # Select skills
    st.markdown("Select Known Skills")
    selected_known = st.multiselect("Skills you already know", skills, default=known_skills)

    st.markdown("Mark Completed Skills")
    selected_completed = st.multiselect("Skills you've completed learning", skills, default=completed_skills)

    # Display missing
    missing_skills = [s for s in skills if s not in selected_known]
    st.markdown("Missing Skills")
    for s in missing_skills:
        st.markdown("- " + s)

    # Save
    def save_to_sheet():
        existing_row = next((i for i, row in enumerate(records) if row["email"] == email), None)
        new_data = [email, role, ",".join(selected_known), ",".join(selected_completed), str(datetime.now())]

        if existing_row is not None:
            sheet.update(f"A{existing_row+2}:E{existing_row+2}", [new_data])
        else:
            sheet.append_row(new_data)

        st.success("Progress saved!")

    if st.button("Save Progress"):
        save_to_sheet()

    # Sidebar summary
    st.sidebar.markdown("Dashboard")
    st.sidebar.markdown(f"**Role:** {role}")
    st.sidebar.markdown(f"**Known Skills:** {len(selected_known)}")
    st.sidebar.markdown(f"**Completed Skills:** {len(selected_completed)}")
    st.sidebar.markdown(f"**Missing Skills:** {len(missing_skills)}")
