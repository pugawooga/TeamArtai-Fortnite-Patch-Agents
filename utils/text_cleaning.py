import re

def clean_text(text):
    """
    Basic cleanup: remove weird spacing, HTML artifacts, etc.
    """
    if not isinstance(text, str):
        return ""

    text = re.sub(r'\s+', ' ', text)
    text = text.replace("\u00a0", " ").strip()
    return text
