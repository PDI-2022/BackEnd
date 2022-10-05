from email.encoders import encode_noop
import json
from flask import request, send_file, Blueprint
from flask_api import status
from datetime import datetime
import base64
import os
import cv2
import numpy as np
import csv

images_folder = "./images"
upload_bp = Blueprint("upload", __name__, url_prefix="/api/v1/upload")
def create_folder():
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

def save(imageBase64 : str, filename : str, extension : str):
    create_folder()
    image = base64.b64decode(imageBase64)
    now =  datetime.now().strftime("%H-%M-%S.%f")
    filename = "{0}/{1}-{2}.{3}".format("images", filename, now, extension)
    print(filename)
    with open(filename, 'wb') as file:
        file.write(image)

@upload_bp.route("", methods=['POST'])
def upload():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json;charset=UTF-8'):
        data = request.json
        loadInternal = json.loads(data["internalImg"])
        loadExternal = json.loads(data["externalImg"])

        #Parte Interna
        filename = loadInternal["filename"]
        extension = loadInternal["extension"]
        imageBase64_intern = loadInternal["image"]
        save(imageBase64_intern, filename , extension)

        #Parte Externa
        filename = loadExternal["filename"]
        extension = loadExternal["extension"]
        imageBase64_extern = loadExternal["image"]
        save(imageBase64_extern, filename , extension)
        
        csv_name = process_data(imageBase64_intern, imageBase64_extern)

        return send_file(csv_name, "text/csv")
    else:
        return 'Content-Type not supported', status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

def process_data(intern, extern):
    buffer_intern = base64.b64decode(intern)
    nparr = np.frombuffer(buffer_intern, np.uint8)
    input_image = cv2.imdecode(nparr, flags=1)

    bg_removed_image = remove_background(input_image)
    white_percentage_intern = extract_white_percentage(bg_removed_image)

    buffer_extern = base64.b64decode(extern)
    nparr = np.frombuffer(buffer_extern, np.uint8)
    input_image = cv2.imdecode(nparr, flags=1)

    bg_removed_image = remove_background(input_image)
    white_percentage_extern = extract_white_percentage(bg_removed_image)

    header = ['Semente', 'Lado', 'Porcentagem de Branco']
    rows = []

    rows.append([1, 'externo', '{:.2f}%'.format(white_percentage_extern * 100)])
    rows.append([1, 'interno','{:.2f}%'.format(white_percentage_intern * 100)])

    with open('relatorio.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
        
    return 'relatorio.csv'
        

def extract_white_percentage(input_image):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    lower = np.array([0,0,168])
    upper = np.array([172,111,255])   
    mask = cv2.inRange(hsv, lower, upper)

    white_extracted_image = cv2.bitwise_and(input_image, input_image, mask = mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(white_extracted_image)

    return pixels_extracted_white/pixels_number_seed


def remove_background(input_image):
    used_threshold, thresholded_bgr_image = cv2.threshold(input_image, 110, 255, cv2.THRESH_BINARY)
    thresholded_blue_component, thresholded_green_component, thresholded_red_component = cv2.split(thresholded_bgr_image)

    mask_filtered = cv2.medianBlur(thresholded_red_component, 5)

    result_image = cv2.bitwise_and(input_image, input_image, mask = mask_filtered)

    return result_image