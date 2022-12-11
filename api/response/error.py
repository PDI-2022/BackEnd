import datetime


class Error:
    def __init__(self, msg: str, status: int):
        self.message = msg
        self.status = status
        self.timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
