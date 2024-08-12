from constants import PLA_LRS_NUM, SLA_LRS_NUM, FSRN_LRS_NUM, CTA_LRS_NUM


class GenerateFileNumber:
    """ This class is used to generate a file number for PLA, SLA, FSRN, CTA
        in the LRS file format

    """

    def __init__(self, company_code, file_number, submission_number):

        self.company_code = company_code
        self.file_number = file_number
        self.submission_number = submission_number

    def generate_pla_parent_number(self):
        """ Generates a parent number in the LRS format for PLA

        Returns
        -------
            parent_number(str): HC6-70-6-xxxxx

        """
        return f'{PLA_LRS_NUM}-{self.company_code}'

    def generate_pla_file_number(self):
        """ Generates a file number in the LRS format for PLA

        Returns
        -------
            The number returned depends on if the file and submission number match

            1.
                HC6-70-6-xxxxx-xxxxxx

            2.
                HC6-70-6-xxxxx-xxxxxx.xxxxxx

        """
        if self.file_number == self.submission_number:

            return f'{PLA_LRS_NUM}-{str(self.company_code)}-{str(self.file_number)}'

        else:

            return f'{PLA_LRS_NUM}-{str(self.company_code)}-{str(self.file_number)}.{str(self.submission_number)}'

    def generate_sla_parent_number(self):
        """ Generates a parent number in the LRS format for SLA

        Returns
        -------
            parent_number(str): HC6-70-7-xxxxx

        """
        return f'{SLA_LRS_NUM}-{self.company_code}'

    def generate_sla_file_number(self):
        """ Generates a file number in the LRS format for SLA

        Returns
        -------
            The number returned depends on if the file and submission number match

            1.
                HC6-70-7-xxxxx-xxxxxx

            2.
                HC6-70-7-xxxxx-xxxxxx.xxxxxx

        """
        if self.file_number == self.submission_number:

            return f'{SLA_LRS_NUM}-{str(self.company_code)}-{str(self.file_number)}'

        else:

            return f'{SLA_LRS_NUM}-{str(self.company_code)}-{str(self.file_number)}.{str(self.submission_number)}'

    def generate_fsrn_parent_number(self):
        """ Generates a parent number in the LRS format for FSRN

        Returns
        -------
            parent_number(str): HC6-27-7-xxxxx

        """
        return f'{FSRN_LRS_NUM}-{self.company_code}'

    def generate_fsrn_file_number(self):
        """ Generates a file number in the LRS format for fsrn

        Returns
        -------
            The number returned depends on if the file and submission number match

            1.
                HC6-24-7-xxxxx-xxxxxx

            2.
                HC6-24-7-xxxxx-xxxxxx.xxxxxx

        """
        if self.file_number == self.submission_number:

            return f'{FSRN_LRS_NUM}-{str(self.company_code)}-{str(self.file_number)}'

        else:

            return f'{FSRN_LRS_NUM}-{str(self.company_code)}-{str(self.file_number)}.{str(self.submission_number)}'

    def generate_cta_parent_number(self):
        """ Generates a parent number in the LRS format for CTA

        Returns
        -------
            parent_number(str): HC6-11-8-xxxxx

        """
        return f'{CTA_LRS_NUM}-{self.company_code}'

    def generate_cta_file_number(self):
        """ Generates a file number in the LRS format for CTA

        Returns
        -------
            The number returned depends on if the file and submission number match

            1.
                HC6-11-8-xxxxx-xxxxxx

            2.
                HC6-11-8-xxxxx-xxxxxx.xxxxxx

        """
        if self.file_number == self.submission_number:

            return f'{CTA_LRS_NUM}-{str(self.company_code)}-{str(self.file_number)}'

        else:

            return f'{CTA_LRS_NUM}-{str(self.company_code)}-{str(self.file_number)}.{str(self.submission_number)}'
