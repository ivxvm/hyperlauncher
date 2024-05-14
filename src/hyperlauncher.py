from os import path

import ctypes
import requests
import dearpygui.dearpygui as dpg
import discord_rpc as _

import settings
import constants
import locale_screen
import login_screen
import main_screen
import git_install_screen
import git_installer

FONT_PATH = path.join(path.dirname(__file__), "assets/Minecraft_1.1.ttf")
LOGO_PATH = path.join(path.dirname(__file__), "assets/logo.png")
ICON_PATH = path.join(path.dirname(__file__), "assets/icon.ico")


def main():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    dpg.create_context()
    dpg.create_viewport(title="Hyperlauncher",
                        resizable=False,
                        small_icon=ICON_PATH,
                        large_icon=ICON_PATH,
                        width=constants.WINDOW_WIDTH,
                        height=constants.WINDOW_HEIGHT,
                        x_pos=int(screensize[0] / 2 -
                                  constants.WINDOW_WIDTH / 2),
                        y_pos=int(screensize[1] / 2 - constants.WINDOW_HEIGHT / 2))
    dpg.setup_dearpygui()

    with dpg.font_registry():
        with dpg.font(FONT_PATH, size=20) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.bind_font(font)

    with dpg.texture_registry():
        width, height, _, data = dpg.load_image(LOGO_PATH)
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="tag:logo")

    with dpg.theme(tag="theme:hyperlink"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 0, 0, 0])
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, [29, 151, 236, 25])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [29, 151, 236])

    with dpg.theme(tag="theme:error_text"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 0, 0, 0])
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, [0, 0, 0, 0])
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, [0, 0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [243, 109, 116])

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            for component, color in constants.MAIN_THEME_COLORS:
                dpg.add_theme_color(component, color, category=dpg.mvThemeCat_Core)
        with dpg.theme_component(dpg.mvButton):
            for component, color in constants.MAIN_THEME_BUTTON_COLORS:
                dpg.add_theme_color(component, color)
        with dpg.theme_component(dpg.mvListbox):
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 6)

    dpg.bind_theme(global_theme)

    # dpg.show_style_editor()

    dpg.add_window(tag="tag:window")
    dpg.set_primary_window("tag:window", True)

    try:
        login_response = requests.post(f'{constants.AUTH_SERVER_URL}/login',
                                       json={"username": settings.username,
                                             "token": settings.token},
                                       verify=not constants.IS_LOCALHOST)

        if login_response.status_code == 200:
            dpg.set_viewport_title(f"Hyperlauncher [{settings.username}]")
            settings.reload_user_settings()
            settings.set_token(login_response.text)

        if settings.locale:
            if login_response.status_code == 200:
                if git_installer.check_git_installed():
                    main_screen.render_main_screen()
                else:
                    git_install_screen.render_git_install_screen()
            else:
                login_screen.render_login_screen()
        else:
            locale_screen.render_locale_screen()
    except:
        with dpg.group(tag="tag:connection_error", parent="tag:window"):
            y = constants.WINDOW_HEIGHT / 2 - 32
            for message in ["Не вдалося підключитися до сервера!",
                            "Error connecting to the server!"]:
                error_button = dpg.add_button(label=message,
                                              pos=[0, y],
                                              width=constants.WINDOW_WIDTH)
                dpg.bind_item_theme(error_button, "theme:error_text")
                y += 64

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
