from ollama import Client

from rag_ui.inference.prompt import construct_prompt
from rag_ui.core.modules.product_search import websosanh_search

def fix_latex_response(response: str) -> str:
    response = response.replace('\\(', '$')
    response = response.replace('\\)', '$')

    return response

def intent_recognition(
        model: str, 
        client: Client,
        user_message: str = None
    ):
    """
    Add a layer to recognize user's intent
    Output should be ['None', 'Summarize']
    """
    response = client.chat(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": """You are great at recognizing the user's intent from their message,
                    if the user's intent is to summarize the content from an url, 
                    return a dict with the key 'Summarize' with the value being the url,
                    otherwise return a dict with the key 'None' and the value being 'None'.
                    Return only in a string so that i can directly pass that string into json.loads 
                    to get the dict, no additional words like: 'Here is the response', ...
                    """
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    intent = response['message']['content']
    return intent

def ollama_chat_response(
        model: str, 
        client: Client,
        history: list[str],
        tool_call=False, 
        context: str = None,
    ):    
    """Get ollama response"""
    messages = construct_prompt(history=history, context=context)

    final_response = client.chat(model, messages, keep_alive=-1)
    full_response = final_response['message']['content']

    if 'deepseek' in model:
        full_response = full_response.split('</think>')[-1]

    full_response = fix_latex_response(full_response)

    return full_response

def ollama_product_call(
        model: str,
        client: Client,
        user_message: str = None
    ):
    """Heuristicly calling websosanh_search"""
    # Recognize user intent to buy something
    response = client.chat(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": """You are great at recognizing if the user wants to buy something, 
                    response with only the word indicating the product the user wants to buy, 
                    'None' if the user does not want to buy anything"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    item = response['message']['content']
    json_res = ""
    if item == 'None':
        pass
    else:
        # Call the function
        json_res = websosanh_search(keyword=item)
    return json_res

def ollama_embed_response(
        model: str, 
        client: Client,
        input: list[str], 
    ) -> list[list[float]]:
    response = client.embed(model, input)
    return response['embeddings']