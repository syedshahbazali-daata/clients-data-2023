import time, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

set_date = "16/05/23"  # format: 13/05/23 (dd/mm/yy)
available_hours = ['06']
username = "andrewwhyte94"
password = "kUkLc6GKHR!Fd9T"

########################################################################################################################
# Functions

available_hours = [f'contains(text(), "{x}:")' for x in available_hours]
available_hours = ' or '.join(available_hours)
available_hours_xpath = f"""//div[@class="fullsheet_container_available"]/a[{available_hours}]"""


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
    seven_days = now + timedelta(days=9)
    seven_days = int(str(seven_days.strftime("%d")))
    return seven_days


def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass


def get_element(ele):
    while True:
        try:
            element = driver.find_element(By.XPATH, ele)
            return element
        except Exception as e:
            # print(e)
            pass


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()

driver.get('https://www.stockwoodvale.com/')
specific_clicker("//li/a[text()='Book a tee time']")
time.sleep(3)
# close tab 0 and switch to tab 1

driver.close()
driver.switch_to.window(driver.window_handles[0])

find_element_send_text('//input[@id="username_field"]', username)
find_element_send_text('//input[@id="password_field"]', password)
specific_clicker('//*[@id="submit_auth"]')
time.sleep(3)

# Reaching the Booking Page

specific_clicker('//input[@value="Make A Booking"]')
specific_clicker("//a[contains(text(), ' Golf  ')]")
specific_clicker('//input[@value="SUBMIT"]')

while True:
    specific_clicker(f"//a[contains(@onclick, '{set_date}')]")  # click on the date
    get_element('//div[@class="prices_container"]')

    # get the available times
    website_available_times = driver.find_elements(By.XPATH, available_hours_xpath)
    if len(website_available_times) == 0:
        print("No available times")
        specific_clicker('//div[@id="page_overlay"]//div[@class="activity_viewtimes_close"]/a')  # close the popup
        driver.refresh()
        continue

    specific_clicker(available_hours_xpath)  # click on the available time
    input("Press Enter to continue...")
