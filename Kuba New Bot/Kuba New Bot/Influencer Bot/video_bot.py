import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

import random

email_of_user = "cuentapropista.k@gmail.com"  # Email of the user
password_of_user = "@Muhammad@1"  # Password of the user
category_no = 2  # Category number
brand_name = "Cuba"  # Brand name


########################################################################################################################
# Functions
########################################################################################################################

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


def switch_tab(tab_number):
    while True:
        try:
            driver.switch_to.window(driver.window_handles[tab_number])
            break
        except:
            pass


def get_file_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read().strip().split("\n")

    return data


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()

# open new tab


driver.get('https://kbocuba.com/users/member_login')

find_element_send_text('(//div[@class="main_login_form"]//input[@id="login_email"])[2]', email_of_user)
find_element_send_text('(//div[@class="main_login_form"]//input[@id="login_password"])[2]', password_of_user)
specific_clicker('(//input[@type="submit"])[2]')
time.sleep(2)

# switch Language to English
driver.get("https://kbocuba.com/home/do_language/eng")

#
all_influencers_videos = []
channels_list = get_file_data("channels_list.txt")
for channel in channels_list:
    channel_url = channel + "/videos"
    driver.get(channel_url)
    time.sleep(2)
    # zoom out
    driver.execute_script("document.body.style.zoom='50%'")
    time.sleep(2)
    videos_urls = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, '//a[@id="video-title-link"]')]
    all_influencers_videos.extend(videos_urls)

# shuffle all_influencers_videos

random.shuffle(all_influencers_videos)

driver.execute_script("document.body.style.zoom='100%'")
for single_video in all_influencers_videos:
    already_done = get_file_data("Already_done.txt")
    if single_video in already_done:
        continue
    driver.get("https://kbocuba.com/videos")
    specific_clicker("(//a/span[text()='add_circle'])[2]")
    find_element_send_text('//input[@name="data[url]"]', single_video)
    specific_clicker("//*[text()='Fetch Video']")
    while True:
        try:
            driver.find_element(By.XPATH, '//select[@name="data[category_id]"]')
            break
        except:
            time.sleep(1)

    driver.find_element(By.XPATH, "//select[@name='data[category_id]']//option[text()='Influencer']").click()
    time.sleep(1)
    specific_clicker("//*[text()='Save Video']")
    time.sleep(3)
    with open("Already_done.txt", "a", encoding="utf-8") as f:
        f.write(f"{single_video}\n")

driver.quit()
