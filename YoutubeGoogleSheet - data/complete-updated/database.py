from datetime import datetime, timedelta

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


def update_home_data():
    while True:
        try:
            sheet = client.open_by_url(sheet_url).worksheet("CONTENT")
            data = sheet.get_all_values()
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df.fillna('NA')
            df = df.drop_duplicates(subset=['DATE', 'TIME', 'VIDEO TITLE'], keep='first')
            # Combine 'Date' and 'Time' columns into a single 'DateTime' column
            df['DateTime'] = df['DATE'] + ' ' + df['TIME']
            # Pivot the data
            df_pivot = df.pivot(index='DateTime', columns='VIDEO TITLE', values='VIEWS')
            df_pivot = df_pivot.fillna('NA')
            df_pivot = df_pivot.reset_index().rename_axis(None, axis=1)

            # sort data by DateTime column
            df_pivot = df_pivot.sort_values(by=['DateTime'], ascending=False)

            # upload the csv file to google sheets
            update_sheet("HOME", df_pivot.values.tolist(), df_pivot.columns.values.tolist())

            break
        except Exception as e:
            print(e)
            print("Error in updating cell")
            time.sleep(10)
            continue

def filter_csv_data(df, time_difference):
    # Convert the 'DATETIME' column to datetime format
    df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%d-%m-%Y %H:%M')

    # Sort the DataFrame by the 'DATETIME' column
    df = df.sort_values(by='DATETIME')

    new_df = pd.DataFrame(columns=df.columns)
    last_row = df.iloc[0]['DATETIME']
    # Add the first row to the new DataFrame
    new_df = pd.concat([new_df, df.iloc[[0]]])

    for index, row in df.iterrows():
        if (last_row + timedelta(minutes=time_difference)) == row['DATETIME']:
            # Add the current row to the new DataFrame
            new_df = pd.concat([new_df, pd.DataFrame(row).T])
            last_row = row['DATETIME']

    # Convert the 'VIEWS' column to numeric and remove the commas

    new_df['VIEWS'] = new_df['VIEWS'].str.replace(',', '')
    new_df['VIEWS'] = pd.to_numeric(new_df['VIEWS'])
    new_df['VIEWS_DIFFERENCE'] = new_df['VIEWS'].diff()

    # Fill the first row with 0
    new_df['VIEWS_DIFFERENCE'] = new_df['VIEWS_DIFFERENCE'].fillna(0)

    # Convert DATETIME column to string
    new_df['DATETIME'] = new_df['DATETIME'].astype(str)

    return new_df



def get_content_data(video_title, min_duration, total_or_difference):
    while True:
        try:
            sheet = client.open_by_url(sheet_url).worksheet("CONTENT")
            data = sheet.get_all_values()
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df.fillna('NA')
            df = df.drop_duplicates(subset=['DATE', 'TIME', 'VIDEO TITLE'], keep='first')
            # Combine 'Date' and 'Time' columns into a single 'DateTime' column
            df['DATETIME'] = df['DATE'] + ' ' + df['TIME']

            # remove DATE and TIME and VIDEO ID columns
            df = df.drop(['DATE', 'TIME', 'VIDEO ID'], axis=1)

            # DATETIME column to 0th index
            cols = df.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            df = df[cols]

            # index false
            df = df.reset_index(drop=True)

            # filter the data by video title
            df = df[df['VIDEO TITLE'] == video_title]

            df_x = filter_csv_data(df, min_duration)
            # index false
            df_x = df_x.reset_index(drop=True)
            print(total_or_difference)

            if total_or_difference == "total":
                # then remove the VIEWS_DIFFERENCE column
                df_x = df_x.drop(['VIEWS_DIFFERENCE'], axis=1)
                # upload the csv file to google sheets
                print(df_x.values.tolist())
                update_sheet("FILTERS", df_x.values.tolist(), df_x.columns.values.tolist())
            elif total_or_difference == "difference":
                # then remove the VIEWS column
                df_x = df_x.drop(['VIEWS'], axis=1)
                # upload the csv file to google sheets
                print(df_x.values.tolist())
                update_sheet("FILTERS", df_x.values.tolist(), df_x.columns.values.tolist())




            break
        except Exception as e:
            print(e)
            print("Error in updating cell filter")
            time.sleep(10)
            continue



def get_videos_list():
    while True:
        try:
            sheet = client.open_by_url(sheet_url).worksheet("CONTENT")
            data = sheet.get_all_values()
            videos_list = [video_title[3] for video_title in data[1:]]
            video_titles = list(set(videos_list))
            print(len(video_titles))
            return video_titles
        except Exception as e:
            print(e)
            print("Error in updating cell")
            time.sleep(10)
            continue


