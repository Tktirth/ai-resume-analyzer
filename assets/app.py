import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("AI Resume Analyzer")
st.subheader("HR Resume Screening Dashboard")


# ---------------------------------------------------
# JOB DESCRIPTION
# ---------------------------------------------------

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


# ---------------------------------------------------
# SKILL DATABASE
# ---------------------------------------------------

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


# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])


# ---------------------------------------------------
# EXTRACT TEXT FROM PDF
# ---------------------------------------------------

def extract_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text.lower()


# ---------------------------------------------------
# SKILL EXTRACTION
# ---------------------------------------------------

def extract_skills(text):

    found = []

    for skill in skills_db:

        if skill in text:
            found.append(skill)

    return found


# ---------------------------------------------------
# ATS SCORE
# ---------------------------------------------------

def ats_similarity(resume, job):

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform([resume, job])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(score * 100)


# ---------------------------------------------------
# RESUME SECTION ANALYSIS
# ---------------------------------------------------

def section_analysis(text):

    sections = {

        "Skills":"skills",
        "Projects":"projects",
        "Experience":"experience",
        "Education":"education",
        "Certifications":"certifications"

    }

    results = {}

    for name, keyword in sections.items():

        if keyword in text:
            results[name] = 1
        else:
            results[name] = 0

    return results


# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button("Analyze Resume"):

    if uploaded_file is None:

        st.warning("Please upload a resume first.")
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


# ---------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("ATS Score", f"{ats_score}%")

    col2.metric("Matched Skills", len(matched))

    col3.metric("Missing Skills", len(missing))


# ---------------------------------------------------
# SKILL MATCH PROGRESS BARS
# ---------------------------------------------------

    st.subheader("Skill Match Dashboard")

    for skill in jd_skills:

        if skill in resume_skills:

            st.progress(1.0, text=f"{skill} ✓")

        else:

            st.progress(0.2, text=f"{skill} Missing")


# ---------------------------------------------------
# RESUME SECTION STATUS
# ---------------------------------------------------

    st.subheader("Resume Structure Analysis")

    cols = st.columns(5)

    names = list(sections.keys())

    values = list(sections.values())

    for i in range(len(names)):

        if values[i] == 1:

            cols[i].success(names[i])

        else:

            cols[i].error(names[i])


# ---------------------------------------------------
# IMPROVEMENT SUGGESTIONS
# ---------------------------------------------------

    st.subheader("Improvement Suggestions")

    improvements = []

    if ats_score < 60:
        improvements.append("Increase keyword alignment with the job description.")

    if missing:
        improvements.append("Add missing skills such as: " + ", ".join(missing[:5]))

    if sections["Projects"] == 0:
        improvements.append("Add AI/ML projects with GitHub links.")

    if sections["Experience"] == 0:
        improvements.append("Include internship or relevant work experience.")

    if sections["Certifications"] == 0:
        improvements.append("Add relevant certifications.")

    if improvements:

        for item in improvements:
            st.warning(item)

    else:

        st.success("Your resume is well aligned with the role.")


# ---------------------------------------------------
# HR RECOMMENDATION
# ---------------------------------------------------

    st.subheader("Hiring Recommendation")

    if ats_score > 70:

        st.success("Strong Candidate")

    elif ats_score > 40:

        st.info("Moderate Candidate")

    else:

        st.error("Needs Improvement")


# ---------------------------------------------------
# GRAPH 1 SKILL GAP
# ---------------------------------------------------

    st.subheader("Skill Gap Graph")

    labels = ["Matched Skills","Missing Skills"]

    values = [len(matched), len(missing)]

    fig, ax = plt.subplots()

    ax.bar(labels, values)

    ax.set_ylabel("Skill Count")

    ax.set_title("Skill Gap Analysis")

    st.pyplot(fig)


# ---------------------------------------------------
# GRAPH 2 ATS SCORE
# ---------------------------------------------------

    st.subheader("ATS Score Visualization")

    fig2, ax2 = plt.subplots()

    ax2.barh(["ATS Score"], [ats_score])

    ax2.set_xlim(0,100)

    ax2.set_title("Resume Alignment")

    st.pyplot(fig2)


# ---------------------------------------------------
# GRAPH 3 RESUME SECTION COVERAGE
# ---------------------------------------------------

    st.subheader("Resume Section Coverage")

    fig3, ax3 = plt.subplots()

    ax3.bar(names, values)

    ax3.set_ylim(0,1)

    ax3.set_title("Resume Structure")

    st.pyplot(fig3)


# ---------------------------------------------------
# GRAPH 4 RESUME READINESS
# ---------------------------------------------------

    st.subheader("Resume Readiness")

    issues = len(improvements)

    good = max(1, 5 - issues)

    sizes = [good, issues]

    labels = ["Good Areas","Needs Improvement"]

    fig4, ax4 = plt.subplots()

    ax4.pie(sizes, labels=labels, autopct="%1.1f%%")

    ax4.set_title("Overall Resume Readiness")

    st.pyplot(fig4)
