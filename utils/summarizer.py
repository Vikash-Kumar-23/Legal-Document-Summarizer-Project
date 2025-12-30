import google.generativeai as genai
import os
import time
from pathlib import Path

def get_prompt(prompt_name):
    """Load prompt template from file."""
    prompt_path = Path(__file__).parent.parent / "prompts" / f"{prompt_name}.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def configure_llm(model_name="gemini-flash-latest"):
    """Configure the Gemini LLM API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    
    if not model_name.startswith("models/"):
        model_full_path = f"models/{model_name}"
    else:
        model_full_path = model_name
        
    return genai.GenerativeModel(model_full_path)

from utils.chunker import chunk_text

def generate_summary(text, model):
    """Summarize legal document using LLM with chunking support."""
    prompt_template = get_prompt("summary_prompt")
    
    # 1. Chunk the text if it's too long (Increased chunk size to 15000 to reduce requests)
    chunks = chunk_text(text, chunk_size=15000, overlap=1000)
    
    def safe_generate(prompt_text, max_retries=3):
        """Helper to handle 429 errors with auto-retry."""
        for attempt in range(max_retries):
            try:
                return model.generate_content(prompt_text).text
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    time.sleep(10) # Wait 10 seconds before retrying
                    continue
                raise e

    if len(chunks) == 1:
        # Single chunk processing
        prompt = f"{prompt_template}\n\nDocument Text:\n{text}"
        try:
            return safe_generate(prompt)
        except Exception as e:
            return f"Error during summarization: {str(e)}"
    
    # 2. Multi-chunk processing
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        if i > 0:
            time.sleep(5) # 5 second gap between chunks
            
        chunk_prompt = f"Summarize this part of a legal document (Part {i+1}):\n\n{chunk}"
        try:
            summary_part = safe_generate(chunk_prompt)
            chunk_summaries.append(summary_part)
        except Exception as e:
            print(f"Error processing chunk {i+1}: {e}")
            
    # 3. Combine and generate final summary
    time.sleep(5)
    combined_text = "\n\n".join(chunk_summaries)
    final_prompt = f"{prompt_template}\n\nSummarized Parts:\n{combined_text}"
    
    try:
        return safe_generate(final_prompt)
    except Exception as e:
        return f"Error during final summarization: {str(e)}"
