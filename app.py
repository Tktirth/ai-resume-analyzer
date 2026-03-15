import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("AI Resume Analyzer")
st.subheader("HR Style Resume Screening System")


# -------------------------
# JOB DESCRIPTION
# -------------------------

JOB_DESCRIPTION = """
Junior AI/ML Engineer

Required Skills:
Python
Machine Learning
Deep Learning
TensorFlow
PyTorch
Pandas
NumPy
Docker
AWS
Linux
Git
Data Analysis
"""

jd_text = JOB_DESCRIPTION.lower()


# -------------------------
# SKILL DATABASE
# -------------------------

skills_db = [

"python","java","c++","javascript","sql",

"machine learning","deep learning","nlp",
"tensorflow","pytorch","scikit learn",

"data analysis","pandas","numpy",
"statistics","data visualization",

"cyber security","network security",
"ethical hacking",

"docker","kubernetes","aws","linux",

"flask","fastapi","react","node",

"git","github","power bi","tableau"

]


# -------------------------
# UPLOAD RESUME
# -------------------------

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])


# -------------------------
# EXTRACT TEXT
# -------------------------

def extract_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            content = page.extract_text()

            if content:
                text += content

    return text.lower()


# -------------------------
# EXTRACT SKILLS
# -------------------------

def extract_skills(text):

    found = []

    for skill in skills_db:

        if skill in text:
            found.append(skill)

    return found


# -------------------------
# ATS SCORE
# -------------------------

def ats_similarity(resume, jd):

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform([resume, jd])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(score * 100)


# -------------------------
# RESUME SECTION CHECK
# -------------------------

def section_analysis(text):

    sections = {

        "Skills":"skills",
        "Projects":"projects",
        "Experience":"experience",
        "Education":"education",
        "Certifications":"certifications"

    }

    result = {}

    for name, keyword in sections.items():

        if keyword in text:
            result[name] = 1
        else:
            result[name] = 0

    return result


# -------------------------
# ANALYZE
# -------------------------

if st.button("Analyze Resume"):

    if uploaded_file is None:

        st.warning("Upload a resume first")
        st.stop()


    with st.spinner("Analyzing resume..."):

        resume_text = extract_text(uploaded_file)

        resume_skills = extract_skills(resume_text)

        jd_skills = extract_skills(jd_text)

        matched = list(set(resume_skills) & set(jd_skills))

        missing = list(set(jd_skills) - set(resume_skills))

        ats_score = ats_similarity(resume_text, jd_text)

        sections = section_analysis(resume_text)


    st.success("Analysis Complete")


# -------------------------
# DASHBOARD METRICS
# -------------------------

    col1,col2,col3 = st.columns(3)

    col1.metric("ATS Score", f"{ats_score}%")

    col2.metric("Matched Skills", len(matched))

    col3.metric("Missing Skills", len(missing))


# -------------------------
# SKILL ANALYSIS
# -------------------------

    st.subheader("Matched Skills")

    st.write(matched if matched else "No matched skills")


    st.subheader("Missing Skills")

    st.write(missing if missing else "No missing skills")


# -------------------------
# SECTION ANALYSIS
# -------------------------

    st.subheader("Resume Sections")

    section_names = list(sections.keys())

    section_values = list(sections.values())

    st.write(sections)


# -------------------------
# IMPROVEMENT ENGINE
# -------------------------

    st.subheader("Resume Improvement Suggestions")

    improvements = []


    if ats_score < 60:
        improvements.append("Improve keyword alignment with job description")


    if missing:
        improvements.append("Add missing skills if you have experience")


    if sections["Projects"] == 0:
        improvements.append("Add AI/ML projects with GitHub links")


    if sections["Experience"] == 0:
        improvements.append("Add internship or relevant work experience")


    if sections["Certifications"] == 0:
        improvements.append("Add relevant certifications (AWS, ML, etc)")


    if improvements:

        for item in improvements:
            st.write("•", item)

    else:
        st.write("Resume looks strong for this role")


# -------------------------
# HIRING DECISION
# -------------------------

    st.subheader("HR Recommendation")

    if ats_score > 70:
        st.success("Strong Candidate")

    elif ats_score > 45:
        st.info("Moderate Candidate")

    else:
        st.error("Needs Improvement")


# -------------------------
# GRAPH 1 SKILL GAP
# -------------------------

    st.subheader("Skill Gap Graph")

    labels = ["Matched Skills","Missing Skills"]

    values = [len(matched),len(missing)]

    fig,ax = plt.subplots()

    ax.bar(labels,values)

    ax.set_title("Skill Gap")

    ax.set_ylabel("Number of Skills")

    st.pyplot(fig)


# -------------------------
# GRAPH 2 ATS SCORE
# -------------------------

    st.subheader("ATS Score Visualization")

    fig2,ax2 = plt.subplots()

    ax2.barh(["ATS Score"],[ats_score])

    ax2.set_xlim(0,100)

    ax2.set_title("Resume Alignment")

    st.pyplot(fig2)


# -------------------------
# GRAPH 3 SECTION COVERAGE
# -------------------------

    st.subheader("Resume Section Coverage")

    fig3,ax3 = plt.subplots()

    ax3.bar(section_names,section_values)

    ax3.set_ylim(0,1)

    ax3.set_title("Resume Structure")

    st.pyplot(fig3)


# -------------------------
# GRAPH 4 IMPROVEMENT PRIORITY
# -------------------------

    st.subheader("Improvement Priority")

    issues = len(improvements)

    good = 5 - issues

    sizes = [good,issues]

    labels = ["Good Areas","Needs Improvement"]

    fig4,ax4 = plt.subplots()

    ax4.pie(sizes,labels=labels,autopct="%1.1f%%")

    ax4.set_title("Resume Readiness")

    st.pyplot(fig4)
