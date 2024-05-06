import requests
import json
import constants

modpacks_config = json.loads(requests.get(constants.MODPACKS_CONFIG_URL).text)
modpack_titles = [m['title'] for _, m in modpacks_config.items()]
modpack_config_by_title = {cfg['title']: {
    **cfg, 'name': name} for name, cfg in modpacks_config.items()}
