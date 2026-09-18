"""Application configuration: external, user-replaceable image folders.

The PyAutoGUI reference images are intentionally NOT bundled into the exe.
They live in an ``images/`` folder next to the executable (frozen) or next to
this file (source checkout), so users on different resolutions can capture
and maintain their own images without rebuilding the exe.

Layout::

    <app root>/
        <exe or main.py>
        images/
            login/        login dialog reference images
            menubar/      LRS menu bar reference images
            file_insert/  File > Insert dialog reference images
            file_search/  File > Find dialog reference images
            file_status/  Edit > Status dialog reference images
            folder_tab/   folder-tab (VOL/WAL/DB/CD) reference images
            title_bar/    LRS window title-bar icon
            legacy/       old unreferenced captures, kept for reference
"""

import os
import sys


def get_frozen_status() -> bool:
    """True when running from a PyInstaller executable."""
    return bool(getattr(sys, "frozen", False))


def get_app_root() -> str:
    """Folder containing the exe (frozen) or this source file (dev)."""
    if get_frozen_status():
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


APP_ROOT = get_app_root()

# External image root: <app root>/images (never inside the exe).
image_path = os.path.join(APP_ROOT, "images")

login_image_path = os.path.join(image_path, "login")
menubar_image_path = os.path.join(image_path, "menubar")
file_insert_image_path = os.path.join(image_path, "file_insert")
file_search_image_path = os.path.join(image_path, "file_search")
file_status_image_path = os.path.join(image_path, "file_status")
folder_tab_image_path = os.path.join(image_path, "folder_tab")
titlebar_image_path = os.path.join(image_path, "title_bar")

IMAGE_FOLDERS = (
    login_image_path,
    menubar_image_path,
    file_insert_image_path,
    file_search_image_path,
    file_status_image_path,
    folder_tab_image_path,
    titlebar_image_path,
)

# Manifest of images the RPA bots actually look up. Used by the GUI
# "Images" page and by tests to verify the external layout.
REQUIRED_IMAGES = {
    "login": ["login_user_id.PNG", "login_password.PNG", "login_login_btn.PNG"],
    "menubar": [
        "file.PNG",
        "file_find.PNG",
        "edit.PNG",
        "edit_insert.PNG",
        "edit_status.png",
        "view.PNG",
        "favourites.PNG",
        "tools.PNG",
        "folders_tab.PNG",
        "refresh.PNG",
        "view_box.PNG",
    ],
    "file_insert": [
        "file_number.PNG",
        "file_status.PNG",
        "file_title_english.PNG",
        "ok_btn.PNG",
        "disabled_next_btn.PNG",
        "next_btn.PNG",
        "from_date.PNG",
        "to_date.PNG",
        "comment.PNG",
    ],
    "file_search": ["fast_find_criteria.PNG", "find_now_btn.PNG"],
    "file_status": [
        "file_status.PNG",
        "status_date.PNG",
        "update_all.PNG",
        "close.PNG",
        "ok_btn.PNG",
    ],
    "folder_tab": [
        "vol_1.PNG",
        "vol_1_alt.PNG",
        "vol_2.PNG",
        "wal_1.PNG",
        "db_1.PNG",
        "cd_1.PNG",
        "edit.PNG",
        "edit_update.PNG",
    ],
    "title_bar": ["lrs_icon.PNG", "lrs_icon2.png"],
}


def ensure_image_dirs() -> None:
    """Create the external image folders so users can drop in captures."""
    for folder in IMAGE_FOLDERS:
        os.makedirs(folder, exist_ok=True)


def _folder_for_key(key: str) -> str:
    return {
        "login": login_image_path,
        "menubar": menubar_image_path,
        "file_insert": file_insert_image_path,
        "file_search": file_search_image_path,
        "file_status": file_status_image_path,
        "folder_tab": folder_tab_image_path,
        "title_bar": titlebar_image_path,
    }[key]


def validate_images():
    """Return a sorted list of required image paths missing from disk."""
    missing = []
    for folder_key, filenames in REQUIRED_IMAGES.items():
        folder = _folder_for_key(folder_key)
        for name in filenames:
            full = os.path.join(folder, name)
            if not os.path.isfile(full):
                missing.append(full)
    return sorted(missing)


imu_dashboard_path = (
    r"N:\BLSS\HC6 Health Risk Protection\HC6-101 Regulatory Reporting\SMD"
    r"\NHPD Dashboard\NNHPD Dashboard - IMU.xlsx"
)
