from ollama import Client

from rag_ui.core.config import config
from rag_ui.inference.prompt import construct_prompt
from rag_ui.core.modules.search import websosanh_search

OLLAMA_HOST = config.OLLAMA_NGROK_URL

def ollama_chat_response(
        model: str, 
        tool_call=False, 
        context=None,
        user_message=None
    ):
    client = Client(host=OLLAMA_HOST)
    
    if tool_call:
        messages = construct_prompt(user_message, context)

        available_functions = {
            'websosanh_search': websosanh_search,
        }
        response = client.chat(
            model,
            messages,
            tools=[websosanh_search]
        )
        for tool in response.message.tool_calls or []:
            function_to_call = available_functions.get(tool.function.name)
            if function_to_call:
                products_json = function_to_call(keyword=tool.function.arguments.get('keyword'))
                context = products_json
            else:
                print('Function not found:', tool.function.name)
        # if response.message.tool_calls:
        #     messages.append(response.message)
        #     messages.append({
        #         "role": "tool",
        #         "content": products_json,
        #         "name": tool.function.name
        #     })

    messages = construct_prompt(user_message, context)
    final_response = client.chat(model, messages)
    full_response = final_response['message']['content']
    if 'deepseek' in model:
        true_response = full_response.split('</think>')[-1]
        return true_response

    return full_response

def ollama_product_call(
        model: str,
        user_message: str = None
    ):
    client = Client(host=OLLAMA_HOST)
    # Heuristicly calling websosanh_search
    
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
        # # Casual response
        # full_response = client.chat(
        #     model=model,
        #     messages=[
        #         {
        #             "role": "system", 
        #             "content": """You are great at casual conversation, 
        #             response with a casual message"""
        #         },
        #         {
        #             "role": "user",
        #             "content": user_message
        #         }
        #     ]
        # )
        pass
    else:
        # Call the function
        json_res = websosanh_search(keyword=item)

    #     # Continue the conversation
    #     full_response = client.chat(
    #         model=model,
    #         messages=[
    #             {
    #                 "role": "system", 
    #                 "content": f"""You are great at customer service, the user asked for a product, 
    #                 and the information about the product has been provided in the <context> tag, 
    #                 please respond to the user in an organized format which specified the product's 
    #                 'productName', 'price', 'detailUrl', 'merchantDomain', 'provins', 'image'.
    #                 <context>{json_res}</context>"""
    #             },
    #             {
    #                 "role": "user",
    #                 "content": user_message
    #             }
    #         ]
    #     )
    # full_response = full_response['message']['content']
    # if 'deepseek' in model:
    #     true_response = full_response.split('</think>')[-1]
    #     return true_response, json_res
    # return full_response, json_res
    return json_res

def ollama_embed_response(
        model: str, 
        input: list[str], 
    ) -> list[list[float]]:

    client = Client(host=OLLAMA_HOST)
    response = client.embed(model, input)
    return response['embeddings']

if __name__ == '__main__':
    print(ollama_chat_response("llama3.2", [{"role": "user", "content": "Hello"}]))