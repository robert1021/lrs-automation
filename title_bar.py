import time
import pyautogui
from utilities import search_for_image
from config import *


class TitleBar:

    def __init__(self):
        self.icon_img = os.path.join(titlebar_image_path, "lrs_icon.PNG")

    def click_icon(self):
        icon_coord = search_for_image(self.icon_img)
        pyautogui.moveTo(icon_coord)
        pyautogui.move(50, 0)
        time.sleep(0.25)
        pyautogui.click()
