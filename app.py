from dotenv import load_dotenv
import streamlit as st
import os
import fitz
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_response(input_prompt, resume_text, job_desc):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": input_prompt + "\n\nResume Content:\n" + resume_text + "\n\nJob Description:\n" + job_desc
            }
        ],
        max_tokens=2048
    )
    return response.choices[0].message.content

def extract_pdf_text(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        return text
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage matches")

input_prompt1 = """
You are an experinced HR with tech experience in the field of any one job role from Data Science, Full stack Web developement, Big Data Engineering, DEVOPS,
Data Analyst, your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the application in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Application Tracking System) scanner with deep understanding of any one job role Data Science, Full stack Web developement, Big Data Engineering,
DEVOPS, Data Analyst and deep ATS functionality, your task is to evaluate the resume against the provided job description. Give me the percentage of 
match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thought.
"""

if submit1:
    if uploaded_file is not None:
        resume_text = extract_pdf_text(uploaded_file)
        response = get_response(input_prompt1, resume_text, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        resume_text = extract_pdf_text(uploaded_file)
        response = get_response(input_prompt3, resume_text, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")