import os
import time, csv
from datetime import datetime

import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

available_times = ['11:00 AM', '11:10 AM', '11:20 AM', '11:30 AM', '11:40 AM', '11:50 AM']
username = "13219"
password = "Tfg@4001"


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


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()
url = f"https://www.mesaverdecc.com/make-a-tee-time-298.html"

driver.get('https://www.mesaverdecc.com/member-login')

find_element_send_text('//input[@id="lgUserName"]', username)
find_element_send_text('//input[@id="lgPassword"]', password)
specific_clicker('//*[@id="lgLoginButton"]')
time.sleep(3)

checking = 0
available_times = [f"text()='{x}'" for x in available_times]
available_times = ' or '.join(available_times)
while True:
    driver.get(url)
    # scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)
    check_day = get_day(['wednesday', 'friday', 'tuesday'])

    if check_day is None:
        print('not wednesday or friday or tuesday')

    while True:
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@data-fturl="Member_select"]'))
            break
        except Exception as e:
            print(e)

    check_day_xpath = f"//td/a[text()='{check_day}']/.."
    # check_day_xpath = f"//td/a[text()='5']/.."

    # zoom out 50%


    while True:
        try:
            driver.find_element(By.XPATH, check_day_xpath).click()
            break
        except Exception as e:
            print(e)

    time.sleep(2)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@data-fturl="Member_select"]'))


    # switch to iframe

    xpath = f"//div[text()='5 Open']/../..//a[{available_times}]"
    print('working')

    try:
        driver.find_element(By.XPATH, xpath).click()
    except:
        checking += 1
        print(f'NOT FOUND [{checking}][{datetime.now().strftime("%H:%M:%S")}]')

        continue

    while True:
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe'))
            break
        except:
            pass

    specific_clicker("//li/*[text()='Partners']")
    time.sleep(1)
    while True:
        try:
            members_element = driver.find_elements(By.XPATH, '(//div[@class="ftMs-resultList"])[1]//span')
            if len(members_element) > 0:
                break
        except Exception as e:
            pass

    for member in members_element:
        member.click()

    input("add: ")
    specific_clicker("//a[text()='Submit Request']")
    time.sleep(1)
    input("submit: ")
