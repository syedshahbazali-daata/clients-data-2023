import os
import pickle
import random
from datetime import datetime
from threading import Thread

import undetected_chromedriver as uc  # pip install undetected-chromedriver
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time


########################################################################################################################
#                                                                                                                      #
#                                        PLEASE DON'T CHANGE ANYTHING BELOW                                            #
#                                                                                                                      #
########################################################################################################################


def get_file_data(file):
    with open(file) as f:
        data = f.read().strip()
        my_file_data = data.split('\n')

    return my_file_data


def find_element_click(location_of_the_element):
    """
    :param location_of_the_element: XPATH of te any web element.
    :return: Find element until it present on webpage and click on it.
    """
    while True:
        try:
            driver.find_element(By.XPATH, location_of_the_element).click()
            break
        except Exception as e:
            # print(e)
            pass


def find_element_send_text(location_of_the_element, type_message):
    """
        :param location_of_the_element: XPATH of te any web element.
        :return: Find element until it present on webpage and click on it.
        """
    while True:
        try:
            driver.find_element(By.XPATH, location_of_the_element).clear()

            driver.find_element(By.XPATH, location_of_the_element).send_keys(type_message)
            break
        except Exception as e:
            print(e)
        pass


def specific_clicker(ele):
    while True:
        try:
            element = driver.find_element(By.XPATH, ele)
            webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

            break
        except Exception as e:
            # print(e)
            pass


def specific_clicker_pass(ele):
    try:
        element = driver.find_element(By.XPATH, ele)
        webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()


    except Exception as e:
        # print(e)
        pass


def specific_clicker_with_direct(element):
    try:

        webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()


    except Exception as e:
        print(e)
        pass


def driver_go(url):
    """
    :param url: URL of the webpage.
    :return: Open the webpage without Command error.
    """
    while True:
        try:
            driver.get(url)
            break
        except Exception as e:
            print(e)
            input('Press any key to continue...')

            pass


def update_data(file, data):
    with open(file, "a") as f:
        f.write(f"{data}\n")


def playlist_track(playlist_id):
    import requests

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    querystring = {"fields": "tracks", "additional_types": "track,episode", "offset": "0", "limit": "25",
                   "market": "from_token"}

    payload = ""
    headers = {
        "accept-language": "en",
        "sec-ch-ua-mobile": "?0",
        "authorization": "Bearer BQDYwwzey2SsKFXAAf8sgOsYAaabbBO8G86T3B8Yp5F2yTFKkOSHmFezmJcfmIrbvl7PPconDSfknIKzrkmzG1glfj-lvu-bwQlPODB9tQkLGL_QIR1dEaVjGp7E6z7XZYVCbLWCVdlxLIW0EyXJXPIPtHrSgbEN890SjHcqPjS-5BIt4sSjLP2N00jAZIRxud05n9mA0nQlPA8yJoJr0SkJ2V-1OyybDOOARN2xY17CGGviedRTcsNjMWUkQwtKfdwKohvtonVbgorr-3f7_XpxdiCvTJnl7Z4D2A3kk6OVPwyjk5I7WTrrEYoaY15fE-x7wFaEjbMP1pq7TswFKS1hrWAM",
        "accept": "application/json",
        "Referer": "https://open.spotify.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "spotify-app-version": "1.1.93.541.gc6ce4634",
        "app-platform": "WebPlayer",
        "client-token": "AAAY4nJ0S7GQMyyjg9bOtEorX9h02YiEWlr785OBeoDzb8FOS1euZJE15x9yV5EnRKUUMzjbl6T0NJ/okrMzeXM3CpD6HptUKKRNai3d6KnbsDroGwSErTDQMnBct/1vEsZ+ZsVl3lWpf+TGjmAvXccosDMCEuyVgPm6B9vh6JWewj6OpFbeT8JSuXOO442wPYcWQJJu13LSxMTvUvWeplfauphcgPyHuFK4F4j5+h2XlZHzR7Zqk9KpUSQDTPvrZwElb1rUo7uLnRutMDvuKo+zM2pV6aDanqtogMfG/SSqaQ==",

    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    response = response.json()
    tracks = [str(single['sharing_info']['uri']).replace('spotify:track:', '') for single in
              response['tracks']['items']]
    return tracks


def time_to_seconds(mytime: str):
    get_time_obj = datetime.strptime(mytime, '%M:%S')
    result = get_time_obj.second + get_time_obj.minute * 60
    return int(result)


check_playlist = []


def timer_in_background(seconds: int):
    point = 0
    time.sleep(12)
    while True:
        time.sleep(1)
        point += 1
        print("Playlist Time: ", point, seconds)
        if point >= seconds:
            check_playlist.append("1")
            break


def play_spotify_playlists(Account_file, playlist_file):
    if len(playlist_file) > 0:
        global driver
        driver = uc.Chrome()  # open chrome driver
        driver.maximize_window()
        driver_go('https://accounts.spotify.com/en/login')
        with open(f'Accounts FIles/{Account_file}', 'rb') as f:
            account_cookies = pickle.load(f)

        for cookie in account_cookies:
            driver.add_cookie(cookie)

        for single_playlist in playlist_file:

            splitted_url = single_playlist.replace('https://', '').split(':')
            print(splitted_url)

            single_playlist_url = f"https://{splitted_url[0]}"
            playlist_time = int(splitted_url[1]) * 60
            song_time = int(splitted_url[2])

            driver_go(single_playlist_url)

            # Check Login or Not
            while True:
                try:
                    driver.find_element(By.XPATH, "//span[text()='Log in']")
                    raise Exception('Login Failed - Cookies are Expired')
                except Exception as e:
                    pass

                try:
                    driver.find_element(By.XPATH, '//button[@data-testid="user-widget-link"]')
                    break
                except Exception as e:
                    pass

            # Get all tracks in the playlist
            time.sleep(4)
            for checking in range(5):
                specific_clicker_pass('//div[@id]/button[@aria-label="Close"]')

            print("Playing Playlist: ", single_playlist_url)
            t1 = Thread(target=timer_in_background, args=[playlist_time])
            t1.start()

            while True:
                if len(check_playlist) == 1:
                    check_playlist.clear()
                    break
                try:

                    rand_keys = [Keys.END, Keys.UP]
                    driver.find_element(By.XPATH, '//main').send_keys(random.choice(rand_keys))
                    driver.find_element(By.XPATH, '//main').send_keys(random.choice(rand_keys))

                    time.sleep(2)

                except Exception as e:

                    pass

                tracks_play_elements = driver.find_elements(By.XPATH,
                                                            '//div[@role="row"]//div[@data-testid="tracklist-row"]/div[@role="gridcell"]/div/button')

                if len(tracks_play_elements) > 0:
                    specific_clicker_with_direct(random.choice(tracks_play_elements))
                    specific_clicker_with_direct(random.choice(tracks_play_elements))

                    while True:
                        try:
                            current_time = driver.find_element(By.XPATH, '//div[@data-testid="playback-position"]').text
                            specific_clicker_pass('//footer//button[@aria-label="Play"]')

                            time_to_play = time_to_seconds(str(current_time))
                            time_for_each_track = int(song_time)



                            if time_to_play > time_for_each_track or len(check_playlist) > 0:
                                break
                        except Exception as e:
                            pass
        driver.quit()
