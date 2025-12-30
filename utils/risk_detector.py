def detect_risks(text, model):
    """Detect legal risks in document using LLM and template."""
    import time
    from utils.summarizer import get_prompt
    prompt_template = get_prompt("risk_prompt")
    prompt = f"{prompt_template}\n\nDocument Text:\n{text}"
    
    # Extra safety delay for free tier
    time.sleep(1)
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during risk detection: {str(e)}"
