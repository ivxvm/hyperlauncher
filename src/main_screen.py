import dearpygui.dearpygui as dpg
import webbrowser

from constants import *

import settings
import remote_config
import modpack
import dpg_stdout_redirect
import login_screen


def handle_selected_modpack_change():
    selected_modpack = dpg.get_value("tag:main/selected_modpack")
    settings.settings_file.setsave("selected_modpack", str(selected_modpack.encode('utf-8')))
    modpack_config = remote_config.modpack_config_by_title[selected_modpack]
    dpg.set_value("tag:main/description", modpack_config["description"])


def handle_username_change():
    settings.settings_file.setsave("username", str(
        dpg.get_value("tag:main/username").encode('utf-8')))


def handle_logout():
    dpg.delete_item("tag:main")
    login_screen.render_login_screen()


def handle_play():
    cfg = remote_config.modpack_config_by_title[dpg.get_value("tag:main/selected_modpack")]
    modpack.ensure_modpack_installed(cfg)
    modpack.start_modpack(cfg)


def render_main_screen():
    with dpg.group(tag="tag:main", parent="tag:window"):
        with dpg.group(horizontal=True):
            dpg.add_text("Нікнейм")
            dpg.add_input_text(
                tag="tag:main/username",
                default_value=settings.saved_username,
                callback=handle_username_change)
            dpg.add_button(label="[Перелогінитись]", callback=handle_logout)

        with dpg.group(horizontal=True):
            dpg.add_listbox(
                width=MODPACKS_LISTBOX_WIDTH,
                tag="tag:main/selected_modpack",
                items=remote_config.modpack_titles,
                default_value=settings.saved_selected_modpack or remote_config.modpack_titles[0],
                callback=handle_selected_modpack_change)

            with dpg.child_window(height=300, autosize_x=True):
                dpg.add_text(tag="tag:main/description",
                             default_value=remote_config.modpack_config_by_title[
                                 settings.saved_selected_modpack or remote_config.modpack_titles[0]
                             ]["description"],
                             wrap=WINDOW_WIDTH - MODPACKS_LISTBOX_WIDTH - 100)

        with dpg.child_window(height=346):
            with dpg.collapsing_header(label="Налаштування", default_open=False):
                dpg.add_input_int(label="Мін. оперативки",
                                  tag="tag:main/min_ram",
                                  default_value=4096,
                                  min_value=2048,
                                  max_value=8096,
                                  step=512,
                                  min_clamped=True,
                                  max_clamped=True)
                dpg.add_input_int(label="Макс. оперативки",
                                  tag="tag:main/max_ram",
                                  default_value=8192,
                                  min_value=4096,
                                  max_value=16384,
                                  step=512,
                                  min_clamped=True,
                                  max_clamped=True)

            with dpg.collapsing_header(label="Лог", tag="tag:main/log_header", default_open=False):
                dpg_stdout_redirect.log_window_id = dpg.add_child_window(height=200)

        with dpg.group(tag="tag:main/bottom_buttons_spacer_group"):
            dpg.add_spacer(tag="tag:main/bottom_buttons_spacer")

        with dpg.group(tag="tag:main/bottom_buttons", horizontal=True):
            dpg.add_spacer(width=128)
            dpg.add_button(
                label="[Запуск]",
                width=116,
                height=24,
                callback=handle_play)
            dpg.add_spacer(width=400)
            discord_link = dpg.add_button(
                label="[discord]",
                width=120,
                height=24,
                callback=lambda: webbrowser.open(DISCORD_URL))
            github_link = dpg.add_button(
                label="[github]",
                width=100,
                height=24,
                callback=lambda: webbrowser.open(GITHUB_URL))
            dpg.bind_item_theme(discord_link, "theme:hyperlink")
            dpg.bind_item_theme(github_link, "theme:hyperlink")
