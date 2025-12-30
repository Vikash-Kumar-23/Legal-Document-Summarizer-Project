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
    
    # 1. Chunk the text if it's too long
    chunks = chunk_text(text, chunk_size=8000, overlap=500)
    
    if len(chunks) == 1:
        # Single chunk processing
        prompt = f"{prompt_template}\n\nDocument Text:\n{text}"
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error during summarization: {str(e)}"
    
    # 2. Multi-chunk processing
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        # Small delay to respect free tier RPM limits
        if i > 0:
            time.sleep(1.5)
            
        chunk_prompt = f"Summarize this part of a legal document (Part {i+1}):\n\n{chunk}"
        try:
            response = model.generate_content(chunk_prompt)
            chunk_summaries.append(response.text)
        except Exception as e:
            print(f"Error processing chunk {i+1}: {e}")
            
    # 3. Combine and generate final summary
    # Final delay before the merge call
    time.sleep(1.5)
    combined_text = "\n\n".join(chunk_summaries)
    final_prompt = f"{prompt_template}\n\nSummarized Parts:\n{combined_text}"
    
    try:
        final_response = model.generate_content(final_prompt)
        return final_response.text
    except Exception as e:
        return f"Error during final summarization: {str(e)}"
