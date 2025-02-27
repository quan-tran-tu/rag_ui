import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @property
    def PROVIDER(self):
        return os.getenv("PROVIDER")
    @property
    def LLM_MODEL(self):
        return os.getenv("LLM_MODEL")
    @property
    def EMBEDDING_MODEL(self):
        return os.getenv("EMBEDDING_MODEL")
    @property       
    def EMBEDDING_DIM(self):
        return int(os.getenv("EMBEDDING_DIM"))
    @property
    def EMBEDDING_MAX_WORDS(self):
        return int(os.getenv("EMBEDDING_MAX_WORDS"))
    @property
    def OLLAMA_NGROK_URL(self):
        return os.getenv("OLLAMA_NGROK_URL")
    @property
    def WHISPER_NGROK_URL(self):
        return os.getenv("WHISPER_NGROK_URL")
    
config = Config()