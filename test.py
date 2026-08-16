from dotenv import load_dotenv
import streamlit as st
import os
import fitz
from gorq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_response(input_prompt, resume_text, job_des):
    response = client.chat.completions.create(
        model = "llams-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": input_prompt + "\n\nResume Content:\n" + resume_text + "\n\nJob Description:\n" + job_des
            }
        ],
        max_token = 2048
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
