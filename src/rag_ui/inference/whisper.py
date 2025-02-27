# from faster_whisper import WhisperModel

# model_size = "large-v3"

# model = WhisperModel(model_size, device="cuda", compute_type="float16")
# segments, info = model.transcribe("src/rag_ui/data/audio/recorded_audio.wav", beam_size=5, language="vi", condition_on_previous_text=False)

# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

import subprocess

import requests

from rag_ui.core.config import config

WHISPER_URL = config.WHISPER_NGROK_URL + "/transcribe"

def whispercpp() -> str:
    ret = subprocess.check_output(
        ["/home/tuquan/rag_ui/whisper.cpp/build/bin/whisper-cli", "-m", "/home/tuquan/rag_ui/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin", "-nt", "true", "-l", "vi", "/home/tuquan/rag_ui/src/rag_ui/data/audio/recorded_audio.wav"],
    )

    return ret.decode('utf-8')

def whisper_api(filepath) -> str:
    with open(filepath, "rb") as f:
        files = {"file": f}
        headers = {"accept": "application/json"}
        response = requests.post(WHISPER_URL, files=files, headers=headers)
        transcribed = response.json()['transcribe']
        return transcribed

if __name__ == "__main__":
    ret = subprocess.check_output(
        ["/home/tuquan/rag_ui/whisper.cpp/build/bin/whisper-cli", "-m", "/home/tuquan/rag_ui/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin", "-nt", "true", "-l", "vi", "/home/tuquan/rag_ui/src/rag_ui/data/audio/16khz.wav"],
    )
    print(ret.decode('utf-8'))
