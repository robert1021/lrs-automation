import time
import pyautogui
import pydirectinput
from utilities import search_for_image
from config import *


class FileSearch:

    def __init__(self):
        self.fast_find_criteria_img = os.path.join(file_search_image_path, "fast_find_criteria.PNG")
        self.find_now_btn_img = os.path.join(file_search_image_path, "find_now_btn.PNG")

    def click_find_now_button(self):
        find_now_btn_coord = search_for_image(self.find_now_btn_img)
        pyautogui.moveTo(find_now_btn_coord)
        time.sleep(0.25)
        pyautogui.click()

    def search_for_file(self, file_number):
        fast_find_criteria_coord = search_for_image(self.fast_find_criteria_img)
        pyautogui.moveTo(fast_find_criteria_coord)
        pyautogui.move(75, 77)
        time.sleep(0.25)
        pydirectinput.doubleClick()
        pydirectinput.press("backspace")
        time.sleep(0.25)
        pyautogui.write(f"*{file_number}")
        time.sleep(0.25)
        self.click_find_now_button()

