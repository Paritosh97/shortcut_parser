import xbmc
import xbmcaddon
import time
from shortcuts import get_shortcuts

ADDON = xbmcaddon.Addon()
MONITOR_INTERVAL = 10  # Check every 10 seconds

xbmc.log("🚀 Shortcut Parser Service Started!", xbmc.LOGINFO)

while not xbmc.abortRequested:
    shortcuts = get_shortcuts()
    xbmc.log(f"🔄 Found {len(shortcuts)} shortcuts.", xbmc.LOGINFO)
    time.sleep(MONITOR_INTERVAL)
