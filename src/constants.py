import dearpygui.dearpygui as dpg

LAUCNHER_CONFIG_FILE = "~/hyperlauncher.conf"
MODPACKS_CONFIG_URL = "https://raw.githubusercontent.com/ivxvm/hypercube-modpacks/main/hypercube-modpacks.json"
DISCORD_URL = "https://discord.com/invite/4dv9qGebhW"
GITHUB_URL = "https://github.com/ivxvm?tab=repositories"
AUTH_SERVER_URL = "https://localhost:8443"
IS_LOCALHOST = "localhost" in AUTH_SERVER_URL

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
LOGO_WIDTH = 400
LOGO_HEIGHT = 400
LOGO_OFFSET_TOP = 40
MODPACKS_LISTBOX_WIDTH = 300

DETACHED_PROCESS = 0x00000008

MAIN_THEME_COLORS = [
    [dpg.mvThemeCol_WindowBg, (39, 39, 68)],
    [dpg.mvThemeCol_ChildBg, (20, 20, 34)],
    [dpg.mvThemeCol_Header, (20, 20, 34)],
    [dpg.mvThemeCol_FrameBg, (20, 20, 34)],
    [dpg.mvThemeCol_Border, (139, 109, 156, 0)],
    [dpg.mvThemeCol_Text, (198, 159, 165)],
    [dpg.mvThemeCol_FrameBgActive, (78, 47, 98)]
]
