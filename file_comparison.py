from dashboard_report_processor import DashboardReportProcessor
from report_processor import ReportProcessor
import pandas as pd


class FileComparison:

    def __init__(self, lrs_report_path, imu_dashboard_report_path, imu_dashboard_sheet):

        self.sheet = imu_dashboard_sheet
        self.lrs = ReportProcessor(lrs_report_path)
        # process the report - add data to data_dict
        self.lrs.process_report()
        self.imu = DashboardReportProcessor(imu_dashboard_report_path, self.sheet)
        # process the report - add data to data_df
        self.imu.process_report()

        self.parent_files_to_create_df = None
        self.files_submissions_to_create_df = None

    def get_files_to_create(self):
        """ Processes data and figures out which files / submissions need to be created in LRS.
            Also figures out what parent files need to be created in LRS.

        """
        parent_files_to_create = []
        files_submissions_to_create = []

        # iterate imu dashboard data df as namedtuples
        for row in self.imu.data_df.itertuples():
            # check if the file number is a key in the lrs data dict
            if row.lrs_file_number not in self.lrs.data_dict:
                # append rows to list of file and submissions that need to be created in LRS
                files_submissions_to_create.append(row)

                # check if parent file needs to be created
                if row.lrs_par_number not in self.lrs.data_dict:
                    # append rows to list that holds parent files that need to be created in LRS
                    parent_files_to_create.append(row)

        # remove duplicates from parent df
        par_df = pd.DataFrame(parent_files_to_create).drop_duplicates(subset=['company_name'])

        # Might be no parent files
        # Only filter if there is files
        if not par_df.empty:
            self.parent_files_to_create_df = par_df[['COMPANY_CODE', 'company_name', 'lrs_par_number']]

        # Only do manipulation if there is files to create
        if files_submissions_to_create:
            self.files_submissions_to_create_df = pd.DataFrame(files_submissions_to_create).drop_duplicates(
                subset=['lrs_file_number']).drop(columns=['Index', 'lrs_par_number'], axis=1)

    def create_parent_files_report(self):
        """ Creates Excel report of parent files that need to be created in LRS.

        """
        if self.parent_files_to_create_df is not None:
            self.parent_files_to_create_df.to_excel(f'LRS-{self.sheet}-PAR-TO-CREATE.xlsx', index=False)
