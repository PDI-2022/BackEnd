import jwt
from api.constants.secret import secret
from datetime import datetime, timezone, timedelta


def generate(email: str, id: int):
    user_data = {"id": id, "email": email}
    return jwt.encode(
        {
            "user_data": user_data,
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=3600),
        },
        secret,
        algorithm="HS256",
    )


def validate(token) -> bool:
    try:
        jwt.decode(token, secret, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        return False
    return True
