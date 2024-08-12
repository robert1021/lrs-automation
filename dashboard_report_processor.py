from generate_file_number import GenerateFileNumber
from constants import PLA_SHEET, SLA_SHEET, FSRN_SHEET, CTA_SHEET
import pandas as pd


class DashboardReportProcessor:
    # set the max columns to none
    pd.set_option('display.max_columns', None)

    def __init__(self, report_path, sheet_name):

        self.report_path = report_path

        if sheet_name not in [PLA_SHEET, SLA_SHEET, FSRN_SHEET, CTA_SHEET]:
            raise Exception('Incorrect sheet name')
        else:
            self.sheet_name = sheet_name

        # holds all data
        self.data_df = None

        # holds only licensed data
        self.licensed_data_df = None
        # holds only withdrawn and refused data
        self.withdrawn_refused_data_df = None
        # holds only rejected and had license data
        self.licensed_rejected_data_df = None
        # holds only rejected no license data
        self.rejected_data_df = None

    def process_report(self):
        """ Reads the report path in as a dataframe
            Filters out the rows that don't have a completed date
            Sets the data_df in constructor

        """

        df = pd.read_excel(self.report_path, sheet_name=self.sheet_name)

        # filter out rows where completed date not null (no completed date)
        df = df[df.completed_date.notnull()]

        self.data_df = df

        self.__add_lrs_file_number_to_row()

    def __add_lrs_file_number_to_row(self):
        """ Iterates over data_df and adds lrs file number to a new column lrs_file_number

        """
        # create lrs file number column
        self.data_df['lrs_file_number'] = ''
        self.data_df['lrs_par_number'] = ''

        # iterate the df
        for row in self.data_df.itertuples():
            # create instance of file gen class
            imu_file = GenerateFileNumber(str(int(row.COMPANY_CODE)), str(int(row.file_no)),
                                          str(int(row.SUBMISSION_ID)))

            lrs_file_number = None
            lrs_par_number = None

            # generate lrs file number depending on which sheet you are using pla, sla, fsrn, cta
            if self.sheet_name == PLA_SHEET:
                lrs_file_number = imu_file.generate_pla_file_number()
                lrs_par_number = imu_file.generate_pla_parent_number()
            elif self.sheet_name == SLA_SHEET:
                lrs_file_number = imu_file.generate_sla_file_number()
                lrs_par_number = imu_file.generate_sla_parent_number()
            elif self.sheet_name == FSRN_SHEET:
                lrs_file_number = imu_file.generate_fsrn_file_number()
                lrs_par_number = imu_file.generate_fsrn_parent_number()
            elif self.sheet_name == CTA_SHEET:
                lrs_file_number = imu_file.generate_cta_file_number()
                lrs_par_number = imu_file.generate_cta_parent_number()

            # set lrs file number in each row
            self.data_df.loc[row.Index, 'lrs_file_number'] = lrs_file_number
            self.data_df.loc[row.Index, 'lrs_par_number'] = lrs_par_number
