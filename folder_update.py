import time
import pyautogui
import pydirectinput
from utilities import search_for_image
from config import *


class FolderUpdate:

    def __init__(self):
        self.to_date_img = os.path.join(file_insert_image_path, "to_date.PNG")
        self.comment_img = os.path.join(file_insert_image_path, "comment.PNG")
        self.ok_btn_img = os.path.join(file_insert_image_path, "ok_btn.PNG")

    def update_to_date(self, date):
        to_date_coord = search_for_image(self.to_date_img)
        pyautogui.moveTo(to_date_coord)
        time.sleep(0.25)
        pyautogui.move(130, 0)
        time.sleep(0.25)
        pyautogui.click()
        for i in range(20):
            pyautogui.press("backspace")
        time.sleep(0.25)
        pyautogui.write(date)
        time.sleep(0.25)
        pyautogui.move(57, 3)
        time.sleep(0.25)
        pyautogui.click()

    def update_comment(self, text: str):
        comment_coord = search_for_image(self.comment_img)
        pyautogui.moveTo(comment_coord)
        time.sleep(0.25)
        pyautogui.move(175, 0)
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(0.25)
        for i in range(20):
            pydirectinput.press("down")
        time.sleep(0.25)
        for i in range(20):
            pydirectinput.press("right")
        time.sleep(0.25)
        pyautogui.write(text)

    def click_ok_button(self):
        ok_btn_coord = search_for_image(self.ok_btn_img)
        pyautogui.moveTo(ok_btn_coord)
        time.sleep(0.25)
        pyautogui.click()
