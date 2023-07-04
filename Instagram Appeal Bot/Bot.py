import os
import time, csv
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
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


# Functions
def facebook_appeal(full_name, mail_address, username_x, phone_x, appeal_text):
    find_element_send_text('//input[@name="name"]', full_name)
    find_element_send_text('//input[@name="email"]', mail_address)
    find_element_send_text('//input[@name="instagram_username"]', username_x)
    find_element_send_text('//input[@name="mobile_number"]', phone_x)
    find_element_send_text('//*[@name="appeal_reason"]', appeal_text)
    specific_clicker('//form//button[@type="submit"]')
    time.sleep(7)


def instagram_link_1(full_name, username_x, mail_address, country, appeal_text):
    find_element_send_text('//input[@name="name"]', full_name)
    find_element_send_text('//input[@name="username"]', username_x)
    find_element_send_text('//input[@name="email"]', mail_address)
    find_element_send_text('//form//input[@aria-label="Enter a country name..."]', country)
    find_element_send_text('//*[@name="user_comment"]', appeal_text)
    specific_clicker('//form//button[@type="submit"]')
    time.sleep(7)


def instagram_link_2(full_name, username_x, mail_address, country):
    specific_clicker('(//*[@name="AccountType"])[2]')
    find_element_send_text('//input[@name="name"]', full_name)
    find_element_send_text('(//form//input[@type="text"])[3]', username_x)
    find_element_send_text('(//form//input[@type="text"])[4]', mail_address)
    find_element_send_text('(//form//input[@type="text"])[5]', country)
    specific_clicker('//form//button[@type="submit"]')
    time.sleep(7)

def instagram_link_3(full_name, username_x, mail_address, country, files):
    specific_clicker('(//label/input[@type="radio"])[2]')
    find_element_send_text('//input[@name="name"]', full_name)
    find_element_send_text('(//form//input[@type="text"])[3]', username_x)
    find_element_send_text('(//form//input[@type="text"])[4]', mail_address)
    find_element_send_text('(//form//input[@type="text"])[5]', country)
    for single_file in files:
        driver.find_element(By.XPATH, '//form//input[@type="file"]').send_keys(single_file)
        time.sleep(1)
    specific_clicker('//form//button[@type="submit"]')
    time.sleep(7)



data = pd.read_excel('data.xlsx')

links = ['https://m.facebook.com/help/contact/606967319425038', 'https://help.instagram.com/contact/1784471218363829',
         'https://help.instagram.com/contact/1652567838289083', 'https://help.instagram.com/contact/396169787183059']
for single_link in links:
    options = uc.ChromeOptions()
    proxies_list = get_file_data('proxies')
    my_proxy = random.choice(proxies_list)
    proxy = get_proxy_auth_extension(my_proxy)
    options.add_argument(f'--load-extension={proxy}')
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.get(single_link)
    time.sleep(5)
    facebook_appeal(data['Full Name'][0], data['Email'][0], data['Username'][0], data['Phone'][0], data['Appeal Text'][0])


