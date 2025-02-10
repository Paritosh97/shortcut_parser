import os
import platform
import json
import subprocess
import xbmcaddon
import xbmcgui

# Windows-only import
if platform.system() == "Windows":
    import win32com.client  # For parsing .lnk files

ADDON = xbmcaddon.Addon()
PROFILE_DIR = ADDON.getAddonInfo('profile')

GROUPS_FILE = os.path.join(PROFILE_DIR, "groups.json")
SETTINGS_FILE = os.path.join(PROFILE_DIR, "settings.json")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"auto_refresh": True, "refresh_interval": 10}

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

def load_groups():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_groups(groups):
    with open(GROUPS_FILE, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=4)

def get_shortcuts():
    shortcuts = []
    groups = load_groups()

    for group in groups:
        folder, category = group['folder'], group['category']

        if not os.path.exists(folder):
            continue

        for filename in os.listdir(folder):
            shortcut_path = os.path.join(folder, filename)
            shortcut_info = None

            if platform.system() == "Windows" and filename.endswith(".lnk"):
                shell = win32com.client.Dispatch("WScript.Shell")
                link = shell.CreateShortcut(shortcut_path)
                shortcut_info = {
                    'name': os.path.splitext(filename)[0],
                    'target': link.TargetPath,
                    'icon': link.IconLocation.split(',')[0] if link.IconLocation else "",
                    'category': category
                }
            elif platform.system() in ["Linux", "Darwin"] and filename.endswith(".desktop"):
                with open(shortcut_path, "r", encoding="utf-8") as f:
                    target, icon = "", ""
                    for line in f:
                        if line.startswith("Exec="):
                            target = line.split("=", 1)[1].strip()
                        if line.startswith("Icon="):
                            icon = line.split("=", 1)[1].strip()
                    shortcut_info = {
                        'name': os.path.splitext(filename)[0],
                        'target': shortcut_path,
                        'icon': icon if os.path.exists(icon) else "",
                        'category': category
                    }
            elif os.path.islink(shortcut_path):
                target = os.readlink(shortcut_path)
                shortcut_info = {
                    'name': filename,
                    'target': target,
                    'icon': "",
                    'category': category
                }

            if shortcut_info:
                shortcuts.append(shortcut_info)

    return shortcuts

def launch_shortcut(target):
    if platform.system() == "Windows":
        os.startfile(target)
    elif platform.system() in ["Linux", "Darwin"]:
        if target.endswith(".desktop"):
            subprocess.Popen(["xdg-open", target])
        else:
            subprocess.Popen(target, shell=True)

def manage_settings():
    dialog = xbmcgui.Dialog()
    options = ["Toggle Auto Refresh", "Set Refresh Interval (minutes)", "Manage Groups"]
    choice = dialog.select("Settings", options)

    settings = load_settings()
    if choice == 0:
        settings["auto_refresh"] = not settings["auto_refresh"]
        save_settings(settings)
    elif choice == 1:
        new_interval = dialog.input("Enter Refresh Interval (minutes)", type=xbmcgui.INPUT_NUMERIC)
        if new_interval.isdigit():
            settings["refresh_interval"] = int(new_interval)
            save_settings(settings)
    elif choice == 2:
        manage_groups()

def manage_groups():
    groups = load_groups()
    options = ["Add Group"] + [f"Edit: {g['category']}" for g in groups] + ["Delete Group"]
    dialog = xbmcgui.Dialog()
    choice = dialog.select("Manage Groups", options)

    if choice == 0:
        folder = dialog.browse(0, "Select Shortcut Folder", "files")
        category = dialog.input("Enter Category Name")
        if folder and category:
            groups.append({'folder': folder, 'category': category})
            save_groups(groups)
    elif choice > 0 and choice <= len(groups):
        index = choice - 1
        folder = dialog.browse(0, "Select Shortcut Folder", "files", groups[index]['folder'])
        category = dialog.input("Enter Category Name", defaultt=groups[index]['category'])
        if folder and category:
            groups[index] = {'folder': folder, 'category': category}
            save_groups(groups)
    elif choice == len(groups) + 1 and groups:
        index = dialog.select("Select Group to Delete", [g['category'] for g in groups])
        if index != -1:
            del groups[index]
            save_groups(groups)
