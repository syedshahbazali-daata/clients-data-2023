import os
import time, csv
from datetime import datetime

import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


########################################################################################################################
# Functions

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
            print(e)
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


def get_day(require_days: list) -> (int, str):
    # current date
    from datetime import datetime
    from datetime import timedelta
    now = datetime.now()
    current_date = now.strftime("%m/%d/%Y")
    # current day: Friday
    current_day = str(now.strftime("%A")).lower()
    if current_day not in require_days:
        return None

    # add 7 days
    seven_days = now + timedelta(days=7)
    seven_days = int(str(seven_days.strftime("%d")))
    return seven_days


def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()
url = f"https://compra.cinepolis.com/?cinemaVistaId=187&showtimeVistaId=10989"
driver.get(url)
input("add: ")

