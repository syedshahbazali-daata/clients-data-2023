import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# action_chains = ActionChains(driver)

import random

import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

########################################################################################################################


bot_token = '6069041211:AAFv-8fUFgb7FbF91yspB0mpETnGfM5zFTw'
bot_chatID = '1868271284'
sheet_url = 'https://docs.google.com/spreadsheets/d/19TYtdlUg4gPk2QxWGjGSZiQNRs_3LsiXA3X12QlnHbs/edit?usp=sharing'


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
        if page_number > 10:
            index_of_product = "Not Found with in 40 pages"
            result = [page_number, index_of_product, search_term, product_listing_id]
            return result
        try:
            # scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(1, 4))
            search_results_products = driver.find_elements(By.XPATH, '//div[@data-search-results-container]//li//div/a')
            search_results_products = [str(x.get_attribute('data-listing-id')) for x in search_results_products]
            search_results_products = list(set(search_results_products))
            print("Found Products: ", str(len(search_results_products)))

            if product_listing_id in search_results_products:
                index_of_product = search_results_products.index(product_listing_id)

                result = [page_number, index_of_product, search_term, product_listing_id]

                return result
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


while True:
    date_yesterday = get_file_data("already_done.txt")[0]
    date_today = datetime.today().strftime('%Y-%m-%d')
    if date_yesterday == date_today:
        print("Already Done Today")
        time.sleep(60)
        continue

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds_sheet = ServiceAccountCredentials.from_json_keyfile_name(
        r"connection_api.json", scope)
    client = gspread.authorize(creds_sheet)
    sheet = client.open_by_url(sheet_url).sheet1
    while True:
        try:
            products_data = sheet.get_all_values()[1:]
            break
        except:
            pass

    for single_product in products_data:
        input_search_term = str(single_product[0])
        input_product_listing_id = str(single_product[1])

        options = webdriver.ChromeOptions()
        options.headless = False
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1920, 1080)
        result_response = find_product(input_product_listing_id, input_search_term)
        message = f"STAT\n\nPage Number: {result_response[0]}\n" \
                  f"Index of Product: {result_response[1]}\n" \
                  f"Search Term: {result_response[2]}\n" \
                  f"Product Listing ID: {result_response[3]}\n" \
                  f"Current Time: {datetime.now().strftime('%d %b %Y ')}"

        telegram_bot_sendtext(message)
        driver.quit()

    with open("already_done.txt", "w", encoding="utf-8") as file:
        file.write(date_today)
