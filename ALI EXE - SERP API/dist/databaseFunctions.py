import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds_sheet = ServiceAccountCredentials.from_json_keyfile_name(
    r"Google Sheets.json", scope)
client = gspread.authorize(creds_sheet)
sheet_url = "https://docs.google.com/spreadsheets/d/1Ou4xWFvCw17DhpihJLwSQUMoyRPk5n_SXwS1GHYarZU/edit?usp=sharing"
sheet = client.open_by_url(sheet_url)


def setup_google_sheet(number):
    sub_sheet_records = sheet.get_worksheet(number)
    return sub_sheet_records


def get_column_data(sheet_number, column_index):
    """
    :param column_name: Name of the column.
    :return: Returns the data of the column.
    """
    sub_sheet_records = setup_google_sheet(sheet_number)
    column_data = sub_sheet_records.col_values(column_index)
    return column_data


def update_sheet(sheet_number, values: list):
    # insert new row
    sub_sheet_records = setup_google_sheet(sheet_number)
    sub_sheet_records.insert_row(values, index=2)


def cell_update(sheet_number, row, column, value):
    sub_sheet_records = setup_google_sheet(sheet_number)
    sub_sheet_records.update_cell(row, column, value)


