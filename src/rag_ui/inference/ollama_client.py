from ollama import Client

def ollama_chat_response(
        model: str, 
        messages: list[dict], 
        stream=False
    ):

    client = Client()
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

    client = Client()
    response = client.embed(model, input)
    return response['embeddings']

if __name__ == '__main__':
    print(ollama_chat_response("llama3.2", [{"role": "user", "content": "Hello"}]))