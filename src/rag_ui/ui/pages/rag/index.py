import dash
from ollama import Client

from rag_ui.ui.pages.rag.callbacks import register_callbacks
from rag_ui.ui.pages.rag.layout import layout as rag_layout
from rag_ui.db.vectorstore import init_milvus_client, create_collection
from rag_ui.core.config import config

OLLAMA_HOST = config.OLLAMA_NGROK_URL

dash.register_page(__name__, path='/')

milvus_client = init_milvus_client()
create_collection(milvus_client, "documents", config.EMBEDDING_DIM)

layout = rag_layout

ollama_client = Client(host=OLLAMA_HOST)
# Seed ollama
ollama_client.chat(
    model=config.LLM_MODEL,
    messages=[
        {"role": "user", "content": "Xin chào"},
    ]
)
register_callbacks(milvus_client, ollama_client)