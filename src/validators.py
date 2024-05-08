import re


def validate_username(value: str):
    return len(value) >= 3 and re.match('^[0-9a-zA-Z_]+$', value)


def validate_password(value: str):
    return len(value) >= 4 and not re.match('\s', value)
