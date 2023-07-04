import csv
import os
import random
import shutil
import re
import time
import urllib.request
from datetime import datetime

from tqdm import tqdm
import requests
from xextract import String
from bs4 import BeautifulSoup
import pandas as pd
from database_connection import *

import threading
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    path = os.path.join(BASE_DIR, "Dandenong", name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def clear_download_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    for folder in os.listdir(folder_path):
        shutil.rmtree(os.path.join(folder_path, folder))


def pdf_links_scraper(application_number):
    application_number_reformat = application_number.replace("_", "/")
    url = "https://planningdocuments.cgd.vic.gov.au/functions.php"

    querystring = {"plnNum": f"{application_number_reformat}"}

    response = requests.request("GET", url, params=querystring)

    soup = str(response.text)
    pdf_links = eval(re.findall(r'(\[.*?])', soup)[0])
    pdf_links = ["https://planningdocuments.cgd.vic.gov.au/functions.php?plnNumDown=" + i['openVersion'] for i
                 in pdf_links]
    

    return pdf_links


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


def scrape_page(app_id):
    url = "https://mygreaterdandenong.com/eProperty/P1/eTrack/eTrackApplicationDetails.aspx"

    querystring = {"r": "P1.WEBGUEST", "f": "$P1.ETR.APPDET.VIW", "ApplicationId": app_id}

    payload = ""
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-GB,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "ASP.NET_SessionId=qybucun4zai0yg45jojd1gy4",
        "Referer": "https://mygreaterdandenong.com/eProperty/P1/eTrack/eTrackApplicationSearchResults.aspx?r=P1.WEBGUEST&f=%24P1.ETR.RESULTS.VIW",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",

        "sec-ch-ua-mobile": "?0",

    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    soup = str(BeautifulSoup(response.text, 'html.parser'))
    # print(soup)
    # quit()

    try:
        application_number = String(xpath="//td[text()='Application ID No.']/../td[2]").parse_html(soup)[0]
        application_number = application_number.replace("/", "_")
    except:
        application_number = ""

    try:
        application_address = String(xpath="//noscript//input", attr="value").parse_html(soup)[1]
        print("x")
    except:
        application_address = ""

    try:
        application_description = String(xpath="//td[text()='Proposal Description']/../td[2]").parse_html(soup)[0]
    except:
        application_description = ""

    try:

        pdf_links = pdf_links_scraper(application_number)
        for pdf_index, pdf_link in enumerate(pdf_links):
            print(pdf_link)
            download_file_path = os.getcwd() + f"/Dandenong/{application_number}_{pdf_index + 1}.pdf"
            download_file(pdf_link, download_file_path)
            s3_path = f"Dandenong/{application_number}/{application_number}_{pdf_index + 1}.pdf"
            s3.upload_file(download_file_path, bucket_name, s3_path)
            print(f"File uploaded to S3: {s3_path}")

            os.remove(download_file_path)
        

    except:
        pass

    cursor.execute("SELECT MAX(id) FROM ScrapersData")
    max_id = str(int(cursor.fetchall()[0][0]) + 1)

    record = (
        max_id, application_number, application_address, application_description, "", "", "Dandenong", "", "", "", "")
    add_row_to_table("ScrapersData", record)
    print(f"Added to database: {application_number}")

    with open('../ScraperLogs.csv', 'a', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        # Tracking ID,Scraper,Date,Time
        current_date = datetime.now().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        csv_writer.writerow([app_id, "Dandenong", current_date, current_time])

    return record


driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get(
    'https://mygreaterdandenong.com/eProperty/P1/eTrack/eTrackApplicationSearchResults.aspx?r=P1.WEBGUEST&f=%24P1.ETR.RESULTS.VIW')

# Pre-work
specific_clicker("//a[text()='Advertised Applications']")
specific_clicker('//a[@id="cgdAgreeTerms"]')

# Main work

applications_ids = []

while True:
    applications_names = driver.find_elements(By.XPATH, "//table//tr[@class='normalRow' or @class='alternateRow']/td/a")
    print(applications_names)

    if len(applications_names) > 0:
        applications_names = [i.text for i in applications_names]
        applications_ids.extend(applications_names)

        try:
            driver.find_element(By.XPATH, "//*[text()='...']")
            driver.find_element(By.XPATH, '//*[@class="pagerRow"]//span/..//following-sibling::*')
            specific_clicker('//*[@class="pagerRow"]//span/..//following-sibling::*')
            time.sleep(2)
        except:
            break

        print(f"Found {len(applications_names)} applications")

    else:
        time.sleep(2)

for application_id in applications_names:
    df = pd.read_csv('../ScraperLogs.csv')
    already_done = df[df['Scraper'] == 'Dandenong']['Tracking ID'].tolist()
    if application_id in already_done:
        continue
    result = scrape_page(application_id)

clear_download_folder("Dandenong")
