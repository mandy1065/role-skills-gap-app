
import streamlit as st

# Inject custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f7f9fc;
        }
        .title {
            font-size: 2.5em;
            font-weight: bold;
            color: #003366;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 1.2em;
            color: #444444;
            text-align: center;
            margin-bottom: 30px;
        }
        .footer {
            position: fixed;
            bottom: 20px;
            width: 100%;
            text-align: center;
            font-size: 0.9em;
            color: #888888;
        }
        .stMarkdown {
            font-size: 1.05em;
        }
    </style>
"""", unsafe_allow_html=True)

# Role, Skills and Corresponding Courses
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
    }
}

st.markdown('<div class="title">Skill Gap Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find missing skills for your role and recommended courses to upskill.</div>', unsafe_allow_html=True)

role = st.selectbox("ðŸŽ¯ Select your role", list(roles.keys()))

if role:
    st.markdown("### âœ… Select the skills you already have")
    selected_skills = st.multiselect("Choose your known skills", list(roles[role]["skills"].keys()))

    missing_skills = [s for s in roles[role]["skills"] if s not in selected_skills]

    if missing_skills:
        st.markdown("### âŒ Missing Skills & Recommended Courses")
        for skill in missing_skills:
            st.markdown(f"- **{skill}** â†’ [Course Link]({roles[role]['skills'][skill]})")
    else:
        st.success("ðŸŽ‰ You have all the listed skills for this role!")

# Add Footer
st.markdown('<div class="footer">Powered by <strong>Brainyscout</strong></div>', unsafe_allow_html=True)
