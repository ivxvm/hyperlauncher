import os
import subprocess
import uuid
import git
import minecraft_launcher_lib
import dearpygui.dearpygui as dpg

import constants

###############################################################################


class CustomRemoteProgress(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(
            op_code,
            cur_count,
            max_count,
            cur_count / (max_count or 100.0),
            message or "NO MESSAGE",
        )


current_max = 0


def set_status(status: str):
    print(status)


def set_progress(progress: int):
    if current_max != 0:
        print(f"{progress}/{current_max}")


def set_max(new_max: int):
    global current_max
    current_max = new_max


PROGRESS_CB = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}

###############################################################################


def ensure_modpack_installed(cfg):
    modpack_directory = os.path.expanduser(cfg["directory_path"])
    current_version_file = os.path.join(
        modpack_directory, "client-version.txt")
    should_download_client = True
    if os.path.isfile(current_version_file):
        with open(current_version_file, 'r') as file:
            current_client_version = file.read().replace('\n', '')
            if current_client_version == cfg["client_version"]:
                should_download_client = False
    if should_download_client:
        minecraft_launcher_lib.forge.install_forge_version(
            cfg["client_version"], modpack_directory, callback=PROGRESS_CB)
        with open(current_version_file, 'w') as file:
            file.write(cfg["client_version"])
    repo = git.Repo.init(modpack_directory)
    origin = None
    if len(repo.remotes) == 0:
        origin = repo.create_remote("origin", cfg["repository_url"])
    else:
        origin = repo.remotes[0]
    for fetch_info in origin.fetch(progress=CustomRemoteProgress()):
        print("Updated %s to %s" % (fetch_info.ref, fetch_info.commit))
    repo.create_head("main", origin.refs.main)
    repo.heads.main.set_tracking_branch(origin.refs.main)
    repo.heads.main.checkout()
    # repo.head.reset(index=True, working_tree=True)


def start_modpack(cfg):
    modpack_directory = os.path.expanduser(cfg["directory_path"])
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
        cfg["client_version"].replace("-", "-forge-"),
        modpack_directory,
        {
            "username": dpg.get_value("tag:main/username"),
            "uid": uuid.uuid4().hex,
            "token": "",
            "jvmArguments": [
                "-Xms4G",
                "-Xmx8G",
                "-XX:+UseG1GC",
                "-XX:+ParallelRefProcEnabled",
                "-XX:MaxGCPauseMillis=200",
                "-XX:+UnlockExperimentalVMOptions",
                "-XX:+DisableExplicitGC",
                "-XX:+AlwaysPreTouch",
                "-XX:G1NewSizePercent=30",
                "-XX:G1MaxNewSizePercent=40",
                "-XX:G1HeapRegionSize=8M",
                "-XX:G1ReservePercent=20",
                "-XX:G1HeapWastePercent=5",
                "-XX:G1MixedGCCountTarget=4",
                "-XX:InitiatingHeapOccupancyPercent=15",
                "-XX:G1MixedGCLiveThresholdPercent=90",
                "-XX:G1RSetUpdatingPauseTimePercent=5",
                "-XX:SurvivorRatio=32",
                "-XX:+PerfDisableSharedMem",
                "-XX:MaxTenuringThreshold=1"
            ]
        })
    subprocess.Popen(minecraft_command,
                     cwd=modpack_directory,
                     close_fds=True,
                     creationflags=constants.DETACHED_PROCESS)
