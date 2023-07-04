import os
import random
import time, csv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

time_between_follow = random.randint(5, 15)  # min/max seconds between each follow


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

followers = get_file_data('followers.txt')
for single_follower in followers:
    driver.get(single_follower)
    time.sleep(2)

    loaded = False

    for i in range(1, 10):
        try:
            no_of_followers = str(driver.find_element(By.XPATH,
                                                      "//section//*[contains(text(), 'followers')]/*[@title]").text).strip().replace(
                ",", "")
            no_of_followers = int(no_of_followers)
            print(no_of_followers)
            loaded = True
            break
        except:
            pass

    if not loaded:
        continue

    if no_of_followers > 1000:
        continue

    try:
        driver.find_element(By.XPATH, "//header//button//*[text()='Follow']")

    except:
        print("Already Following")
        continue

    specific_clicker("//header//button//*[text()='Follow']")
driver.quit()
