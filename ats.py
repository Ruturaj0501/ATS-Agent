import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai
import io
import base64

from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash-latest')
    response=model.generate_content([input,pdf_content,prompt])
    return response.text

def input_pdf(file):
    if file is not None:
        reader=pdf.PdfReader(file)
        text=""
        for page in reader.pages:
            text+=page.extract_text()
        return text
    

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Resume Expert")
input_text=st.text_area("Job Description:",key="input_text")
file=st.file_uploader("Upload Resume", type=["pdf"])

if file is not None:
    st.write("PDF file uploaded successfully!")

submit1=st.button("Tell me about this resume")
submit2=st.button("How can i improve this resume?")
submit3=st.button("Percentage match")

prompt1="You are an ATS expert. Please analyze the resume and provide a detailed analysis of the resume in relation to the job description provided. Include any relevant information that would be useful for the user.Also highlight its strength and weakness"
prompt2="You are HR expert. Please analyze the resume and provide a detailed analysis of the resume in relation to the job description provided. Include any relevant information that would be useful for the user tell how can he improve resume. Also highlight its strength and weakness"
prompt3="You are an ATS expert. Tell the percentage match with the job description and how can he enchance his profile"

if submit1:
    if file is not None:
        pdf_content=input_pdf(file)
        response=get_response(prompt1,pdf_content,input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please upload a PDF file")

if submit2:
    if file is not None:
        pdf_content=input_pdf(file)
        response=get_response(prompt2,pdf_content,input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please upload a PDF file")

if submit3:
    if file is not None:
        pdf_content=input_pdf(file)
        response=get_response(prompt3,pdf_content,input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please upload a PDF file")

