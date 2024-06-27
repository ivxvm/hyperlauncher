import requests
import json
import constants
import localization
import settings

modpack_config_json = json.loads(requests.get(constants.MODPACKS_CONFIG_URL).text)

modpack_config_by_name = None
modpack_titles_by_locale = None
modpack_config_by_locale_and_title = None


def invalidate_modpacks():
    global modpack_config_by_name, modpack_titles_by_locale, modpack_config_by_locale_and_title
    modpack_config_by_name = {
        k: v for k, v in modpack_config_json.items()
        if not v.get("hidden") or settings.debug_mode == "True" and settings.username in v.get("maintainers")
    }
    modpack_titles_by_locale = {
        locale.name: [m['title'][locale.name]
                      for _, m in modpack_config_by_name.items()]
        for locale in localization.LOCALES
    }
    modpack_config_by_locale_and_title = {
        locale.name: {
            cfg['title'][locale.name]: {**cfg, 'name': name}
            for name, cfg in modpack_config_by_name.items()
        }
        for locale in localization.LOCALES
    }
