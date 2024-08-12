from utilities import get_frozen_status
import os
import sys

image_path = os.path.join(sys._MEIPASS, "images") if get_frozen_status() is True else "images"
file_insert_image_path = os.path.join(image_path, "file_insert")
file_search_image_path = os.path.join(image_path, "file_search")
file_status_image_path = os.path.join(image_path, "file_status")
folder_tab_image_path = os.path.join(image_path, "folder_tab")
menubar_image_path = os.path.join(image_path, "menubar")
titlebar_image_path = os.path.join(image_path, "title_bar")

imu_dashboard_path = r"N:\BLSS\HC6 Health Risk Protection\HC6-101 Regulatory Reporting\SMD\NHPD Dashboard\NNHPD Dashboard - IMU.xlsx"