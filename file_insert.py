import os.path
import time
import pyautogui
from utilities import search_for_image
from config import *


class FileInsert:

    def __init__(self):
        self.file_number_img = os.path.join(file_insert_image_path, "file_number.PNG")
        self.file_status_img = os.path.join(file_insert_image_path, "file_status.PNG")
        self.file_title_english_img = os.path.join(file_insert_image_path, "file_title_english.PNG")
        self.ok_btn_img = os.path.join(file_insert_image_path, "ok_btn.PNG")
        self.disabled_next_btn_img = os.path.join(file_insert_image_path, "disabled_next_btn.PNG")
        self.next_btn_img = os.path.join(file_insert_image_path, "next_btn.PNG")
        self.from_date_img = os.path.join(file_insert_image_path, "from_date.PNG")
        self.to_date_img = os.path.join(file_insert_image_path, "to_date.PNG")
        self.comment_img = os.path.join(file_insert_image_path, "comment.PNG")

    def enter_file_number(self, file_number):
        file_number_coord = search_for_image(self.file_number_img)
        pyautogui.moveTo(file_number_coord)
        time.sleep(0.25)
        pyautogui.move(150, 0)
        time.sleep(0.25)
        pyautogui.click()
        for i in range(20):
            pyautogui.press("backspace")
        time.sleep(0.25)
        pyautogui.write(file_number)

    def enter_file_status(self, status: str):
        file_status_coord = search_for_image(self.file_status_img)
        pyautogui.moveTo(file_status_coord)
        time.sleep(0.25)
        pyautogui.move(150, 0)
        time.sleep(0.25)
        pyautogui.click()
        for i in range(10):
            pyautogui.press("backspace")
        time.sleep(0.25)
        pyautogui.write(status)

    def enter_file_title_english(self, title: str):
        file_title_coord = search_for_image(self.file_title_english_img)
        pyautogui.moveTo(file_title_coord)
        time.sleep(0.25)
        pyautogui.move(150, 0)
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.write(title)

    def click_ok_button(self):
        ok_btn_coord = search_for_image(self.ok_btn_img)
        pyautogui.moveTo(ok_btn_coord)
        time.sleep(0.25)
        pyautogui.click()

    def add_folder(self):
        disabled_next_btn_coord = search_for_image(self.disabled_next_btn_img)
        pyautogui.moveTo(disabled_next_btn_coord)
        time.sleep(0.25)
        pyautogui.move(70, 0)
        time.sleep(0.25)
        pyautogui.click()
        pyautogui.move(0, 148)
        time.sleep(1)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.move(0, -175)
        time.sleep(0.25)
        pyautogui.click()
        next_btn_coord = search_for_image(self.next_btn_img)
        pyautogui.moveTo(next_btn_coord)
        time.sleep(0.25)
        pyautogui.click()

    def enter_from_date(self, date: str):
        from_date_coord = search_for_image(self.from_date_img)
        pyautogui.moveTo(from_date_coord)
        time.sleep(0.25)
        pyautogui.move(120, 0)
        time.sleep(0.25)
        pyautogui.click()
        for i in range(20):
            pyautogui.press("backspace")
        time.sleep(0.25)
        pyautogui.write(date)

    def enter_to_date(self, date: str):
        to_date_coord = search_for_image(self.to_date_img)
        pyautogui.moveTo(to_date_coord)
        time.sleep(0.25)
        pyautogui.move(120, 0)
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.write(date)
        time.sleep(0.25)
        pyautogui.move(57, 3)
        time.sleep(0.25)
        pyautogui.click()

    def enter_comment(self, comment: str):
        comment_coord = search_for_image(self.comment_img)
        pyautogui.moveTo(comment_coord)
        time.sleep(0.25)
        pyautogui.move(100, 0)
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.write(comment)
