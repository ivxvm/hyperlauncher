import os
import re
import time
import webbrowser
import dearpygui.dearpygui as dpg

from threading import Thread

import constants
import settings
import remote_config
import modpack
import skins
import logger
import game_log_printer
import login_screen

import localization
from localization import localize

MODPACKS_LISTBOX_WIDTH = 400

SETTINGS_INDENT = 28
SETTINGS_INPUT_WIDTH = 570

PROFILE_SETTINGS_LABEL_WIDTH = 128
GENERAL_SETTINGS_LABEL_WIDTH = 224

MODPACK_SETTINGS_LABEL_WIDTH = 256
MODPACK_SETTINGS_INPUT_WIDTH = 144

FILE_DIALOG_WIDTH = 880
FILE_DIALOG_HEIGHT = 560

SKIN_SHORT_PATH_LEN = 38
WORKING_FOLDER_SHORT_PATH_LEN = 33

MIN_RAM_MIN_VALUE = 2048
MIN_RAM_MAX_VALUE = 8096
MAX_RAM_MIN_VALUE = 4096
MAX_RAM_MAX_VALUE = 16384
RAM_STEP = 512

MODPACK_PROCESS_WATCHER_INTERVAL = 1

main_screen_rendered_at_least_once = False
is_ongoing_installation = False


def handle_selected_modpack_change():
    selected_modpack_title = dpg.get_value("tag:main/selected_modpack")
    modpack_config = remote_config.modpack_config_by_locale_and_title[settings.locale][selected_modpack_title]
    selected_modpack = modpack_config['name']
    settings.set_selected_modpack(selected_modpack)
    settings.reload_modpack_settings()
    dpg.set_value("tag:main/min_ram", settings.min_ram)
    dpg.set_value("tag:main/max_ram", settings.max_ram)
    dpg.set_value("tag:main/modpack_news", render_news(modpack_config["news"][settings.locale]))
    dpg.set_value("tag:main/modpack_description", modpack_config["description"][settings.locale])
    dpg.set_value("tag:main/modpack_notes", render_notes(modpack_config["notes"][settings.locale]))


def handle_skin_selected(_, data):
    dpg.set_value("tag:main/skin_file_path",
                  short_path(SKIN_SHORT_PATH_LEN, data["file_path_name"]))
    settings.set_skin_path(data["file_path_name"])


def handle_working_folder_selected(_, data):
    dpg.set_value("tag:main/working_folder",
                  short_path(WORKING_FOLDER_SHORT_PATH_LEN, data["file_path_name"]))
    settings.set_working_folder(data["file_path_name"])


def handle_locale_selected(_, data):
    settings.set_locale(localization.locale_name_by_title[data])
    dpg.delete_item("tag:main")
    render_main_screen()


def handle_logout():
    dpg.delete_item("tag:main")
    login_screen.render_login_screen()


def handle_play_kill():
    global is_ongoing_installation
    modpack_process = modpack.current_modpack_process
    if modpack_process and modpack_process.poll() == None:
        modpack_process.kill()
    else:
        modpack_config = remote_config.modpack_config_by_name[settings.selected_modpack]
        modpack_folder = modpack.get_modpack_folder(modpack_config)
        skins_folder = f"{modpack_folder}/cachedImages/skins"
        dpg.set_value("tag:main/log_header", True)
        is_ongoing_installation = True
        invalidate_play_button()
        skins.sync_own_skin(username=settings.username,
                            token=settings.token,
                            skin_path=settings.skin_path,
                            skins_folder=skins_folder)
        skins.sync_skins(skins_folder=skins_folder)
        modpack.ensure_modpack_installed(modpack_config)
        modpack.start_modpack(modpack_config)
        is_ongoing_installation = False
        game_log_printer.scheduled_timeout = constants.GAME_LOG_PRINTER_PREDELAY


def render_news(news):
    return "\n\n".join(["\n".join(entry) for entry in news])


def render_notes(notes):
    return "\n".join(notes)


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
    global main_screen_rendered_at_least_once
    main_screen_rendered_at_least_once = True

    if not settings.selected_modpack:
        settings.set_selected_modpack(next(iter(remote_config.modpack_config_by_name)))

    with dpg.group(tag="tag:main", parent="tag:window"):
        with dpg.group(horizontal=True):
            selected_modpack_config = remote_config.modpack_config_by_name[settings.selected_modpack]
            modpack_titles = remote_config.modpack_titles_by_locale[settings.locale]
            with dpg.group():
                dpg.add_text("", indent=2)
                dpg.add_listbox(
                    width=MODPACKS_LISTBOX_WIDTH,
                    tag="tag:main/selected_modpack",
                    items=modpack_titles,
                    num_items=len(modpack_titles),
                    default_value=selected_modpack_config['title'][settings.locale],
                    callback=handle_selected_modpack_change)
            with dpg.tab_bar(tag="tag:main/modpack_tab_bar"):
                with dpg.tab(label=localize("Новини"), tag="tag:main/modpack_news_tab"):
                    with dpg.child_window(height=300, autosize_x=True):
                        dpg.add_text(tag="tag:main/modpack_news",
                                     default_value=render_news(selected_modpack_config["news"][settings.locale]),
                                     wrap=constants.WINDOW_WIDTH - MODPACKS_LISTBOX_WIDTH - 100)
                with dpg.tab(label=localize("Опис"), tag="tag:main/modpack_description_tab"):
                    with dpg.child_window(height=300, autosize_x=True):
                        dpg.add_text(tag="tag:main/modpack_description",
                                     default_value=selected_modpack_config["description"][settings.locale],
                                     wrap=constants.WINDOW_WIDTH - MODPACKS_LISTBOX_WIDTH - 100)
                with dpg.tab(label=localize("Нотатки"), tag="tag:main/modpack_notes_tab"):
                    with dpg.child_window(height=300, autosize_x=True):
                        dpg.add_text(tag="tag:main/modpack_notes",
                                     default_value=render_notes(
                                         selected_modpack_config["notes"][settings.locale]),
                                     wrap=constants.WINDOW_WIDTH - MODPACKS_LISTBOX_WIDTH - 100)

        dpg.add_spacer()

        with dpg.child_window(height=340):
            with dpg.collapsing_header(label=localize("Профіль"), default_open=False):
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(default_value=localize("Нікнейм"),
                                       readonly=True,
                                       width=PROFILE_SETTINGS_LABEL_WIDTH)
                    dpg.add_input_text(default_value=settings.username,
                                       readonly=True,
                                       width=SETTINGS_INPUT_WIDTH)
                    dpg.add_button(label=localize("[Перелогінитись]"), callback=handle_logout)
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(default_value=localize("Скін"),
                                       readonly=True,
                                       width=PROFILE_SETTINGS_LABEL_WIDTH)
                    dpg.add_input_text(tag="tag:main/skin_file_path",
                                       default_value=short_path(
                                           SKIN_SHORT_PATH_LEN, settings.skin_path or localize("Не вибрано")),
                                       readonly=True,
                                       width=SETTINGS_INPUT_WIDTH)
                    dpg.add_button(label=localize("[Вибрати]"),
                                   callback=lambda: dpg.show_item("tag:main/skin_file_dialog"))
                    if dpg.does_alias_exist("tag:main/skin_file_dialog"):
                        dpg.remove_alias("tag:main/skin_file_dialog")
                    with dpg.file_dialog(tag="tag:main/skin_file_dialog",
                                         width=FILE_DIALOG_WIDTH,
                                         height=FILE_DIALOG_HEIGHT,
                                         show=False,
                                         callback=handle_skin_selected):
                        dpg.add_file_extension(".png")

            with dpg.collapsing_header(label=localize("Загальні налаштування"), default_open=False):
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(default_value=localize("Робоча папка"),
                                       readonly=True,
                                       width=GENERAL_SETTINGS_LABEL_WIDTH)
                    dpg.add_input_text(tag="tag:main/working_folder",
                                       width=474,
                                       readonly=True,
                                       default_value=short_path(WORKING_FOLDER_SHORT_PATH_LEN,
                                                                os.path.expanduser(settings.working_folder)))
                    dpg.add_button(label=localize("[Вибрати]"),
                                   callback=lambda: dpg.show_item("tag:main/working_folder_dialog"))
                    if dpg.does_alias_exist("tag:main/working_folder_dialog"):
                        dpg.remove_alias("tag:main/working_folder_dialog")
                    dpg.add_file_dialog(tag="tag:main/working_folder_dialog",
                                        directory_selector=True,
                                        width=FILE_DIALOG_WIDTH,
                                        height=FILE_DIALOG_HEIGHT,
                                        show=False,
                                        callback=handle_working_folder_selected)
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(default_value=localize("Мова"),
                                       readonly=True,
                                       width=GENERAL_SETTINGS_LABEL_WIDTH)
                    dpg.add_combo([locale.title for locale in localization.LOCALES],
                                  default_value=localization.locale_title_by_name[settings.locale],
                                  width=200,
                                  callback=handle_locale_selected)

            with dpg.collapsing_header(label=localize("Налаштування модпаку"), default_open=False):
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(default_value=localize("Мін. оперативки"),
                                       readonly=True,
                                       width=MODPACK_SETTINGS_LABEL_WIDTH)
                    dpg.add_input_int(tag="tag:main/min_ram",
                                      width=MODPACK_SETTINGS_INPUT_WIDTH,
                                      default_value=settings.min_ram,
                                      min_value=MIN_RAM_MIN_VALUE,
                                      max_value=MIN_RAM_MAX_VALUE,
                                      step=RAM_STEP,
                                      min_clamped=True,
                                      max_clamped=True,
                                      callback=lambda _, data: settings.set_min_ram(data))
                with dpg.group(horizontal=True, indent=SETTINGS_INDENT):
                    dpg.add_input_text(default_value=localize("Макс. оперативки"),
                                       readonly=True,
                                       width=MODPACK_SETTINGS_LABEL_WIDTH)
                    dpg.add_input_int(tag="tag:main/max_ram",
                                      width=MODPACK_SETTINGS_INPUT_WIDTH,
                                      default_value=settings.max_ram,
                                      min_value=MAX_RAM_MIN_VALUE,
                                      max_value=MAX_RAM_MAX_VALUE,
                                      step=RAM_STEP,
                                      min_clamped=True,
                                      max_clamped=True,
                                      callback=lambda _, data: settings.set_max_ram(data))

            with dpg.collapsing_header(label=localize("Лог"), tag="tag:main/log_header", default_open=False):
                logger.log_window_id = dpg.add_child_window(height=200,
                                                            border=False,
                                                            indent=SETTINGS_INDENT + 4)

        with dpg.group(tag="tag:main/bottom_buttons_spacer_group"):
            dpg.add_spacer(tag="tag:main/bottom_buttons_spacer")

        with dpg.group(tag="tag:main/bottom_buttons", horizontal=True):
            dpg.add_spacer(width=64)
            dpg.add_button(
                tag="tag:main/play_kill_button",
                label=localize("[Запуск]"),
                width=116,
                height=24,
                callback=handle_play_kill)
            dpg.add_spacer(tag="tag:main/play_kill_button_right_margin",
                           width=500)
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


def invalidate_play_button():
    if dpg.does_alias_exist("tag:main/play_kill_button"):
        modpack_process = modpack.current_modpack_process
        if is_ongoing_installation:
            dpg.set_item_label("tag:main/play_kill_button", "")
            dpg.set_item_width("tag:main/play_kill_button", 1)
            dpg.set_item_width("tag:main/play_kill_button_right_margin", 615)
        elif modpack_process and modpack_process.poll() == None:
            dpg.set_item_label("tag:main/play_kill_button", localize("[Вимкнути]"))
            dpg.set_item_width("tag:main/play_kill_button", 146)
            dpg.set_item_width("tag:main/play_kill_button_right_margin", 470)
        else:
            dpg.set_item_label("tag:main/play_kill_button", localize("[Запуск]"))
            dpg.set_item_width("tag:main/play_kill_button", 116)
            dpg.set_item_width("tag:main/play_kill_button_right_margin", 500)


def start_modpack_process_watcher():
    def watcher():
        while True:
            if main_screen_rendered_at_least_once:
                invalidate_play_button()
            time.sleep(MODPACK_PROCESS_WATCHER_INTERVAL)
    thread = Thread(target=watcher, daemon=True)
    thread.start()


start_modpack_process_watcher()
