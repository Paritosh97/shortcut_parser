import xbmc
import xbmcaddon
import time
from shortcuts import get_shortcuts

ADDON = xbmcaddon.Addon()

def auto_refresh():
    settings = ADDON.getSetting("auto_refresh")
    refresh_interval = int(ADDON.getSetting("refresh_interval"))

    while settings:
        xbmc.executebuiltin("Container.Refresh")
        time.sleep(refresh_interval * 60)
        settings = ADDON.getSetting("auto_refresh")

if __name__ == '__main__':
    auto_refresh()
