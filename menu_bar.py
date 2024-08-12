import time
import pyautogui
from utilities import search_for_image
from config import *


class MenuBar:

    def __init__(self):
        self.file_img = os.path.join(menubar_image_path, "file.PNG")
        self.file_find_img = os.path.join(menubar_image_path, "file_find.PNG")
        self.edit_img = os.path.join(menubar_image_path, "edit.PNG")
        self.edit_insert_img = os.path.join(menubar_image_path, "edit_insert.PNG")
        self.edit_status_img = os.path.join(menubar_image_path, "edit_status.png")
        self.view_img = os.path.join(menubar_image_path, "view.PNG")
        self.favourites_img = os.path.join(menubar_image_path, "favourites.PNG")
        self.tools_img = os.path.join(menubar_image_path, "tools.PNG")
        self.folders_tab_img = os.path.join(menubar_image_path, "folders_tab.PNG")
        self.refresh_img = os.path.join(menubar_image_path, "refresh.PNG")
        self.box_view_img = os.path.join(menubar_image_path, "view_box.PNG")

    def click_file(self):
        file_coord = search_for_image(self.file_img)
        pyautogui.moveTo(file_coord)
        time.sleep(0.25)
        pyautogui.click()

    def click_edit(self):
        edit_coord = search_for_image(self.edit_img)
        pyautogui.moveTo(edit_coord)
        time.sleep(0.25)
        pyautogui.click()

    def click_view(self):
        view_coord = search_for_image(self.view_img)
        pyautogui.moveTo(view_coord)
        time.sleep(0.25)
        pyautogui.click()

    def open_file_search(self):
        self.click_file()
        find_coord = search_for_image(self.file_find_img)
        pyautogui.moveTo(find_coord)
        time.sleep(0.25)
        pyautogui.click()

    def open_file_insert(self):
        self.click_edit()
        insert_coord = search_for_image(self.edit_insert_img)
        pyautogui.moveTo(insert_coord)
        time.sleep(0.25)
        pyautogui.click()

    def open_file_status(self):
        self.click_edit()
        status_coord = search_for_image(self.edit_status_img)
        pyautogui.moveTo(status_coord)
        time.sleep(0.25)
        pyautogui.click()

    def click_folders_tab(self):
        folders_tab_coord = search_for_image(self.folders_tab_img)
        pyautogui.moveTo(folders_tab_coord)
        time.sleep(0.25)
        pyautogui.click()

    def click_refresh(self):
        refresh_coord = search_for_image(self.refresh_img)
        pyautogui.moveTo(refresh_coord)
        time.sleep(0.25)
        pyautogui.click()

    def click_box_view(self):
        box_view = search_for_image(self.box_view_img)
        pyautogui.moveTo(box_view)
        time.sleep(0.25)
        pyautogui.click()

    def switch_to_box_view(self):
        self.click_view()
        self.click_box_view()
