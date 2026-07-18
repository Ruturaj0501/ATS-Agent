import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai
from io import BytesIO
from xhtml2pdf import pisa
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf(file):
    if file is not None:
        reader = pdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def generate_pdf_button(content, filename="Advanced_ATS_Resume.pdf"):
    html_template = f"""
    <html>
        <body style="font-family: Arial; font-size: 12px; line-height: 1.5;">
            <div style="padding: 20px;">
                {content.replace(chr(10), '<br/>')}
            </div>
        </body>
    </html>
    """
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html_template, dest=pdf_buffer)
    if not pisa_status.err:
        pdf_buffer.seek(0)
        st.download_button(
            label="📥 Download Advanced Resume as PDF",
            data=pdf_buffer,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Resume Expert")
input_text = st.text_area("Job Description:", key="input_text")
file = st.file_uploader("Upload Resume", type=["pdf"])

if "show_upgrade_option" not in st.session_state:
    st.session_state.show_upgrade_option = False
if "advanced_resume" not in st.session_state:
    st.session_state.advanced_resume = None
if "pdf_content" not in st.session_state:
    st.session_state.pdf_content = None

if file is not None:
    st.write("PDF file uploaded successfully!")
    st.session_state.pdf_content = input_pdf(file)

submit1 = st.button("Tell me about this resume")
submit2 = st.button("How can i improve this resume?")
submit3 = st.button("Percentage match")

prompt1 = "You are an ATS expert. Please analyze the resume and provide a detailed analysis of the resume in relation to the job description provided. Include any relevant information that would be useful for the user.Also highlight its strength and weakness"
prompt2 = "You are HR expert. Please analyze the resume and provide a detailed analysis of the resume in relation to the job description provided. Include any relevant information that would be useful for the user tell how can he improve resume. Also highlight its strength and weakness"
prompt3 = "You are an ATS expert. Tell the percentage match with the job description and how can he enchance his profile"
prompt_advance = "You are an elite executive resume writer and ATS specialist. Take the provided resume text and rewrite it to perfectly target the provided job description. Optimize bullet points using the X-Y-Z formula (Accomplished X, measured by Y, by doing Z), integrate strong action verbs, embed critical ATS keywords from the job description naturally, and structure the output clearly into professional sections: Summary, Core Competencies, Professional Experience, Projects, and Education. Do not include introductory conversational text, only output the rewritten professional resume."

if submit1:
    if file is not None:
        response = get_response(prompt1, st.session_state.pdf_content, input_text)
        st.subheader("Response:")
        st.write(response)
        st.session_state.show_upgrade_option = True
        st.session_state.advanced_resume = None
    else:
        st.error("Please upload a PDF file")

if submit2:
    if file is not None:
        response = get_response(prompt2, st.session_state.pdf_content, input_text)
        st.subheader("Response:")
        st.write(response)
        st.session_state.show_upgrade_option = True
        st.session_state.advanced_resume = None
    else:
        st.error("Please upload a PDF file")

if submit3:
    if file is not None:
        response = get_response(prompt3, st.session_state.pdf_content, input_text)
        st.subheader("Response:")
        st.write(response)
        st.session_state.show_upgrade_option = True
        st.session_state.advanced_resume = None
    else:
        st.error("Please upload a PDF file")

if st.session_state.show_upgrade_option and file is not None:
    st.markdown("---")
    st.subheader("🚀 Next Step: Upgrade Your Resume")
    st.write("Would you like AI to completely rewrite your resume into an advanced, ATS-optimized version tailored to this job description?")
    
    if st.button("Create Advanced ATS Resume"):
        with st.spinner("Rewriting your resume into an executive-level ATS format..."):
            st.session_state.advanced_resume = get_response(prompt_advance, st.session_state.pdf_content, input_text)
    
    if st.session_state.advanced_resume:
        st.subheader("✨ Advanced ATS-Optimized Resume:")
        st.write(st.session_state.advanced_resume)
        generate_pdf_button(st.session_state.advanced_resume, "Advanced_ATS_Resume.pdf")
