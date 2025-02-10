import base64

from dash import html, no_update, Input, Output, State

from rag_ui.inference.ollama_client import ollama_chat_response, ollama_embed_response
from rag_ui.inference.prompt import construct_prompt
from rag_ui.inference.whisper import whispercpp
from rag_ui.core.config import LLM_MODEL, EMBEDDING_MODEL
from rag_ui.ui.helper import get_latest_user_message, save_uploaded_file
from rag_ui.data.preprocessing import to_text
from rag_ui.db.vectorstore import insert, get_search_results


def register_callbacks(app, *args):
    # -------------------------------------------------------------------------------
    # When the user clicks the button or presses Enter and there is text:
    # - Append the user's message to the conversation.
    # - Append a pending machine answer (loading==True).
    # - Clear the input field.
    # -------------------------------------------------------------------------------
    @app.callback(
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
        ]
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
    @app.callback(
        Output("input-container", "style"),
        Input("conversation-store", "data"),
        prevent_initial_call=True
    )
    def update_container_style(conversation):
        from rag_ui.ui.layout import bottom_style, center_style
        return bottom_style if len(conversation) > 0 else center_style  

    # -------------------------------------------------------------------------------
    # Render user messages right-aligned and machine messages left-aligned.
    # For machine messages, if the answer is pending (loading) display a loading animation.
    # -------------------------------------------------------------------------------
    @app.callback(
        Output("chat-container", "children"),
        Input("conversation-store", "data")
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
                    "alignSelf": "flex-end"
                })
                content = msg["content"]
            elif msg["role"] == "assistant":
                style = base_style.copy()
                style.update({
                    "textAlign": "left",
                    "background": "#d0f0d0",
                    "alignSelf": "flex-start"
                })
                if msg.get("loading"):
                    content = html.Div(
                        [html.Span(), html.Span(), html.Span()],
                        className="loading-dots"
                    )
                else:
                    content = msg["content"]
            messages.append(html.Div(content, style=style))
        return html.Div(messages, style={"display": "flex", "flexDirection": "column"})

    # -------------------------------------------------------------------------------
    # On each interval:
    #   1. Look for the latest assistant message with loading=True.
    #   2. Construct the conversation in the format required by ollama_chat_response,
    #      excluding that loading message itself.
    #   3. Call ollama_chat_response to get the model's answer.
    #   4. Update that assistant message with the answer and set loading=False.
    # -------------------------------------------------------------------------------
    @app.callback(
        Output("conversation-store", "data", allow_duplicate=True),
        Input("conversation-store", "data"),
        prevent_initial_call=True
    )
    def update_machine_answer(conversation):
        if not conversation:
            return no_update

        new_conversation = conversation.copy()
        for i, msg in enumerate(new_conversation):
            # Identify the first assistant message that is loading
            if msg.get("role") == "assistant" and msg.get("loading"):
                try:
                    # Get the latest user message
                    latest_user_message = get_latest_user_message(new_conversation[:i])

                    embedding = ollama_embed_response(EMBEDDING_MODEL, [latest_user_message])[0]
                    # Search for similar embeddings in the Milvus database
                    search_res = get_search_results(args[0], "documents", embedding, ["text", "file_path"])
                    retrieved = [(res["entity"]["file_path"], res["entity"]["text"]) for res in search_res[0]]
                    print("retrieved text: ", retrieved)
                    context = "\n".join([f"File: {file_path}\nRelevance Text: {text}" for file_path, text in retrieved])
                    full_prompts = construct_prompt(context, latest_user_message)
                    # Get the assistant's response from Ollama
                    answer = ollama_chat_response(
                        LLM_MODEL,
                        full_prompts,
                        stream=False
                    )
                except Exception as e:
                    answer = f"Request failed: {str(e)}"
                print("answer:", answer)  # Debug print.
                # Update the pending assistant message with the new answer
                new_conversation[i]["loading"] = False
                new_conversation[i]["content"] = answer

                return new_conversation
        return no_update

    # -------------------------------------------------------------------------------
    # This clears the conversation.
    # -------------------------------------------------------------------------------
    @app.callback(
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
    @app.callback(
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

        file_path = save_uploaded_file(file_bytes, filename)
        text = to_text(file_path)

        res = insert(args[0], text, file_path, collection_name="documents")
        return res
    
    # -------------------------------------------------------------------------------
    # Show to alert result from inserting data into milvus database.
    # -------------------------------------------------------------------------------
    @app.callback(
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
    @app.callback(
        Output("conversation-store", "data", allow_duplicate=True),
        Input("recording-store", "data"),
        State("conversation-store", "data"),
        prevent_initial_call=True
    )
    def add_transcribed(recording_state, conversation):
        if not recording_state:
            transcribed = whispercpp()
            if not transcribed or not transcribed.strip():
                return conversation
            new_conversation = list(conversation) if conversation else []
            # Append the user's message.
            new_conversation.append({"role": "user", "content": transcribed})
            # Append a placeholder assistant response, marked as loading.
            new_conversation.append({"role": "assistant", "content": "", "loading": True})

            return new_conversation
        else:
            return no_update
        
    # -------------------------------------------------------------------------------
    # Change recording icon.
    # -------------------------------------------------------------------------------
    @app.callback(
        Output("record-icon", "className"),
        Input("record-btn", "n_clicks"),
        State("recording-store", "data"),
        prevent_initial_call=True
    )
    def update_record_icon(n_clicks, recording_state):
        if not recording_state:
            return "fas fa-circle"
        else:
            return "fas fa-microphone"
    
