import os
import time, csv
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

################# Telegram ######################

bot_token = '6228806056:AAEAP6NOsbQC1COgBgqaDOsIivN8rrf4YQo'
bot_chatID = '-1001824191901'


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


while True:

    options = webdriver.ChromeOptions()
    options.headless = False
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)

    url = f"https://proscheduler.prometric.com/scheduling/searchAvailability"
    driver.get(url)

    while True:
        try:
            driver.find_element(By.XPATH,
                                "//select[@id='test_sponsor']/option[contains(text(), 'National Board of Medical Examiners')]").click()
            break
        except:
            time.sleep(0.1)

    while True:
        try:
            driver.find_element(By.XPATH, "//select[@name='selectedProgram']/option[contains(text(), 'STEP1')]").click()
            break
        except:
            time.sleep(0.1)

    while True:
        try:
            driver.find_element(By.XPATH,
                                "//select/option[contains(text(), 'United States Medical Licensing Examination')]").click()
            break
        except:
            time.sleep(0.1)
    specific_clicker('//button[@aria-label="Continue to next page"]')

    find_element_send_text('(//input)[1]', '40202')
    find_element_send_text('(//input)[2]', '06/02/2023')
    find_element_send_text('(//input)[3]', '06/05/2023')
    # scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    specific_clicker('//button[@aria-label="Continue to next page"]')
    time.sleep(3)
    while True:
        try:
            driver.find_element(By.XPATH, '//div[@class="row"]//span/strong')
            time.sleep(5)
            break
        except:
            time.sleep(0.1)

    results = driver.find_elements(By.XPATH, '//div[@class="row"]//span/strong')
    for result in results:
        row = str(result.text).strip().lower()
        print(row)
        if 'louisville' in row:
            # telegram_bot_sendtext("""ALERT\nWe Found Louisville""")
            break

    driver.quit()
    # current UTC dateTime
    now = datetime.now()
    current_date = now.strftime("%m/%d/%Y %H:%M:%S")
    # telegram_bot_sendtext(f"LAST CHECKED: {current_date} UTC \n\n")

    time.sleep(300)
