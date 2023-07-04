import gspread  # pip install oauth2client, pandas, flask,selenium
from oauth2client.service_account import ServiceAccountCredentials  # pip install oauth2client
import time
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
sheet_url = 'https://docs.google.com/spreadsheets/d/17bT5HMel9iGlcVYHdoapny9rGc8Zrjpp7ZgFqz8qQDA/edit?usp=sharing'

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
    while True:
        try:
            sheet = client.open_by_url(sheet_url).worksheet(sheet_name)

            # delete row 2
            sheet.delete_row(2)
            record = value
            sheet.insert_row(record, 2)

            break
        except:
            print("Error in updating cell")
            time.sleep(10)
            continue


def update_home():
    while True:
        try:
            df = pd.read_csv('updated_data.csv')
            # upload the csv file to google sheets

            df = df.fillna('NA')

            sheet = client.open_by_url(sheet_url).worksheet("HOME")
            sheet.clear()
            column_names_upper = [str(x.upper()) for x in df.columns.values.tolist()]
            sheet.update([column_names_upper] + df.values.tolist())

            print("Updated Home Data")

            # make column bold with 10 size and other data nunito font but with 9 size
            sheet.format('A1:Z1', {'textFormat': {'bold': True, 'fontSize': 10}})





            break
        except:
            print("Error in updating home")
            time.sleep(10)
            continue


