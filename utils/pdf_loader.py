import pdfplumber
import docx2txt
import io

def extract_text(uploaded_file):
    """Extract text from PDF, DOCX, or TXT file."""
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    if file_extension == "pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                # extract_text() with default settings
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    elif file_extension == "docx":
        return docx2txt.process(uploaded_file)
    elif file_extension == "txt":
        return uploaded_file.read().decode("utf-8")
    return ""
