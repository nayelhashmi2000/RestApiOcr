from flask import Flask, request, render_template
import os
import tempfile
from werkzeug.utils import secure_filename, send_from_directory
from main import OCR, clean_text
from paddleocr import PaddleOCR
from pandas import DataFrame as df
import pandas as pd

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Load the model once when the application starts

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        data = df(columns=['image_name', 'text'])
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(tempfile.gettempdir(), filename))
                text = OCR(os.path.join(tempfile.gettempdir(), filename), ocr, filename, tempfile.gettempdir())
                new_data = df({'image_name': [filename], 'text': [text]})
                data = pd.concat([data, new_data], ignore_index=True)
        if len(files) > 1:
            excel_filename = 'combined_result.xlsx'
        else:
            excel_filename = os.path.splitext(filename)[0] + '.xlsx'
        data.to_excel(os.path.join(tempfile.gettempdir(), excel_filename), index=False)
        return render_template('results.html', tables=[data.to_html(classes='data')], titles=data.columns.values, excel_file=excel_filename)
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(tempfile.gettempdir(), filename, as_attachment=True, environ=request.environ)

if __name__ == '__main__':
    app.run(debug=True)