import os
import time, csv
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

################# Telegram ######################

bot_token = '6166663681:AAF9vLxyN3CfA_Xb8Lomwuy3BD_MajoLF9w'
bot_chatID = '-1001885631289'
alert_message = """New Request Available which matches your Requirements"""


########################################################################################################################
# Functions


def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


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

import subprocess

def close_chrome():
    try:
        subprocess.call(['killall', 'Google Chrome'])
    except:
        pass


with open("Already_done.txt", "w") as file:
    file.write("")

close_chrome()
options = uc.ChromeOptions()
path = "/Users/yliesse/Library/Application Support/Google/Chrome"
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Default')
driver = uc.Chrome(options=options)
driver.maximize_window()
driver.get("https://www.mystudies.com/")
print("\n")
input("Please Confirm Login and Press Enter to Continue: ")
while True:
    already_done = get_file_data("Already_done.txt")

    driver.get("https://www.mystudies.com/mon-compte/tuteur/commandes/disponibles")
    time.sleep(2)
    while True:
        try:
            driver.find_element(By.XPATH, "//table")

            break
        except:
            time.sleep(1)

    orders = driver.find_elements(By.XPATH, '//table//span[@class="text-danger"]/ancestor::tr//a')
    orders = [x.get_attribute("href") for x in orders]
    current_date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if len(orders) == 0:
        print(f"No Orders Match Our requirements [{current_date_time}]")


    for single_order_link in orders:
        if single_order_link in already_done:
            continue
        driver.get(single_order_link)
        time.sleep(2)
        # scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        specific_clicker2("//button[text()=' Je souhaite prendre en charge cette commande']")
        time.sleep(5)
        with open("Already_done.txt", "a", encoding="utf-8") as file:
            file.write(single_order_link + "\n")

        telegram_bot_sendtext(alert_message)

    print(f"Waiting for 15 seconds [{current_date_time}]")
    time.sleep(15)
