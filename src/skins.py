import requests
import hashlib
import os
import shutil

import constants
import utils


def sync_own_skin(username, token, skin_path, skins_folder):
    if not skin_path:
        return
    print("Syncing own skin")
    if not os.path.isfile(skin_path):
        return print("Specified skin file is missing")
    os.makedirs(skins_folder, exist_ok=True)
    shutil.copyfile(skin_path, f"{skins_folder}/{username}.png")
    checksum = get_file_md5(skin_path)
    response = requests.get(
        f'{constants.AUTH_SERVER_URL}/skin-needs-upload?username={username}&checksum={checksum}',
        verify=not constants.IS_LOCALHOST)
    status_code = response.status_code
    if status_code == 200:
        skin_needs_upload = response.json()
        if skin_needs_upload:
            print("Uploading own skin")
            response = requests.post(f'{constants.AUTH_SERVER_URL}/skin',
                                     files={"skin": open(skin_path, 'rb')},
                                     headers={"Authorization": token},
                                     verify=not constants.IS_LOCALHOST)
            status_code = response.status_code
            if status_code != 200:
                print(f"Failed to upload skin, status code: {status_code}")
    else:
        print(f"Failed to sync own skin, status code: {status_code}")


def sync_skins(skins_folder):
    print("Syncing remote skins")
    response = requests.get(f'{constants.AUTH_SERVER_URL}/skins',
                            verify=not constants.IS_LOCALHOST)
    status_code = response.status_code
    if status_code == 200:
        for entry in response.json():
            username = entry["username"]
            remote_skin_checksum = entry.get("skinChecksum")
            if remote_skin_checksum:
                should_download_remote_skin = True
                local_skin_filename = f"{skins_folder}/{username}.png"
                if os.path.isfile(local_skin_filename):
                    local_skin_checksum = get_file_md5(local_skin_filename)
                    if remote_skin_checksum == local_skin_checksum:
                        should_download_remote_skin = False
                if should_download_remote_skin:
                    print(f"Syncing skin for {username}")
                    utils.download_file(f'{constants.AUTH_SERVER_URL}/skin?username={username}', local_skin_filename)
    else:
        print(f"Failed to sync remote skins, status code: {status_code}")


def get_file_md5(path):
    hash = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hash.update(chunk)
    return hash.hexdigest()
