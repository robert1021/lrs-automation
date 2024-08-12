import subprocess
import shutil
import os


if __name__ == "__main__":
    try:
        process = subprocess.run([
            "pyinstaller",
            "--onefile",
            "--add-data", r"utilities.py;.",
            "--add-data", r"constants.py;.",
            "--add-data", r"config.py;.",
            "--add-data", r"batch_import.py;.",
            "--add-data", r"dashboard_report_processor.py;.",
            "--add-data", r"file_comparison.py;.",
            "--add-data", r"generate_file_number.py;.",
            "--add-data", r"report_processor.py;.",
            "--hidden-import=openpyxl",
            "--hidden-import=pandas",
            "--hidden-import=pyautogui",
            "--hidden-import=pydirectinput",
            "generate_batch_import.py"
        ], text=True, check=True)

        shutil.rmtree("build")
        os.remove("generate_batch_import.spec")
        os.rename("dist/generate_batch_import.exe", f"generate_batch_import.exe")
        shutil.rmtree("dist")

    except Exception as e:
        print("Error:", e)