import pyautogui
from utilities import search_for_image
from config import *


class Login:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_user_id_img = os.path.join(image_path, "login_user_id.PNG")
        self.login_password_img = os.path.join(image_path, "login_password.PNG")
        self.login_login_btn_img = os.path.join(image_path, "login_login_btn.PNG")

    def enter_user_id(self):
        user_id_coord = search_for_image(self.login_user_id_img)
        pyautogui.moveTo(user_id_coord)
        pyautogui.move(75, 5)
        pyautogui.click()
        pyautogui.write(self.username, interval=0.1)

    def enter_password(self):
        password_coord = search_for_image(self.login_password_img)
        pyautogui.moveTo(password_coord)
        pyautogui.move(75, 5)
        pyautogui.click()
        pyautogui.write(self.password, interval=0.1)

    def click_login_button(self):
        login_btn_coord = search_for_image(self.login_login_btn_img)
        pyautogui.moveTo(login_btn_coord)
        pyautogui.click()

    def login_user(self):
        self.enter_user_id()
        self.enter_password()
        self.click_login_button()