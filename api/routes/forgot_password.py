from flask import Blueprint, request, jsonify
from flask_api import status
from api.services.email_validator import check
from api.response.error import Error
from config import db
from db.models import User

forgot_password_bp = Blueprint(
    "forgot_password", __name__, url_prefix="/api/v1/forgot-password"
)


@forgot_password_bp.route("", methods=["POST"])
def register():
    content_type = request.headers.get("Content-Type")
    if "application/json" not in content_type:
        return (
            jsonify(
                Error(
                    "Media-type não suportado", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                ).__dict__
            ),
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )

    data = request.json

    if "user" not in data:
        return (
            jsonify(
                Error(
                    "O campo usuário é obrigatório", status.HTTP_400_BAD_REQUEST
                ).__dict__
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    email = data["user"]
    if email is None or email == "":
        return (
            jsonify(
                Error(
                    "O campo usuário é obrigatório", status.HTTP_400_BAD_REQUEST
                ).__dict__
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    if not check(email):
        return (
            jsonify(
                Error(
                    "O email submetido não é válido", status.HTTP_400_BAD_REQUEST
                ).__dict__
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    if "password" not in data:
        return (
            jsonify(
                Error(
                    "O campo senha é obrigatório", status.HTTP_400_BAD_REQUEST
                ).__dict__
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    password = data["password"]
    if password is None or password == "":
        return (
            jsonify(
                Error(
                    "O campo senha é obrigatório", status.HTTP_400_BAD_REQUEST
                ).__dict__
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    user_with_email = db.session.query(User).filter_by(email=email, role="USER").first()
    if user_with_email is None:
        return (
            jsonify(
                Error("Usuário não encontrado", status.HTTP_401_UNAUTHORIZED).__dict__
            ),
            status.HTTP_401_UNAUTHORIZED,
        )

    user_with_email.change_password(password)
    db.session.commit()

    return "", status.HTTP_200_OK
