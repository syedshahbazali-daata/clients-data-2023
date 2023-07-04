import os
import time, csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
import pandas as pd
from textwrap import dedent
import os

########################################################################################################################
# Functions

BASE_DIR = os.path.dirname(os.path.abspath("_file_"))


def get_proxy_auth_extension(proxy):
    if proxy.strip() == '':
        return None
    cred, prox = proxy.split('@')
    PROXY_USER, PROXY_PASS = cred.split(':')
    PROXY_HOST, PROXY_PORT = prox.split(':')
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

                    function callbackFn(details) {
                        return {
                            authCredentials: {
                                username: "%s",
                                password: "%s"
                            }
                        };
                    }

                    chrome.webRequest.onAuthRequired.addListener(
                                callbackFn,
                                {urls: ["<all_urls>"]},
                                ['blocking']
                    );
                    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    fn = os.path.join(BASE_DIR, 'proxy_ext')
    if not os.path.exists(fn):
        os.mkdir(fn)
    m_path = os.path.join(fn, "manifest.json")
    b_path = os.path.join(fn, "background.js")
    with open(m_path, 'w') as f:
        f.write(dedent(manifest_json))
    with open(b_path, 'w') as f:
        f.write(dedent(background_js))
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


def element_xpath_with_text(text):
    return f"//*[text()='{text}' or text()='{text.upper()}' or text()='{text.lower()}' or text()='{text.capitalize()}']"



def get_text(ele):
    while True:
        try:
            element = driver.find_elements(By.XPATH, ele)
            texts = [str(x.text) for x in element]
            return texts
        except Exception as e:
            # print(e)
            pass







options = uc.ChromeOptions()
# proxies_list = get_file_data('proxies.txt')
# my_proxy = random.choice(proxies_list)
# proxy = get_proxy_auth_extension(my_proxy)
# options.add_argument(f'--load-extension={proxy}')
driver = uc.Chrome(options=options)
driver.maximize_window()
driver.get('https://ads.google.com/')
time.sleep(2)

specific_clicker(element_xpath_with_text('Sign in'))

print("NOTE: This program will work with the latest version of Chrome only.")

driver.get(url)
time.sleep(2)
for i in range(5):
    specific_clicker2("//*[text()='Agree']")
    time.sleep(0.5)
# zoom in 150%
# driver.execute_script("document.body.style.zoom='150%'")
while True:
    specific_clicker('//a[@title="View next record"]')
    print(driver.current_url)
    for i in range(5):
        try:
            driver.find_element(By.XPATH, '//*[@title="toggle additional data"]')
            break
        except:
            time.sleep(1)
    specific_clicker2('//*[@title="toggle additional data"]')
from database import *


def update_content():
    while True:
        try:
            df = pd.read_csv('data.csv')
            # upload the csv file to google sheets

            df = df.drop_duplicates(subset=['Date', 'Time', 'Video Title'], keep='last')
            df = df.fillna('NA')

            sheet = client.open_by_url(sheet_url).worksheet("CONTENT")
            sheet.clear()
            column_names_upper = [str(x.upper()) for x in df.columns.values.tolist()]
            sheet.update([column_names_upper] + df.values.tolist())

            print("Updated Content Data")

            # make column bold with 10 size and other data nunito font but with 9 size
            sheet.format('A1:Z1', {'textFormat': {'bold': True, 'fontSize': 10}})

            break
        except:
            print("Error in updating content")
            time.sleep(10)
            continue
