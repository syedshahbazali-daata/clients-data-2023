import os
import time, csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


# SOCIAL MEDIA UPLOADING
def facebook_upload_post(text, file):
    driver.get("https://www.facebook.com/profile.php")
    specific_clicker("//span[text()='Photo/video']")
    while True:
        try:
            driver.find_element(By.XPATH, '//form//input[@type="file"]').send_keys(fr'{file}')
            break
        except:
            time.sleep(1)

    while True:
        try:
            driver.find_element(By.XPATH, """//div[@aria-label="What's on your mind?"]""").send_keys(
                text)
            break
        except:
            time.sleep(1)
    time.sleep(7)
    specific_clicker('//div[@aria-label="Post"]')
    time.sleep(5)


def tiktok_upload_post(text, file):
    driver.get('https://www.tiktok.com/upload?lang=en')
    # wait for //iframe to load 20 seconds
    while True:
        try:
            driver.find_element(By.XPATH, '//iframe')
            break
        except:
            time.sleep(2)
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe'))

    # wait for //input[@accept="video/*"] to load 20 seconds
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@accept="video/*"]')))
    driver.find_element(By.XPATH, '//input[@accept="video/*"]').send_keys(fr"{file}")
    # wait for //div[@role="combobox"] to load 20 seconds
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@role="combobox"]')))
    driver.find_element(By.XPATH, '//div[@role="combobox"]').send_keys(text)
    # scroll to end of page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    while True:
        try:
            driver.find_element(By.XPATH, "//button[@disabled]//*[text()='Post']")
            print('Disable found')
            time.sleep(2)
        except:
            time.sleep(3)
            print('Disable not found')
            break
    # driver.switch_to.default_content()
    #
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe'))
    print('clicking')
    while True:
        try:
            driver.find_element(By.XPATH, "//*[text()='Post']/../..").click()
            print('clicked')
            time.sleep(3)
        except:
            break

    time.sleep(5)


def instagram_uploader(text, file):
    specific_clicker("//*[text()='Create']/..")
    driver.find_element(By.XPATH, '//form[@role="presentation"]/input').send_keys(fr"{file}")

    specific_clicker("//*[text()='Next']")
    time.sleep(3)
    specific_clicker("//*[text()='Next']")
    driver.find_element(By.XPATH, '//div[@aria-label="Write a caption..."]').send_keys(f"{text}")
    specific_clicker("//*[text()='Share']")
    time.sleep(6)


# SELENİUM BOT

close_chrome()
options = uc.ChromeOptions()
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Profile 1')
driver = uc.Chrome(options=options)
driver.maximize_window()



