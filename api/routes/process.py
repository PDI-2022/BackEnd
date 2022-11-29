from flask import jsonify, request, send_file, Blueprint
from flask_api import status
from api.services.storage import save_base64_image, create_folder
from api.constants.folders import images_folder, red_extract_folder, background_removed_folder, white_extract_folder, pagination_folder
from api.services.processing import process_data
from config import db
from db.models import Model
import os
import base64
import cv2

process_bp = Blueprint('process', __name__, url_prefix="/api/v1/process")

def extract_data_and_save(data : any, identifier : str) -> str:
    payload = data[identifier]

    filename = payload['filename']
    extension = payload['extension']
    img = payload['image']
    save_base64_image(img, images_folder, filename , extension)

    return img

@process_bp.route("", methods=['POST'])
def process():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json;charset=UTF-8'):
        return 'Content-Type not supported', status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    data = request.json

    internal_img = extract_data_and_save(data, 'internalImg')
    external_img = extract_data_and_save(data, 'externalImg')

    create_folder(red_extract_folder)
    create_folder(background_removed_folder)
    create_folder(white_extract_folder)
    create_folder(pagination_folder)

    chooseLimiar = data["chooseLimiar"]
    limSup = data["limSup"]
    limInf = data["limInf"]

    seedTogether = data["seedTogether"]

    displayClassificationInfos = data['displayClassificationInfos']
    generatePageWithImages = data['generatePageWithImages']

    model_path = ''
    if displayClassificationInfos:
        model_id = data['modelId']
        model = db.session.query(Model).filter_by(id = model_id).first()
        model_path = model.path

    # if generatePageWithImages:
    #     csv_json, internal_json, external_json = process_data(internal_img, external_img, True, displayClassificationInfos, model_path)
    #     return jsonify({"csv":csv_json,"internSeeds":internal_json,"externSeeds":external_json}), status.HTTP_200_OK
    
    csv_file = process_data(internal_img, external_img, False, displayClassificationInfos, model_path)
    return send_file(csv_file, 'text/csv'), status.HTTP_200_OK     

@process_bp.route("/pagination", methods=['POST'])
def pagination():
    data = request.json
    seeds_array_interno = []
    seeds_array_externo = []

    itens = data["itensPerPage"]
    page = data["page"]


    seeds_images = os.listdir(pagination_folder)
    images_quant = len(seeds_images)
    
    for i in range((page-1)*itens,  ((page-1)*itens + itens)):
        if i < (images_quant/2):
            interno = cv2.imencode(".jpg",cv2.imread(f'{pagination_folder}/Internal_seed_{i}.jpg'))[1]
            externo = cv2.imencode(".jpg",cv2.imread(f'{pagination_folder}/External_seed_{i}.jpg'))[1]
            
            seeds_array_interno.append(str(base64.b64encode(interno)))
            seeds_array_externo.append(str(base64.b64encode(externo)))

    return jsonify({"internSeeds":seeds_array_interno,"externSeeds":seeds_array_externo}), status.HTTP_200_OK
