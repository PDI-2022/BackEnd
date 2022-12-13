import jwt
from api.constants.secret import secret
from datetime import datetime, timezone, timedelta
from db.models import User


def generate(usr: User):
    user_data = {"id": usr.id, "email": usr.email, "role": usr.role}
    return jwt.encode(
        {
            "user_data": user_data,
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=3600),
        },
        secret,
        algorithm="HS256",
    )


def extract_role(token) -> str:
    decoded = jwt.decode(token, secret, algorithms=["HS256"])
    return decoded["user_date"]["role"]


def validate(token):
    try:
        decode = jwt.decode(token, secret, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        return False,""
    return True,decode["user_data"]["role"]
