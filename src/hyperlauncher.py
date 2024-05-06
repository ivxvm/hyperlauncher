import dearpygui.dearpygui as dpg
import ctypes
from constants import *
from main_screen import render_main_screen


def main():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    dpg.create_context()
    dpg.create_viewport(title="Hyperlauncher",
                        resizable=False,
                        width=DEFAULT_WINDOW_WIDTH,
                        height=DEFAULT_WINDOW_HEIGHT,
                        x_pos=int(screensize[0] / 2 -
                                  DEFAULT_WINDOW_WIDTH / 2),
                        y_pos=int(screensize[1] / 2 - DEFAULT_WINDOW_HEIGHT / 2))
    dpg.setup_dearpygui()

    with dpg.font_registry():
        with dpg.font("Minecraft_1.1.ttf", size=20) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.bind_font(font)

    with dpg.theme(tag="hyperlinkTheme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 0, 0, 0])
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, [29, 151, 236, 25])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [29, 151, 236])

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            for component, color in MAIN_THEME_COLORS:
                dpg.add_theme_color(component, color, category=dpg.mvThemeCat_Core)

    dpg.bind_theme(global_theme)

    dpg.show_style_editor()

    render_main_screen()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
