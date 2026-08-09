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