import base64

from dash import html, no_update, Input, Output, State, clientside_callback, ClientsideFunction, callback

from rag_ui.ui.helper import save_uploaded_file

AUDIO_FOLDER = "./src/rag_ui/data/audio/"

def register_callbacks():
    # -------------------------------------------------------------------------------
    # Upload audio and save to server
    # -------------------------------------------------------------------------------
    @callback(
        Output("raw-audio-state", "data"),
        Input("upload-audio", "contents"),
        State("upload-audio", "filename"),
    )
    def process_upload_file(contents, filename):
        if not contents or not filename:
            return no_update
        _, content_string = contents.split(",")
        file_bytes = base64.b64decode(content_string)

        file_path = save_uploaded_file(file_bytes, filename, AUDIO_FOLDER)

        return True
    # -------------------------------------------------------------------------------
    # Change record button text and style
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------
    # Audio playable on uploaded, finished recording or enhanced
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------
    # If there is audio uploaded or recorded, trigger enhance button
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------
    # If there is audio uploaded or recorded, trigger transcribe raw audio button
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------
    # If there is enhanced audio, trigger transcribe clean audio button
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------
    # Display latest text found in transcription store
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------
    # Reset everything when click the reset button
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------
    # Client side recording callback
    # -------------------------------------------------------------------------------
    clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='toggleRecording'
        ),
        Output("speech-recording-store", "data"),
        Input("speech-record-btn", "n_clicks"),
        State("speech-recording-store", "data"),
        prevent_initial_call=True
    )