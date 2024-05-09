import requests
import dearpygui.dearpygui as dpg

import validators
import settings
import constants
import main_screen
import register_screen

LABEL_WIDTH = 100
PRIMARY_BUTTON_WIDTH = 106
SECONDARY_BUTTON_WIDTH = 252
ROW_OFFSET_Y = 40


def handle_login_click():
    username = dpg.get_value("tag:login/username")
    password = dpg.get_value("tag:login/password")

    if not validators.validate_username(username):
        return dpg.set_item_label("tag:login/error",
                                  f'Некоректний логін (має бути від 3 символів, може містити лише цифри, букви і _)')

    if not validators.validate_password(password):
        return dpg.set_item_label("tag:login/error",
                                  f'Некоректний пароль (має бути від 4 символів, не може містити пробіл)')

    response = requests.post(f'{constants.AUTH_SERVER_URL}/login',
                             json={"username": username,
                                   "password": password},
                             verify=not constants.IS_LOCALHOST)
    status_code = response.status_code
    if status_code == 200:
        settings.set_username(username)
        settings.reload_user_settings()
        settings.set_token(response.text)
        dpg.set_viewport_title(f"Hyperlauncher [{settings.username}]")
        dpg.delete_item("tag:login")
        main_screen.render_main_screen()
    else:
        error_text = ''
        match status_code:
            case 401:
                error_text = 'Невірний пароль'
            case 404:
                error_text = 'Користувача не знайдено'
            case _:
                error_text = 'Невідома помилка'
        dpg.set_item_label("tag:login/error", f'Помилка {status_code}: {error_text}')


def handle_register_click():
    dpg.delete_item("tag:login")
    register_screen.render_register_screen()


def render_login_screen():
    dpg.set_viewport_title(f"Hyperlauncher")
    with dpg.group(tag="tag:login", parent="tag:window"):
        dpg.add_image("tag:logo",
                      pos=[constants.WINDOW_WIDTH / 2 - constants.LOGO_WIDTH / 2,
                           constants.LOGO_OFFSET_TOP])
        x = constants.WINDOW_WIDTH / 2 - constants.LOGO_WIDTH / 2
        y = constants.LOGO_OFFSET_TOP + constants.LOGO_HEIGHT + ROW_OFFSET_Y
        dpg.add_text("Нікнейм", pos=[x, y])
        dpg.add_input_text(tag="tag:login/username",
                           width=constants.LOGO_WIDTH - LABEL_WIDTH,
                           pos=[x + LABEL_WIDTH, y],
                           default_value=settings.username,
                           on_enter=True,
                           callback=lambda: dpg.focus_item("tag:login/password"))
        y += ROW_OFFSET_Y
        dpg.add_text("Пароль", pos=[x, y])
        dpg.add_input_text(tag="tag:login/password",
                           password=True,
                           width=constants.LOGO_WIDTH - LABEL_WIDTH,
                           pos=[x + LABEL_WIDTH, y],
                           on_enter=True,
                           callback=handle_login_click)
        y += ROW_OFFSET_Y
        dpg.add_button(
            label="[Увійти]",
            width=PRIMARY_BUTTON_WIDTH,
            pos=[constants.WINDOW_WIDTH / 2 - PRIMARY_BUTTON_WIDTH / 2, y],
            callback=handle_login_click)
        y += ROW_OFFSET_Y
        error_button = dpg.add_button(label="",
                                      tag="tag:login/error",
                                      pos=[0, y],
                                      width=constants.WINDOW_WIDTH)
        dpg.bind_item_theme(error_button, "theme:error_text")
        secondary_button = dpg.add_button(
            label="[Зареєструватись]",
            width=SECONDARY_BUTTON_WIDTH,
            pos=[constants.WINDOW_WIDTH / 2 - SECONDARY_BUTTON_WIDTH / 2,
                 constants.WINDOW_HEIGHT - ROW_OFFSET_Y * 2],
            callback=handle_register_click)
        dpg.bind_item_theme(secondary_button, "theme:hyperlink")
