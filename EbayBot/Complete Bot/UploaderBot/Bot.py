import os
import re
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
    pyperclip.copy(text)
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@aria-label="Description"]'))
    driver.find_element(By.XPATH, '//div[@aria-label="Description"]').send_keys(Keys.CONTROL + 'v')
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

# delete Files

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

def change_color(color):

    while True:
        specific_clicker('//button[@name="attributes.Colour"]')
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, '//input[@name="search-box-attributesColour"]')
            break
        except:
            pass
    find_element_send_text('//input[@name="search-box-attributesColour"]', color)
    time.sleep(1)
    specific_clicker(f'//*[text()="{color}"]')


def change_size(size):
    while True:
        try:
            specific_clicker("//button[contains(@name, 'Size')]")
            time.sleep(1) # //input[contains(@name, 'Size')]
            driver.find_element(By.XPATH, "//input[contains(@name, 'Size')]")
            break
        except:
            pass
    find_element_send_text('//input[contains(@name, "Size")]', size)
    time.sleep(1)
    specific_clicker(f'//*[text()="{size}"]')



def delete_images_from_folder(folder_path):
    folder = os.path.join(os.getcwd(), fr"{folder_path}")
    # delete files from folder
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            os.remove(file_path)
        except Exception as e:
            print(e)


df = pd.read_csv(csv_file, index_col=False)

# if Variants has more than 1 value 6,7,7.c etc then make single product for each variant and delete the original product

new_df = pd.DataFrame(columns=df.columns)
for i, row in df.iterrows():
    variants = row['Variants'].split(',')
    if len(variants) > 1:
        for variant in variants:
            new_row = row.copy()
            new_row['Variants'] = variant
            new_df = new_df.append(new_row, ignore_index=True)
    else:
        new_df = new_df.append(row, ignore_index=True)

# convert new_df to list of lists
data = new_df.values.tolist()

close_chrome()
options = uc.ChromeOptions()
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Default')
# options.add_argument(f'--profile-directory=Profile 1')
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

    delete_images_from_folder(r"Files")  # clear folder
    images_urls = single_product[6].split(',')
    upload_images(images_urls)  # download/upload images
    delete_images_from_folder(r"Files")  # clear folder

    # Title

    title_of_product = "FLASH SALE🎉 " + str(single_product[1])
    pyperclip.copy(title_of_product)
    # find_element_send_text('//input[@name="title"]', title_of_product)
    driver.find_element(By.XPATH, '//input[@name="title"]').clear()
    driver.find_element(By.XPATH, '//input[@name="title"]').send_keys(Keys.CONTROL, 'v')
    # Description
    try:
        description_text = str(single_product[3]).lower().split('|')[0]
        # remove last line if it starts with 'Machine washable'
        if description_text.split('\n')[-1].startswith('machine washable'):
            description_text = '\n'.join(description_text.split('\n')[:-1])
    except:
        description_text = str(single_product[3]).lower()
        if description_text.split('\n')[-1].startswith('machine washable'):
            description_text = '\n'.join(description_text.split('\n')[:-1])



    description_text = description_text.replace('jd exclusive', '')

    # remove any special characters from description
    description_text = re.sub(r"[^a-zA-Z0-9]+", ' ', description_text)





    description_text = description_text.strip().title()




    description_text = "First class next day tracked shipping + delivery 🚚 " + description_text
    write_description(description_text)

    # Color
    color_of_product = str(single_product[8]).strip().title()
    change_color(color_of_product)

    # Size
    size_of_product = str(single_product[7]).strip().upper()
    change_size(size_of_product)


    # Price
    price = round(float(single_product[4]) * 1.1, 2) - 0.01
    driver.find_element(By.XPATH, '//input[@name="price"]').clear()
    find_element_send_text('//input[@name="price"]', str(price))

    #

    # Promoted Listings
    specific_clicker('//*[@aria-label="Promoted Listings Standard"]')

    time.sleep(1)
    specific_clicker('//button[@aria-label="Save for later"]')

    with open('already_done.txt', 'a', encoding='utf-8') as f:
        f.write(str(single_product[0]) + '\n')


    input("add: ")
