import requests
import dearpygui.dearpygui as dpg

import validators
import settings
import constants
import login_screen
import main_screen

LABEL_WIDTH = 128
PRIMARY_BUTTON_WIDTH = 256
SECONDARY_BUTTON_WIDTH = 384
ROW_OFFSET_Y = 40


def handle_register_click():
    username = dpg.get_value("tag:register/username")
    password = dpg.get_value("tag:register/password")
    password_confirmation = dpg.get_value("tag:register/password_confirmation")

    if not validators.validate_username(username):
        return dpg.set_item_label("tag:register/error",
                                  f'Некоректний логін (має бути від 3 символів, може містити лише цифри, букви і _)')

    if not validators.validate_password(password):
        return dpg.set_item_label("tag:register/error",
                                  f'Некоректний пароль (має бути від 4 символів, не може містити пробіл)')

    if password != password_confirmation:
        return dpg.set_item_label("tag:register/error",
                                  f'Паролі не співпадають')

    response = requests.post(f'{constants.AUTH_SERVER_URL}/register',
                             json={"username": username,
                                   "password": password},
                             verify=not constants.IS_LOCALHOST)
    status_code = response.status_code
    if status_code == 200:
        settings.set_token(response.text)
        settings.set_username(username)
        dpg.delete_item("tag:register")
        main_screen.render_main_screen()
    else:
        error_text = ''
        match status_code:
            case 409:
                error_text = 'Користувач вже існує'
            case _:
                error_text = 'Невідома помилка'
        dpg.set_item_label("tag:register/error", error_text)


def handle_login_click():
    dpg.delete_item("tag:register")
    login_screen.render_login_screen()


def render_register_screen():
    with dpg.group(tag="tag:register", parent="tag:window"):
        dpg.add_image("tag:logo",
                      pos=[constants.WINDOW_WIDTH / 2 - constants.LOGO_WIDTH / 2,
                           constants.LOGO_OFFSET_TOP])
        x = constants.WINDOW_WIDTH / 2 - constants.LOGO_WIDTH / 2
        y = constants.LOGO_OFFSET_TOP + constants.LOGO_HEIGHT + ROW_OFFSET_Y
        dpg.add_text("Нікнейм", pos=[x, y])
        dpg.add_input_text(tag="tag:register/username",
                           width=constants.LOGO_WIDTH - LABEL_WIDTH,
                           pos=[x + LABEL_WIDTH, y],
                           default_value=settings.username,
                           on_enter=True,
                           callback=lambda: dpg.focus_item("tag:register/password"))
        y += ROW_OFFSET_Y
        dpg.add_text("Пароль", pos=[x, y])
        dpg.add_input_text(tag="tag:register/password",
                           password=True,
                           width=constants.LOGO_WIDTH - LABEL_WIDTH,
                           pos=[x + LABEL_WIDTH, y],
                           on_enter=True,
                           callback=lambda: dpg.focus_item("tag:register/password_confirmation"))
        y += ROW_OFFSET_Y
        dpg.add_text("Пароль ^2", pos=[x, y])
        dpg.add_input_text(tag="tag:register/password_confirmation",
                           password=True,
                           width=constants.LOGO_WIDTH - LABEL_WIDTH,
                           pos=[x + LABEL_WIDTH, y],
                           on_enter=True,
                           callback=handle_register_click)
        y += ROW_OFFSET_Y
        dpg.add_button(label="[Зареєструватись]",
                       width=PRIMARY_BUTTON_WIDTH,
                       pos=[constants.WINDOW_WIDTH / 2 - PRIMARY_BUTTON_WIDTH / 2, y],
                       callback=handle_register_click)
        y += ROW_OFFSET_Y
        error_button = dpg.add_button(label="",
                                      tag="tag:register/error",
                                      pos=[0, y],
                                      width=constants.WINDOW_WIDTH)
        dpg.bind_item_theme(error_button, "theme:error_text")
        secondary_button = dpg.add_button(
            label="[Увійти з існуючим аккаунтом]",
            width=SECONDARY_BUTTON_WIDTH,
            pos=[constants.WINDOW_WIDTH / 2 - SECONDARY_BUTTON_WIDTH / 2,
                 constants.WINDOW_HEIGHT - ROW_OFFSET_Y * 2],
            callback=handle_login_click)
        dpg.bind_item_theme(secondary_button, "theme:hyperlink")
