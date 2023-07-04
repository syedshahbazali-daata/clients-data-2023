from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from youtubesearchpython import VideosSearch
from database import *


def get_views(video_id):
    while True:
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos_search = VideosSearch(url, limit=1)
        result = videos_search.result()
        try:
            vide_tittle = str(result['result'][0]['title']).strip()
            views_count = int(str(result['result'][0]['viewCount']['text']).strip().replace(",", "").split(" ")[0])

            if "http" in vide_tittle or "//" in vide_tittle or int(views_count) < 10000:
                continue
            else:
                return [vide_tittle, views_count]



        except:
            with open("error.txt", 'a', encoding='utf-8') as file:
                file.write(f"Error in {result}\n{video_id}\n\n")
            return None


def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')
    return data


def get_all_videos_ids():
    playlist_data = get_file_data("playlist.txt")
    list_of_videos_ids = []

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
            list_of_videos_ids.append(video_id)
        driver.quit()
    return list_of_videos_ids


def get_all_views(current_date, current_time):
    data = []
    videos_ids = get_all_videos_ids()

    for video_id in videos_ids:
        views_data = get_views(video_id)
        if views_data is None:
            continue

        row = [current_date, current_time, video_id, views_data[0], views_data[1]]
        data.append(row)

    # append to google sheet (CONTENT)
    add_multiple_rows(data, "CONTENT")


def run_update_content():
    # d-m-Y H:M

    while True:
        current_datetime_x = datetime.now().utcnow().strftime(
            "%d-%m-%Y %H:%M")  # add 5 hours 30 minutes to convert to india time

        if int(current_datetime_x.split(" ")[1].split(":")[1]) % 5 == 0:
            current_datetime_x = (datetime.strptime(current_datetime_x, "%d-%m-%Y %H:%M") + timedelta(hours=5,
                                                                                                      minutes=30)).strftime(
                "%d-%m-%Y %H:%M")  # add 5 hours 30 minutes to convert to india time
            break

    diff_min = 275
    while True:
        try:
            current_date = current_datetime_x.split(" ")[0]
            current_time = current_datetime_x.split(" ")[1]
            get_all_views(current_date, current_time)
            print("Updated content")
            print(current_datetime_x)
            # add 5 minutes to current_datetime_x and update it ( to make consistent with the current time )
            current_datetime_x = (
                    datetime.strptime(current_datetime_x, "%d-%m-%Y %H:%M") + timedelta(minutes=5)).strftime(
                "%d-%m-%Y %H:%M")  # for next update

            print(current_datetime_x)
            update_home_data()

            while True:
                new_current_datetime = datetime.now().utcnow().strftime(
                    "%d-%m-%Y %H:%M")  # add 5 hours 30 minutes to convert to india time
                new_current_datetime = (datetime.strptime(new_current_datetime, "%d-%m-%Y %H:%M") + timedelta(hours=5,
                                                                                                              minutes=30)).strftime("%d-%m-%Y %H:%M")  # add 5 hours 30 minutes to convert to india time
                if new_current_datetime == current_datetime_x:
                    print(new_current_datetime, current_datetime_x)
                    break
                else:
                    time.sleep(1)
        except:
            pass
