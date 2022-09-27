import json
from flask import request, send_file, Blueprint
from flask_api import status
from datetime import datetime
import base64
import os

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
        loadInternal = data["internalImg"]
        loadExternal = data["externalImg"]
        
        #Parte Interna
        filename = loadInternal["filename"]
        extension = loadInternal["extension"]
        imageBase64 = loadInternal["image"]
        save(imageBase64, filename , extension)

        #Parte Externa
        filename = loadExternal["filename"]
        extension = loadExternal["extension"]
        imageBase64 = loadExternal["image"]
        save(imageBase64, filename , extension)

        return send_file("example.csv", "text/csv")
    else:
        return 'Content-Type not supported', status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
