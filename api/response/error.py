import datetime
from flask import jsonify


class Error:
    def __init__(self, msg: str, status: int):
        self.message = msg
        self.status = status
        self.timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


def error_response(msg, status):
    return (
        jsonify(Error(msg, status).__dict__),
        status,
    )
