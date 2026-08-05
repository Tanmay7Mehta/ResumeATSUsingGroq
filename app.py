from dotenv import load_dotenv
import streamlit as st
import base64
import os
import io
import fitz  # PyMuPDF - no system dependencies needed
from google import genai
from google.genai import types

load_dotenv()  # loads GOOGLE_API_KEY from .env file
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, pdf_content, job_desc):
    image_part = types.Part.from_bytes(
        data=base64.b64decode(pdf_content[0]["data"]),
        mime_type="image/jpeg"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[input_prompt, image_part, job_desc]
    )
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open PDF from bytes using PyMuPDF (no poppler needed)
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document[0]
        pix = first_page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("jpeg")

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_bytes).decode()
            }
        ]
        return pdf_parts
        
    else:
        return FileNotFoundError("No file uploaded")

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
#submit2 = st.button("How Can I Improvise my Skills")
#submit3 = st.button("What are the Keywords that are missing")
submit3 = st.button("Percentage matches")

input_prompt1 = """
You are an experinced HR with tech experience in the field of any one job role from Data Science, Full stack Web developement, Big Data Engineering, DEVOPS,
Data Analyst, your task is to review the provided resume against the job description for rhese profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the application in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Application Tracking System) scanner with deep understanding of any one job role Data Science, Full stack Web developement, Big Data Engineering,
DEVOPS, Data Analyst and deep ATS dunctionality, your task is to evaluate the resume agains the provided job description. Give me the perecentage of 
match if the resume matches the job descroption. First the output should come as percentage and then keywords missing and last final thought.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Respose is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Respose is")
        st.write(response)
    else:
        st.write("Please upload the resume")