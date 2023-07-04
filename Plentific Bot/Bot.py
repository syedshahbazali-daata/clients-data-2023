import os
import time, csv
from datetime import datetime

import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc #
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


def click_check_box():
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            specific_clicker('//div[@data-props-divider="full-width"]//input[@type="checkbox"]')
            check_box = driver.find_elements(By.XPATH, "//*[name()='svg' and @data-testid='CheckBoxIcon']")
            if len(check_box) > 0:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            print(e)
            pass


def clean_duplicates(file_x):
    data = get_file_data(file_x)
    data = list(set(data))
    with open('Already done.txt', 'w', encoding='utf-8') as file_n:
        file_n.write("")
    for single_x in data:
        with open('Already done.txt', 'a', encoding='utf-8') as file_n:
            file_n.write(single_x + '\n')


close_chrome()
options = uc.ChromeOptions()
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
# path for mac
# path = "/Users/jean-pierrecolombo/Library/Application Support/Google/Chrome"
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Default')
driver = uc.Chrome(options=options)
driver.maximize_window()
# PLENTIFIC BOT:
driver.get('https://app.plentific.com/')
input("Press Enter to continue: ")

specific_clicker("//a/*[text()='Leads']/..")
time.sleep(3)

all_links = driver.find_elements(By.XPATH, '//div[@class="InfiniteScrolling"]//a')
for single_link in all_links:
    single_link_x = single_link.get_attribute("href")
    with open('Already done.txt', 'a', encoding='utf-8') as file:
        file.write(single_link_x + '\n')

while True:
    specific_clicker("//a/*[text()='Leads']/..")
    while True:
        try:
            driver.find_element(By.XPATH, '(//div[@class="InfiniteScrolling"]//a)[1]').get_attribute('href')

            break
        except:
            time.sleep(2)
            specific_clicker("//a/*[text()='Leads']/..")
            time.sleep(2)
    already_done = get_file_data('Already done.txt')
    links = driver.find_elements(By.XPATH, '(//div[@class="InfiniteScrolling"]//a)[1]')
    for single_new_x in links:
        single_new_link = single_new_x.get_attribute("href")
        if single_new_link not in already_done:
            print(single_new_link)
            print("New Job Found")

            driver.get(single_new_link)
            while True:
                try:
                    driver.find_element(By.XPATH, "//dt[text()='Price']")
                    break
                except:
                    print("Loading Job")
                    time.sleep(1)
                    pass

            try:
                driver.find_element(By.XPATH, "//*[text()='Free']")
                print("Free Job")
            except:
                print("Paid Job so skipped")
                with open('Already done.txt', 'a', encoding='utf-8') as file:
                    file.write(single_new_link + '\n')
                continue

            try:
                driver.find_element(By.XPATH, "//*[text()='Emergency']")
                print("Emergency Job")
                with open('Already done.txt', 'a', encoding='utf-8') as file:
                    file.write(single_new_link + '\n')
                continue
            except:
                pass

            try:
                driver.find_element(By.XPATH, "//*[text()='Sorry, this lead is no longer available to claim']")
                print("Sorry, this lead is no longer available to claim")
                with open('Already done.txt', 'a', encoding='utf-8') as file:
                    file.write(single_new_link + '\n')
                continue
            except:
                pass
            try:
                driver.find_element(By.XPATH, "//*[text()='End of tenancy repairs / maintenance']")
                print("End of tenancy repairs / maintenance")
                with open('Already done.txt', 'a', encoding='utf-8') as file:
                    file.write(single_new_link + '\n')
                continue
            except:
                pass

            click_check_box()
            specific_clicker("//button[text()='Get this lead']")
            with open('Already done.txt', 'a', encoding='utf-8') as file:
                file.write(single_new_link + '\n')