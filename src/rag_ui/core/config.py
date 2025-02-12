import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("PROVIDER")
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM"))
EMBEDDING_MAX_WORDS = int(os.getenv("EMBEDDING_MAX_WORDS"))
OLLAMA_NGROK_URL = os.getenv("OLLAMA_NGROK_URL")
WHISPER_NGROK_URL = os.getenv("WHISPER_NGROK_URL")
