import streamlit as st
import os
import time
from dotenv import load_dotenv
from utils.pdf_loader import extract_text
from utils.text_cleaner import clean_text
from utils.summarizer import configure_llm, generate_summary
from utils.risk_detector import detect_risks

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Legal Document Summarizer", page_icon="⚖️", layout="wide")

st.title("⚖️ Legal Document Summarizer & Risk Detector")
st.write("Upload a legal document (PDF, DOCX, or TXT) to get a professional summary and risk analysis.")

# Sidebar for Instructions
with st.sidebar:
    st.header("⚖️ Legal AI")
    st.write("### Instructions")
    st.write("1. Upload a contract or legal document.")
    st.write("2. Preview the extracted text.")
    st.write("3. Click 'Analyze Document' to get insights.")
    st.markdown("---")
    st.info("This tool uses AI to simplify complex legal documents into plain English.")

# Default model selection (moved from sidebar)
model_option = "gemini-2.5-flash-lite"

# Input Method Selection
input_method = st.radio("Choose Input Method:", ["Upload File", "Paste Text Manually"])

raw_text = ""

if input_method == "Upload File":
    uploaded_file = st.file_uploader("Choose a legal document", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        with st.spinner("📑 Extracting text from document..."):
            raw_text = extract_text(uploaded_file)
else:
    raw_text = st.text_area("Paste your legal document text here:", height=300, placeholder="Paste contract text...")

if raw_text:
    # 2. Clean Text
    with st.spinner("🧹 Cleaning and preparing text..."):
        cleaned_text = clean_text(raw_text)
    
    # 3. Preview
    st.subheader("📄 Document Content Preview")
    st.text_area("Content Preview:", cleaned_text[:2000] + ("..." if len(cleaned_text) > 2000 else ""), height=200)

    # Analysis Button
    if st.button("🔍 Analyze Document", use_container_width=True):
        if not raw_text.strip():
            st.error("Please upload a document or paste text first!")
        elif not os.getenv("GOOGLE_API_KEY"):
            st.error("API Key not found! Please set it in the .env file.")
        else:
            # Configure LLM
            model = configure_llm(model_option)
            if not model:
                st.error("Failed to configure LLM. Please check your API Key.")
            else:
                # Create two columns for Summary and Risk
                sum_col, risk_col = st.columns(2)
                
                with sum_col:
                    with st.spinner("📝 Generating summary..."):
                        summary = generate_summary(cleaned_text, model)
                        st.subheader("📌 Executive Summary")
                        st.markdown(summary)
                
                # Small delay to prevent API Quota limits (Free Tier)
                time.sleep(2)
                
                with risk_col:
                    with st.spinner("🚩 Detecting risks..."):
                        risks = detect_risks(cleaned_text, model)
                        st.subheader("🚩 Potential Risks")
                        st.markdown(risks)
else:
    st.info("👋 Welcome! Please upload a document or paste text to begin the analysis.")
