import requests
import os

import constants


def download_file(url, path):
    with requests.get(url, stream=True, verify=not constants.IS_LOCALHOST) as r:
        r.raise_for_status()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
