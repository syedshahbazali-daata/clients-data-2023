import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import csv
from youtubesearchpython import VideosSearch
from database import *
import pandas as pd
from updateContent import update_content


# from keepAlive import *


########################################################################################################################


def get_views(video_id):
    videos_search = VideosSearch(video_id, limit=1)
    result = videos_search.result()
    try:
        vide_tittle = str(result['result'][0]['title']).strip()
        views_count = int(str(result['result'][0]['viewCount']['text']).strip().replace(",", "").split(" ")[0])

        return [vide_tittle, views_count]

    except:
        return None


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


def get_all_videos_ids():
    with open("videos_data.txt", 'w', encoding='utf-8') as file:
        file.write("")
    playlist_data = get_file_data("playlist.txt")

    for single_playlist in playlist_data:
        global driver
        options = webdriver.ChromeOptions()
        options.headless = False
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1920, 1080)
        driver.get(single_playlist)
        time.sleep(4)
        # zoom out
        driver.execute_script("document.body.style.zoom='25%'")
        time.sleep(4)

        videos_id = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
        videos_id = [str(x.get_attribute("href")).split("?v=")[1].split("&")[0] for x in videos_id]
        for video_id in videos_id:
            with open("videos_data.txt", 'a', encoding='utf-8') as file:
                file.write(video_id + "\n")

        driver.quit()


def get_all_views():
    videos_id = get_file_data("videos_data.txt")
    current_date = datetime.now().strftime("%d-%m-%Y")
    already_done = get_file_data("already_done.txt")
    already_done = [str(x) for x in already_done if str(x) != ""]

    if len(already_done) > 2:
        with open("already_done.txt", 'w', encoding='utf-8') as file:
            file.write(current_date + "\n")

        # clear json file
        with open("data.json", 'w', encoding='utf-8') as file:
            json.dump([], file, indent=4)

    if str(current_date) in already_done:
        with open("already_done.txt", 'a', encoding='utf-8') as file:
            file.write(current_date + "\n")

    current_time = datetime.now().strftime("%H:%M")
    for video_id in videos_id:
        views_data = get_views(video_id)
        if views_data is None:
            continue

        # add in to csv file
        with open("data.csv", 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)

            writer.writerow([current_date, current_time, video_id, views_data[0], views_data[1]])


def run():
    get_all_videos_ids()
    get_all_views()


def run_bot():
    while True:
        run()
        print("Sleeping for 5 minutes")

        # Read the CSV file
        df = pd.read_csv('data.csv')
        df = df.drop_duplicates(subset=['Date', 'Time', 'Video Title'], keep='last')
        # Combine 'Date' and 'Time' columns into a single 'DateTime' column
        df['DateTime'] = df['Date'] + ' ' + df['Time']

        # Pivot the data
        df_pivot = df.pivot(index='DateTime', columns='Video Title', values='Views')

        # Reset the index and rename the columns
        df_pivot = df_pivot.reset_index().rename_axis(None, axis=1)
        df_pivot.to_csv('updated_data.csv', index=False, na_rep='NA')
        update_home()
        update_content()

        time.sleep(60 * 5)




