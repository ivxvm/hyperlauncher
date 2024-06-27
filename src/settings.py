import os
import ast

from easysettings import EasySettings

import constants

###############################################################################


settings_file = EasySettings(os.path.expanduser(constants.LAUCNHER_CONFIG_FILE))


def save_utf8_value(key, value):
    return settings_file.setsave(key, str(value.encode('utf-8')))


def load_utf8_value(key):
    return ast.literal_eval(settings_file.get(key, "b''")).decode("utf-8")


def global_setter(name):
    def set_value(value):
        globals()[name] = value
        save_utf8_value(name, value)
    return set_value


def global_cleaner(name):
    def clear_value():
        globals()[name] = None
        settings_file.remove(name)
        settings_file.save()
    return clear_value


###############################################################################


username = load_utf8_value("username")
working_folder = load_utf8_value("working_folder") or "~"
locale = load_utf8_value("locale")
debug_mode = load_utf8_value("debug_mode")

set_username = global_setter("username")
set_working_folder = global_setter("working_folder")
set_locale = global_setter("locale")
clear_locale = global_cleaner("locale")
set_debug_mode = global_setter("debug_mode")


###############################################################################


selected_modpack = None
token = None
skin_path = None


def reload_user_settings():
    global selected_modpack, token, skin_path
    selected_modpack = load_utf8_value(f"{username}_selected_modpack")
    token = load_utf8_value(f"{username}_token")
    skin_path = load_utf8_value(f"{username}_skin_path")


def user_scoped_setter(name):
    def set_value(value):
        globals()[name] = value
        save_utf8_value(f"{username}_{name}", value)
    return set_value


set_selected_modpack = user_scoped_setter("selected_modpack")
set_token = user_scoped_setter("token")
set_skin_path = user_scoped_setter("skin_path")


###############################################################################


min_ram = None
max_ram = None


def reload_modpack_settings():
    global min_ram, max_ram
    min_ram = settings_file.get(f"{selected_modpack}_min_ram", constants.DEFAULT_MIN_RAM)
    max_ram = settings_file.get(f"{selected_modpack}_max_ram", constants.DEFAULT_MAX_RAM)


def modpack_scoped_setter(name):
    def set_value(value):
        print(f"{selected_modpack}_{name}", name, value)
        globals()[name] = value
        settings_file.setsave(f"{selected_modpack}_{name}", value)
    return set_value


set_min_ram = modpack_scoped_setter("min_ram")
set_max_ram = modpack_scoped_setter("max_ram")


###############################################################################


reload_user_settings()
reload_modpack_settings()
