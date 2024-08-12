import pandas as pd


class ReportProcessor:

    def __init__(self, report_path):
        self.report_path = report_path

        # dict to hold all numbers
        self.data_dict = {}

    def process_report(self):
        """ Reads the report path in as a dataframe
            Filters out the rows with garbage data
            Iterates through rows with file numbers and creates keys from those numbers in a dict

        """

        df = pd.read_csv(self.report_path, encoding='unicode_escape')

        # filter out rows without useful data and select only column with file numbers
        df = df.loc[df['All File Metadata'] != 'All File Metadata']

        # iterate through df rows and add numbers as keys to dict
        for number in df.iloc[:, 1]:
            self.data_dict[number] = 'FILE' if len(number.rsplit('-', 1)[1]) > 5 else 'PAR'
