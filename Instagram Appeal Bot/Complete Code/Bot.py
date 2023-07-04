import os
import time, csv
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc  # pip install undetected-chromedriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from faker import Faker  # pip install Faker
import random
from textwrap import dedent
import os

########################################################################################################################
# Functions
import os

BASE_DIR = os.path.dirname(os.path.abspath("__file__"))


def get_proxy_extension(proxy):
    if proxy.strip() == '':
        return None
    PROXY_HOST, PROXY_PORT = proxy.split(':')

    manifest_json = """
                    {
                        "version": "1.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                    """

    background_js = """
                    var config = {
                            mode: "fixed_servers",
                            rules: {
                            singleProxy: {
                                scheme: "http",
                                host: "%s",
                                port: parseInt(%s)
                            },
                            bypassList: ["localhost"]
                            }
                        };

                    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
                    """

    fn = os.path.join(BASE_DIR, 'proxy_ext')
    if not os.path.exists(fn):
        os.mkdir(fn)

    m_path = os.path.join(fn, "manifest.json")
    b_path = os.path.join(fn, "background.js")

    with open(m_path, 'w') as f:
        f.write(manifest_json)
    with open(b_path, 'w') as f:
        f.write(background_js % (PROXY_HOST, PROXY_PORT))

    return fn


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


# Functions
def facebook_appeal(full_name, mail_address, username_x, phone_x, appeal_text):
    driver.get('https://m.facebook.com/help/contact/606967319425038')
    find_element_send_text('//input[@name="name"]', full_name)
    find_element_send_text('//input[@name="email"]', mail_address)
    find_element_send_text('//input[@name="instagram_username"]', username_x)
    find_element_send_text('//input[@name="mobile_number"]', phone_x)
    find_element_send_text('//*[@name="appeal_reason"]', appeal_text)
    specific_clicker('//form//button[@type="submit"]')
    print('Facebook Appeal Done')
    time.sleep(7)


def instagram_link_1(full_name, username_x, mail_address, country, appeal_text):
    driver.get('https://help.instagram.com/contact/1784471218363829')
    find_element_send_text('//input[@name="name"]', full_name)
    find_element_send_text('//input[@name="username"]', username_x)
    find_element_send_text('//input[@name="email"]', mail_address)
    find_element_send_text('//form//input[@aria-label="Enter a country name..."]', country)
    find_element_send_text('//*[@name="user_comment"]', appeal_text)
    specific_clicker('//form//button[@type="submit"]')
    print('Instagram Link 1 Done')
    time.sleep(10)
    try:
        response = str(driver.find_element(By.XPATH, '//div[@role="dialog"]//div[@id]').text).lower()
        if "is active" in response:
            print("Instagram Link 1 Done")
            with open('AlreadyDone.txt', 'a') as file:
                file.write(f'{username_x}\n')
    except:
        pass


def instagram_link_2(full_name, username_x, mail_address, country):
    driver.get('https://help.instagram.com/contact/1652567838289083')
    specific_clicker('(//*[@name="AccountType"])[2]')
    find_element_send_text('//input[@name="name"]', full_name)
    find_element_send_text('(//form//input[@type="text"])[3]', username_x)
    find_element_send_text('(//form//input[@type="text"])[4]', mail_address)
    find_element_send_text('(//form//input[@type="text"])[5]', country)
    driver.find_element(By.XPATH, '(//form//input[@type="text"])[5]').send_keys(Keys.ENTER)
    time.sleep(1)
    specific_clicker('//form//button[@type="submit"]')
    print('Instagram Link 2 Done')
    time.sleep(7)


def instagram_link_3(full_name, username_x, mail_address, country, files):
    driver.get('https://help.instagram.com/contact/396169787183059')
    specific_clicker('(//label/input[@type="radio"])[2]')
    find_element_send_text('//input[@name="name"]', full_name)
    find_element_send_text('(//form//input[@type="text"])[3]', username_x)
    find_element_send_text('(//form//input[@type="text"])[4]', mail_address)
    find_element_send_text('(//form//input[@type="text"])[5]', country)
    # driver.find_element(By.XPATH, '(//form//input[@type="text"])[5]').send_keys(Keys.ENTER)
    time.sleep(3)
    for single_file in files:
        while True:
            try:
                driver.find_element(By.XPATH, '//form//input[@type="file"]').send_keys(single_file)
                break
            except:
                time.sleep(1)
    time.sleep(10)
    specific_clicker('//form//button[@type="submit"]')
    print('Instagram Link 3 Done')
    time.sleep(7)

import ctypes

def set_cmd_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)


data = pd.read_csv('data.csv')
faker = Faker()

while True:
    for single_account in data.values:

        already_done = get_file_data('AlreadyDone.txt')
        username_ = single_account[0]
        email_ = str(single_account[1])
        full_name_ = faker.name()
        phone_ = f"+49{random.randint(1000000000, 9999999999)}"
        country_ = random.choice(['Germany', 'Singapore'])
        appeal_text = f"""I am writing to appeal the recent disabling of my Instagram account, @{username_}, and kindly request a thorough review of my case for reinstatement. I believe there may have been a misunderstanding or a mistake leading to the account suspension, and I would appreciate your attention and assistance in resolving this matter."""

        if "@" not in email_:
            email_ = f"{username_}{random.randint(1, 100000)}@gmail.com"

        if username_ in already_done:
            continue

            # wildest_modelz

        options = uc.ChromeOptions()
        proxies_list = get_file_data('proxies')
        my_proxy = random.choice(proxies_list)
        proxy = get_proxy_extension(my_proxy)
        options.add_argument(f'--load-extension={proxy}')
        driver = uc.Chrome(options=options)
        driver.maximize_window()

        files = os.listdir('Screenshots')
        main_file = os.getcwd() + '\\Screenshots'
        files = [fr'{main_file}\{file}' for file in files]
        for x in range(2):
            title_bar = f"Instagram Appeal Bot | Proxy in use: {proxy} | Account in use: {username_} "
            set_cmd_title(title_bar)
            input("add: ")
            facebook_appeal(full_name_, email_, username_, phone_, appeal_text)
            instagram_link_1(full_name_, username_, email_, country_, appeal_text)
            instagram_link_2(full_name_, username_, email_, country_)
            instagram_link_3(full_name_, username_, email_, country_, files)
            print(f'{username_} Done {x + 1} times')

        print("Done")
        driver.quit()
