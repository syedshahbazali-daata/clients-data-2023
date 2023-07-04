import os
import time, csv
from datetime import datetime

import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


no_of_pages = 3
########################################################################################################################
# Functions

def get_text_pass(xpath):
    try:
        text = driver.find_element(By.XPATH, xpath).text
        return text
    except:
        return ""

def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')
    return data


def find_element_send_text(ele, text, clear=True):
    while True:
        try:
            input_field = driver.find_element(By.XPATH, ele)
            if clear:
                input_field.clear()
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
            # print(e)
            pass


def specific_clicker2(ele):
    try:
        element = driver.find_element(By.XPATH, ele)
        webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

    except Exception as e:
        # print(e)
        pass


def get_text(ele):
    while True:
        try:
            element = driver.find_elements(By.XPATH, ele)
            texts = [str(x.text) for x in element]
            return texts
        except Exception as e:
            # print(e)
            pass


def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass


def insert_record(record_x:tuple):
    sql = "INSERT INTO listings (url, title, price, description, features, address, images) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, record_x)
    connection.commit()
    print(cursor.rowcount, "record inserted.")


import mysql.connector

connection = mysql.connector.connect(
    user='baldo',
    password='AVNS_31sHK4CCPIr6p4Ifgzd',
    host='db-mysql-nyc1-47136-do-user-12226124-0.b.db.ondigitalocean.com',
    port=25060,
    database='Baldo',

)

cursor = connection.cursor()

close_chrome()
# Database is Connected Successfully
print("Database is connected successfully")

options = uc.ChromeOptions()
# path = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"
# using os
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Profile 1')
driver = uc.Chrome(options=options)

driver.maximize_window()
driver.get("https://www.easybroker.com/agent/mls_properties?country=mx&reset_page=true")

input("Please apply Filters and Press enter: ")

list_of_urls = []
while True:
    try:
        current_page = driver.find_element(By.XPATH, '//span[@class="pagination-button page current"]')
        current_page = int(current_page.text)
        print(current_page)
    except:
        continue

    if current_page > no_of_pages:
        break


    # //h6/a

    property_urls = driver.find_elements(By.XPATH, '//h6/a')
    property_urls = [x.get_attribute('href') for x in property_urls]
    already_scraped = get_file_data('Already_scraper.txt')

    with open("Already_scraper.txt", 'a', encoding='utf-8') as file:
        for url in property_urls:
            if url not in already_scraped:
                file.write(url + '\n')
                list_of_urls.append(url)
    specific_clicker('//*[@class="next page pagination-button "]')
    time.sleep(5)


for url in list_of_urls:
    driver.get(url)
    time.sleep(3)
    images = driver.find_elements(By.XPATH, '//div[@class="gallery"]//img')
    images = [x.get_attribute('src') for x in images]
    images = ", ".join(images)

    title = get_text_pass('//section/div[@class="property-title"]')
    price = get_text_pass('//div[@class="price"]/*[@class="digits"]')
    description = get_text_pass('//p[@class="text-description"]')

    features = driver.find_elements(By.XPATH, '//div[@class="listing__features"]/div')
    features = [str(x.text).lower() for x in features]
    features = ", ".join(features)

    # scroll bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    try:
        # switch to iframe
        driver.switch_to.frame(driver.find_element(By.XPATH, '//div[@id="map_container"]/iframe'))

    except:
        pass

    address = get_text_pass('//div[@class="address"]')
    driver.switch_to.default_content()

    record = (title, price, description, features, address, url, images)
    print(record)
    try:
        insert_record(record)
    except:
        pass



driver.quit()













