from datetime import datetime, timedelta

import gspread  # pip install oauth2client, pandas, flask,selenium
from oauth2client.service_account import ServiceAccountCredentials  # pip install oauth2client
import time

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
sheet_url = 'https://docs.google.com/spreadsheets/d/1UNTwKP57yItfySQzuR8baBrBiJ-Qw2q3WmHsdkxsDyk/edit?usp=sharing'

creds_sheet = ServiceAccountCredentials.from_json_keyfile_name(
    r"GoogleSheetsApi.json", scope)
client = gspread.authorize(creds_sheet)

print("Google Sheets API Connected")


# FUNCTION TO GET THE DATA FROM THE GOOGLE SHEET


def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')
    return data


def update_row(value: list, sheet_name):
    """
    this function updates the row in the google sheet
    """

    while True:
        try:
            sheet = client.open_by_url(sheet_url).worksheet(sheet_name)

            # delete row 2
            sheet.delete_row(2)  # delete row 2
            record = value
            sheet.insert_row(record, 2)

            break
        except:
            print("Error in updating cell")
            time.sleep(10)
            continue


def add_multiple_rows(record: list, sheet_name):
    while True:
        try:
            sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
            sheet.insert_rows(record, 2)
            break
        except:
            print("Error in updating cell")
            time.sleep(10)
            continue


def update_sheet(sheet_name, record: list, column_names: list):
    while True:
        try:
            sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
            sheet.clear()
            sheet.update([column_names] + record)
            break
        except Exception as e:
            print(e)
            print("Error in updating cell")
            time.sleep(10)
            continue

