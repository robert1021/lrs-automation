"""LRS Automation: business logic plus the GUI entry point.

The old ``rich`` text UI is gone; :func:`run_app` now launches the tkinter
GUI from :mod:`gui`. The ``handle_*`` helpers below are reused by the GUI
worker threads and stay importable for scripting.
"""

import os
import time
from datetime import datetime

import pandas as pd

from menu_bar import MenuBar
from file_insert import FileInsert
from title_bar import TitleBar
from enums import LRSTools
from file_comparison import FileComparison
from constants import PLA_SHEET, SLA_SHEET, FSRN_SHEET, CTA_SHEET
from batch_import import BatchImport


def _emit(on_log, message):
    if on_log is not None:
        on_log(message)
    else:
        print(message)


def _require_file(path: str, label: str) -> str:
    cleaned = (path or "").strip().strip("'\"")
    if not cleaned:
        raise ValueError(f"{label}: no file selected.")
    if not os.path.isfile(cleaned):
        raise ValueError(f"{label}: file not found: {cleaned}")
    return cleaned


def handle_generate_batch_import(imu_path: str, pla_path: str, sla_path: str,
                                 fsrn_path: str, cta_path: str,
                                 on_log=None) -> str:
    """Compare LRS reports to the IMU dashboard and build output workbooks."""
    imu_path = _require_file(imu_path, "IMU Dashboard")
    pla_path = _require_file(pla_path, "PLA submissions")
    sla_path = _require_file(sla_path, "SLA submissions")
    fsrn_path = _require_file(fsrn_path, "FSRN submissions")
    cta_path = _require_file(cta_path, "CTA submissions")

    comparisons = []
    for label, report_path, sheet in (
        ("PLA", pla_path, PLA_SHEET),
        ("SLA", sla_path, SLA_SHEET),
        ("FSRN", fsrn_path, FSRN_SHEET),
        ("CTA", cta_path, CTA_SHEET),
    ):
        comparison = FileComparison(lrs_report_path=report_path,
                                    imu_dashboard_report_path=imu_path,
                                    imu_dashboard_sheet=sheet)
        comparison.get_files_to_create()
        _emit(on_log, f"{label} LRS comparison complete")
        comparisons.append(comparison)

    os.makedirs("Output", exist_ok=True)

    parents_dfs = [c.parent_files_to_create_df for c in comparisons]
    if not all(x is None for x in parents_dfs):
        parent_files_to_create_df = pd.concat(parents_dfs)
        parent_filename = f"LRS-PAR-TO-CREATE-{datetime.today().strftime('%Y-%m-%d')}.xlsx"
        parent_full = os.path.join("Output", parent_filename)
        parent_files_to_create_df.to_excel(parent_full, sheet_name="PAR", index=False)
        _emit(on_log, f"Parent files report created: {parent_full}")

    batch_import_obj = BatchImport()
    batch_import_obj.create_lrs_batch_import_report()
    _emit(on_log, f"Batch import file created: {batch_import_obj.batch_import_path}")

    for label, comparison in zip(("PLA", "SLA", "FSRN", "CTA"), comparisons):
        if comparison.files_submissions_to_create_df is not None:
            batch_import_obj.add_to_report(comparison.files_submissions_to_create_df)
            _emit(on_log, f"{label} files added to batch import report")
        else:
            _emit(on_log, f"No {label} files to add to the batch import report")

    return "success"


def handle_parent_files_rpa(file_path: str, on_log=None) -> str:
    """Drive the LRS File Insert dialog once per parent row."""
    file_path = _require_file(file_path, "Parent file data")
    df = pd.read_excel(file_path)
    total = len(df)
    titlebar = TitleBar()
    titlebar.click_icon()

    for i, row in enumerate(df.itertuples()):
        _emit(on_log, f"Parent file {i + 1} of {total}")
        parent_number = str(row.lrs_par_number)
        company_name = str(row.company_name)

        lrs_menubar = MenuBar()
        lrs_file_insert = FileInsert()

        lrs_menubar.open_file_insert()
        lrs_file_insert.enter_file_number(parent_number)
        time.sleep(0.25)
        lrs_file_insert.enter_file_status("PAR")
        time.sleep(0.25)
        lrs_file_insert.enter_file_title_english(company_name)
        time.sleep(0.25)
        lrs_file_insert.click_ok_button()
        time.sleep(2)

    return "success"


def handle_submission_files_rpa(file_path, on_log=None) -> str:
    """Drive the LRS File Insert dialog once per submission row."""
    file_path = _require_file(file_path, "Submission file data")
    df = pd.read_excel(file_path)
    total = len(df)
    titlebar = TitleBar()
    titlebar.click_icon()

    for i, row in enumerate(df.itertuples(name=None)):
        _emit(on_log, f"Submission file {i + 1} of {total}")
        file_number = str(row[2])
        file_status = str(row[8])
        file_name = str(row[10])
        file_from_date = str(row[22])
        file_to_date = str(row[23])
        file_comment = str(row[24])

        lrs_menubar = MenuBar()
        lrs_file_insert = FileInsert()

        lrs_menubar.open_file_insert()

        lrs_file_insert.enter_file_number(file_number)
        time.sleep(0.25)
        lrs_file_insert.enter_file_status(file_status)
        time.sleep(0.25)
        lrs_file_insert.enter_file_title_english(file_name)
        time.sleep(0.25)
        lrs_file_insert.add_folder()
        time.sleep(0.25)
        lrs_file_insert.enter_from_date(file_from_date)
        time.sleep(0.25)
        if file_status != "ACT":
            lrs_file_insert.enter_to_date(file_to_date)
            time.sleep(0.25)
        lrs_file_insert.enter_comment(file_comment)
        time.sleep(0.25)
        lrs_file_insert.click_ok_button()
        time.sleep(2)

    return "success"


def run_app():
    """Launch the modern tkinter GUI."""
    from gui import launch
    launch()


__all__ = [
    "LRSTools",
    "handle_generate_batch_import",
    "handle_parent_files_rpa",
    "handle_submission_files_rpa",
    "run_app",
]
