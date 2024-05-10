import time

from threading import Thread

import constants

latest_modpack_folder = None
latest_game_process = None
scheduled_timeout = 0


def game_log_printer_worker():
    global scheduled_timeout
    log_file = None
    while True:
        if scheduled_timeout > 0:
            time.sleep(scheduled_timeout)
            scheduled_timeout = 0
        if latest_game_process and latest_modpack_folder:
            if latest_game_process.poll() == None:
                if not log_file:
                    log_file = open(f'{latest_modpack_folder}/logs/latest.log', 'r')
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
