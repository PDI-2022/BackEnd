from flask import Blueprint, request, jsonify
from flask_api import status
from api.services.token import validate
from api.response.error import error_response


auth_bp = Blueprint("authenticate", __name__, url_prefix="/api/v1/authenticate")


@auth_bp.route("", methods=["POST"])
def auth():
    content_type = request.headers.get("Content-Type")
    if "application/json" not in content_type:
        return error_response(
            "Media-type não suportado", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )

    data = request.json
    if "token" not in data:
        return error_response(
            "O campo token é obrigatório", status.HTTP_400_BAD_REQUEST
        )

    token = data["token"]
    if token is None or token == "":
        return error_response(
            "O campo token é obrigatório", status.HTTP_400_BAD_REQUEST
        )

    if not validate(token):
        return error_response("Usuário não encontrado", status.HTTP_401_UNAUTHORIZED)

    return "", status.HTTP_200_OK
