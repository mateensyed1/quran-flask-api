from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if request.is_json:
        data = request.get_json()
        return jsonify({"status": "Flask is working", "data": data})
    return jsonify({"error": "No file or JSON received"}), 400

if __name__ == '__main__':
    app.run()