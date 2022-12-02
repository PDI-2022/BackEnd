from flask import Blueprint, request
from flask_api import status
from api.services.token import validate

auth_bp = Blueprint("authenticate", __name__, url_prefix="/api/v1/authenticate")


@auth_bp.route("", methods=["POST"])
def auth():
    content_type = request.headers.get("Content-Type")
    if "application/json" not in content_type:
        return "Content-Type not supported", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    data = request.json
    if "token" not in data:
        return "O campo token é obrigatório", status.HTTP_400_BAD_REQUEST

    token = data["token"]
    if token is None or token == "":
        return "O campo token é obrigatório", status.HTTP_400_BAD_REQUEST

    if not validate(token):
        return "Usuário não autorizado", status.HTTP_401_UNAUTHORIZED

    return "", status.HTTP_200_OK
