import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("AI Resume Analyzer")


uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

job_desc = st.text_area("Paste Job Description")


def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            content = page.extract_text()

            if content:
                text += content

    return text.lower()



skills_db = [

"python","machine learning","deep learning","nlp","tensorflow","pytorch",
"data analysis","sql","pandas","numpy","scikit learn",
"cyber security","network security","linux",
"docker","kubernetes","aws",
"flask","fastapi",
"data visualization","statistics","power bi","tableau"

]



def extract_skills(text):

    skills_found = []

    for skill in skills_db:

        if skill in text:
            skills_found.append(skill)

    return skills_found



def semantic_similarity(resume, jd):

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform([resume, jd])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(similarity * 100)



if st.button("Analyze Resume"):


    if uploaded_file is None or job_desc == "":

        st.warning("Please upload resume and paste job description")

        st.stop()


    with st.spinner("Analyzing resume..."):


        resume_text = extract_text(uploaded_file)

        jd_text = job_desc.lower()


        resume_skills = extract_skills(resume_text)

        jd_skills = extract_skills(jd_text)


        matched = list(set(resume_skills) & set(jd_skills))

        missing = list(set(jd_skills) - set(resume_skills))


        ats_score = semantic_similarity(resume_text, jd_text)



    st.success("Analysis Complete")


    col1, col2 = st.columns(2)


    with col1:

        st.metric("ATS Similarity Score", f"{ats_score}%")


    with col2:

        st.metric("Skills Matched", len(matched))



    st.subheader("Matched Skills")

    st.write(matched)



    st.subheader("Missing Skills")

    st.write(missing)



    st.subheader("Resume Suggestions")


    suggestions = []


    if ats_score < 50:
        suggestions.append("Your resume is poorly aligned with the job description.")


    if missing:
        suggestions.append("Add missing skills if you have experience with them.")


    if "projects" not in resume_text:
        suggestions.append("Add a projects section demonstrating real work.")


    if "experience" not in resume_text:
        suggestions.append("Add quantified work experience.")


    if suggestions:

        for s in suggestions:

            st.write("•", s)

    else:

        st.write("Your resume is well aligned with the job role.")



# -----------------------------
# VISUAL ANALYTICS SECTION
# -----------------------------


    st.subheader("Skill Gap Analysis")


    labels = ["Matched Skills", "Missing Skills"]

    values = [len(matched), len(missing)]


    fig, ax = plt.subplots()

    ax.bar(labels, values)

    ax.set_ylabel("Number of Skills")

    ax.set_title("Skill Match Analysis")


    st.pyplot(fig)



    st.subheader("ATS Score Visualization")


    fig2, ax2 = plt.subplots()

    ax2.barh(["ATS Score"], [ats_score])

    ax2.set_xlim(0,100)

    ax2.set_xlabel("Score Percentage")


    st.pyplot(fig2)



    st.subheader("Resume Skill Coverage")


    labels = ["Matched", "Missing"]

    sizes = [len(matched), len(missing)]


    fig3, ax3 = plt.subplots()

    ax3.pie(sizes, labels=labels, autopct="%1.1f%%")

    ax3.set_title("Resume Coverage vs Job Requirements")


    st.pyplot(fig3)
