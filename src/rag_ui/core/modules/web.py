import requests
from bs4 import BeautifulSoup

def extract_text(text) -> str:
    ret = []
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if len(paragraph) > 100:
            ret.append(paragraph)
    return '\n'.join(ret)

def get_raw(url) -> str:
    """
    Get the raw text from the url, optimized for LLM processing.
    Extracts the main content while removing unnecessary elements.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        clean_text = extract_text(text)
        return clean_text
    except Exception as e:
        raise