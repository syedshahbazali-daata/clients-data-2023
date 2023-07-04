import csv
import os
import shutil
from datetime import datetime
import unicodedata
import requests
import urllib.request
from tqdm import tqdm
from xextract import String
import boto3
import pandas as pd
from database_connection import *

S3_ID = 'AKIAVSENCD4FUIEDLBFN'
S3_SECRET_KEY = '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'
bucket_name = 'vestadesigns-scraper-files'
s3 = boto3.client('s3', aws_access_key_id=S3_ID, aws_secret_access_key=S3_SECRET_KEY)


########################################################################################################################
#      DO NOT CHANGE ANYTHING BELOW THIS LINE
########################################################################################################################


def make_dir(name: str):
    BASE_DIR = os.getcwd()
    path = os.path.join(BASE_DIR, "Hume", name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def move_all_files_from_folder_to_folder(folder_from: str, folder_to: str):
    BASE_DIR = os.getcwd()
    path_from = os.path.join(BASE_DIR, folder_from)
    path_to = os.path.join(BASE_DIR, "Monash", folder_to)
    files = os.listdir(path_from)
    for file in files:
        os.rename(os.path.join(path_from, file), os.path.join(path_to, file))
    return len(files)


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


res = requests.get('https://www.hume.vic.gov.au/Building-and-Planning/Statutory-Planning/Applications-at-Advertising')
page_source = str(res.text)

# Application Numbers
application_numbers = String(xpath='//article//p[1]').parse_html(page_source)

# Application Links
application_links = String(xpath='//article//a', attr='href').parse_html(page_source)

# Application Addresses
application_addresses = String(xpath='//article//p[@class="list-item-address"]').parse_html(page_source)

# Application Descriptions
application_descriptions = String(xpath='//article/a/p[4]').parse_html(page_source)

for index, single_link in enumerate(application_links):
    open_main_link = requests.get(single_link)
    main_page_source = str(open_main_link.text)
    # PDF Links
    pdf_links = String(xpath='//ul[@class="related-information-list"]/li/a', attr='href').parse_html(main_page_source)
    pdf_links = [f"https://www.hume.vic.gov.au{pdf_link}" for pdf_link in pdf_links]

    # Update Line
    try:
        application_address = str(String(xpath="//p/a[text()='View Map']/..").parse_html(main_page_source)[0]).strip()
    except:
        application_address = ""

    if application_address == "":
        try:
            application_address = str(
                String(xpath="//h1").parse_html(main_page_source)[0]).strip()
            try:
                application_address = application_address.split(" - ")[1]
            except:
                pass
        except:
            application_address = ""

    try:
        application_description = str(
            String(xpath="//*[text()='Proposal']//following-sibling::*").parse_html(main_page_source)[0]).strip()

    except:
        application_description = ""

    # normalise address
    application_address = unicodedata.normalize("NFKD", application_address).encode("ascii", "ignore").decode("utf-8")

    # Download PDFs
    df = pd.read_csv('../ScraperLogs.csv')
    already_done = df[df['Scraper'] == 'Hume']['Tracking ID'].tolist()
    if application_numbers[index] in already_done:
        continue
    for pdf_index, pdf_link in enumerate(pdf_links):

        # if Scraper=='Hume'

        make_dir(application_numbers[index])
        download_file_path = os.path.join("Hume", application_numbers[index],
                                          f"{application_numbers[index]}_{pdf_index}.pdf")
        download_file_path = os.getcwd() + "\\" + download_file_path
        print(download_file_path)

        download_file(pdf_link, download_file_path)
        s3_path = f"Hume/{application_numbers[index]}/{application_numbers[index]}_{pdf_index}.pdf"
        s3.upload_file(download_file_path, bucket_name, s3_path)
        print(f"File uploaded to S3: {s3_path}")

        # get parent folder name
        os.remove(download_file_path)

        with open('../ScraperLogs.csv', 'a', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            # Tracking ID,Scraper,Date,Time
            current_date = datetime.now().strftime("%d-%m-%Y")
            current_time = datetime.now().strftime("%H:%M:%S")
            csv_writer.writerow([application_numbers[index], "Hume", current_date, current_time])

    # Add to Database
    try:
        cursor.execute("SELECT MAX(id) FROM ScrapersData")
        max_id = str(int(cursor.fetchall()[0][0]) + 1)

        record = (
        max_id, application_numbers[index], application_address, application_description, "", "", "Hume", "", "", "",
        "")
        add_row_to_table("ScrapersData", record)
        print(f"Added to database: {application_numbers[index]}")


    except:
        pass

# Delete all Folders and its contents from Hume Folder
clear_download_folder("Hume")
