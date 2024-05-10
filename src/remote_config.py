import requests
import json
import constants

modpack_config_json = json.loads(requests.get(constants.MODPACKS_CONFIG_URL).text)
modpack_config_by_name = {k: v for k, v in modpack_config_json.items() if not v.get("hidden")}
modpack_titles = [m['title'] for _, m in modpack_config_by_name.items()]
modpack_config_by_title = {cfg['title']: {
    **cfg, 'name': name} for name, cfg in modpack_config_by_name.items()}
