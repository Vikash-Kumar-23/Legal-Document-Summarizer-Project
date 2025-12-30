def detect_risks(text, model):
    """Detect legal risks in document using LLM and template."""
    from utils.summarizer import get_prompt
    prompt_template = get_prompt("risk_prompt")
    prompt = f"{prompt_template}\n\nDocument Text:\n{text}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during risk detection: {str(e)}"
