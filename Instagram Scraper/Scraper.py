import os
import time, csv
from datetime import datetime

import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

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



def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass

def scroll_down(no_of_scrolls):
    for i in range(no_of_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()
hashtags = get_file_data('query.txt')
for hashtag in hashtags:
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    driver.get(url)

    time.sleep(5)
    scroll_down(5)
    post_links = driver.find_elements(By.XPATH, '//main/article//a')
    post_links = ["https://www.instagram.com/"+str(x.get_attribute('href')) for x in post_links]
    # save to csv
    with open('links.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for link in post_links:
            writer.writerow([link])

driver.quit()


