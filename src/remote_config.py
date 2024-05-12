import requests
import json
import constants
import localization

modpack_config_json = json.loads(requests.get(constants.MODPACKS_CONFIG_URL).text)
modpack_config_by_name = {k: v for k, v in modpack_config_json.items() if not v.get("hidden")}

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
