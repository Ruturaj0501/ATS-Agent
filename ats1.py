from io import BytesIO
from xhtml2pdf import pisa

def generate_pdf_button(content, filename="resume_analysis.pdf"):
    """
    Converts text/html content into a downloadable PDF button.
    """
    # Wrap text in basic HTML for PDF generation
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
            label="📥 Download Result as PDF",
            data=pdf_buffer,
            file_name=filename,
            mime="application/pdf"
        )