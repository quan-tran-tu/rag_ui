import requests

from rag_ui.core.config import config

EMBED_URL = config.EMBED_NGROK_URL + "/embed"

def embed_api(texts: list[str]) -> str:
    data = {
        'texts': texts
    }
    response = requests.post(EMBED_URL, json=data)
    response.raise_for_status()
    response = response.json()['embeddings']
    return response