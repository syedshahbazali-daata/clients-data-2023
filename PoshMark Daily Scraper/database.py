import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
sheet_url = 'https://docs.google.com/spreadsheets/d/1qbi8T99J4wZJLZim79yYYk6QSjr096yywxGwHnY17-w/edit?usp=sharing'

creds_sheet = ServiceAccountCredentials.from_json_keyfile_name(
    r"GoogleSheetsApi.json", scope)
client = gspread.authorize(creds_sheet)
sheet = client.open_by_url(sheet_url).sheet1


def get_max_row():
    complete_data = list(sheet.get_all_values())
    return len(complete_data) - 1


def update_sheet(list_of_records):
    while True:
        try:
            sheet.append_rows(list_of_records)
            break
        except:
            print("Error updating sheet, trying again in 5 seconds")
            time.sleep(5)
            continue

