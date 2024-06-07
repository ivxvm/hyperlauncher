import dearpygui.dearpygui as dpg

import constants
import localization
import git_installer


def render_git_install_screen():
    with dpg.group(tag="tag:git_install", parent="tag:window"):
        y = constants.WINDOW_HEIGHT / 2 - 96
        for message in ["Git не знайдено на комп'ютері!",
                        "Зачекайте, згодом буде завантажено і запущено його інсталятор.",
                        "Перезапустіть лаунчер після завершення інсталяції."]:
            error_button = dpg.add_button(label=localization.localize(message),
                                          pos=[0, y],
                                          width=constants.WINDOW_WIDTH)
            dpg.bind_item_theme(error_button, "theme:error_text")
            y += 64
    git_installer.download_and_install_git()
