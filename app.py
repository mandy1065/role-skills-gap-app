
import streamlit as st
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime

st.set_page_config(page_title="Brainyscout Skill Gap Tracker", layout="wide")

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

st.title("Brainyscout Skill Gap Tracker")
st.markdown("Select your role, mark the skills you already have, and get a list of missing skills with course recommendations.")

email = st.text_input("Enter your email:", "")

selected_role = st.selectbox("Select Role", list(roles.keys()))
all_skills = list(roles[selected_role]["skills"].keys())

known_skills = st.multiselect("Select Known Skills", options=all_skills)
missing_skills = [skill for skill in all_skills if skill not in known_skills]

# Save to Google Sheets
if email:
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        email,
        selected_role,
        ", ".join(known_skills),
        ", ".join(missing_skills)
    ])

# Display missing skills and links
if missing_skills:
    st.subheader("Missing Skills & Courses")
    for skill in missing_skills:
        link = roles[selected_role]["skills"][skill]
        st.markdown(f"**{skill}** → [Course Link]({link})")
else:
    st.success("You have all the skills for this role!")

# Full course roadmap
with st.expander("Full Learning Plan"):
    st.write(pd.DataFrame({
        "Skill": list(roles[selected_role]["skills"].keys()),
        "Course Link": list(roles[selected_role]["skills"].values())
    }))

st.markdown("---")
st.markdown('<div style="text-align: center;">Powered by Brainyscout</div>', unsafe_allow_html=True)
