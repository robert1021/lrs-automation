import time
import pyautogui
from utilities import search_for_image
from config import *


class FolderTabWindow:

    def __init__(self):
        self.vol_1_img = os.path.join(folder_tab_image_path, "vol_1.PNG")
        self.vol_1_alt_img = os.path.join(folder_tab_image_path, "vol_1_alt.PNG")
        self.vol_2_img = os.path.join(folder_tab_image_path, "vol_2.PNG")
        self.wal_1_img = os.path.join(folder_tab_image_path, "wal_1.PNG")
        self.db_1_img = os.path.join(folder_tab_image_path, "db_1.PNG")
        self.cd_1_img = os.path.join(folder_tab_image_path, "cd_1.PNG")
        self.edit_img = os.path.join(folder_tab_image_path, "edit.PNG")
        self.edit_update_img = os.path.join(folder_tab_image_path, "edit_update.PNG")

    def open_update_folder(self, coordinates):
        pyautogui.moveTo(coordinates)
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.rightClick()
        time.sleep(0.25)
        edit_coord = search_for_image(self.edit_img)
        pyautogui.moveTo(edit_coord)
        time.sleep(0.25)
        update_coord = search_for_image(self.edit_update_img)
        pyautogui.moveTo(update_coord)
        time.sleep(0.25)
        pyautogui.click()
