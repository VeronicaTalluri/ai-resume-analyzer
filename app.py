import streamlit as st
import openai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume Analyzer")
st.markdown("**Upload your resume and paste a job description — AI will analyze your match instantly.**")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Upload PDF resume", type=["pdf"])
    resume_text = ""
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text()
        st.success("✅ Resume uploaded successfully!")
        with st.expander("Preview Resume Text"):
            st.write(resume_text[:1000] + "...")

with col2:
    st.subheader("💼 Paste Job Description")
    job_description = st.text_area(
        "Paste the full job description here",
        height=250,
        placeholder="Paste the job description you are applying for..."
    )

st.markdown("---")

if st.button("🚀 Analyze My Resume", use_container_width=True):
    if not resume_text:
        st.error("❌ Please upload your resume first.")
    elif not job_description:
        st.error("❌ Please paste a job description.")
    elif not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_api_key_here":
        st.error("❌ Please add your OpenAI API key in the .env file.")
    else:
        with st.spinner("🤖 AI is analyzing your resume..."):
            prompt = f"""
You are an expert resume reviewer and ATS specialist. Analyze the resume against the job description below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide a detailed analysis in the following format:

## 📊 Match Score
Give a match score out of 100 and explain why.

## ✅ Strengths
List 3-5 things from the resume that strongly match the job description.

## ❌ Missing Keywords
List the important keywords and skills from the job description that are missing from the resume.

## 💡 Bullet Point Improvements
Rewrite 3 weak bullet points from the resume using: Action Verb + Task + Measurable Result format.

## 🎯 Overall Recommendation
Give 3 specific action items the candidate should take to improve their chances.
"""
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert ATS resume analyzer and career coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            analysis = response.choices[0].message.content

        st.markdown("## 📋 Analysis Results")
        st.markdown(analysis)

        st.download_button(
            label="📥 Download Analysis",
            data=analysis,
            file_name="resume_analysis.txt",
            mime="text/plain"
        )

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Built by Veronica Talluri | "
    "<a href='https://linkedin.com/in/veronicatalluri'>LinkedIn</a> | "
    "<a href='https://github.com/VeronicaTalluri'>GitHub</a></p>",
    unsafe_allow_html=True
)