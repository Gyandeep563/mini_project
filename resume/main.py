import streamlit as st
import PyPDF2
import io
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq


# # database 
# from database import (
#     create_database,
#     save_resume,
#     get_all_resume,
#     get_resume
# )

# create_database()

with open("prompt.txt", "r", encoding="utf-8") as file:
    prompt_template = file.read()

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

# page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📃",
    layout="centered"
)

st.title("📃AI Resume Analyzer 📃")
st.markdown("Upload your resume and get AI-powered feedback.")


# GROQAI_API_KEY
GROQAI_API_KEY  = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


uploaded_file = st.file_uploader(
    "Upload your resume (PDF or TXT)",
    type=["pdf", "txt"]
)
# pdf_data=uploaded_file.getvalue()
# Job role
job_role = st.text_input(
    "Enter the job role that you are targeting"
)

analyze = st.button("Analyze Resume")


#text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text

#  extract text from PDF or TXT
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(
            io.BytesIO(uploaded_file.read())
        )
    else:
        return uploaded_file.read().decode("utf-8")

# Analyze resume
if analyze and uploaded_file:
    try:
        # Check API key
        if not GROQAI_API_KEY:
            st.error("OpenAI API key not found. Please check your .env file.")
            st.stop()
        # Extract resume content
        file_content = extract_text_from_file(uploaded_file)
        if not file_content.strip():
            st.error("File does not have any readable content.")
            st.stop()
        prompt = (
                prompt_template
                .replace("{job_role}", job_role or "General Job Application")
                .replace("{file_content}", file_content)
)

        client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
        response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "user", "content": prompt_template.format(
            job_role=job_role,
            file_content=file_content
        )}
    ],
    reasoning_effort="low",
    max_completion_tokens=6000,
    temperature=0.2
)
        # Display results
        st.markdown("### Analysis Results")
        
        analysis=response.choices[0].message.content
        st.markdown(analysis)

# save in databases
        # if analysis:
        #     save_resume(
        #         candidate_name="Not Extracted",
        #         filename=uploaded_file.name,
        #         job_role=job_role,
        #         pdf_data=pdf_data,
        #         analysis=analysis
        #     )

        #     st.success("Resume and analysis saved successfully!")
    except Exception as e:
        st.error(f"AN ERROR OCCURRED: {str(e)}")
elif analyze and not uploaded_file:
    st.warning("Please upload your resume first.")


# =======================
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0e1117;
            color: #ffffff;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            z-index: 999;
        }

        .footer span {
            color: #ff4b4b;
            font-weight: bold;
        }
    </style>

    <div class="footer">
        Made   By Gyan  & ALok
    </div>
""", unsafe_allow_html=True)