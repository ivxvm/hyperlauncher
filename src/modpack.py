import os
import uuid
import subprocess
import git
import minecraft_launcher_lib

import constants
import settings


current_modpack_config = None
current_modpack_process = None
current_modpack_process_log = None


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


def get_modpack_folder(modpack_config):
    return modpack_config and os.path.expanduser(settings.working_folder + "/" +
                                                 modpack_config["directory_name"])


def ensure_modpack_installed(modpack_config):
    modpack_folder = os.path.expanduser(settings.working_folder + "/" + modpack_config["directory_name"])
    current_version_file = os.path.join(modpack_folder, "client-version.txt")
    should_download_client = True
    if os.path.isfile(current_version_file):
        with open(current_version_file, 'r') as file:
            current_client_version = file.read().replace('\n', '')
            if current_client_version == modpack_config["client_version"]:
                should_download_client = False
    if should_download_client:
        print(f'Installing minecraft client {modpack_config["client_version"]}')
        minecraft_launcher_lib.forge.install_forge_version(
            modpack_config["client_version"], modpack_folder, callback=PROGRESS_CB)
        with open(current_version_file, 'w') as file:
            file.write(modpack_config["client_version"])
    repo = git.Repo.init(modpack_folder)
    if len(repo.remotes) == 0:
        repo.create_remote("origin", modpack_config["repository_url"])
    print("Syncing modpack files")
    try:
        repo.git.add(".")
        repo.git.commit("-m", "Temp")
        repo.git.pull("origin", "main", "--rebase", "--autostash", "-X", "theirs")
        repo.git.reset("--soft", "HEAD~1")
    except Exception as e:
        print(e)


def start_modpack(modpack_config):
    global current_modpack_config, current_modpack_process, current_modpack_process_log
    print("Starting modpack")
    modpack_directory = os.path.expanduser(settings.working_folder + "/" + modpack_config["directory_name"])
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
        modpack_config["client_version"].replace("-", "-forge-"),
        modpack_directory,
        {
            "username": settings.username,
            "uid": uuid.uuid4().hex,
            "token": uuid.uuid4().hex,
            "jvmArguments": [
                "-Dminecraft.api.auth.host=https://nope.invalid",
                "-Dminecraft.api.account.host=https://nope.invalid",
                "-Dminecraft.api.session.host=https://nope.invalid",
                "-Dminecraft.api.services.host=https://nope.invalid",
                f"-Xms{settings.min_ram}M",
                f"-Xmx{settings.max_ram}M",
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
    current_modpack_config = modpack_config
    if current_modpack_process_log != None:
        current_modpack_process_log.close()
    current_modpack_process_log = open(f'{modpack_directory}/logs/process.log', 'w')
    current_modpack_process = subprocess.Popen(minecraft_command,
                                               cwd=modpack_directory,
                                               close_fds=True,
                                               stdout=current_modpack_process_log,
                                               stderr=current_modpack_process_log,
                                               creationflags=constants.DETACHED_PROCESS)
