import re
from api.constants.email_validator import regex


def check(email):
    return re.fullmatch(regex, email)
