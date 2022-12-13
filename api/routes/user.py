from flask import Blueprint, request, jsonify
from flask_api import status
from api.services.email_validator import check
from api.response.error import error_response
from api.response.pagination import Pagination
from config import db
from db.models import User

user_bp = Blueprint("user", __name__, url_prefix="/api/v1/users")


def validate_content_type(request):
    content_type = request.headers.get("Content-Type")
    if "application/json" not in content_type:
        return (
            False,
            error_response(
                "Media-type não suportado", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            ),
        )
    return True, {}, 0


@user_bp.route("", methods=["POST"])
def register():
    valid, response, errorStatus = validate_content_type(request)
    if not valid:
        return response, errorStatus

    data = request.json

    if "user" not in data:
        return error_response(
            "O campo usuário é obrigatório", status.HTTP_400_BAD_REQUEST
        )

    email = data["user"]
    if email is None or email == "":
        return error_response(
            "O campo usuário é obrigatório", status.HTTP_400_BAD_REQUEST
        )

    if not check(email):
        return error_response(
            "O email submetido não é válido", status.HTTP_400_BAD_REQUEST
        )

    if "password" not in data:
        return error_response(
            "O campo senha é obrigatório", status.HTTP_400_BAD_REQUEST
        )

    password = data["password"]
    if password is None or password == "":
        return error_response(
            "O campo senha é obrigatório", status.HTTP_400_BAD_REQUEST
        )

    user_with_email = db.session.query(User).filter_by(email=email).first()
    if user_with_email is not None:
        return error_response(
            "O email submetido já está registrado", status.HTTP_400_BAD_REQUEST
        )

    new_user = User(email, password)
    db.session.add(new_user)
    db.session.commit()
    return new_user.serialize(), status.HTTP_201_CREATED


@user_bp.route("", methods=["GET"])
def list_paginate():
    offset = request.args.get("offset", type=int)
    limit = request.args.get("limit", type=int)

    if not limit and not offset:
        users = User.query.filter_by(role="USER").all()
        response = list()
        for user in users:
            response.append(user.serialize())
        return jsonify(response), status.HTTP_200_OK

    results = User.query.filter_by(role="USER").paginate(
        page=offset, per_page=limit, error_out=False
    )
    total = User.query.count()
    response = Pagination(results, offset, limit, total).__dict__
    return jsonify(response), status.HTTP_200_OK


@user_bp.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    user = User.query.filter_by(id=id, role="USER").first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return "", status.HTTP_200_OK
    return error_response("Usuário não encontrado", status.HTTP_404_NOT_FOUND)


@user_bp.route("/<int:id>", methods=["PATCH"])
def update(id: int):
    valid, response, errorStatus = validate_content_type(request)
    if not valid:
        return response, errorStatus

    data = request.json
    user = User.query.filter_by(id=id, role="USER").first()
    if not user:
        return error_response("Usuário não encontrado", status.HTTP_404_NOT_FOUND)

    email = data["user"]
    if email is not None or email != "":
        if not check(email):
            return error_response(
                "O email submetido não é válido", status.HTTP_400_BAD_REQUEST
            )
        user.email = email

    password = data["password"]
    if password is not None or password != "":
        user.change_password(password)

    db.session.commit()
    return "", status.HTTP_200_OK
