import time
import pyautogui
from utilities import search_for_image
from config import *


class FileStatus:

    def __init__(self):
        self.file_status_img = os.path.join(file_status_image_path, "file_status.PNG")
        self.status_date_img = os.path.join(file_status_image_path, "status_date.PNG")
        self.update_all_img = os.path.join(file_status_image_path, "update_all.PNG")
        self.close_img = os.path.join(file_status_image_path, "close.PNG")
        self.ok_btn_img = os.path.join(file_status_image_path, "ok_btn.PNG")

    def enter_file_status(self, status: str):
        file_status_coord = search_for_image(self.file_status_img)
        pyautogui.moveTo(file_status_coord)
        time.sleep(0.25)
        pyautogui.move(100, 0)
        time.sleep(0.25)
        pyautogui.click()
        for i in range(10):
            pyautogui.press("backspace")
        time.sleep(0.25)
        pyautogui.write(status)

    def enter_status_date(self, date: str):
        status_date_coord = search_for_image(self.status_date_img)
        pyautogui.moveTo(status_date_coord)
        time.sleep(0.25)
        pyautogui.move(125, 0)
        time.sleep(0.25)
        pyautogui.click()
        for i in range(20):
            pyautogui.press("backspace")
        time.sleep(0.25)
        pyautogui.write(date)

    def click_update_all(self):
        update_all_coord = search_for_image(self.update_all_img)
        pyautogui.moveTo(update_all_coord)
        time.sleep(0.25)
        pyautogui.click()

    def click_close(self):
        close_coord = search_for_image(self.close_img)
        pyautogui.moveTo(close_coord)
        time.sleep(0.25)
        pyautogui.click()

    def click_ok_button(self):
        ok_coord = search_for_image(self.ok_btn_img, confidence=0.9)
        pyautogui.moveTo(ok_coord)
        time.sleep(0.25)
        pyautogui.click()
