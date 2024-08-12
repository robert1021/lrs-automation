import pyautogui
import time
import sys


def get_frozen_status() -> bool:
    """
    Check if the current Python environment is frozen.

    :return: True if the environment is frozen (e.g., packaged into an executable), False otherwise.
    """
    if getattr(sys, "frozen", False):
        return True
    else:
        return False


def terminate_program(message: str):
    print(message)
    sys.exit()


def search_for_image(image: str, confidence=0.9, grayscale=False, wait_time=3, times_to_search=20, quit_program=True):
    search_count = 0
    print("Searching...")
    coord = pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale)
    search_count += 1
    if pyautogui.position() == (0, 0):
        terminate_program("Failsafe triggered...")
    while not coord:
        time.sleep(wait_time)
        print("Searching...")
        coord = pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale)
        search_count += 1
        if pyautogui.position() == (0, 0):
            terminate_program("Failsafe triggered...")
        elif not coord and search_count == times_to_search:
            if quit_program:
                terminate_program("Exiting...")
            return coord
    print("Found!")
    return coord
