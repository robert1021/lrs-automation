import os
from file_comparison import FileComparison
from constants import PLA_SHEET, SLA_SHEET, FSRN_SHEET, CTA_SHEET
import pandas as pd
from datetime import datetime
from batch_import import BatchImport


def generate(imu_path: str, pla_path: str, sla_path: str, fsrn_path: str, cta_path: str):

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

    # Create parent files report - Files that need to be created in LRS
    parent_files_to_create_df = pd.concat(
        [pla_lrs_comparison.parent_files_to_create_df, sla_lrs_comparison.parent_files_to_create_df,
         fsrn_lrs_comparison.parent_files_to_create_df, cta_lrs_comparison.parent_files_to_create_df])

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


if __name__ == '__main__':
    imu = input("Enter path to IMU dashboard: ")
    pla = input("Enter path to LRS PLA report: ")
    sla = input("Enter path to LRS SLA report: ")
    fsrn = input("Enter path to LRS FSRN report: ")
    cta = input("Enter path to LRS CTA report: ")

    if not imu.endswith(".xlsx") or not os.path.isfile(imu):
        raise ValueError("error - file path")
    if not pla.endswith(".csv") or not os.path.isfile(pla):
        raise ValueError("error - file path")
    if not sla.endswith(".csv") or not os.path.isfile(sla):
        raise ValueError("error - file path")
    if not fsrn.endswith(".csv") or not os.path.isfile(fsrn):
        raise ValueError("error - file path")
    if not cta.endswith(".csv") or not os.path.isfile(cta):
        raise ValueError("error - file path")

    generate(imu, pla, sla, fsrn, cta)

    print("Completed successfully!")
