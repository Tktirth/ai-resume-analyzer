import streamlit as st
import pdfplumber

st.set_page_config(page_title="AI Resume Analyzer")

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
    return text

if st.button("Analyze"):

    if uploaded_file is None or job_desc == "":
        st.warning("Please upload resume and job description")
    else:

        with st.spinner("Analyzing resume..."):

            resume_text = extract_text(uploaded_file)

            # Temporary similarity logic
            resume_words = set(resume_text.lower().split())
            jd_words = set(job_desc.lower().split())

            match_score = len(resume_words & jd_words) / len(jd_words)

            st.success("Analysis Complete")

            st.metric("Match Score", f"{round(match_score*100)}%")

            st.subheader("Matched Keywords")
            st.write(list(resume_words & jd_words))
