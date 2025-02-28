import base64

from dash import no_update, Input, Output, State, clientside_callback, ClientsideFunction, callback

from rag_ui.ui.helper import save_uploaded_file
from rag_ui.core.modules.speech_enhance import enhance
from rag_ui.inference.whisper import whisper_api

AUDIO_FOLDER = "./src/rag_ui/data/audio/"
enhanced_audio_path = AUDIO_FOLDER + "enhanced_audio.wav"

def register_callbacks():
    # -------------------------------------------------------------------------------
    # Upload audio and save to server
    # -------------------------------------------------------------------------------
    @callback(
        Output("raw-audio-state", "data", allow_duplicate=True),
        Output("raw-audio-path", "data", allow_duplicate=True),
        Input("upload-audio", "contents"),
        State("upload-audio", "filename"),
        prevent_initial_call=True
    )
    def process_upload_file(contents, filename):
        if not contents or not filename:
            return no_update, ""
        _, content_string = contents.split(",")
        file_bytes = base64.b64decode(content_string)

        file_path = save_uploaded_file(file_bytes, filename, AUDIO_FOLDER)

        return True, file_path

    # -------------------------------------------------------------------------------
    # Change record button text and style
    # -------------------------------------------------------------------------------
    @callback(
        Output("speech-record-btn", "children"),
        Output("speech-record-btn", "style"),
        Output("raw-audio-state", "data", allow_duplicate=True),
        Input("speech-record-btn", "n_clicks"),
        State("speech-recording-store", "data"),
        prevent_initial_call=True,
    )
    def record(n_clicks, is_recording):
        if not is_recording:
            text = "Stop"
            style = {
                "border": "2px solid red"
            }
            return text, style, False
        else:
            text = "Record"
            style = {
                "border": "2px solid lightgrey"
            }
            return text, style, True

    # -------------------------------------------------------------------------------
    # Audio playable on uploaded
    # -------------------------------------------------------------------------------
    @callback(
        Output("raw-audio-player", "src"),
        Input("upload-audio", "contents"),
        prevent_initial_call=True
    )
    def play_raw_audio(contents):
        if contents is None:
            return no_update
        return contents

    # -------------------------------------------------------------------------------
    # If there is audio uploaded or recorded, trigger enhance button
    # -------------------------------------------------------------------------------
    @callback(
        Output("enhanced-audio-state", "data"),
        Output("enhanced-audio-player", "src"),
        Input("enhance-audio-btn", "n_clicks"),
        State("raw-audio-state", "data"),
        State("raw-audio-path", "data"),
    )
    def enhance_audio(n_clicks, has_raw_audio, raw_audio_path):
        if has_raw_audio:
            enhance(raw_audio_path, enhanced_audio_path)
            with open(enhanced_audio_path, 'rb') as audio_file:
                encoded_audio = base64.b64encode(audio_file.read()).decode()
            audio_src = f"data:audio/wav;base64,{encoded_audio}"
            return True, audio_src
        return False, None

    # -------------------------------------------------------------------------------
    # If there is audio uploaded or recorded, trigger transcribe raw audio button
    # -------------------------------------------------------------------------------
    @callback(
        Output("transcription-results-store", "data"),
        Input("transcribe-raw-btn", "n_clicks"),
        State("raw-audio-state", "data"),
        State("raw-audio-path", "data"),
    )
    def transcribe_raw(n_clicks, has_raw_audio, raw_audio_path):
        if has_raw_audio:
            transcribed = whisper_api(raw_audio_path)
            return transcribed
        return no_update
    
    # -------------------------------------------------------------------------------
    # If there is enhanced audio, trigger transcribe clean audio button
    # -------------------------------------------------------------------------------
    @callback(
        Output("transcription-results-store", "data", allow_duplicate=True),
        Input("transcribe-clean-btn", "n_clicks"),
        State("enhanced-audio-state", "data"),
        prevent_initial_call=True
    )
    def transcribe_clean(n_clicks, has_clean_audio):
        if has_clean_audio:
            transcribed = whisper_api(enhanced_audio_path)
            return transcribed
        return no_update
    
    # -------------------------------------------------------------------------------
    # Display latest text found in transcription store
    # -------------------------------------------------------------------------------
    @callback(
        Output("transcription-results", "children"),
        Input("transcription-results-store", "data"),
    )
    def show_transcribed(transcribed):
        return transcribed
    
    # -------------------------------------------------------------------------------
    # Reset everything when click the reset button
    # -------------------------------------------------------------------------------
    @callback(
        Output("raw-audio-state", "data", allow_duplicate=True),
        Output("enhanced-audio-state", "data", allow_duplicate=True),
        Output("transcription-results-store", "data", allow_duplicate=True),
        Output("raw-audio-player", "src", allow_duplicate=True),
        Output("enhanced-audio-player", "src", allow_duplicate=True),
        Input("refresh-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def reset(n_clicks):
        return False, False, "", None, None
    
    # -------------------------------------------------------------------------------
    # Client side recording callback
    # -------------------------------------------------------------------------------
    clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='toggleRecording'
        ),
        Output("speech-recording-store", "data"),
        Output("raw-audio-path", "data"),
        Output("trash", "data"),
        Input("speech-record-btn", "n_clicks"),
        State("speech-recording-store", "data"),
        prevent_initial_call=True
    )

    # -------------------------------------------------------------------------------
    # Update raw audio player when recording
    # -------------------------------------------------------------------------------
    @callback(
        Output("raw-audio-player", "src", allow_duplicate=True),
        Output("raw-audio-state", "data", allow_duplicate=True),
        Input("speech-recording-store", "data"),
        State("raw-audio-path", "data"),
        prevent_initial_call=True
    )
    def update_raw_audio_player(is_recording, path):
        if not is_recording:
            with open(path, 'rb') as audio_file:
                encoded_audio = base64.b64encode(audio_file.read()).decode()
            audio_src = f"data:audio/wav;base64,{encoded_audio}"
            return audio_src, True
        return no_update, no_update