import os
import ast

from easysettings import EasySettings

import constants

settings_file = EasySettings(os.path.expanduser(constants.LAUCNHER_CONFIG_FILE))


def save_utf8_value(key, value):
    return settings_file.setsave(key, str(value.encode('utf-8')))


def load_utf8_value(key):
    return ast.literal_eval(settings_file.get(key, "b''")).decode("utf-8")


username = load_utf8_value("username")
selected_modpack = None
token = None
skin_path = None


def reload_user_settings():
    global selected_modpack, token, skin_path
    selected_modpack = load_utf8_value(f"{username}_selected_modpack")
    token = load_utf8_value(f"{username}_token")
    skin_path = load_utf8_value(f"{username}_skin_path")


def set_username(value):
    global username
    username = value
    save_utf8_value("username", value)


def set_selected_modpack(value):
    global selected_modpack
    selected_modpack = value
    save_utf8_value(f"{username}_selected_modpack", value)


def set_token(value):
    global token
    token = value
    save_utf8_value(f"{username}_token", value)


def set_skin_path(value):
    global skin_path
    skin_path = value
    save_utf8_value(f"{username}_skin_path", value)


reload_user_settings()
