from flask import Blueprint, jsonify, request
from flask_api import status
from api.constants.folders import models_folder
from api.services.storage import decompress_and_save, delete_folder
from api.response.pagination import Pagination
from api.response.error import Error
from config import db
from db.models import Model

model_bp = Blueprint("model", __name__, url_prefix="/api/v1/models")


@model_bp.route("", methods=["POST"])
def create():
    content_type = request.headers.get("Content-Type")
    if "multipart/form-data" not in content_type:
        return (
            jsonify(
                Error(
                    "Media-type não suportado", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                ).__dict__
            ),
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )

    model_name = request.form.get("name")
    if model_name == "" or model_name is None:
        return (
            jsonify(
                Error(
                    "Nome do modelo é obrigatório", status.HTTP_400_BAD_REQUEST
                ).__dict__
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    model_description = request.form.get("description")
    if model_description == "" or model_description is None:
        return (
            jsonify(
                Error(
                    "Descrição do modelo é obrigatória", status.HTTP_400_BAD_REQUEST
                ).__dict__
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    model_compressed_file = request.files.get("model")
    filename = model_compressed_file.name
    if filename == "":
        return (
            jsonify(
                Error(
                    "Arquivo contendo o modelo é obrigatório",
                    status.HTTP_400_BAD_REQUEST,
                ).__dict__
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    model_path = decompress_and_save(
        models_folder,
        model_compressed_file.stream._file,
        model_compressed_file.filename,
    )
    new_model = Model(model_name, model_path, model_description)
    db.session.add(new_model)
    db.session.commit()

    return "", status.HTTP_201_CREATED


@model_bp.route("", methods=["GET"])
def list_paginate():
    offset = request.args.get("offset", type=int)
    limit = request.args.get("limit", type=int)

    if not limit and not offset:
        models = Model.query.all()
        response = list()
        for model in models:
            response.append(model.serialize())
        return jsonify(response), status.HTTP_200_OK

    results = Model.query.paginate(page=offset, per_page=limit, error_out=False)
    total = Model.query.count()
    response = Pagination(results, offset, limit, total).__dict__
    return jsonify(response), status.HTTP_200_OK


@model_bp.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    model = Model.query.filter_by(id=id).first()
    if model:
        delete_folder(model.path)
        db.session.delete(model)
        db.session.commit()
        return "", status.HTTP_200_OK
    return (
        jsonify(Error("Modelo não encontrado", status.HTTP_404_NOT_FOUND).__dict__),
        status.HTTP_404_NOT_FOUND,
    )
