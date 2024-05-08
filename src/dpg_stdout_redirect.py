import sys
import dearpygui.dearpygui as dpg

import constants

log_window_id = None
original_stdout = sys.stdout


class DpgOutput():
    def flush(**args):
        pass

    def write(self, text: str):
        stripped_text = text.strip()
        if len(stripped_text) > 0:
            try:
                dpg.set_value("tag:main/log_header", True)
                dpg.add_text(stripped_text,
                             parent=log_window_id,
                             wrap=constants.WINDOW_WIDTH - 100)
                dpg.set_y_scroll(
                    log_window_id, -1.0)
            except:
                original_stdout.write(stripped_text)
                original_stdout.write('\n')


sys.stdout = DpgOutput()
