# OCR Application

This application uses Optical Character Recognition (OCR) to extract text from images.

## Dependencies

This application uses the following libraries:

- OpenCV
- PaddleOCR
- PIL
- Flask
- Pyhton = 3.7.0

You can install these with pip:

```bash
pip install -r requirements.txt 
```
## Usage

To run the application, first start the Flask server:

```bash
python api.py
```
Then, navigate to http://127.0.0.1:5000/ in your web browser. You can upload an image or multiple images, and the application will extract the text from the images and display it. You can also download the results as an Excel file.

## Code Overview

The main function in main.py processes an image as follows:

- The image is read and resized.
- The PaddleOCR model is used to extract text from the image.
- The extracted text is cleaned and returned.
- The Flask application in api.py provides a web interface for this functionality. It allows you to upload images, processes them using the - function from main.py, and displays the results. It makes the file excel file displayed downlaodable as well.

The Flask application in api.py provides a web interface for this functionality. It allows you to upload images, processes them using the function from main.py, and displays the results.

