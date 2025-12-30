import time
from utils.chunker import chunk_text
from utils.summarizer import get_prompt

def detect_risks(text, model):
    """Detect legal risks in document using LLM and template with chunking support."""
    prompt_template = get_prompt("risk_prompt")
    
    # 1. Chunk the text if it's too long
    chunks = chunk_text(text, chunk_size=8000, overlap=500)
    
    if len(chunks) == 1:
        # Single chunk processing
        prompt = f"{prompt_template}\n\nDocument Text:\n{text}"
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error during risk detection: {str(e)}"
    
    # 2. Multi-chunk processing
    chunk_risks = []
    for i, chunk in enumerate(chunks):
        chunk_prompt = f"Identify potential legal risks in this part of a document (Part {i+1}):\n\n{chunk}"
        try:
            # Small delay to respect 10 RPM limit of Flash-Lite
            if i > 0:
                time.sleep(2)
                
            response = model.generate_content(chunk_prompt)
            chunk_risks.append(response.text)
        except Exception as e:
            print(f"Error processing risk chunk {i+1}: {e}")
            
    # 3. Combine and generate final risk analysis
    combined_risks = "\n\n".join(chunk_risks)
    final_prompt = f"{prompt_template}\n\nDetected Risk Points from Parts:\n{combined_risks}"
    
    try:
        # Final small delay before last call
        time.sleep(2)
        final_response = model.generate_content(final_prompt)
        return final_response.text
    except Exception as e:
        return f"Error during final risk analysis: {str(e)}"
