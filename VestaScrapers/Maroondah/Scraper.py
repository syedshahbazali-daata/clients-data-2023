import csv
import os
import random
import time
import threading
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

import boto3
import urllib.request
from tqdm import tqdm
import pandas as pd
from database_connection import *

# import selenium
S3_ID = 'AKIAVSENCD4FUIEDLBFN'
S3_SECRET_KEY = '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'
bucket_name = 'vestadesigns-scraper-files'
s3 = boto3.client('s3', aws_access_key_id=S3_ID, aws_secret_access_key=S3_SECRET_KEY)


# s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-2'})

########################################################################################################################
#      DO NOT CHANGE ANYTHING BELOW THIS LINE
########################################################################################################################



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


def make_dir(name: str):
    BASE_DIR = os.getcwd()
    path = os.path.join(BASE_DIR, 'Maroondah', name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_file_data(file):
    with open(file) as f:
        data = f.read().strip()
        my_file_data = data.split('\n')
    return my_file_data


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


driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get(
    'https://www.maroondah.vic.gov.au/Development/Planning/Planning-step-by-step/Advertised-planning-applications')
specific_clicker('//main/div//p/a')

# Scraped Applications urls
page_number = 1
all_applications_urls = []
while True:
    driver.get(
        f'https://eservices.maroondah.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquirySummaryView.aspx?PageNumber={page_number}')
    time.sleep(3)
    applications_links = driver.find_elements(By.XPATH, '//table[@class="ContentPanel"]//div/a')
    if len(applications_links) < 3:
        break

    applications_links = [all_applications_urls.append(i.get_attribute("href")) for i in applications_links]
    page_number += 1

# Go to each Scrape Link
import re

for single_application_link in all_applications_urls:
    df = pd.read_csv('../ScraperLogs.csv')
    already_done = df[df['Scraper'] == 'Maroondah']['Tracking ID'].tolist()
    if single_application_link in already_done:
        continue
    driver.get(single_application_link)
    page_source = str(driver.page_source).lower()
    try:
        application_no = re.findall(r'application number.*?AlternateContentText.*?>([^<]+)'.lower(), page_source)[0]
        application_no = application_no.strip().replace("/", "_")
    except:
        application_no = None

    try:
        application_location = re.findall(r'Application Location.*?AlternateContentText.*?>([^<]+)'.lower(),
                                          page_source)[0]
    except:
        application_location = None

    try:
        application_description = re.findall(r'Application Description.*?AlternateContentText.*?>([^<]+)'.lower(),
                                             page_source)[0]
    except:
        application_description = None
        continue

    try:
        make_dir(application_no)
    except:
        continue
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe'))
    pdf_links = [i.get_attribute('href') for i in driver.find_elements(By.XPATH, '//td/a')]
    for pdf_index, pdf_link in enumerate(pdf_links):
        download_file_path = os.path.join("Maroondah", application_no,
                                          f"{application_no}_{pdf_index + 1}.pdf")
        download_file_path = os.getcwd() + "\\" + download_file_path
        download_file(pdf_link, download_file_path)

        s3_path = f"Maroondah/{application_no}/{application_no}_{pdf_index + 1}.pdf"
        s3.upload_file(download_file_path, bucket_name, s3_path)
        print(f"File uploaded to S3: {s3_path}")
        os.remove(download_file_path)


    driver.switch_to.default_content()

    cursor.execute("SELECT MAX(id) FROM ScrapersData")
    max_id = str(int(cursor.fetchall()[0][0]) + 1)

    print([application_no, application_location, application_description])
    record = (max_id, application_no, application_location, application_description, "", "", "Maroondah", "", "", "","")
    add_row_to_table("ScrapersData", record)
    print(f"Added to database: {application_no}")

    with open('../ScraperLogs.csv', 'a', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        # Tracking ID,Scraper,Date,Time
        current_date = datetime.now().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        csv_writer.writerow([single_application_link, "Maroondah", current_date, current_time])

driver.quit()
delete_folders("Maroondah")