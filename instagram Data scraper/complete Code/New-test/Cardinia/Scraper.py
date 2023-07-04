import csv
import os
import random
import shutil
import time
import urllib.request
from datetime import datetime

from tqdm import tqdm
import requests
from xextract import String
from bs4 import BeautifulSoup
import pandas as pd
from database_connection import *
import boto3

# import selenium
S3_ID = 'AKIAVSENCD4FUIEDLBFN'
S3_SECRET_KEY = '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'
bucket_name = 'vestadesigns-scraper-files'
s3 = boto3.client('s3', aws_access_key_id=S3_ID, aws_secret_access_key=S3_SECRET_KEY)


########################################################################################################################
#      DO NOT CHANGE ANYTHING BELOW THIS LINE
########################################################################################################################

def make_dir(name: str):
    BASE_DIR = os.getcwd()
    path = os.path.join(BASE_DIR, "Cardinia", name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def clear_download_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    for folder in os.listdir(folder_path):
        shutil.rmtree(os.path.join(folder_path, folder))


def download_file(url, save_path):
    with urllib.request.urlopen(url) as url_handle:
        with open(save_path, 'wb') as file_handle:
            total_size = int(url_handle.info().get('Content-Length', 0))
            block_size = 1024  # 1 Kibibyte
            t = tqdm(total=total_size, unit='B', unit_scale=True, desc=save_path.split('/')[-1])
            while True:
                buffer = url_handle.read(block_size)
                if not buffer:
                    break
                file_handle.write(buffer)
                t.update(len(buffer))
    t.close()
    if total_size != 0 and t.n != total_size:
        print("Error during download!")
    else:
        print(f'File downloaded to {save_path}')


def get_file_data(file):
    with open(file) as f:
        data = f.read().strip()
        my_file_data = data.split('\n')
    return my_file_data


def delete_folders(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isdir(file_path):
                # if the current file is a folder, delete it and its contents
                os.rmdir(file_path)
                print("Deleted folder: " + file_path)
        except Exception as e:
            print(f'Error: {e}')


res = requests.get("https://www.cardinia.vic.gov.au/advertisedplanningapplications")
soup = str(BeautifulSoup(res.text, 'html.parser'))

# Table
table_rows = String(xpath='//tbody//tr').parse_html(soup)

data_list = []

for index in range(len(table_rows)):
    xpath = f"(//tbody//tr)[{index}]/td"
    try:
        application_number = String(xpath=f"({xpath})[1]/a").parse_html(soup)[0]
        application_number = application_number.replace('/', '_')
    except:
        application_number = ""

    try:
        application_url = String(xpath=f"({xpath})[1]/a", attr='href').parse_html(soup)[0]
    except:
        application_url = ""

    try:
        application_description = String(xpath=f"({xpath})[2]").parse_html(soup)[0]
    except:
        application_description = ""
    try:
        application_address = String(xpath=f"({xpath})[3]").parse_html(soup)[0]
    except:
        application_address = ""

    data_list.append([application_number, application_url, application_description, application_address])

for data_row in data_list:
    df = pd.read_csv('../ScraperLogs.csv')
    already_done = df[df['Scraper'] == 'Cardinia']['Tracking ID'].tolist()
    page_url = data_row[1]
    if page_url in already_done:
        continue
    if data_row[1] == "":
        continue

    requests.get(page_url)
    res = requests.get(page_url)
    soup = str(BeautifulSoup(res.text, 'html.parser'))

    # PDF LINKs
    pdf_links = String(xpath='//ul[@class="download__meta-list"]//a', attr='href').parse_html(soup)

    for pdf_index, pdf_link in enumerate(pdf_links):
        print(pdf_link)
        download_file_path = os.getcwd() + f"/Cardinia/{data_row[0]}_{pdf_index + 1}.pdf"
        download_file(pdf_link, download_file_path)
        s3_path = f"Cardinia/{data_row[0]}/{data_row[0]}_{pdf_index + 1}.pdf"
        s3.upload_file(download_file_path, bucket_name, s3_path)
        print(f"File uploaded to S3: {s3_path}")

        os.remove(download_file_path)

    cursor.execute("SELECT MAX(id) FROM ScrapersData")
    max_id = str(int(cursor.fetchall()[0][0]) + 1)
    record = (max_id, data_row[0], data_row[3], data_row[2], "", "", "Cardinia", "", "", "", "")

    # Upload to S3

    add_row_to_table("ScrapersData", record)
    print(f"Added to database: {data_row[0]}")

    with open('../ScraperLogs.csv', 'a', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        # Tracking ID,Scraper,Date,Time
        current_date = datetime.now().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        csv_writer.writerow([data_row[1], "Cardinia", current_date, current_time])

clear_download_folder("Cardinia")