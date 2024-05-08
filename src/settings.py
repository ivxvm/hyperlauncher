import os
import ast

from easysettings import EasySettings

import constants

settings_file = EasySettings(os.path.expanduser(constants.LAUCNHER_CONFIG_FILE))


def save_utf8_value(key, value):
    return settings_file.setsave(key, str(value.encode('utf-8')))


def load_utf8_value(key):
    return ast.literal_eval(settings_file.get(key, "b''")).decode("utf-8")


saved_username = load_utf8_value("username")
saved_selected_modpack = load_utf8_value("selected_modpack")
saved_token = load_utf8_value("token")


def set_username(value):
    global saved_username
    saved_username = value
    save_utf8_value("username", value)


def set_token(value):
    global saved_token
    saved_token = value
    save_utf8_value("token", value)
