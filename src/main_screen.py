import os
import webbrowser
import dearpygui.dearpygui as dpg

import constants
import settings
import remote_config
import modpack
import skins
import dpg_stdout_redirect
import login_screen

SETTINGS_INDENT = 28
SETTINGS_INPUT_WIDTH = 550
PROFILE_SETTINGS_LABEL_WIDTH = 128
GAME_SETTINGS_LABEL_WIDTH = 256


def handle_selected_modpack_change():
    selected_modpack = dpg.get_value("tag:main/selected_modpack")
    settings.set_selected_modpack(selected_modpack)
    modpack_config = remote_config.modpack_config_by_title[selected_modpack]
    dpg.set_value("tag:main/description", modpack_config["description"])


def handle_logout():
    dpg.delete_item("tag:main")
    login_screen.render_login_screen()


def handle_play():
    cfg = remote_config.modpack_config_by_title[settings.selected_modpack]
    modpack_folder = os.path.expanduser(cfg["directory_path"])
    skins_folder = f"{modpack_folder}/cachedImages/skins"
    skins.sync_own_skin(username=settings.username,
                        token=settings.token,
                        skin_path=settings.skin_path,
                        skins_folder=skins_folder)
    skins.sync_skins(skins_folder=skins_folder)
    modpack.ensure_modpack_installed(cfg)
    modpack.start_modpack(cfg)


def handle_skin_selected(_, data):
    dpg.set_value("tag:main/skin_file_path", data["file_path_name"])
    settings.set_skin_path(data["file_path_name"])


def render_main_screen():
    with dpg.group(tag="tag:main", parent="tag:window"):
        with dpg.group(horizontal=True):
            dpg.add_listbox(
                width=constants.MODPACKS_LISTBOX_WIDTH,
                tag="tag:main/selected_modpack",
                items=remote_config.modpack_titles,
                default_value=settings.selected_modpack or remote_config.modpack_titles[0],
                callback=handle_selected_modpack_change)

            with dpg.child_window(height=300, autosize_x=True):
                dpg.add_text(tag="tag:main/description",
                             default_value=remote_config.modpack_config_by_title[
                                 settings.selected_modpack or remote_config.modpack_titles[0]
                             ]["description"],
                             wrap=constants.WINDOW_WIDTH - constants.MODPACKS_LISTBOX_WIDTH - 100)

        with dpg.child_window(height=346):
            with dpg.collapsing_header(label="Профіль", default_open=False):
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(width=PROFILE_SETTINGS_LABEL_WIDTH, readonly=True, default_value="Нікнейм")
                    dpg.add_input_text(width=SETTINGS_INPUT_WIDTH,
                                       readonly=True,
                                       default_value=settings.username)
                    dpg.add_button(label="[Перелогінитись]", callback=handle_logout)
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(width=PROFILE_SETTINGS_LABEL_WIDTH, readonly=True, default_value="Скін")
                    dpg.add_input_text(width=SETTINGS_INPUT_WIDTH,
                                       tag="tag:main/skin_file_path", readonly=True, default_value=settings.skin_path)
                    dpg.add_button(label="[Вибрати]", callback=lambda: dpg.show_item("tag:main/skin_file_dialog"))
                    if dpg.does_alias_exist("tag:main/skin_file_dialog"):
                        dpg.remove_alias("tag:main/skin_file_dialog")
                    with dpg.file_dialog(tag="tag:main/skin_file_dialog",
                                         width=700,
                                         height=400,
                                         show=False,
                                         callback=handle_skin_selected):
                        dpg.add_file_extension(".png")

            with dpg.collapsing_header(label="Налаштування", default_open=False):
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(width=GAME_SETTINGS_LABEL_WIDTH,
                                       readonly=True, default_value="Мін. оперативки")
                    dpg.add_input_int(tag="tag:main/min_ram",
                                      width=144,
                                      default_value=4096,
                                      min_value=2048,
                                      max_value=8096,
                                      step=512,
                                      min_clamped=True,
                                      max_clamped=True)
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(width=GAME_SETTINGS_LABEL_WIDTH,
                                       readonly=True, default_value="Макс. оперативки")
                    dpg.add_input_int(tag="tag:main/max_ram",
                                      width=144,
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
            dpg.add_spacer(width=64)
            dpg.add_button(
                label="[Запуск]",
                width=116,
                height=24,
                callback=handle_play)
            dpg.add_spacer(width=500)
            discord_link = dpg.add_button(
                label="[discord]",
                width=120,
                height=24,
                callback=lambda: webbrowser.open(constants.DISCORD_URL))
            github_link = dpg.add_button(
                label="[github]",
                width=100,
                height=24,
                callback=lambda: webbrowser.open(constants.GITHUB_URL))
            dpg.bind_item_theme(discord_link, "theme:hyperlink")
            dpg.bind_item_theme(github_link, "theme:hyperlink")
