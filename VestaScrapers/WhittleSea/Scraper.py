import csv
import os
import random
import time
import threading
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from database_connection import *
import boto3

# import selenium


S3_ID = 'AKIAVSENCD4FUIEDLBFN'
S3_SECRET_KEY = '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'
bucket_name = 'vestadesigns-scraper-files'
s3 = boto3.client('s3', aws_access_key_id=S3_ID, aws_secret_access_key=S3_SECRET_KEY)

# s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-2'})

########################################################################################################################
#      DO NOT CHANGE ANYTHING BELOW THIS LINE
########################################################################################################################

def find_element_send_text(ele, text, clear):
    while True:
        try:
            input_field = driver.find_element(By.XPATH, ele)
            if clear:
                input_field.clear()
                time.sleep(1)
            input_field.send_keys(text)

            break
        except:
            time.sleep(0.1)


def specific_clicker(ele):
    for i in range(10):
        try:
            element = driver.find_element(By.XPATH, ele)
            webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

            break
        except Exception as e:
            time.sleep(0.5)
            # print(e)


def specific_clicker_pass(ele):
    try:
        element = driver.find_element(By.XPATH, ele)
        webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

    except Exception as e:
        pass


def get_text(ele):
    while True:
        try:
            element = driver.find_elements(By.XPATH, ele)
            texts = [str(x.text) for x in element]
            return texts
        except Exception as e:
            pass
            # print(e)


def get_text_fine(ele):
    try:
        element = driver.find_element(By.XPATH, ele)
        texts = str(element.text)
    except:

        texts = ''
    return texts



def get_number_of_files(file: str):
    BASE_DIR = os.getcwd()
    path = os.path.join(BASE_DIR, file)
    files = os.listdir(path)

    return len(files)


def make_dir(name: str):
    BASE_DIR = os.getcwd()
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def move_all_files_from_folder_to_folder(folder_from: str, folder_to: str):
    BASE_DIR = os.getcwd()
    path_from = os.path.join(BASE_DIR, folder_from)
    path_to = os.path.join(BASE_DIR, "whittlesea", folder_to)
    files = os.listdir(path_from)
    for file in files:
        os.rename(os.path.join(path_from, file), os.path.join(path_to, file))
    return len(files)


def get_file_data(file):
    with open(file) as f:
        data = f.read().strip()
        my_file_data = data.split('\n')
    return my_file_data


def check_types_of_files(folder: str):
    BASE_DIR = os.getcwd()
    path = os.path.join(BASE_DIR, folder)
    files = os.listdir(path)
    types = []
    for file in files:
        types.append(file.split('.')[-1])

    return types


def keep_checking_for_files():
    while True:
        list_of_files_type = check_types_of_files('downloads')
        if 'crdownload' not in list_of_files_type:
            return True
        time.sleep(3)
        print(list_of_files_type)


import shutil

def clear_download_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    for folder in os.listdir(folder_path):
        shutil.rmtree(os.path.join(folder_path, folder))

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)

        print(f"The folder {folder_path} and its contents have been deleted.")
    except:
        print(f"The folder {folder_path} does not exist.")


from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    # Create Chrome options object
    options = Options()

    # Read list of proxies from Proxies.txt file
    # proxies_list = get_file_data('Proxies.txt')
    # # Choose a random proxy from the list
    # my_proxy = random.choice(proxies_list)
    # Create a Chrome extension for proxy authentication using the chosen proxy
    # proxy = get_proxy_auth_extension(my_proxy)
    # Add the extension to the Chrome options
    # options.add_argument(f'--load-extension={proxy}')
    # Create a new Chrome driver with the options
    options.add_experimental_option("prefs", {
        "download.default_directory": fr"{os.getcwd()}\downloads",
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "download.directory_upgrade": True
    })

    driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
    driver.maximize_window()
    import json

    with open('data.json') as f:
        data = json.load(f)

    list_of_ids = []
    result = data['actions'][1]['returnValue']['returnValue']
    for index, single in enumerate(result):
        name = single.get('Name', '')
        address = single.get('Property_Address__c', '')
        description = single.get('Description_of_the_Development__c', '')
        url = 'https://online.whittlesea.vic.gov.au/s/applicationpageforpr?recordId=' + single['Id']
        list_of_ids.append([name, address, description, url])

    # for index, record in enumerate(list_of_ids[117:]):
    for index, record in enumerate(list_of_ids[698:]):
        url = record[3]
        try:
            print(url)
            driver.get(url)
        except:
            continue

        df = pd.read_csv('../ScraperLogs.csv')
        already_done = df[df['Scraper'] == 'Whittlesea']['Tracking ID'].tolist()

        if url in already_done:
            continue

        with open('../ScraperLogs.csv', 'a', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            # Tracking ID,Scraper,Date,Time
            current_date = datetime.now().strftime("%d-%m-%Y")
            current_time = datetime.now().strftime("%H:%M:%S")
            csv_writer.writerow([url, "Whittlesea", current_date, current_time])
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, "//*[text()='There are no supporting documents to show.']")
            print('No documents')


        except:
            PDF_links = driver.find_elements(By.XPATH, '//button[@title="Click to view document"]')
            for pdf_index, element in enumerate(PDF_links):
                old_no_files = get_number_of_files('downloads')
                specific_clicker(f'(//button[@title="Click to view document"])[{pdf_index + 1}]')
                time.sleep(2)
                for i in range(10):
                    new_no_files = get_number_of_files('downloads')
                    if new_no_files > old_no_files:
                        break
                    else:
                        time.sleep(1)

                time.sleep(2)

            keep_checking_for_files()
            time.sleep(3)
            file_name_from_text = record[0].replace('-', '_')
            make_dir("whittlesea")
            make_dir("whittlesea/" + file_name_from_text)
            time.sleep(2)
            move_all_files_from_folder_to_folder('downloads', file_name_from_text)

            s3_upload_folder = f"whittlesea/{file_name_from_text}"
            print(os.listdir(s3_upload_folder))

            print("Uploading to S3")
            for file in os.listdir(s3_upload_folder):
                if '.PDF' in file.upper():
                    print("1")
                    upload_file_bucket = bucket_name
                    upload_file_key = f"whittlesea/{file_name_from_text}/" + file
                    upload_file_path = os.path.join('whittlesea', file_name_from_text, file)
                    print("2")
                    s3.upload_file(upload_file_path, upload_file_bucket, upload_file_key)
                    print("3")
                    print(f'Uploaded {file} to S3')

            print("Done uploading to S3")
            cursor.execute("SELECT MAX(id) FROM ScrapersData")
            max_id = str(int(cursor.fetchall()[0][0]) + 1)

            record = (max_id, record[0], record[1], record[2], "", "", "whittlesea",  "", "", "", "")
            delete_folder('whittlesea')
            add_row_to_table("ScrapersData", record)
            print("Done adding to database")




    driver.quit()


