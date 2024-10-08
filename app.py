import os
import openpyxl
import shutil
import time
from menu_bar import MenuBar
from file_insert import FileInsert
from title_bar import TitleBar
from rich.console import Console
from rich.prompt import Prompt
from enums import *
from file_comparison import FileComparison
from constants import PLA_SHEET, SLA_SHEET, FSRN_SHEET, CTA_SHEET
from datetime import datetime
import pandas as pd
from batch_import import BatchImport


def handle_generate_batch_import(imu_path: str, pla_path: str, sla_path: str, fsrn_path: str, cta_path: str) -> str:
    # Compare LRS report to dashboard report
    # PLA
    pla_lrs_comparison = FileComparison(lrs_report_path=pla_path,
                                        imu_dashboard_report_path=imu_path,
                                        imu_dashboard_sheet=PLA_SHEET)
    pla_lrs_comparison.get_files_to_create()
    print("PLA LRS comparison complete")

    # SLA
    sla_lrs_comparison = FileComparison(lrs_report_path=sla_path,
                                        imu_dashboard_report_path=imu_path,
                                        imu_dashboard_sheet=SLA_SHEET)
    sla_lrs_comparison.get_files_to_create()
    print("SLA LRS comparison complete")

    # FSRN
    fsrn_lrs_comparison = FileComparison(lrs_report_path=fsrn_path,
                                         imu_dashboard_report_path=imu_path,
                                         imu_dashboard_sheet=FSRN_SHEET)
    fsrn_lrs_comparison.get_files_to_create()
    print("FSRN LRS comparison complete")

    # CTA
    cta_lrs_comparison = FileComparison(lrs_report_path=cta_path,
                                        imu_dashboard_report_path=imu_path,
                                        imu_dashboard_sheet=CTA_SHEET)
    cta_lrs_comparison.get_files_to_create()
    print("CTA LRS comparison complete")

    # Create output dir
    if not os.path.isdir('Output'):
        os.mkdir('Output')

    parents_dfs = [pla_lrs_comparison.parent_files_to_create_df, sla_lrs_comparison.parent_files_to_create_df,
                   fsrn_lrs_comparison.parent_files_to_create_df, cta_lrs_comparison.parent_files_to_create_df]

    if not all(x is None for x in parents_dfs):
        # Create parent files report - Files that need to be created in LRS
        parent_files_to_create_df = pd.concat(parents_dfs)

        # Export parent files to create DF to excel file
        parent_filename = f"LRS-PAR-TO-CREATE-{datetime.today().strftime('%Y-%m-%d')}.xlsx"
        parent_files_to_create_df.to_excel(
            fr"Output\{parent_filename}",
            sheet_name='PAR', index=False)

        print("Parent files report created")

    # Create batch import object
    batch_import_obj = BatchImport()

    # Create report from template
    batch_import_obj.create_lrs_batch_import_report()

    print("Batch import file created")

    # Add data to report

    # PLA
    if pla_lrs_comparison.files_submissions_to_create_df is not None:
        batch_import_obj.add_to_report(pla_lrs_comparison.files_submissions_to_create_df)
        print("PLA files added to batch import report")
    else:
        print("No PLA files to add to the batch import report")

    # SLA
    if sla_lrs_comparison.files_submissions_to_create_df is not None:

        batch_import_obj.add_to_report(sla_lrs_comparison.files_submissions_to_create_df)
        print("SLA files added to batch import report")
    else:
        print("No SLA files to add to the batch import report")

    # FSRN
    if fsrn_lrs_comparison.files_submissions_to_create_df is not None:
        batch_import_obj.add_to_report(fsrn_lrs_comparison.files_submissions_to_create_df)
        print("FSRN files added to batch import report")
    else:
        print("No FSRN files to add to the batch import report")

    # CTA
    if cta_lrs_comparison.files_submissions_to_create_df is not None:
        batch_import_obj.add_to_report(cta_lrs_comparison.files_submissions_to_create_df)
        print("CTA files added to batch import report")
    else:
        print("No CTA files to add to the batch import report")

    return "success"


def handle_parent_files_rpa(file_path: str) -> str:
    df = pd.read_excel(file_path)
    titlebar = TitleBar()
    titlebar.click_icon()

    for row in df.itertuples():
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


def handle_submission_files_rpa(file_path) -> str:
    df = pd.read_excel(file_path)
    titlebar = TitleBar()
    titlebar.click_icon()

    for row in df.itertuples(name=None):
        # Get column data
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
    console = Console()
    console.print("LRS Automation Tool", style="bold green")
    console.print(f"{'-' * 50}", style="bold blue")

    while True:

        tool_selection_input = Prompt.ask(prompt="[bold green]Which tool would you like to use?[/bold green]",
                                          choices=LRSTools.get_values(), show_choices=True, case_sensitive=False,
                                          console=console)

        results = ""

        if tool_selection_input.lower() == LRSTools.GENERATE_BATCH_IMPORT.value.lower():
            imu_dashboard_path_input = Prompt.ask("[bold green]Enter path to the IMU Dashboard[/bold green]",
                                                  console=console)
            pla_path_input = Prompt.ask("[bold green]Enter path to the PLA submissions[/bold green]", console=console)
            sla_path_input = Prompt.ask("[bold green]Enter path to the SLA submissions[/bold green]", console=console)
            fsrn_path_input = Prompt.ask("[bold green]Enter path to the FSRN submissions[/bold green]", console=console)
            cta_path_input = Prompt.ask("[bold green]Enter path to the CTA submissions/bold green]", console=console)

            results = handle_generate_batch_import(imu_dashboard_path_input, pla_path_input, sla_path_input,
                                                   fsrn_path_input,
                                                   cta_path_input)

        elif tool_selection_input.lower() == LRSTools.PARENT_FILES_RPA.value.lower():
            file_path_input = Prompt.ask(
                "[bold green]Enter path to the file containing parent file data[/bold green]", console=console)

            results = handle_parent_files_rpa(file_path_input)

        elif tool_selection_input.lower() == LRSTools.SUBMISSION_FILES_RPA.value.lower():
            file_path_input = Prompt.ask(
                "[bold green]Enter path to the file containing submission file data[/bold green]", console=console)

            results = handle_submission_files_rpa(file_path_input)

        console.print(f"{results}", style="bold green")
        run_another_input = Prompt.ask(prompt="[bold blue]Would you like to run another tool?[/bold blue]",
                                       choices=["Yes", "No"], show_choices=True, case_sensitive=False, console=console)

        if run_another_input.lower() == "no":
            console.print(f"Exiting...", style="bold red")
            break
