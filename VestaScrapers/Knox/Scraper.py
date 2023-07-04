import csv
import os
import random
import shutil
import time
import urllib.request
from datetime import datetime

import pandas as pd
from tqdm import tqdm
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import boto3
from database_connection import *

# import selenium
sheet_url = 'https://docs.google.com/spreadsheets/d/1Lid5x1Qfk_ME5h-YHKE70nkJmlsbB2MbC_lHNlzZTu4/edit?usp=sharing'
S3_ID = 'AKIAVSENCD4FUIEDLBFN'
S3_SECRET_KEY = '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'
bucket_name = 'vestadesigns-scraper-files'
s3 = boto3.client('s3', aws_access_key_id=S3_ID, aws_secret_access_key=S3_SECRET_KEY)


########################################################################################################################
#      DO NOT CHANGE ANYTHING BELOW THIS LINE
########################################################################################################################


def make_dir(name: str):
    BASE_DIR = os.getcwd()
    path = os.path.join(BASE_DIR, "Knox", name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


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


def clear_download_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    for folder in os.listdir(folder_path):
        shutil.rmtree(os.path.join(folder_path, folder))


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


driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get(
    'https://www.knox.vic.gov.au/our-services/building-and-planning/planning-services-and-permits/planning-applications-available-public-view')

# Pre-work
while True:
    try:
        advertisement_url = driver.find_element(By.XPATH,
                                                "//a[text()='see planning applications that are currently being advertised']").get_attribute(
            "href")
        driver.get(advertisement_url)

        break
    except:
        time.sleep(0.1)

specific_clicker('//input[@aria-label="Advertised Planning Applications"]')
specific_clicker('//input[@value="Next"]')
date_year_ago = str(time.strftime("%d/%m/%Y", time.localtime(time.time() - 31536000)))
find_element_send_text("//*[text()='From Date']/../input", date_year_ago, True)
specific_clicker('//input[@value="Search"]')

# Main work

while True:
    applications_urls = driver.find_elements(By.XPATH, '//table[@id="gridResults"]//td/a')

    if len(applications_urls) > 0:
        applications_urls = [url.get_attribute("href") for url in applications_urls]
        break
    else:
        time.sleep(2)

for application_url in applications_urls:
    df = pd.read_csv('../ScraperLogs.csv')
    already_done = df[df['Scraper'] == 'Knox']['Tracking ID'].tolist()
    if application_url in already_done:
        continue
    driver.get(application_url)
    time.sleep(2)

    # Get application number

    try:
        applications_number = driver.find_element(By.XPATH,
                                                  "//*[text()='Application Number']/following-sibling::*").text
    except:
        applications_number = ""

    # Get application address
    try:
        applications_address = driver.find_element(By.XPATH, "//*[text()='Property Address']/../..//div").text
    except:
        applications_address = ""

    # Get application description
    try:
        applications_description = driver.find_element(By.XPATH, "//*[text()='Description']/following-sibling::*").text
    except:
        applications_description = ""

    # print([applications_number, applications_address, applications_description])

    # Get application PDF's
    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe"))

    # //td//a[@title]
    pdfs = driver.find_elements(By.XPATH, "//td//a[@title]")
    pdfs = [pdf.get_attribute("href") for pdf in pdfs]

    for download_url in pdfs:
        applications_number = applications_number.replace("/", "_")
        make_dir(applications_number)
        download_file_path = os.path.join("Knox", applications_number, download_url.split('=')[-1])
        download_file_path = os.getcwd() + "\\" + download_file_path + ".pdf"
        download_file(download_url, download_file_path)

        s3_path = f"Knox/{applications_number}/{download_url.split('=')[-1]}.pdf"
        s3.upload_file(download_file_path, bucket_name, s3_path)
        print(f"File uploaded to S3: {s3_path}")

        os.remove(download_file_path)
        cursor.execute("SELECT MAX(id) FROM ScrapersData")
        max_id = str(int(cursor.fetchall()[0][0]) + 1)

        record = (max_id, applications_number, applications_address, applications_description, "", "", "Knox", "", "", "", "")
        print(record)
        add_row_to_table("ScrapersData", record)

    with open('../ScraperLogs.csv', 'a', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        # Tracking ID,Scraper,Date,Time
        current_date = datetime.now().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        csv_writer.writerow([application_url, "Knox", current_date, current_time])

driver.quit()
clear_download_folder("Knox")
