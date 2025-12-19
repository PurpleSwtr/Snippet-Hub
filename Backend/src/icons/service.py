import os
from pathlib import Path
from src.core.config import settings

def get_directory(floader: str):
    icons_path = os.path.join(settings.FRONT_STATIC_DIR, floader)
    if not os.path.isdir(icons_path):
        raise NotADirectoryError(f"Pack not found")
    return icons_path

def get_icons_names(pack: str):
    icons_path = get_directory(floader=pack)
    all_items = os.listdir(icons_path)
    files_only = [item for item in all_items if os.path.isfile(os.path.join(icons_path, item))]
    return files_only

def get_icon(pack: str ,filename: str):
    icon_path = get_directory(floader=pack)
    return os.path.join(icon_path, filename)

