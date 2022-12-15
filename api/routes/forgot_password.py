from flask import Blueprint, request, jsonify
from flask_api import status
from api.services.email_validator import check
from api.response.error import error_response
from config import db
from db.models import User

forgot_password_bp = Blueprint(
    "forgot_password", __name__, url_prefix="/api/v1/forgot-password"
)


@forgot_password_bp.route("", methods=["POST"])
def register():
    content_type = request.headers.get("Content-Type")
    if "application/json" not in content_type:
        return error_response(
            "Media-type não suportado", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )

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

    user_with_email = db.session.query(User).filter_by(email=email, role="USER").first()
    if user_with_email is None:
        return error_response("Usuário não encontrado", status.HTTP_401_UNAUTHORIZED)

    user_with_email.change_password(password)
    db.session.commit()

    return "", status.HTTP_200_OK
