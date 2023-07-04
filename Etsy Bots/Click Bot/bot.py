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
    # "http://vdtdaksm-rotate:tj0p16tz6bxk@p.webshare.io:80/" -> vdtdaksm-rotate:tj0p16tz6bxk@p.webshare.io:80

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


# search Function
def search_on_etsy(search_term):
    driver.get("https://www.etsy.com/")
    time.sleep(random.randint(1, 4))
    find_element_send_text('//input[@data-id="search-query"]', search_term)
    time.sleep(random.randint(1, 4))
    driver.find_element(By.XPATH, '//input[@data-id="search-query"]').send_keys(Keys.ENTER)
    return str(driver.current_url)


def find_product(product_listing_id, search_term):
    search_product_on_etsy = search_on_etsy(search_term) + "&page="
    page_number = 1
    while True:
        try:
            time.sleep(random.randint(1, 4))
            search_results_products = driver.find_elements(By.XPATH, '//div[@data-search-results-container]//li//div/a')
            search_results_products = [str(x.get_attribute('data-listing-id')) for x in search_results_products]
            search_results_products = list(set(search_results_products))
            print("Found Products: ", str(len(search_results_products)))

            if product_listing_id in search_results_products:
                print(f"Found your Listing #{product_listing_id} at Page {page_number}")
                specific_clicker(
                    f"//div[@data-search-results-container]//li//div/a[@data-listing-id='{product_listing_id}']")
                print("Clicked on the Product")
                time.sleep(random.randint(7, 13))

                # scroll down
                

                return True
            else:
                page_number += 1
                driver.get(search_product_on_etsy + str(page_number))
                time.sleep(random.randint(1, 4))
        except:
            print(f"Not Found your Listing #{product_listing_id} at Page {page_number}")
            pass


def switch_to_new_tab():
    while True:
        try:
            driver.switch_to.window(driver.window_handles[-1])
            print("Switched to New Tab")
            break
        except:
            pass


# lDDrIwcaqzJ3TJni1bncp8cFXAT1oq2UUcVcoLOP0XNJldWEBXXGg2AllMPOkH4D


while True:
    products_data = get_file_data('products')[1:]
    for single_product in products_data:
        input_product_listing_id = single_product.split(',')[0]
        input_search_term = single_product.split(',')[1]
        options = uc.ChromeOptions()
        proxies_list = get_file_data('Proxies.txt')
        my_proxy = random.choice(proxies_list)
        proxy = get_proxy_auth_extension(my_proxy)
        options.add_argument(f'--load-extension={proxy}')
        driver = uc.Chrome(options=options)
        driver.maximize_window()
        find_product(input_product_listing_id, input_search_term)
        driver.quit()

    print("Sleep for 12 minutes")
    time.sleep(12 * 60)
