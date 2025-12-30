# ⚖️ Legal Document Summarizer & Risk Detector

An AI-powered application designed to help users quickly understand complex legal documents and identify potential risks. Built with **Streamlit** and **Google Gemini LLM**.

## 🚀 Features
- **Multi-Format Support**: Upload PDF, DOCX, or TXT legal documents.
- **AI Summarization**: Get a professional executive summary focusing on key parties, obligations, and dates.
- **Risk Detection**: Automatically identify potential liabilities, unfavorable clauses, and hidden risks.
- **Modular Architecture**: Clean code structure with separated utilities and prompt templates.

## 📂 Project Structure
```text
legal_document_summarizer/
│
├── app.py                # Main Streamlit application
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables (API Key)
│
├── utils/                # Modular logic components
│   ├── pdf_loader.py     # Text extraction logic
│   ├── text_cleaner.py   # Text preprocessing
│   ├── chunker.py        # Logic for handling long documents
│   ├── summarizer.py     # LLM summary generation
│   └── risk_detector.py  # LLM risk analysis logic
│
├── prompts/              # Prompt engineering templates
│   ├── summary_prompt.txt # Template for document summary
│   └── risk_prompt.txt    # Template for risk detection
│
├── data/                 # Data storage
│   └── sample_contracts/ # Folder for testing sample documents
│
└── README.md             # Project documentation
```

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
cd legal_document_summarizer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_actual_key_here
   ```

### 4. Run the Application
```bash
python -m streamlit run app.py
```

## 📝 Usage
1. Open the application in your browser (usually `http://localhost:8501`).
2. Upload a legal document.
3. Review the text preview to ensure extraction was successful.
4. Click **Analyze Document** to generate both a summary and a risk report.

## ⚖️ Disclaimer
*This tool is for informational purposes only and does not constitute legal advice. Always consult with a qualified legal professional before signing any contract.*
