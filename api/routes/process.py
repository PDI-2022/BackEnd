from flask import jsonify, request, send_file, Blueprint
from flask_api import status
from api.services.storage import create_folder
from api.constants.folders import (
    red_extract_folder,
    background_removed_folder,
    white_extract_folder,
    pagination_folder,
    imagens_cortadas_folder,
    embriao_folder,
)
from api.services.processing import process_data, process_embriao
from config import db
from db.models import Model
from api.services.classification import model
from api.services.token import extract_id

import os
import base64
import cv2
import torch

process_bp = Blueprint("process", __name__, url_prefix="/api/v1/process")
embriao_model = torch.hub.load(
    "ultralytics/yolov5", "custom", path="models_embriao/V5/bestM.pt"
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model()


def extract_data(data, identifier) -> str:
    payload = data[identifier]
    return payload["image"]


@process_bp.route("", methods=["POST"])
def process():
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json;charset=UTF-8":
        return "Content-Type not supported", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    token = request.headers.get("token")
    print(token)
    user_id = extract_id(token)

    data = request.json

    # base64 das duas imagens enviadas.
    internal_img = extract_data(data, "internalImg")
    external_img = extract_data(data, "externalImg")

    # variáveis referentes ao limiar superior e inferior.
    #
    # Limiar superior.
    limSup = data["limSup"]
    #
    # Limiar inferior.
    limInf = data["limInf"]

    # Booleano para saber se a imagem é com o sem grid (com grid = False, sem grid = True).
    seedTogether = data["seedTogether"]

    # Número de classes que as sementes podem ter (default = 7, limite = 7).
    seedsClassNumberInput = data["seedsClassNumberInput"]

    # Booleano responsável por definir se será necessário classificar as sementes ou nâo.
    displayClassificationInfos = data["displayClassificationInfos"]

    # Booleano responsável por verificar se será renderizada a página com as imagens das sementes cortadas.
    generatePageWithImages = data["generatePageWithImages"]

    # Booleano responsável por saber se o embrião também será analisado.
    classificationYolo = data["classificationYolo"]

    model_path = ""
    if displayClassificationInfos:
        model_id = data["modelId"]
        model = db.session.query(Model).filter_by(id=model_id).first()
        model_path = model.path
    else:
        model = ""

    csv_file = process_data(
        user_id,
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
        seedsClassNumberInput,
    )
    return send_file(csv_file, "text/csv"), status.HTTP_200_OK


@process_bp.route("/pagination", methods=["POST"])
def pagination():
    data = request.json
    seeds_array_interno = []
    seeds_array_externo = []

    itens = data["itensPerPage"]
    page = data["page"]

    token = request.headers.get("token")
    user_id = extract_id(token)

    pagination_folder_per_id = "users_folders_imgs/{}{}".format(user_id, pagination_folder)
    seeds_images = os.listdir(pagination_folder_per_id)
    images_quant = len(seeds_images)

    for i in range((page - 1) * itens, ((page - 1) * itens + itens)):
        if i < (images_quant / 2):
            interno = cv2.imencode(
                ".jpg", cv2.imread(f"{pagination_folder_per_id}/Internal_seed_{i}.jpg")
            )[1]
            externo = cv2.imencode(
                ".jpg", cv2.imread(f"{pagination_folder_per_id}/External_seed_{i}.jpg")
            )[1]

            seeds_array_interno.append(str(base64.b64encode(interno)))
            seeds_array_externo.append(str(base64.b64encode(externo)))

    return (
        jsonify(
            {"internSeeds": seeds_array_interno, "externSeeds": seeds_array_externo}
        ),
        status.HTTP_200_OK,
    )


@process_bp.route("/embriao", methods=["GET"])
def embriao():

    token = request.headers.get("token")
    user_id = extract_id(token)

    embriao_folder_per_id = "users_folders_imgs/{}{}".format(user_id, embriao_folder)

    embrioes_names = os.listdir(embriao_folder_per_id)

    embrioes = []
    for image in embrioes_names:
        number = image[8]
        number = number + image[9] if image[9] != "." else number + ""
        number = (
            number + image[10] if image[10] != "." and image[10] != "j" else number + ""
        )
        number = int(number)
        embriao_atual = cv2.imread(embriao_folder_per_id + f"/semente-{number}.jpg")
        embrioes.append((number, embriao_atual))
        infosEmbriao = f"./users_folders_imgs/{user_id}/images/infosEmbriao"
        create_folder(infosEmbriao)
    csv_file = process_embriao(infosEmbriao, embrioes)

    return send_file(csv_file, "text/csv"), status.HTTP_200_OK
