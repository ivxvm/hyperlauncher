import dearpygui.dearpygui as dpg

LAUNCHER_FOLDER = "~/hyperlauncher"
OLD_LAUNCHER_CONFIG_FILE = "~/hyperlauncher.conf"
MODPACKS_CONFIG_URL = "https://raw.githubusercontent.com/ivxvm/hypercube-modpacks/main/hypercube-modpacks.json"

AUTH_SERVER_URL = "https://hypercube.in.ua:8443"
IS_LOCALHOST = "localhost" in AUTH_SERVER_URL

GIT_WINDOWS_URL = "https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/Git-2.45.0-64-bit.exe"
GIT_WATCHER_INTERVAL = 1

GITHUB_URL = "https://github.com/ivxvm/hyperlauncher"
DISCORD_URL = "https://discord.com/invite/4dv9qGebhW"

FONT_URL = "https://github.com/ivxvm/hyperlauncher/raw/main/src/assets/Minecraft_1.1.ttf"
ICON_URL = "https://github.com/ivxvm/hyperlauncher/raw/main/src/assets/icon.ico"
LOGO_URL = "https://raw.githubusercontent.com/ivxvm/hyperlauncher/main/src/assets/logo.png"

DISCORD_CLIENT_ID = "1238431431437582397"

DISCORD_PRESENCE_WORKER_INTERVAL = 5
GAME_LOG_PRINTER_WORKER_INTERVAL = 0.1
GAME_LOG_PRINTER_PREDELAY = 5

DEFAULT_MIN_RAM = 4096
DEFAULT_MAX_RAM = 8192

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

LOGO_WIDTH = 400
LOGO_HEIGHT = 400
LOGO_OFFSET_TOP = 40

DETACHED_PROCESS = 0x00000008

MAIN_THEME_COLORS = [
    [dpg.mvThemeCol_WindowBg, (39, 39, 68)],
    [dpg.mvThemeCol_ChildBg, (20, 20, 34)],
    [dpg.mvThemeCol_Header, (20, 20, 34)],
    [dpg.mvThemeCol_FrameBg, (20, 20, 34)],
    [dpg.mvThemeCol_Border, (139, 109, 156)],
    [dpg.mvThemeCol_Text, (198, 159, 165)],
    [dpg.mvThemeCol_FrameBgActive, (78, 47, 98)],
    [dpg.mvThemeCol_Tab, (20, 20, 34)],
    [dpg.mvThemeCol_TabActive, (78, 47, 98)],
]

MAIN_THEME_BUTTON_COLORS = [
    [dpg.mvThemeCol_Button, [0, 0, 0, 0]],
    [dpg.mvThemeCol_ButtonActive, [0, 0, 0]],
    [dpg.mvThemeCol_ButtonHovered, [242, 211, 171, 25]],
    [dpg.mvThemeCol_Text, [242, 211, 171]],
]
