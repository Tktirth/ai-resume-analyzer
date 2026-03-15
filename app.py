import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# Streamlit Page Config
# -----------------------------

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("AI Resume Analyzer")
st.markdown("HR-style resume screening system")


# -----------------------------
# Predefined Job Description
# -----------------------------

JOB_DESCRIPTION = """
We are hiring a Junior AI/ML Engineer.

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


# -----------------------------
# Upload Resume
# -----------------------------

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])


# -----------------------------
# Skill Database
# -----------------------------

skills_db = [

# programming
"python","java","c++","javascript","sql",

# ai/ml
"machine learning","deep learning","nlp","tensorflow","pytorch","scikit learn",

# data
"data analysis","pandas","numpy","statistics","data visualization",

# cybersecurity
"cyber security","network security","ethical hacking","penetration testing",

# cloud/devops
"docker","kubernetes","aws","linux",

# web
"flask","fastapi","react","node",

# tools
"git","github","power bi","tableau"

]


# -----------------------------
# Extract Text From PDF
# -----------------------------

def extract_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text.lower()


# -----------------------------
# Extract Skills
# -----------------------------

def extract_skills(text):

    found = []

    for skill in skills_db:

        if skill in text:
            found.append(skill)

    return found


# -----------------------------
# ATS Similarity Score
# -----------------------------

def ats_score(resume, job):

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform([resume, job])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(score * 100)


# -----------------------------
# Resume Section Analysis
# -----------------------------

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
            results[name] = "Present"
        else:
            results[name] = "Missing"

    return results


# -----------------------------
# Analyze Button
# -----------------------------

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

        similarity = ats_score(resume_text, jd_text)

        sections = section_analysis(resume_text)


    st.success("Analysis Complete")


# -----------------------------
# Metrics Dashboard
# -----------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ATS Score", f"{similarity}%")

    with col2:
        st.metric("Matched Skills", len(matched))

    with col3:
        st.metric("Missing Skills", len(missing))


# -----------------------------
# Skills Display
# -----------------------------

    st.subheader("Matched Skills")

    if matched:
        st.write(matched)
    else:
        st.write("No matching skills found.")


    st.subheader("Missing Skills")

    if missing:
        st.write(missing)
    else:
        st.write("No missing skills.")


# -----------------------------
# Resume Sections
# -----------------------------

    st.subheader("Resume Section Analysis")

    st.write(sections)


# -----------------------------
# HR Feedback
# -----------------------------

    st.subheader("HR Feedback")

    feedback = []

    if similarity < 40:
        feedback.append("Resume poorly aligned with job description.")

    if missing:
        feedback.append("Add missing skills relevant to the role.")

    if sections["Projects"] == "Missing":
        feedback.append("Include real AI/ML projects.")

    if sections["Experience"] == "Missing":
        feedback.append("Add relevant work or internship experience.")

    if feedback:
        for f in feedback:
            st.write("•", f)
    else:
        st.write("Resume is well aligned with job requirements.")


# -----------------------------
# Hiring Recommendation
# -----------------------------

    st.subheader("Hiring Recommendation")

    if similarity > 70:
        st.success("Strong Candidate")

    elif similarity > 40:
        st.info("Moderate Candidate")

    else:
        st.error("Not Ready for Role")


# -----------------------------
# Visualization: Skill Gap
# -----------------------------

    st.subheader("Skill Gap Analysis")

    labels = ["Matched", "Missing"]

    values = [len(matched), len(missing)]

    fig, ax = plt.subplots()

    ax.bar(labels, values)

    ax.set_ylabel("Skill Count")

    ax.set_title("Skill Match vs Missing")

    st.pyplot(fig)


# -----------------------------
# Visualization: ATS Score
# -----------------------------

    st.subheader("ATS Score Visualization")

    fig2, ax2 = plt.subplots()

    ax2.barh(["ATS Score"], [similarity])

    ax2.set_xlim(0,100)

    ax2.set_xlabel("Score")

    st.pyplot(fig2)


# -----------------------------
# Resume Skill Coverage
# -----------------------------

    st.subheader("Resume Coverage")

    sizes = [len(matched), len(missing)]

    if sum(sizes) == 0:

        st.warning("No skills detected in resume.")

    else:

        fig3, ax3 = plt.subplots()

        ax3.pie(sizes, labels=["Matched","Missing"], autopct="%1.1f%%")

        ax3.set_title("Skill Coverage")

        st.pyplot(fig3)
