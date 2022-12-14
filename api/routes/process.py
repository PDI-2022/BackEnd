from flask import jsonify, request, send_file, Blueprint
from flask_api import status
from api.services.storage import create_folder
from api.constants.folders import images_folder, red_extract_folder, background_removed_folder, white_extract_folder, pagination_folder, imagens_cortadas_folder, embriao_folder
from api.services.processing import process_data, process_embriao
from config import db
from db.models import Model
from api.services.classification import model
import re

import os
import base64
import cv2
import torch

process_bp = Blueprint('process', __name__, url_prefix="/api/v1/process")
embriao_model = torch.hub.load('ultralytics/yolov5', 'custom', path="models_embriao/V5/bestM.pt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model()

def extract_data(data : any, identifier : str) -> str:
    payload = data[identifier]

    filename = payload['filename']
    extension = payload['extension']
    img = payload['image']

    return img

@process_bp.route("", methods=['POST'])
def process():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json;charset=UTF-8'):
        return 'Content-Type not supported', status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    data = request.json

    # base64 das duas imagens enviadas.
    internal_img = extract_data(data, 'internalImg')
    external_img = extract_data(data, 'externalImg')

    #cria as pastas a serem usadas pela aplicação.
    create_folder(red_extract_folder)
    create_folder(background_removed_folder)
    create_folder(white_extract_folder)
    create_folder(pagination_folder)
    create_folder(imagens_cortadas_folder)

    #variáveis referentes ao limiar superior e inferior.
    #
    #Booleano para saber se foi selecionado o valor default, ou customizado.
    chooseLimiar = data["chooseLimiar"]
    #  
    #Limiar superior.
    limSup = data["limSup"]
    #
    #Limiar inferior.
    limInf = data["limInf"]

    #Booleano para saber se a imagem é com o sem grid (com grid = False, sem grid = True).
    seedTogether = data["seedTogether"]

    #Número de classes que as sementes podem ter (default = 7, limite = 7).
    seedsClassNumberInput = data["seedsClassNumberInput"]

    #Booleano responsável por definir se será necessário classificar as sementes ou nâo.
    displayClassificationInfos = data['displayClassificationInfos']

    #Booleano responsável por verificar se será renderizada a página com as imagens das sementes cortadas.
    generatePageWithImages = data['generatePageWithImages']

    #Booleano responsável por saber se o embrião também será analisado.
    classificationYolo = data['classificationYolo']

    model_path = ''
    if displayClassificationInfos:
        model_id = data['modelId']
        model = db.session.query(Model).filter_by(id = model_id).first()
        model_path = model.path
    else :
        model = ""

    csv_file = process_data(
        internal_img, 
        external_img, 
        generatePageWithImages, 
        displayClassificationInfos, 
        model_path,
        int(limInf),
        int(limSup),
        seedTogether,
        model,
        embriao_model,
        classificationYolo,
        seedsClassNumberInput
    )
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


@process_bp.route("/embriao", methods=['GET'])
def embriao():
    embrioes_names = os.listdir(embriao_folder)
    total_embrioes = len(embrioes_names)
    
    embrioes = []
    for image in embrioes_names:
        number = image[8]
        number  = number + image[9] if image[9] != '.' else number + ''
        number  = number + image[10] if image[10] != '.' and image[10] != 'j' else number + ''
        number = int(number)
        embriao_atual = cv2.imread(embriao_folder + f'/semente-{number}.jpg')
        embrioes.append((number, embriao_atual))

    csv_file = process_embriao(embrioes)

    return send_file(csv_file, 'text/csv'), status.HTTP_200_OK 