def detect_risks(text, model):
    """Detect legal risks in document using LLM and template."""
    import time
    from utils.summarizer import get_prompt
    prompt_template = get_prompt("risk_prompt")
    prompt = f"{prompt_template}\n\nDocument Text:\n{text}"
    
    # Extra safety delay for free tier
    time.sleep(10) # 10 second delay to avoid hitting rate limits after summary
    
    def safe_generate(prompt_text, max_retries=3):
        """Helper to handle 429 errors with auto-retry."""
        for attempt in range(max_retries):
            try:
                return model.generate_content(prompt_text).text
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    time.sleep(15) # Wait 15 seconds before retrying
                    continue
                raise e
    
    try:
        return safe_generate(prompt)
    except Exception as e:
        return f"Error during risk detection: {str(e)}"
