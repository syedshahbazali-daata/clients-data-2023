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

def youtube_mp3_downloader(url):
    split_url = url
    driver.get(f"https://tomp3.cc/youtube-to-mp3/{split_url}")
    time.sleep(3)
    specific_clicker('//button[@id="btn-convert"]')
    specific_clicker("//a[text()=' Download']")
    time.sleep(10)


def get_videos_from_youtube():

    all_videos = set()
    while True:
        videos_urls = driver.find_elements(By.XPATH, '//a[@id="video-title-link"]')
        videos_urls = [x.get_attribute('href').split("=")[1] for x in videos_urls if x.get_attribute('href') != None]
        print(len(videos_urls))
        print(len(all_videos))
        all_videos.update(videos_urls)
        if len(all_videos) >= amount_of_videos:
            break

        # zoom out
        driver.execute_script("document.body.style.zoom='25%'")


        time.sleep(6)

    all_videos = list(all_videos)[:amount_of_videos]
    return all_videos

print("""
Select Platform:
1. Youtube
2. Rumble
""")
platform_name = int(input("Enter Platform Name (1/2): "))
channel_url = input("Enter Channel URL: ")
amount_of_videos = int(input("No. of Videos: "))
print("""
Download Type: 
1. Videos
2. Streams
""")
download_type = int(input("Enter Download Type (1/2): "))
if download_type == 1:
    channel_url = channel_url + "/videos"
elif download_type == 2:
    channel_url = channel_url + "/streams"



options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()
driver.get(channel_url)


if platform_name == 1:
    my_videos = get_videos_from_youtube()
    for video in my_videos:
        youtube_mp3_downloader(video)
        print("downloading...")



input("Press Enter to Exit: ")
driver.quit()