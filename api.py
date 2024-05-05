from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
from main import OCR, clean_text
from paddleocr import PaddleOCR

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Load the model once when the application starts

@app.route('/ocr', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected for uploading"}), 400
        if file:
            filename = secure_filename(file.filename)
            temp_path = os.path.join(tempfile.gettempdir(), filename)
            file.save(temp_path)
            text = OCR(temp_path, ocr, filename, tempfile.gettempdir())
            return jsonify({'image_name': filename, 'text': text})
        else:
            return jsonify({"error": "Unsupported file type"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port, threaded=False)