import csv
import os
import random
import shutil
import time
import threading
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
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


def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)

        print(f"The folder {folder_path} and its contents have been deleted.")
    except:
        print(f"The folder {folder_path} does not exist.")


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
    while True:
        try:
            element = driver.find_element(By.XPATH, ele)
            webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

            break
        except Exception as e:
            pass
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
    path_to = os.path.join(BASE_DIR, "Monash", folder_to)
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

def clear_download_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    for folder in os.listdir(folder_path):
        shutil.rmtree(os.path.join(folder_path, folder))


def keep_checking_for_files():
    while True:
        list_of_files_type = check_types_of_files('downloads')
        if 'crdownload' not in list_of_files_type:
            return True
        time.sleep(3)
        print(list_of_files_type)


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

    driver.get('https://www.monash.vic.gov.au/Planning-Development/Proposed-Developments/View-Planning-Applications')
    specific_clicker("//*[text()='currently advertised for public comment']")
    while True:
        try:
            driver.switch_to.window(driver.window_handles[1])
            break
        except:
            time.sleep(1)

    time.sleep(5)
    table_elements = driver.find_elements(By.XPATH, '//table[@id="gridResults"]//td[1]/a')
    print(len(table_elements))
    links = [str(x.get_attribute('href')) for x in table_elements]
    articles_text = [str(x.text) for x in table_elements]
    articles_text = [x.replace('/', '_') for x in articles_text]

    primary_addresses = driver.find_elements(By.XPATH, '//table[@id="gridResults"]//td[2]')
    primary_addresses_text = [str(x.text) for x in primary_addresses]

    descriptions = driver.find_elements(By.XPATH, '//table[@id="gridResults"]//td[4]')
    descriptions_text = [str(x.text) for x in descriptions]

    for index, single_link in enumerate(links):
        df = pd.read_csv('../ScraperLogs.csv')
        already_done = df[df['Scraper'] == 'Monash']['Tracking ID'].tolist()
        if articles_text[index] in already_done:
            continue

        driver.get(single_link)
        while True:
            try:
                documents_link = str(
                    driver.find_element(By.XPATH, "//*[text()='View planning application documents']").get_attribute(
                        'href'))
                break
            except:
                time.sleep(1)

        driver.get(documents_link)
        time.sleep(3)
        while True:
            try:

                files_links = driver.find_elements(By.XPATH, '//table[@id="articleList"]//td[1]/a')
                # if len(files_links) == 0:
                #     continue
                files_links = [str(x.get_attribute('href')) for x in files_links]
                print(files_links)
                for file_link in files_links:
                    old_no_files = get_number_of_files('downloads')
                    driver.get(file_link)
                    print(file_link)
                    while True:
                        new_no_files = get_number_of_files('downloads')
                        if new_no_files > old_no_files:
                            break
                        else:
                            time.sleep(1)

                break
            except:
                time.sleep(1)

        keep_checking_for_files()
        time.sleep(3)
        file_name_from_text = articles_text[index].replace('/', '_')

        make_dir("Monash")
        make_dir("Monash/" + file_name_from_text)
        time.sleep(2)
        move_all_files_from_folder_to_folder('downloads', file_name_from_text)

        s3_upload_folder = f"Monash/{file_name_from_text}"
        for file in os.listdir(s3_upload_folder):
            if '.PDF' in file.upper():
                upload_file_bucket = bucket_name
                upload_file_key = f"Monash/{file_name_from_text}/" + file
                upload_file_path = os.path.join('Monash', file_name_from_text, file)
                s3.upload_file(upload_file_path, upload_file_bucket, upload_file_key)
                print(f'Uploaded {file} to S3')

        cursor.execute("SELECT MAX(id) FROM ScrapersData")
        max_id = str(int(cursor.fetchall()[0][0]) + 1)
        record = (max_id, articles_text[index], primary_addresses_text[index], descriptions_text[index], "", "",
                  "Monash", "", "", "", "")

        add_row_to_table("ScrapersData", record)
        print(f"Added to database: {articles_text[index]}")

        with open('../ScraperLogs.csv', 'a', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            # Tracking ID,Scraper,Date,Time
            current_date = datetime.now().strftime("%d-%m-%Y")
            current_time = datetime.now().strftime("%H:%M:%S")
            csv_writer.writerow([articles_text[index], "Monash", current_date, current_time])
    driver.quit()


clear_download_folder("downloads")
clear_download_folder("Monash")
