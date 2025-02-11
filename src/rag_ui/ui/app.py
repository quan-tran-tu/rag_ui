from flask import request
import dash
from dash import Output, Input, State, clientside_callback, ClientsideFunction
import ffmpeg

from rag_ui.db.vectorstore import init_milvus_client, create_collection
from rag_ui.core.config import EMBEDDING_DIM

# Include Font Awesome for icons.
external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

milvus_client = init_milvus_client()
create_collection(milvus_client, "documents", EMBEDDING_DIM)

# Update the index_string to include the CSS for the icon buttons and other global styles.
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta charset="utf-8">
        <title>Chat Mock App</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                width: 100%;
                height: 100%;
                font-family: Arial, sans-serif;
            }
            /* Loading dots animation for machine “typing” indicator */
            .loading-dots {
                display: flex;
                align-items: center;
            }
            .loading-dots span {
                display: block;
                width: 8px;
                height: 8px;
                margin: 0 2px;
                background: #555;
                border-radius: 50%;
                animation: loading 1.4s infinite ease-in-out both;
            }
            .loading-dots span:nth-child(1) {
                animation-delay: -0.32s;
            }
            .loading-dots span:nth-child(2) {
                animation-delay: -0.16s;
            }
            @keyframes loading {
                0%, 80%, 100% {
                    transform: scale(0);
                } 40% {
                    transform: scale(1);
                }
            }
            /* Icon button styles */
            .icon-button {
                background: #424242;
                border: none;
                padding: 10px;
                cursor: pointer;
                font-size: 18px;
                color: #fff;
                transition: background-color 0.3s ease;
            }
            .icon-button:hover {
                background: #616161;
            }
            *, *:before, *:after {
                box-sizing: border-box;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Import the layout defined in layout.py
from rag_ui.ui.layout import layout
app.layout = layout

# Register all callbacks with the app.
from rag_ui.ui.callbacks import register_callbacks
register_callbacks(app, milvus_client)

@app.server.route("/save_audio", methods=["POST"])
def save_audio():
    if "audio" not in request.files:
        return "No file received", 400
    
    audio_file = request.files["audio"]
    save_path = "./src/rag_ui/data/audio/recorded_audio.webm"
    wav_path = "./src/rag_ui/data/audio/recorded_audio.wav"
    audio_file.save(save_path)
    try:
        (
            ffmpeg
                .input(save_path)
                .output(wav_path, acodec="pcm_s16le", ar="16000", ac=1)
                .run(overwrite_output=True)
        )
        return "Audio saved successfully", 200
    except ffmpeg.Error as e:
        print(f"Error ffmpeg conversion: {e}")

clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='toggleRecording'
    ),
    Output("recording-store", "data"),
    Input("record-btn", "n_clicks"),
    State("recording-store", "data"),
    prevent_initial_call=True
)


if __name__ == '__main__':
    app.run_server(debug=False)
