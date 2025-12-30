def chunk_text(text, chunk_size=4000, overlap=200):
    """Split long text into manageable chunks for the LLM."""
    if not text:
        return []
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
