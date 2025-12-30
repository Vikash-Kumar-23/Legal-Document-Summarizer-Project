import re

def clean_text(text):
    """Clean extracted text for better LLM processing."""
    if not text:
        return ""

    # 1. Remove page headers/footers (common patterns like "Page X of Y" or lone numbers at start/end of lines)
    text = re.sub(r'(?m)^\s*(Page|PAGE)\s*\d+\s*(of|OF)?\s*\d*\s*$', '', text)
    text = re.sub(r'(?m)^\s*\d+\s*$', '', text)

    # 2. Remove extra spaces
    text = re.sub(r' +', ' ', text)
    
    # 3. Normalize newlines (max 2 consecutive newlines to preserve paragraphs but remove excessive gaps)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)

    # 4. Remove leading/trailing whitespace
    return text.strip()
