import dash
import ffmpeg
from flask import request
from dash import html

# Include Font Awesome for icons.
external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)

app.layout = dash.page_container

@app.server.route("/save_audio", methods=["POST"])
def save_audio():
    if "audio" not in request.files:
        return {"message": "No file received", "code": 400, "path": ""}
    
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
        return {"message": "Audio saved successfully", "code": 200, "path": wav_path}
    except ffmpeg.Error as e:
        print(f"Error ffmpeg conversion: {e}")


if __name__ == '__main__':
    app.run(debug=False)
