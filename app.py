"""
Streamlit Skill Gap Analysis App
================================

This Streamlit application allows a user to choose a target role and
select which of the required skills they already possess.  It then
computes the missing skills and offers course recommendations that
cover those gaps.  The data used here is derived from reputable
sources – for example, Product School and other educational
providers – and summarises the core skills required for Product
Managers, UX Researchers and Product Analysts.  Each course
recommendation includes a name, a brief description and a link to the
course provider.

The user interface is intentionally simple: choose a role, tick off
your existing skills, then review the missing skills and suggested
courses.  Feel free to extend or modify the lists of skills and
courses to suit your needs.
"""

import streamlit as st
import pandas as pd


@st.cache_data
def get_role_skills():
    """
    Returns a dictionary mapping roles to the list of
    fundamental skills expected for that role.

    The skill sets were compiled from multiple credible
    sources.  See the accompanying documentation for
    more detail on the derivation of each skill.
    """
    return {
        "Product Manager": [
            "Strategic thinking",
            "Market sensitivity",
            "User‑centric design",
            "Writing technical requirements",
            "Data analysis",
            "UX/UI design",
            "Collaboration & leadership",
            "Empathy",
            "Problem‑solving",
        ],
        "UX Researcher": [
            "Empathy",
            "Analytical thinking",
            "Effective communication",
            "Curiosity",
            "Problem‑solving",
            "Collaboration",
            "Technical proficiency",
        ],
        "Product Analyst": [
            "Data analysis",
            "Market research",
            "Product management tools",
            "UX design",
            "A/B testing",
            "SQL & database knowledge",
            "Communication",
            "Problem‑solving",
            "Critical thinking",
            "Stakeholder management",
            "Teamwork & collaboration",
            "Adaptability",
            "Attention to detail",
        ],
    }


@st.cache_data
def get_skill_courses():
    """
    Returns a mapping from skill to a list of course dictionaries.  Each
    course dictionary contains the course name, a brief description and
    a URL.  A single skill may be covered by multiple courses.
    """
    return {
        # Courses for Product Manager skills
        "Strategic thinking": [
            {
                "name": "Strategic Management – Copenhagen Business School",
                "url": "https://www.coursera.org/learn/strategic-management",
                "description": "Develop long‑term vision and strategic planning abilities with a focus on organizational and competitive strategy.",
            },
        ],
        "Market sensitivity": [
            {
                "name": "Market Research and Consumer Behavior – IE University",
                "url": "https://www.coursera.org/learn/market-research",
                "description": "Learn to analyse markets, understand consumer behaviour and design surveys to gather insights.",
            },
        ],
        "User‑centric design": [
            {
                "name": "Google UX Design Professional Certificate",
                "url": "https://www.coursera.org/professional-certificates/google-ux-design",
                "description": "Master the fundamentals of user research, wireframing, prototyping and usability testing for digital products.",
            },
        ],
        "Writing technical requirements": [
            {
                "name": "Client Needs and Software Requirements – University of Alberta",
                "url": "https://www.coursera.org/learn/software-requirements",
                "description": "Learn to elicit, analyse and document software requirements in agile and traditional projects.",
            },
        ],
        "Data analysis": [
            {
                "name": "Google Data Analytics Professional Certificate",
                "url": "https://www.coursera.org/professional-certificates/google-data-analytics",
                "description": "Build data literacy, clean and prepare data, and create dashboards and visualisations to communicate insights.",
            },
            {
                "name": "SQL for Data Science – University of California, Davis",
                "url": "https://www.coursera.org/learn/sql-for-data-science",
                "description": "Gain hands‑on experience with SQL queries, database design, data cleansing and analysis.",
            },
        ],
        "UX/UI design": [
            {
                "name": "Google UX Design Professional Certificate",
                "url": "https://www.coursera.org/professional-certificates/google-ux-design",
                "description": "Understand user research, design principles and prototyping for intuitive experiences.",
            },
        ],
        "Collaboration & leadership": [
            {
                "name": "High Performance Collaboration: Leadership, Teamwork, and Negotiation – Northwestern University",
                "url": "https://www.coursera.org/learn/leadership-collaboration",
                "description": "Develop negotiation, teamwork and leadership skills for high‑performance teams.",
            },
        ],
        "Empathy": [
            {
                "name": "Emotional Intelligence: Cultivating Immensely Human Interactions – University of Michigan",
                "url": "https://www.coursera.org/learn/emotional-intelligence",
                "description": "Cultivate empathy, communication and interpersonal skills to connect with users and colleagues.",
            },
        ],
        "Problem‑solving": [
            {
                "name": "Creative Problem Solving – University of Minnesota",
                "url": "https://www.coursera.org/learn/creative-problem-solving",
                "description": "Boost creative and critical thinking abilities and learn frameworks for innovative problem solving.",
            },
        ],
        # Additional skills for UX Researcher
        "Analytical thinking": [
            {
                "name": "Google Data Analytics Professional Certificate",
                "url": "https://www.coursera.org/professional-certificates/google-data-analytics",
                "description": "Develop analytical skills through data cleaning, analysis and visualisation projects.",
            },
        ],
        "Effective communication": [
            {
                "name": "High Performance Collaboration: Leadership, Teamwork, and Negotiation – Northwestern University",
                "url": "https://www.coursera.org/learn/leadership-collaboration",
                "description": "Learn to communicate effectively with stakeholders and negotiate in collaborative environments.",
            },
        ],
        "Curiosity": [
            {
                "name": "Creative Problem Solving – University of Minnesota",
                "url": "https://www.coursera.org/learn/creative-problem-solving",
                "description": "Build curiosity and innovative thinking through structured problem‑solving techniques.",
            },
        ],
        "Collaboration": [
            {
                "name": "High Performance Collaboration: Leadership, Teamwork, and Negotiation – Northwestern University",
                "url": "https://www.coursera.org/learn/leadership-collaboration",
                "description": "Gain collaboration and negotiation skills essential for working in cross‑functional teams.",
            },
        ],
        "Technical proficiency": [
            {
                "name": "Google UX Design Professional Certificate",
                "url": "https://www.coursera.org/professional-certificates/google-ux-design",
                "description": "Understand user research techniques, wireframing and prototyping tools for digital product design.",
            },
            {
                "name": "Client Needs and Software Requirements – University of Alberta",
                "url": "https://www.coursera.org/learn/software-requirements",
                "description": "Learn to identify and translate user needs into technical software requirements.",
            },
        ],
        # Additional skills for Product Analyst
        "Market research": [
            {
                "name": "Market Research and Consumer Behavior – IE University",
                "url": "https://www.coursera.org/learn/market-research",
                "description": "Master market analysis, survey design and consumer behaviour insights.",
            },
        ],
        "Product management tools": [
            {
                "name": "Strategic Management – Copenhagen Business School",
                "url": "https://www.coursera.org/learn/strategic-management",
                "description": "Understand strategic frameworks and tools used in product and business management.",
            },
            {
                "name": "Client Needs and Software Requirements – University of Alberta",
                "url": "https://www.coursera.org/learn/software-requirements",
                "description": "Learn to prioritise and manage product requirements using agile approaches.",
            },
        ],
        "UX design": [
            {
                "name": "Google UX Design Professional Certificate",
                "url": "https://www.coursera.org/professional-certificates/google-ux-design",
                "description": "Gain foundational knowledge in user research, design thinking, prototyping and usability testing.",
            },
        ],
        "A/B testing": [
            {
                "name": "Google Data Analytics Professional Certificate",
                "url": "https://www.coursera.org/professional-certificates/google-data-analytics",
                "description": "Learn to design experiments, perform A/B tests and interpret results using data analytics tools.",
            },
        ],
        "SQL & database knowledge": [
            {
                "name": "SQL for Data Science – University of California, Davis",
                "url": "https://www.coursera.org/learn/sql-for-data-science",
                "description": "Build fluency in SQL querying, database design and data wrangling for analysis.",
            },
        ],
        "Communication": [
            {
                "name": "High Performance Collaboration: Leadership, Teamwork, and Negotiation – Northwestern University",
                "url": "https://www.coursera.org/learn/leadership-collaboration",
                "description": "Develop communication and negotiation skills for managing stakeholders and teams.",
            },
        ],
        "Critical thinking": [
            {
                "name": "Creative Problem Solving – University of Minnesota",
                "url": "https://www.coursera.org/learn/creative-problem-solving",
                "description": "Sharpen critical thinking and reasoning through structured innovation methods.",
            },
        ],
        "Stakeholder management": [
            {
                "name": "High Performance Collaboration: Leadership, Teamwork, and Negotiation – Northwestern University",
                "url": "https://www.coursera.org/learn/leadership-collaboration",
                "description": "Learn to manage stakeholders, negotiate priorities and foster effective collaboration.",
            },
        ],
        "Teamwork & collaboration": [
            {
                "name": "High Performance Collaboration: Leadership, Teamwork, and Negotiation – Northwestern University",
                "url": "https://www.coursera.org/learn/leadership-collaboration",
                "description": "Build teamwork skills and understand group dynamics for successful project delivery.",
            },
        ],
        "Adaptability": [
            {
                "name": "Creative Problem Solving – University of Minnesota",
                "url": "https://www.coursera.org/learn/creative-problem-solving",
                "description": "Cultivate adaptability and flexibility to adjust to changing business contexts.",
            },
        ],
        "Attention to detail": [
            {
                "name": "SQL for Data Science – University of California, Davis",
                "url": "https://www.coursera.org/learn/sql-for-data-science",
                "description": "Practice detailed data querying and quality checks necessary for precise analysis.",
            },
        ],
    }


def main():
    st.set_page_config(page_title="Skill Gap & Course Recommendations", page_icon="🎯", layout="wide")
    st.title("Skill Gap Analysis & Course Recommendations")
    st.markdown(
        """
        Use this tool to understand which skills you may still need to develop for a particular career path, and discover
        relevant courses to fill those gaps.  Simply select a role and tick off the skills you already possess – the app
        will show you any missing skills and recommend courses that cover them.
        """
    )

    role_skills = get_role_skills()
    skill_courses = get_skill_courses()

    role = st.selectbox("Select your target role", ["(choose a role)"] + list(role_skills.keys()))

    if role and role != "(choose a role)":
        required_skills = role_skills[role]
        st.subheader(f"Required skills for {role}")
        st.write(
            "Below is a list of key skills for the selected role. Tick the ones you already possess in order to identify gaps."
        )
        user_skills = st.multiselect(
            "Select the skills you already have", options=required_skills, default=[]
        )
        missing = list(sorted(set(required_skills) - set(user_skills)))

        # Display results
        if user_skills:
            st.success(f"You selected {len(user_skills)} skill(s).")
        else:
            st.info("You have not selected any skills yet.")

        if missing:
            st.warning(f"Missing skills ({len(missing)}): {', '.join(missing)}")
            st.subheader("Recommended Courses")
            # Build a list of recommended courses for each missing skill
            for skill in missing:
                courses = skill_courses.get(skill, [])
                if courses:
                    with st.expander(f"Courses for '{skill}'"):
                        for course in courses:
                            name = course.get("name")
                            url = course.get("url")
                            desc = course.get("description")
                            st.markdown(f"- **{name}** – {desc}  ")
                            st.markdown(f"  [View Course]({url})")
                else:
                    st.info(f"No specific courses listed for {skill}.")
        else:
            if role:
                st.success(
                    "Congratulations! According to the selected skill set you have all the required skills for this role."
                )
    else:
        st.info("Please select a role to begin.")


if __name__ == "__main__":
    main()
