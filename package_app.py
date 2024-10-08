import subprocess
import shutil
import os

if __name__ == "__main__":
    try:
        process = subprocess.run([
            "pyinstaller",
            "--onefile",
            "--add-data", "images;images",
            "--add-data", r"enums.py;.",
            "--add-data", r"utilities.py;.",
            "--add-data", r"constants.py;.",
            "--add-data", r"config.py;.",
            "--add-data", r"batch_import.py;.",
            "--add-data", r"dashboard_report_processor.py;.",
            "--add-data", r"file_comparison.py;.",
            "--add-data", r"generate_file_number.py;.",
            "--add-data", r"report_processor.py;.",
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
            "main.py"
        ], text=True, check=True)

        shutil.rmtree("build")
        os.remove("main.spec")
        os.rename("dist/main.exe", f"LRS Automation Tool.exe")
        shutil.rmtree("dist")

    except Exception as e:
        print("Error:", e)