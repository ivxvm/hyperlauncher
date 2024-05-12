import dearpygui.dearpygui as dpg

import constants
import settings
import localization
import login_screen

ROW_OFFSET_Y = 40


def handle_locale_select(_, data):
    settings.set_locale(localization.locale_name_by_title[data])
    dpg.delete_item("tag:locale")
    login_screen.render_login_screen()


def render_locale_screen():
    with dpg.group(tag="tag:locale", parent="tag:window"):
        dpg.add_image("tag:logo",
                      pos=[constants.WINDOW_WIDTH / 2 - constants.LOGO_WIDTH / 2,
                           constants.LOGO_OFFSET_TOP])
        x = constants.WINDOW_WIDTH / 2 - constants.LOGO_WIDTH / 2
        y = constants.LOGO_OFFSET_TOP + constants.LOGO_HEIGHT + ROW_OFFSET_Y
        dpg.add_listbox(items=[locale.title for locale in localization.LOCALES],
                        num_items=2,
                        default_value="",
                        width=constants.LOGO_WIDTH,
                        pos=[x, y],
                        callback=handle_locale_select)
