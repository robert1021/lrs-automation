import time
from menu_bar import MenuBar
from file_status import FileStatus
from file_search import FileSearch
from folder_tab_window import FolderTabWindow
from folder_update import FolderUpdate
from title_bar import TitleBar
from utilities import search_for_image
import pandas as pd


def enter_lrs_discontinuation(submission_number: str, npn: str, discontinuation_date):
    lrs_menubar = MenuBar()
    lrs_file_search = FileSearch()
    lrs_file_status = FileStatus()
    lrs_folder_tab_window = FolderTabWindow()
    lrs_folder_update = FolderUpdate()

    print(submission_number)
    lrs_menubar.open_file_search()
    time.sleep(1)
    lrs_file_search.search_for_file(submission_number)
    time.sleep(1)
    lrs_menubar.click_folders_tab()
    time.sleep(1)
    # Open file status
    lrs_menubar.open_file_status()
    time.sleep(1)
    lrs_file_status.enter_file_status("DOR")
    time.sleep(0.25)
    lrs_file_status.enter_status_date(discontinuation_date)
    time.sleep(0.25)
    lrs_file_status.click_update_all()
    time.sleep(0.25)
    lrs_file_status.click_close()
    time.sleep(0.25)
    lrs_file_status.click_ok_button()
    time.sleep(1)
    lrs_menubar.click_refresh()
    time.sleep(3)

    # Update folders
    # VOL 1
    vol_1_coord = search_for_image(lrs_folder_tab_window.vol_1_img, times_to_search=2, quit_program=False)
    print(vol_1_coord)
    print("VOL 1")
    time.sleep(1)
    if vol_1_coord is not None:
        lrs_folder_tab_window.open_update_folder(vol_1_coord)
        time.sleep(2)
        # Issue with date out of range - LRS bug?
        # lrs_folder_update.update_to_date(date)
        lrs_folder_update.update_comment(f" Discontinued - {npn} ")
        time.sleep(1)
        lrs_folder_update.click_ok_button()
    else:
        # Check for ALT
        vol_1_alt_coord = search_for_image(lrs_folder_tab_window.vol_1_alt_img, times_to_search=2,
                                           quit_program=False)
        print(vol_1_alt_coord)
        print("VOL 1 ALT")
        time.sleep(1)
        if vol_1_alt_coord is not None:
            lrs_folder_tab_window.open_update_folder(vol_1_alt_coord)
            time.sleep(2)
            # Issue with date out of range - LRS bug?
            # lrs_folder_update.update_to_date(date)
            lrs_folder_update.update_comment(f" Discontinued - {npn} ")
            time.sleep(1)
            lrs_folder_update.click_ok_button()

    # VOL 2 - Optional
    vol_2_coord = search_for_image(lrs_folder_tab_window.vol_2_img, times_to_search=2, quit_program=False)
    print(vol_2_coord)
    print("VOL 2")
    time.sleep(1)
    if vol_2_coord is not None:
        lrs_folder_tab_window.open_update_folder(vol_2_coord)
        time.sleep(2)
        lrs_folder_update.update_comment(f" Discontinued - {npn} ")
        time.sleep(1)
        lrs_folder_update.click_ok_button()

    # VOL 3 - Optional
    # etc...

    # Update Wallets - Optional
    wal_1_coord = search_for_image(lrs_folder_tab_window.wal_1_img, times_to_search=2, quit_program=False)
    print(wal_1_coord)
    print("WAL 1")
    time.sleep(1)
    if wal_1_coord is not None:
        lrs_folder_tab_window.open_update_folder(wal_1_coord)
        time.sleep(2)
        lrs_folder_update.update_comment(f" Discontinued - {npn} ")
        time.sleep(1)
        lrs_folder_update.click_ok_button()

    # Update DB - Optional
    db_1_coord = search_for_image(lrs_folder_tab_window.db_1_img, times_to_search=2, quit_program=False)
    print(db_1_coord)
    print("DB 1")
    time.sleep(1)
    if db_1_coord is not None:
        lrs_folder_tab_window.open_update_folder(db_1_coord)
        time.sleep(2)
        lrs_folder_update.update_comment(f" Discontinued")
        time.sleep(1)
        lrs_folder_update.click_ok_button()

    # Update CD - Optional
    cd_1_coord = search_for_image(lrs_folder_tab_window.cd_1_img, times_to_search=2, quit_program=False)
    print(cd_1_coord)
    print("CD 1")
    time.sleep(1)
    if cd_1_coord is not None:
        lrs_folder_tab_window.open_update_folder(cd_1_coord)
        time.sleep(2)
        lrs_folder_update.update_comment(f" Discontinued - {npn} ")
        time.sleep(1)
        lrs_folder_update.click_ok_button()

    time.sleep(3)


if __name__ == '__main__':
    path = input("Enter path to excel file containing submission data: ")
    date = input("Enter the Discontinuation Date: ")
    df = pd.read_excel(path, dtype=str)

    titlebar = TitleBar()
    titlebar.click_icon()

    for row in df.itertuples():
        enter_lrs_discontinuation(str(row.SUBMISSION), str(row.NPN), str(date))
