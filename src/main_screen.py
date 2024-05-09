import os
import re
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
SETTINGS_INPUT_WIDTH = 570

PROFILE_SETTINGS_LABEL_WIDTH = 128
GENERAL_SETTINGS_LABEL_WIDTH = 192
GAME_SETTINGS_LABEL_WIDTH = 256

FILE_DIALOG_WIDTH = 880
FILE_DIALOG_HEIGHT = 560

SKIN_SHORT_PATH_LEN = 38
WORKING_FOLDER_SHORT_PATH_LEN = 33


def handle_selected_modpack_change():
    modpack_config = remote_config.modpack_config_by_title[dpg.get_value("tag:main/selected_modpack")]
    selected_modpack = modpack_config['name']
    settings.set_selected_modpack(selected_modpack)
    settings.reload_modpack_settings()
    dpg.set_value("tag:main/min_ram", settings.min_ram)
    dpg.set_value("tag:main/max_ram", settings.max_ram)
    dpg.set_value("tag:main/description", modpack_config["description"])


def handle_skin_selected(_, data):
    dpg.set_value("tag:main/skin_file_path",
                  short_path(SKIN_SHORT_PATH_LEN, data["file_path_name"]))
    settings.set_skin_path(data["file_path_name"])


def handle_working_folder_selected(_, data):
    dpg.set_value("tag:main/working_folder",
                  short_path(WORKING_FOLDER_SHORT_PATH_LEN, data["file_path_name"]))
    settings.set_working_folder(data["file_path_name"])


def handle_logout():
    dpg.delete_item("tag:main")
    login_screen.render_login_screen()


def handle_play():
    modpack_config = remote_config.modpack_config_by_name[settings.selected_modpack]
    modpack_folder = os.path.expanduser(settings.working_folder + "/" + modpack_config["directory_name"])
    skins_folder = f"{modpack_folder}/cachedImages/skins"
    skins.sync_own_skin(username=settings.username,
                        token=settings.token,
                        skin_path=settings.skin_path,
                        skins_folder=skins_folder)
    skins.sync_skins(skins_folder=skins_folder)
    modpack.ensure_modpack_installed(modpack_config)
    modpack.start_modpack(modpack_config)


def short_path(len, path):
    chunk = path[-len:]
    if ':' in chunk and chunk[0] != ':':
        return chunk
    else:
        match = re.search(r"[\\/]", chunk)
        if match:
            return "..." + chunk[match.start():]
        else:
            return chunk


def render_main_screen():
    with dpg.group(tag="tag:main", parent="tag:window"):
        with dpg.group(horizontal=True):
            dpg.add_listbox(
                width=constants.MODPACKS_LISTBOX_WIDTH,
                tag="tag:main/selected_modpack",
                items=remote_config.modpack_titles,
                default_value=remote_config.modpack_config_by_name[
                    settings.selected_modpack or
                    next(iter(remote_config.modpack_config_by_name))
                ]['title'],
                callback=handle_selected_modpack_change)

            with dpg.child_window(height=300, autosize_x=True):
                dpg.add_text(tag="tag:main/description",
                             default_value=remote_config.modpack_config_by_name[
                                 settings.selected_modpack or
                                 next(iter(remote_config.modpack_config_by_name))
                             ]["description"],
                             wrap=constants.WINDOW_WIDTH - constants.MODPACKS_LISTBOX_WIDTH - 100)

        dpg.add_spacer()

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
                    dpg.add_input_text(tag="tag:main/skin_file_path",
                                       width=SETTINGS_INPUT_WIDTH,
                                       readonly=True,
                                       default_value=short_path(SKIN_SHORT_PATH_LEN, settings.skin_path or "Не вибрано"))
                    dpg.add_button(label="[Вибрати]", callback=lambda: dpg.show_item("tag:main/skin_file_dialog"))
                    if dpg.does_alias_exist("tag:main/skin_file_dialog"):
                        dpg.remove_alias("tag:main/skin_file_dialog")
                    with dpg.file_dialog(tag="tag:main/skin_file_dialog",
                                         width=FILE_DIALOG_WIDTH,
                                         height=FILE_DIALOG_HEIGHT,
                                         show=False,
                                         callback=handle_skin_selected):
                        dpg.add_file_extension(".png")

            with dpg.collapsing_header(label="Загальні налаштування", default_open=False):
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(width=GENERAL_SETTINGS_LABEL_WIDTH,
                                       readonly=True,
                                       default_value="Робоча папка")
                    dpg.add_input_text(tag="tag:main/working_folder",
                                       width=506,
                                       readonly=True,
                                       default_value=short_path(WORKING_FOLDER_SHORT_PATH_LEN,
                                                                os.path.expanduser(settings.working_folder)))
                    dpg.add_button(label="[Вибрати]", callback=lambda: dpg.show_item("tag:main/working_folder_dialog"))
                    if dpg.does_alias_exist("tag:main/working_folder_dialog"):
                        dpg.remove_alias("tag:main/working_folder_dialog")
                    dpg.add_file_dialog(tag="tag:main/working_folder_dialog",
                                        directory_selector=True,
                                        width=FILE_DIALOG_WIDTH,
                                        height=FILE_DIALOG_HEIGHT,
                                        show=False,
                                        callback=handle_working_folder_selected)

            with dpg.collapsing_header(label="Налаштування модпаку", default_open=False):
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(width=GAME_SETTINGS_LABEL_WIDTH,
                                       readonly=True,
                                       default_value="Мін. оперативки")
                    dpg.add_input_int(tag="tag:main/min_ram",
                                      width=144,
                                      default_value=settings.min_ram,
                                      min_value=2048,
                                      max_value=8096,
                                      step=512,
                                      min_clamped=True,
                                      max_clamped=True,
                                      callback=lambda _, data: settings.set_min_ram(data))
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(width=GAME_SETTINGS_LABEL_WIDTH,
                                       readonly=True,
                                       default_value="Макс. оперативки")
                    dpg.add_input_int(tag="tag:main/max_ram",
                                      width=144,
                                      default_value=settings.max_ram,
                                      min_value=4096,
                                      max_value=16384,
                                      step=512,
                                      min_clamped=True,
                                      max_clamped=True,
                                      callback=lambda _, data: settings.set_max_ram(data))

            with dpg.collapsing_header(label="Лог", tag="tag:main/log_header", default_open=False):
                dpg_stdout_redirect.log_window_id = dpg.add_child_window(height=200,
                                                                         border=False,
                                                                         indent=SETTINGS_INDENT + 4)

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
