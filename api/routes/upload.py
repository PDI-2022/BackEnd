import json
from flask import jsonify, request, send_file, Blueprint
from flask_api import status
from api.services.storage import save_base64_image
from api.constants.folders import images_folder
from api.services.processing import process_data


upload_bp = Blueprint("upload", __name__, url_prefix="/api/v1/upload")

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
        save_base64_image(imageBase64_intern, images_folder, filename , extension)

        #Parte Externa
        filename = loadExternal["filename"]
        extension = loadExternal["extension"]
        imageBase64_extern = loadExternal["image"]
        save_base64_image(imageBase64_extern, images_folder, filename , extension)
        
        csv_name = process_data(imageBase64_intern, imageBase64_extern,False)

        return send_file(csv_name, "text/csv")
    else:
        return 'Content-Type not supported', status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

@upload_bp.route("/wtImg", methods=['POST'])
def uploadWtImg():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json;charset=UTF-8'):
        data = request.json
        loadInternal = json.loads(data["internalImg"])
        loadExternal = json.loads(data["externalImg"])

        #Parte Interna
        filename = loadInternal["filename"]
        extension = loadInternal["extension"]
        imageBase64_intern = loadInternal["image"]
        save_base64_image(imageBase64_intern, images_folder, filename , extension)

        #Parte Externa
        filename = loadExternal["filename"]
        extension = loadExternal["extension"]
        imageBase64_extern = loadExternal["image"]
        save_base64_image(imageBase64_extern, images_folder, filename , extension)
        
        csv_name,intJson,extJson = process_data(imageBase64_intern, imageBase64_extern,True)

        return jsonify({"csv":csv_name,"internSeeds":intJson,"externSeeds":extJson})
    else:
        return 'Content-Type not supported', status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        
