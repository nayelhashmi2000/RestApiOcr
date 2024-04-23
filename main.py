import argparse
import os
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import cv2
import re
import numpy as np
from pandas import DataFrame as df

def clean_text(text):
    # Convert to uppercase
    text = text.upper()
    # Remove spaces and replace B2 with BZ if at the start, ensure BZ is followed by a single hyphen
    text = re.sub(r' ', '', text)
    text = re.sub(r'^B2', 'BZ', text)
    text = re.sub(r'^BZ(?=[^-])', 'BZ-', text)  # Add a dash only if there isn't already one
    # Remove all characters except letters, numbers, and hyphen
    text = re.sub(r'[^A-Z0-9-]', '', text)
    #if text starts with 32 or 3Z replace with BZ
    text = re.sub(r'^(32|3Z)', 'BZ', text)
    return text

def OCR(img_path, ocr, image_name, result_dir):
    #check if image name is a path
    if '/' in image_name:
        image_name = image_name.split('/')[-1]
    image_name = image_name.split('.')[0]
    img = cv2.imread(img_path)
    new_size = (320, 280)
    resized_img = cv2.resize(img, new_size)
    
    result = ocr.ocr(resized_img, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)

    result = result[0]
    image = Image.open(img_path).convert('RGB')
    image = image.resize(new_size)
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    #convert txts into one string
    text = ' '.join(txts)
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='arial.ttf')
    im_show = Image.fromarray(im_show)
    result_path = os.path.join(result_dir, f'{image_name}_result.jpg')
    im_show.save(result_path)
    text = clean_text(text)
    print(text)
    return text
  