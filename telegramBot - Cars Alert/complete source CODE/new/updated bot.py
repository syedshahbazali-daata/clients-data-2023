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
from threading import Thread
import requests
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


def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
    params = {
        'chat_id': bot_chatID,
        'parse_mode': 'HTML',
        'text': bot_message
    }
    response = requests.post(send_text, data=params)
    return response.json()




def process_row(single_row):
    # code to be executed for each row
    xpath = f"(//div[contains(@class,'GO-Results-Row')])[{single_row}]"

    ad_link = driver.find_element(By.XPATH, f"{xpath}/a").get_attribute("href")
    title = get_text(f"({xpath}//div/span)[1]")
    registracija = get_text(f"{xpath}//td[text()='1.registracija']//following-sibling::td")
    gorivo = get_text(f"{xpath}//td[text()='Gorivo']//following-sibling::td")
    km_ = get_text(f"{xpath}//td[text()='Prevoženih']//following-sibling::td")
    menjalnik = get_text(f"{xpath}//td[text()='Menjalnik']//following-sibling::td")
    motor = get_text(f"{xpath}//td[text()='Motor']//following-sibling::td")
    price = get_text(f"({xpath}//div[@class='GO-Results-Price-TXT-Regular'])[2]")

    if str(ad_link) in already_done:
        print("Already done")
        return

    title_formatted = '<a href="' + ad_link + '" target="_blank" class="GO-Results-Title-Link">' + title + '</a>'
    main_url = "https://www.avto.net/"

    message = f"<strong>RSS feed for: </strong>{main_url}\nTitle: {title_formatted}\n1.registracija: {registracija}\nPrevoženih: {km_}\nGorivo: {gorivo}\nMenjalnik: {menjalnik}\nMotor: {motor}\n\nPrice: {price}".strip()

    # telegram_bot_sendtext(message)
    print("message sent")

    with open("already_done.txt", "a", encoding='utf-8') as file:
        file.write(ad_link + "\n")


threads = []


def get_text(ele):
    try:
        element = driver.find_element(By.XPATH, ele)
        return element.text
    except Exception as e:
        # print(e)
        return "NA"


bot_token = '5792992329:AAGGGWh_qA5G0V3cfva3GfjuU7KKERpdVlI'
bot_chatID = '-1001988258620'
url = "https://www.avto.net/Ads/results_100.asp?oglasrubrika=1&prodajalec=2"


def close_chrome():
    try:
        os.system("taskkill /f /im chrome.exe")
    except:
        pass


close_chrome()
options = uc.ChromeOptions()
proxies_list = get_file_data('proxies.txt')
my_proxy = random.choice(proxies_list)
proxy = get_proxy_auth_extension(my_proxy)
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
# options.add_argument(f'--profile-directory=Default')
options.add_argument(f'--profile-directory=Profile 3')
options.add_argument(f'--load-extension={proxy}')

driver = uc.Chrome(options=options)
driver.maximize_window()

while True:
    driver.get(url)
    input("Add: ")
    work = False
    for check in range(20):
        try:
            driver.find_element(By.XPATH, "//div[contains(@class,'GO-Results-Row')]")
            work = True
            print("found")
            break
        except:
            print("not found")
            time.sleep(1)

    if work:
        print("working now")
        already_done = get_file_data("already_done.txt")
        all_rows = driver.find_elements(By.XPATH, "//div[contains(@class,'GO-Results-Row')]")
        total_row = len(all_rows)
        for single_row in range(1, total_row + 1):
            # Create a new thread for each row and pass the `single_row` value
            t = Thread(target=process_row, args=(single_row,))
            threads.append(t)
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()



    else:
        pass


# check ip address in json format: https://api.myip.com