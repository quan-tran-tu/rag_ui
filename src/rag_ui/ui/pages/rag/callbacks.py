import os
import base64

import requests

from dash import html, no_update, Input, Output, State, clientside_callback, ClientsideFunction, callback, dcc

from rag_ui.inference.ollama_client import ollama_chat_response, ollama_embed_response, ollama_product_call
from rag_ui.core.config import config
from rag_ui.ui.helper import get_latest_user_message, save_uploaded_file, create_product_div
from rag_ui.ui.pages.rag.layout import bottom_style, center_style
from rag_ui.data.preprocessing import to_text
from rag_ui.db.vectorstore import insert, get_search_results
from rag_ui.core.modules.speech_enhance import enhance
from rag_ui.inference.whisper import whisper_api
from rag_ui.inference.embed import embed_api

UPLOAD_FOLDER = "./src/rag_ui/data/documents/"

def register_callbacks(*args):
    # -------------------------------------------------------------------------------
    # When the user clicks the button or presses Enter and there is text:
    # - Append the user's message to the conversation.
    # - Append a pending machine answer (loading==True).
    # - Clear the input field.
    # -------------------------------------------------------------------------------
    @callback(
        [
            Output("center-input", "value"),
            Output("conversation-store", "data")
        ],
        [
            Input("enter-btn", "n_clicks"),
            Input("center-input", "n_submit")
        ],
        [
            State("center-input", "value"),
            State("conversation-store", "data"),
        ],
    )
    def process_submission(n_clicks, n_submit, text, conversation):
        if not text or not text.strip():
            return no_update, conversation

        new_conversation = list(conversation) if conversation else []

        # Append the user's message.
        new_conversation.append({"role": "user", "content": text})
        # Append a placeholder assistant response, marked as loading.
        new_conversation.append({"role": "assistant", "content": "", "loading": True})

        # Clear the input.
        return "", new_conversation

    # -------------------------------------------------------------------------------
    # Move the input container to the bottom if conversation has children.
    # -------------------------------------------------------------------------------
    @callback(
        Output("center-container", "style"),
        Input("conversation-store", "data")
    )
    def update_container_style(conversation):
        if len(conversation) > 0:
            return bottom_style
        else:
            return center_style

    # -------------------------------------------------------------------------------
    # Render user messages right-aligned and machine messages left-aligned.
    # For machine messages, if the answer is pending (loading) display a loading animation.
    # -------------------------------------------------------------------------------
    @callback(
        Output("chat-container", "children"),
        Input("conversation-store", "data"),
    )
    def update_chat(conversation):
        print("Updated conversation:", conversation)  # Debug print.
        if not conversation:
            return []
        
        messages = []
        for msg in conversation:
            base_style = {
                "margin": "10px 20px",
                "padding": "10px",
                "borderRadius": "10px",
                "maxWidth": "70%",
            }
            if msg["role"] == "user":
                style = base_style.copy()
                style.update({
                    "textAlign": "right",
                    "background": "#e0e0e0",
                    "alignSelf": "flex-end",
                    "background": "#4d4d4d",
                    "color": "#fff", 
                })
                content = msg["content"]
            elif msg["role"] == "assistant":
                style = base_style.copy()
                style.update({
                    "textAlign": "left",
                    "background": "#d0f0d0",
                    "alignSelf": "flex-start",
                    "background": "#212121",
                    "color": "#fff",
                    "lineHeight": "1.6",
                    "maxWidth": "100%",
                    "width": "100%",
                    "margin": "10px 0"  
                })
                if msg.get("loading"):
                    content = html.Div(
                        [html.Span(), html.Span(), html.Span()],
                        className="loading-dots"
                    )
                else:
                    if msg['json_res']:
                        content = create_product_div(msg["json_res"]) # Create a html.Div with the product info
                    else:
                        content = msg["content"]
            messages.append(html.Div(dcc.Markdown(content, mathjax=True), style=style))
        return html.Div(messages, style={"display": "flex", "flexDirection": "column"})

    # -------------------------------------------------------------------------------
    # On each interval:
    #   1. Look for the latest assistant message with loading=True.
    #   2. Construct the conversation in the format required by ollama_chat_response,
    #      excluding that loading message itself.
    #   3. Call ollama_chat_response to get the model's answer.
    #   4. Update that assistant message with the answer and set loading=False.
    # -------------------------------------------------------------------------------
    @callback(
        Output("conversation-store", "data", allow_duplicate=True),
        Input("conversation-store", "data"),
        State("search-mode", "data"),
        prevent_initial_call=True
    )
    def update_machine_answer(conversation, search):
        if not conversation:
            return no_update

        new_conversation = conversation.copy()
        for i, msg in enumerate(new_conversation):
            # Identify the first assistant message that is loading
            if msg.get("role") == "assistant" and msg.get("loading"):
                try:
                    json_res = ""
                    # Get the latest user message
                    latest_user_message = get_latest_user_message(new_conversation[:i])

                    if not search:
                        # embedding = ollama_embed_response(config.EMBEDDING_MODEL, [latest_user_message])[0]
                        embedding = embed_api([latest_user_message])[0]
                        # Search for similar embeddings in the Milvus database
                        search_res = get_search_results(args[0], "documents", embedding, ["text", "file_path"])
                        retrieved = [(res["entity"]["file_path"], res["entity"]["text"]) for res in search_res[0]]
                        print("retrieved text: ", retrieved)
                        context = "\n".join([f"File: {file_path}\nRelevance Text: {text}" for file_path, text in retrieved])
                        # Get the assistant's response from Ollama
                        answer = ollama_chat_response(
                            config.LLM_MODEL,
                            context=context,
                            user_message=latest_user_message
                        )
                    else:
                        # answer = ollama_chat_response(
                        #     config.LLM_MODEL,
                        #     user_message=latest_user_message,
                        #     tool_call=True
                        # )
                        answer = ""
                        json_res = ollama_product_call(
                            config.LLM_MODEL,
                            user_message=latest_user_message
                        )

                except Exception as e:
                    answer = f"Request failed: {str(e)}"

                print("answer:", answer)  # Debug print.
                # Update the pending assistant message with the new answer
                new_conversation[i]["loading"] = False
                new_conversation[i]["content"] = answer
                new_conversation[i]["json_res"] = json_res

                return new_conversation
        return no_update

    # -------------------------------------------------------------------------------
    # This clears the conversation.
    # -------------------------------------------------------------------------------
    @callback(
        Output("conversation-store", "data", allow_duplicate=True),
        Input("new-chat-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def new_chat(n_clicks):
        return []
    
    # -------------------------------------------------------------------------------
    # Upload a document then: (In the future will parallel storing the document and 
    #                           processing the content)
    #   1. Store the document content.
    #   2. Transform the document content to chunks of text.
    #   3. Embed the chunks of text using Ollama and save the embeddings to Milvus.
    # -------------------------------------------------------------------------------
    @callback(
        Output("alert-store", "data"),
        Input("upload-doc", "contents"),
        State("upload-doc", "filename"),
        prevent_initial_call=True
    )
    def process_upload_file(contents, filename):
        if not contents or not filename:
            return no_update
        _, content_string = contents.split(",")
        file_bytes = base64.b64decode(content_string)

        file_path = save_uploaded_file(file_bytes, filename, UPLOAD_FOLDER)
        text = to_text(file_path)

        res = insert(args[0], text, file_path, collection_name="documents")
        return res
    
    # -------------------------------------------------------------------------------
    # Show to alert result from inserting data into milvus database.
    # -------------------------------------------------------------------------------
    @callback(
        Output("alert-box", "message"),
        Output("alert-box", "displayed"),
        Input("alert-store", "data"),
        prevent_initial_call=True
    )
    def show_alert(message):
        return message, True
    
# -------------------------------------------------------------------------------
# Transcribe audio recorded and add to conversation store.
# -------------------------------------------------------------------------------
@callback(
    Output("conversation-store", "data", allow_duplicate=True),
    Input("record-btn", "n_clicks"),
    State("recording-store", "data"),
    State("conversation-store", "data"),
    prevent_initial_call=True
)
def add_transcribed(n_clicks, recording_state, conversation):
    if recording_state is False:  # Only process after recording has stopped
        filepath = "/home/tuquan/rag_ui/src/rag_ui/data/audio/recorded_audio.wav"
        enhanced_path = "/home/tuquan/rag_ui/src/rag_ui/data/audio/enhanced.wav"
        
        # Check if the file exists before processing
        if os.path.exists(filepath):
            enhance(filepath, enhanced_path)
            
            transcribed = whisper_api(enhanced_path)
            
            if not transcribed or not transcribed.strip():
                return no_update
                
            new_conversation = list(conversation) if conversation else []
            # Append the user's message.
            new_conversation.append({"role": "user", "content": transcribed})
            # Append a placeholder assistant response, marked as loading.
            new_conversation.append({"role": "assistant", "content": "", "loading": True})
            
            return new_conversation
    
    return no_update

# -------------------------------------------------------------------------------
# Client side recording callback
# -------------------------------------------------------------------------------
clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='toggleRecording'
    ),
    Output("recording-store", "data"),
    Output("raw-path", "data"),
    Output("record-icon", "className"),
    Input("record-btn", "n_clicks"),
    State("recording-store", "data"),
    prevent_initial_call=True
)

# -------------------------------------------------------------------------------
# Trigger search mode
# -------------------------------------------------------------------------------
@callback(
    Output("search-mode", "data"),
    Output("search-btn", "style"),
    Input("search-btn", "n_clicks"),
    State("search-mode", "data"),
    prevent_initial_call=True
)
def toggle_search_mode(n_clicks, search_mode):
    if search_mode:
        style = {
            "display": "flex",
            "alignItems": "center",
            "background": "#303030",
            "border": "1px solid white",
            "borderRadius": "20px",
            "padding": "5px 10px",
            "cursor": "pointer",  
            "color": "white", 
        }
    else:
        style = {
            "display": "flex",
            "alignItems": "center",
            "background": "#303030",
            "border": "1px solid red",
            "borderRadius": "20px",
            "padding": "5px 10px",
            "cursor": "pointer",  
            "color": "red",
        }
    return not search_mode, style