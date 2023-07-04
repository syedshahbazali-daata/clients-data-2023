import os
import time, csv
from datetime import datetime
import pandas as pd
from selenium.webdriver.common.keys import Keys

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip

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
        except Exception as e:
            print(e)
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


def write_description(text):
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@aria-label="Description"]'))
    driver.find_element(By.XPATH, '//div[@aria-label="Description"]').send_keys(
        text)
    driver.switch_to.default_content()


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


os.chdir(os.path.dirname(os.path.abspath(__file__)))
csv_file = '../Scraper/jdsports.csv'

import requests


def download_image(image_url, folder_path, file_name):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    headers = {
        "authority": "i8.amplience.net",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "cache-control": "max-age=0",
        "if-modified-since": "Sun, 21 May 2023 05:06:19 GMT",

        "sec-ch-ua-mobile": "?0",

        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    # Send a GET request to the URL
    response = requests.get(image_url, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        # Extract the file name from the URL

        # Determine the file path to save the image
        file_path = os.path.join(folder_path, file_name)

        # Save the image to the specified file path
        with open(file_path, "wb") as file:
            file.write(response.content)

        print("Image downloaded successfully!")
        return True
    else:
        print("Failed to download the image.")
        return False


def upload_images(images):
    for i, image in enumerate(images):
        image_url = image.split('?')[0]
        file_name = f'image-{i + 1}.jpg'
        check_upload = download_image(image_url, r"Files", file_name)
        if not check_upload:
            return False

        time.sleep(4)
        driver.find_element(By.XPATH, '//input[@type="file"]') \
            .send_keys(os.path.join(os.getcwd(), r"Files", file_name))
        time.sleep(4)


df = pd.read_csv(csv_file, index_col=False)
data = df.values.tolist()
print(data)
close_chrome()
options = uc.ChromeOptions()
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Profile 1')
driver = uc.Chrome(options=options)
driver.maximize_window()

for single_product in list(data):
    print(single_product)

    driver.get('https://www.ebay.co.uk/sl/prelist/suggest?sr=shstart')

    # Select Category
    find_element_send_text("""//input[@aria-label="Tell us what you're selling"]""", single_product[-1])
    time.sleep(1)
    driver.find_element(By.XPATH, """//input[@aria-label="Tell us what you're selling"]""").send_keys(Keys.ENTER)
    specific_clicker("//button[text()='Continue without match']")
    specific_clicker('//fieldset//input')
    specific_clicker("//button[text()='Continue to listing']")

    time.sleep(5)

    # images
    images_urls = single_product[6].split(',')
    upload_images(images_urls)

    # delete files from folder
    folder = os.path.join(os.getcwd(), r"Files")
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            os.remove(file_path)
        except Exception as e:
            print(e)

    # Title
    find_element_send_text('//input[@name="title"]', single_product[1])

    # Description
    write_description(single_product[3])

    # Price
    price = round(float(single_product[4]) * 1.1, 2)
    driver.find_element(By.XPATH, '//input[@name="price"]').clear()
    find_element_send_text('//input[@name="price"]', str(price))
    input("add: ")




# what is MDN full form: Mozilla Developer Network
# why MDN: because it is the most reliable source of information on JavaScript
# is MDN just for JavaScript: no, it is for all web technologies
# for python: https://docs.python.org/3/








