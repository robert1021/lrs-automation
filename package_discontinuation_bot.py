import subprocess
import shutil
import os


if __name__ == "__main__":
    try:
        process = subprocess.run([
            "pyinstaller",
            "--onefile",
            "--add-data", "images;images",
            "--add-data", r"utilities.py;.",
            "--add-data", r"constants.py;.",
            "--add-data", r"config.py;.",
            "--add-data", r"file_insert.py;.",
            "--add-data", r"file_search.py;.",
            "--add-data", r"file_status.py;.",
            "--add-data", r"folder_tab_window.py;.",
            "--add-data", r"folder_update.py;.",
            "--add-data", r"menu_bar.py;.",
            "--add-data", r"title_bar.py;.",
            "--hidden-import=openpyxl",
            "--hidden-import=pandas",
            "--hidden-import=pyautogui",
            "--hidden-import=pydirectinput",
            "discontinuation_bot.py"
        ], text=True, check=True)

        shutil.rmtree("build")
        os.remove("discontinuation_bot.spec")
        os.rename("dist/discontinuation_bot.exe", f"discontinuation_bot.exe")
        shutil.rmtree("dist")

    except Exception as e:
        print("Error:", e)