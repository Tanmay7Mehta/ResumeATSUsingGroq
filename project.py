from dotenv import load_dotenv
import streamlit as st
import os
import fitz
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))