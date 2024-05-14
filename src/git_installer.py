import os
import time
import subprocess
import git

from threading import Thread

import constants
import utils


def check_git_installed():
    try:
        git.Repo.init(os.path.expanduser(f"~/hyperlauncher-bare-repo"), bare=True)
    except git.exc.GitCommandNotFound:
        return False
    return True


def setup_git_installed_watcher(process):
    def watcher():
        while process.poll() == None:
            time.sleep(constants.GIT_WATCHER_INTERVAL)
        os._exit(1)
    thread = Thread(target=watcher, daemon=True)
    thread.start()


def download_and_install_git():
    def worker():
        basename = os.path.basename(constants.GIT_WINDOWS_URL)
        installer_save_path = os.path.expanduser(f"~/Downloads/{basename}")
        utils.download_file(constants.GIT_WINDOWS_URL, installer_save_path)
        setup_git_installed_watcher(
            subprocess.Popen(installer_save_path,
                             close_fds=True,
                             creationflags=constants.DETACHED_PROCESS))
    thread = Thread(target=worker, daemon=True)
    thread.start()
