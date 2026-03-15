import streamlit as st

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer")

st.write("Deployment is working.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

job_desc = st.text_area("Paste Job Description")

if st.button("Analyze"):
    st.success("App working correctly!")
