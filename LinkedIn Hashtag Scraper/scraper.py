import os
import time, csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

save_file_name = f"Save data"


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


def main(hashtag, csv_file_name):

    options = uc.ChromeOptions()
    # path = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"
    # using os
    path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
    options.add_argument(fr"user-data-dir={path}")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(f'--profile-directory=Profile 1')
    global driver
    driver = uc.Chrome(options=options)
    driver.maximize_window()

    url = f"https://www.linkedin.com/search/results/content/?keywords={hashtag.replace('#', '%23')}"
    driver.get(url)
    input("add")
    # zoom out to 50%
    driver.execute_script("document.body.style.zoom='50%'")
    # scroll down
    for i in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        posts = driver.find_elements(By.XPATH,
                                     '(//*[@id="main"]//ul[@class="reusable-search__entity-result-list list-style-none"]/li)')
        for single_post in range(len(posts)):
            index = single_post + 1
            xpath_post = f'(//*[@id="main"]//ul[@class="reusable-search__entity-result-list list-style-none"]/li)[{index}]'

            try:
                name = driver.find_element(By.XPATH, f"{xpath_post}//*[contains(@class, 'actor__name')]/span/span").text
            except:
                name = ""

            try:
                profile_link = driver.find_element(By.XPATH, f"{xpath_post}//*[contains(@class, 'app-aware-link')]") \
                    .get_attribute("href")
            except:
                profile_link = ""

            try:
                likes = driver.find_element(By.XPATH, f"{xpath_post}//*[@alt='like']/../span").text
            except:
                likes = ""

            try:
                comments = driver.find_element(By.XPATH,
                                               f"{xpath_post}//*[contains(@aria-label, 'comments')]/span").text
            except:
                comments = ""

            record = [profile_link, name, likes, comments]
            print(record)
            with open(f"LinkedIn CSV/{csv_file_name}.csv", 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(record)
        specific_clicker2("//span[text()='Show more results']")
        time.sleep(2)
    driver.quit()


########################################################################################################################


if __name__ == '__main__':
    hashtags_list = get_file_data('hashtags.txt')
    for single_hashtag in hashtags_list:
        main(single_hashtag, save_file_name)
