# LRS Automation

This project is a Python-based Robotic Process Automation (RPA) tool designed to automate data entry tasks for the LRS (Legacy Review System). It provides a command-line interface to help users process and import data from Excel spreadsheets into the LRS application.

## Features

*   **Generate Batch Import:** Compares data from various source spreadsheets (PLA, SLA, FSRN, CTA) against a central IMU Dashboard report to identify new records that need to be created. It generates a summary Excel file for parent files and a batch import file for submission files.
*   **Parent Files RPA:** Automates the creation of "Parent Files" in the LRS application. It reads data from a specified Excel file and uses GUI automation to enter the information.
*   **Submission Files RPA:** Automates the creation of "Submission Files" in the LRS application, reading the necessary data from an Excel file and performing the data entry through GUI automation.
*   **Interactive CLI:** A user-friendly command-line interface, built with `rich`, guides the user through the available tools and prompts for necessary inputs.

## Dependencies

The project relies on the following Python libraries:

*   PyAutoGUI
*   PyScreeze
*   PyDirectInput
*   openpyxl
*   pandas
*   opencv-python
*   pyinstaller
*   rich
*   pillow

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd lrs-automation
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
    Install the required packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The project uses a `config.py` file for configuration. The primary configuration is the path to the images used for GUI automation. The tool is pre-configured to work with the included `images` directory.

The `imu_dashboard_path` in `config.py` is hardcoded to a network drive:
`N:\BLSS\HC6 Health Risk Protection\HC6-101 Regulatory Reporting\SMD\NHPD Dashboard\NNHPD Dashboard - IMU.xlsx`

Ensure that you have access to this path or update it to the correct location of your `IMU.xlsx` file.

## Usage

Run the application from the command line:

```bash
python main.py
```

The application will launch and present you with a menu of available tools.

### 1. Generate Batch Import

This tool prepares the data for the RPA processes.

1.  Select "Generate Batch Import" from the main menu.
2.  The tool will prompt you to enter the file paths for the following reports:
    *   IMU Dashboard
    *   PLA submissions
    *   SLA submissions
    *   FSRN submissions
    *   CTA submissions
3.  Once the paths are provided, the tool will process the files and create two output files in a new `Output` directory:
    *   `LRS-PAR-TO-CREATE-YYYY-MM-DD.xlsx`: Contains the parent files that need to be created.
    *   `LRS-BATCH-IMPORT-YYYY-MM-DD.xlsx`: Contains the submission files for the batch import.

### 2. Parent Files RPA

This tool automates the creation of parent files in the LRS application.

**Important:** Before running this tool, ensure the LRS application is open and visible on your screen.

1.  Select "Parent Files RPA" from the main menu.
2.  Provide the path to the `LRS-PAR-TO-CREATE-YYYY-MM-DD.xlsx` file generated in the previous step.
3.  The RPA bot will take over your mouse and keyboard to automate the data entry process. Do not interfere with the computer during this process.

### 3. Submission Files RPA

This tool automates the creation of submission files in the LRS application.

**Important:** Before running this tool, ensure the LRS application is open and visible on your screen.

1.  Select "Submission Files RPA" from the main menu.
2.  Provide the path to the `LRS-BATCH-IMPORT-YYYY-MM-DD.xlsx` file.
3.  The RPA bot will automate the data entry. Do not interfere with the computer during this process.

---
