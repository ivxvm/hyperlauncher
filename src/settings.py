import os
import ast

from easysettings import EasySettings

import constants

settings_file = EasySettings(os.path.expanduser(constants.LAUCNHER_CONFIG_FILE))
saved_nickname = ast.literal_eval(settings_file.get("nickname", "b''")).decode("utf-8")
saved_selected_modpack = ast.literal_eval(settings_file.get("selected_modpack", "b''")).decode("utf-8")
