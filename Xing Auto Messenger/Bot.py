import os
import time, csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
from selenium.webdriver.common.keys import Keys

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


def send_message(profile_url):
    driver.get(profile_url)
    while True:
        try:
            name = str(driver.find_element(By.XPATH, '//section//div[@data-testid="PhotoWrapper"]//img[@aria-label]')
                   .get_attribute('aria-label'))
            break
        except:
            time.sleep(1)
            continue

    message = f"Hello {name}"

    while True:
        specific_clicker2('//button[@aria-label="Mehr"]')
        time.sleep(3)
        try:

            driver.find_element(By.XPATH, '//li/button[@data-xds="TextButton"]/..')
            print("Message Button Found")
            specific_clicker('//li/button[@data-xds="TextButton"]/..')

            break
        except:
            continue

    while True:
        try:
            driver.find_element(By.XPATH, '//form//textarea')
            print("Message Box Found")
            pyperclip.copy(message)
            driver.find_element(By.XPATH, '//form//textarea').send_keys(Keys.CONTROL + "v")

            break
        except:
            time.sleep(1)
            continue

    specific_clicker('//form/button')
    print("Message Sent")
    with open("Already_done.txt", "a", encoding="utf-8") as file:
        file.write(profile_url + "\n")
    time.sleep(3)


def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass


close_chrome()
options = uc.ChromeOptions()
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Default')
driver = uc.Chrome(options=options)
driver.maximize_window()
driver.get("https://www.xing.com/discover/updates")

input("Please Search for the people you want to send messages to and press enter: ")
message_people = int(input("How many people do you want to send messages to?:  "))
people_profile_urls_list = set()
while True:
    more_pages = False
    for i in range(10):
        try:
            current_page = driver.find_element(By.XPATH, "(//li/span[contains(@class, 'pagination')])[1]").text
            current_page = int(current_page)
            total_pages = driver.find_element(By.XPATH, "(//li/span[contains(@class, 'pagination')])[3]").text
            total_pages = int(total_pages)
            print(current_page, total_pages)
            more_pages = True
            break
        except:
            time.sleep(1)
            more_pages = False
            continue

    time.sleep(3)
    people_profile_urls = driver.find_elements(By.XPATH, "//div[@data-qa='results-list']/a[contains(@href, 'profile')]")
    people_profile_urls = [x.get_attribute('href') for x in people_profile_urls]
    already_sent = get_file_data('Already_done.txt')
    for url in people_profile_urls:
        if url not in already_sent:
            people_profile_urls_list.add(url)


    print(len(people_profile_urls_list))
    if len(people_profile_urls_list) >= message_people:
        break


    if more_pages:
        if current_page == total_pages:

            break

        specific_clicker("(//li/a[contains(@class, 'pagination')])[2]")
    print(len(people_profile_urls_list))


people_profile_urls_list = list(people_profile_urls_list)
print(f"Total people found on Search results: {len(people_profile_urls_list)}")
print("Starting to send messages")
counter = 0
for url in people_profile_urls_list:
    if counter == message_people:
        break
    send_message(url)
    time.sleep(3)
    counter += 1
    print(f"Message sent to {counter} people")


print("All messages sent")





