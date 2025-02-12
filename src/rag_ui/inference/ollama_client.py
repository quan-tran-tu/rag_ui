from ollama import Client

from rag_ui.core.config import OLLAMA_NGROK_URL

OLLAMA_HOST = OLLAMA_NGROK_URL

def ollama_chat_response(
        model: str, 
        messages: list[dict], 
        stream=False
    ):

    client = Client(host=OLLAMA_HOST)
    # if stream:
    #     for part in client.chat(model, messages, stream=stream):
    #         yield part['message']['content']
    # else:
    response = client.chat(model, messages, stream=False)
    return response['message']['content']

def ollama_embed_response(
        model: str, 
        input: list[str], 
    ) -> list[list[float]]:

    client = Client(host=OLLAMA_HOST)
    response = client.embed(model, input)
    return response['embeddings']

if __name__ == '__main__':
    print(ollama_chat_response("llama3.2", [{"role": "user", "content": "Hello"}]))