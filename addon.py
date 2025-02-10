import sys
import xbmcaddon
import xbmcplugin
import xbmcgui
import urllib.parse
from shortcuts import get_shortcuts, launch_shortcut, manage_settings

ADDON = xbmcaddon.Addon()
PLUGIN_URL = sys.argv[0]

# Ensure HANDLE is always an integer
HANDLE = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else -1


def list_shortcuts():
    shortcuts = get_shortcuts()
    for shortcut in shortcuts:
        list_item = xbmcgui.ListItem(label=f"[{shortcut['category']}] {shortcut['name']}")
        list_item.setArt({'icon': shortcut['icon'], 'thumb': shortcut['icon']})
        list_item.setProperty('IsPlayable', 'true')
        url = f'{PLUGIN_URL}?action=launch&target={urllib.parse.quote(shortcut["target"])}'
        xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=False)

    if HANDLE >= 0:  # Ensure valid handle before calling xbmcplugin.endOfDirectory
        xbmcplugin.endOfDirectory(HANDLE)


def router():
    params = {}

    # Ensure sys.argv[2] exists and is not empty before parsing
    if len(sys.argv) > 2 and sys.argv[2]:
        params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

    action = params.get('action')

    if action == 'launch' and 'target' in params:
        launch_shortcut(urllib.parse.unquote(params['target']))
    elif action == 'settings':
        manage_settings()
    else:
        list_shortcuts()


if __name__ == '__main__':
    router()
