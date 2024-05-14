import time

from threading import Thread

import constants
import modpack


scheduled_timeout = 0


def game_log_printer_worker():
    global scheduled_timeout
    log_file = None
    while True:
        if scheduled_timeout > 0:
            time.sleep(scheduled_timeout)
            scheduled_timeout = 0
        modpack_process = modpack.current_modpack_process
        modpack_folder = modpack.get_modpack_folder(modpack.current_modpack_config)
        if modpack_process and modpack_folder:
            if modpack_process.poll() == None:
                if not log_file:
                    log_file = open(f'{modpack_folder}/logs/latest.log', 'r')
                while True:
                    line = log_file.readline()
                    if line:
                        print(line)
                    else:
                        break
            else:
                if log_file:
                    log_file.close()
                    log_file = None
        time.sleep(constants.GAME_LOG_PRINTER_WORKER_INTERVAL)


game_log_printer_thread = Thread(target=game_log_printer_worker, daemon=True)
game_log_printer_thread.start()
