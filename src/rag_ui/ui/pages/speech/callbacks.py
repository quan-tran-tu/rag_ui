from dash import html, no_update, Input, Output, State, clientside_callback, ClientsideFunction, callback

def register_callbacks():
    
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