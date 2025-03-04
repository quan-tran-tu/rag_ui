from ollama import Client

from rag_ui.inference.prompt import construct_prompt
from rag_ui.core.modules.search import websosanh_search


def fix_latex_response(response: str) -> str:
    response = response.replace('\\(', '$')
    response = response.replace('\\)', '$')

    return response

def ollama_chat_response(
        model: str, 
        client: Client,
        tool_call=False, 
        context=None,
        history=None,
        # user_message=None, 
    ):    
    if tool_call:
        messages = construct_prompt(history, context)

        available_functions = {
            'websosanh_search': websosanh_search,
        }
        response = client.chat(
            model,
            messages,
            tools=[websosanh_search],
            keep_alive=-1
        )
        for tool in response.message.tool_calls or []:
            function_to_call = available_functions.get(tool.function.name)
            if function_to_call:
                products_json = function_to_call(keyword=tool.function.arguments.get('keyword'))
                context = products_json
            else:
                print('Function not found:', tool.function.name)

    messages = construct_prompt(history, context)
    final_response = client.chat(model, messages, keep_alive=-1)
    full_response = final_response['message']['content']
    if 'deepseek' in model:
        true_response = full_response.split('</think>')[-1]
        return true_response

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

if __name__ == '__main__':
    print(ollama_chat_response("llama3.2", [{"role": "user", "content": "Hello"}]))