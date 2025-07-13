
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return jsonify({"status": "Flask is working", "data": {"test": "hello from app"}})

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"status": "error", "message": "No audio file in request"}), 400

    audio_file = request.files["audio"]
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.save(filepath)

    model_path = "../models/ggml-tiny.bin"
    whisper_exe_path = "../bin/Release/whisper-cli.exe"
    result_path = "transcription.txt"

    command = [
        whisper_exe_path,
        "-m", model_path,
        "-f", filepath,
        "-otxt",
        "-of", "transcription"
    ]

    try:
        subprocess.run(command, check=True)
        with open(result_path, "r", encoding="utf-8") as f:
            transcription = f.read().strip()
        return jsonify({"status": "success", "transcription": transcription})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)})
    except Exception as ex:
        return jsonify({"status": "error", "message": str(ex)})

if __name__ == "__main__":
    app.run(debug=True)
