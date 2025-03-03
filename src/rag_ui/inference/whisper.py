import requests

from rag_ui.core.config import config

WHISPER_URL = config.WHISPER_NGROK_URL + "/transcribe"

def whisper_api(filepath) -> str:
    with open(filepath, "rb") as f:
        files = {"file": f}
        headers = {"accept": "application/json"}
        response = requests.post(WHISPER_URL, files=files, headers=headers)
        transcribed = response.json()['transcribe']
        return transcribed