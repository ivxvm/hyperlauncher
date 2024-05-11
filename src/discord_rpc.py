import time

from threading import Thread
from pypresence import Presence

import constants

RPC_STATE_NONE = "RPC_STATE_NONE"
RPC_STATE_MENU = "RPC_STATE_MENU"
RPC_STATE_GAME = "RPC_STATE_GAME"

rpc_state = RPC_STATE_NONE
rpc_data = {"large_image": "hypercube-logo"}

latest_modpack_title = None
latest_game_process = None

rpc = Presence(constants.DISCORD_CLIENT_ID)


def presence_worker():
    global rpc_state, rpc_data
    while True:
        try:
            rpc.connect()
        except:
            time.sleep(constants.DISCORD_PRESENCE_WORKER_INTERVAL)
            continue
        while True:
            new_rpc_state = rpc_state
            if latest_game_process and latest_game_process.poll() == None:
                new_rpc_state = RPC_STATE_GAME
                rpc_data["details"] = f'Грає в збірку "{latest_modpack_title}"'
            else:
                new_rpc_state = RPC_STATE_MENU
                rpc_data["details"] = "В меню лаунчера"
            if new_rpc_state != rpc_state:
                rpc_data["start"] = int(time.time())
                rpc_state = new_rpc_state
            rpc.update(**rpc_data)
            time.sleep(constants.DISCORD_PRESENCE_WORKER_INTERVAL)


presence_worker_thread = Thread(target=presence_worker, daemon=True)
presence_worker_thread.start()
