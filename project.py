from dotenv import load_dotenv
import streamlit as st
import os
import fitz
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def gret_response(input_propmt, resume_text, job_des):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": input_propmt + "\n\n Resume Content:\n" + resume_text + "\n\n Job Description:\n" + job_des
            }
        ],
        max_tokens=2048
    )
    return response.choice[0].message.content

def extract_pdf_text(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text +=page.get_text()
        return text
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me aboout the resume")
submit2 = st.button("Percentage match")