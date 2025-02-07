import base64

from dash import html, no_update, Input, Output, State

from rag_ui.inference.ollama_client import ollama_chat_response, ollama_embed_response
from rag_ui.inference.prompt import construct_prompt
from rag_ui.core.config import LLM_MODEL, EMBEDDING_MODEL
from rag_ui.ui.helper import get_latest_user_message, save_uploaded_file
from rag_ui.data.preprocessing import to_text
from rag_ui.db.vectorstore import insert, get_search_results


def register_callbacks(app, *args):
    # -------------------------------------------------------------------------------
    # Callback 1: Process submission.
    #
    # When the user clicks the button or presses Enter and there is text:
    # - Append the user's message to the conversation.
    # - Append a pending machine answer (loading==True).
    # - Mark that a submission has occurred.
    # - Clear the input field.
    # -------------------------------------------------------------------------------
    @app.callback(
        [
            Output("submission-store", "data"),
            Output("center-input", "value"),
            Output("conversation-store", "data")
        ],
        [
            Input("speech-to-text-btn", "n_clicks"),
            Input("center-input", "n_submit")
        ],
        [
            State("center-input", "value"),
            State("conversation-store", "data"),
            State("submission-store", "data")
        ]
    )
    def process_submission(n_clicks, n_submit, text, conversation, submitted):
        if not text or not text.strip():
            return submitted, no_update, conversation

        new_conversation = list(conversation) if conversation else []

        # Append the user's message.
        new_conversation.append({"role": "user", "content": text})

        # Append a placeholder assistant response, marked as loading.
        new_conversation.append({"role": "assistant", "content": "", "loading": True})

        # Flag that a submission has occurred and clear the input.
        return True, "", new_conversation

    # -------------------------------------------------------------------------------
    # Callback 2: Update the input container's style.
    #
    # Move the input container to the bottom if a submission has occurred.
    # -------------------------------------------------------------------------------
    @app.callback(
        Output("input-container", "style"),
        Input("submission-store", "data")
    )
    def update_container_style(submitted):
        from rag_ui.ui.layout import bottom_style, center_style
        return bottom_style if submitted else center_style

    # -------------------------------------------------------------------------------
    # Callback 3: Update the button's icon based on input field content.
    #
    # Display an up arrow when there is text; otherwise, display a microphone.
    # -------------------------------------------------------------------------------
    @app.callback(
        Output("button-icon", "className"),
        Input("center-input", "value")
    )
    def update_icon(value):
        if value and value.strip():
            return "fas fa-arrow-up"  
        return "fas fa-microphone"    

    # -------------------------------------------------------------------------------
    # Callback 4: Update the chat container with the conversation history.
    #
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
    # Callback 5: Update pending machine answer by calling the ollama API.
    #
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
    # Callback 6: Reset the conversation and submission store when the New Chat button is clicked.
    #
    # This clears the conversation and resets the submission marker.
    # -------------------------------------------------------------------------------
    @app.callback(
        [
            Output("conversation-store", "data", allow_duplicate=True),
            Output("submission-store", "data", allow_duplicate=True)
        ],
        Input("new-chat-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def new_chat(n_clicks):
        return [], False
    
    # -------------------------------------------------------------------------------
    # Callback 7: Upload a document.
    #
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
    # Callback 8: Alert.
    #
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