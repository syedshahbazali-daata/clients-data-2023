import random
import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc

usr = "puneetsuper_starrrr"
user_input = 50


def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass


def get_file_data(file_x):
    with open(file_x, "r") as file_x:
        data = file_x.read().strip().split("\n")
    return data


def specific_clicker(ele):
    while True:
        try:
            element = driver.find_element(By.XPATH, ele)
            webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

            break
        except Exception as e:
            # print(e)
            pass


TIMEOUT = 10

close_chrome()

options = webdriver.ChromeOptions()
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Default')

driver = uc.Chrome(options=options)

driver.get('https://www.instagram.com/{}/'.format(usr))
driver.maximize_window()
time.sleep(random.randint(4, 8))

# //a[contains(@href, 'followers')]

specific_clicker("//a[contains(@href, 'followers')]")
time.sleep(3)
# scroll down to load few followers
for i in range(1, 5):
    driver.execute_script("window.scrollTo(0, 100);")
    time.sleep(random.randint(1, 5))
    print("scrolling down")

already_followed = get_file_data("followers.txt")
followers = driver.find_elements(By.XPATH, "//a/img/..")
count = 0
for follower in followers:

    follower_url = follower.get_attribute("href")
    if follower_url in already_followed:
        continue

    with open("followers.txt", "a") as file:
        file.write(follower_url + "\n")
    count += 1
    if count == user_input:
        break

driver.close()
