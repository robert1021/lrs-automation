import time
from menu_bar import MenuBar
from file_insert import FileInsert
from title_bar import TitleBar
import pandas as pd


def enter_lrs_parent(parent_number: str, company_name: str):
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


if __name__ == '__main__':
    path = input("Enter path to excel file containing parent file data: ")
    df = pd.read_excel(path)

    titlebar = TitleBar()
    titlebar.click_icon()

    for row in df.itertuples():
        enter_lrs_parent(str(row.lrs_par_number), str(row.company_name))
