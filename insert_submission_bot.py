import time
import pandas as pd
from menu_bar import MenuBar
from file_insert import FileInsert
from title_bar import TitleBar


def enter_lrs_submission(file_number, file_status, file_name, file_from_date, file_to_date, file_comment):
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


if __name__ == '__main__':
    path = input("Enter path to excel file containing submission data: ")
    df = pd.read_excel(path)

    titlebar = TitleBar()
    titlebar.click_icon()

    for row in df.itertuples(name=None):
        # Get column data
        lrs_file_number = str(row[2])
        lrs_file_status = str(row[8])
        lrs_file_name = str(row[10])
        lrs_file_from_date = str(row[22])
        lrs_file_to_date = str(row[23])
        lrs_file_comment = str(row[24])

        enter_lrs_submission(lrs_file_number, lrs_file_status, lrs_file_name, lrs_file_from_date, lrs_file_to_date,
                             lrs_file_comment)
