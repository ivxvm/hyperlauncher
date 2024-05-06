import dearpygui.dearpygui as dpg

import settings
import main_screen


def handle_login_click():
    dpg.delete_item("tag:login")
    main_screen.render_main_screen()


def render_login_screen():
    with dpg.window(tag="tag:login", pos=[9999, 0]):
        dpg.set_primary_window("tag:login", True)
        with dpg.group(horizontal=True):
            dpg.add_text("Нікнейм")
            dpg.add_input_text(tag="tag:login/nickname", default_value=settings.saved_nickname)
        with dpg.group(horizontal=True):
            dpg.add_text("Пароль")
            dpg.add_input_text(tag="tag:login/password")
        dpg.add_button(label="Увійти", callback=handle_login_click)
