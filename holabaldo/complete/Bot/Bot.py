import os
import time, csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import mysql.connector
import random


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


def data_scraper(search_term):
    url = ""
    driver.get(url)
    time.sleep(1)

    specific_clicker("//button[@class='btn btn-primary']")
    time.sleep(1)
    data = []
    for i in range(1, 100):
        try:
            data.append(get_text(f"//div[@class='col-md-12']//div[{i}]//div[@class='card-body']//h5"))
        except:
            break
    return data


def download_image(image_url, folder_path):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Send a GET request to the URL
    response = requests.get(image_url)

    if response.status_code == 200:
        # Extract the file name from the URL
        file_name = "image-" + str(random.randint(1, 10040)) + str(random.randint(1, 10400)) + ".png"

        # Determine the file path to save the image
        file_path = os.path.join(folder_path, file_name)

        # Save the image to the specified file path
        with open(file_path, "wb") as file:
            file.write(response.content)

        print("Image downloaded successfully!")
    else:
        print("Failed to download the image.")


def upload_image(btn_no, image_paths):
    specific_clicker(f"(//button[@data-caption])[{btn_no}]")
    specific_clicker('/html/body/div[30]/div[1]/div/div/div[3]/div[1]/div/button[1]')
    for image_path in image_paths:
        driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(image_path)
    specific_clicker('/html/body/div[30]/div[1]/div/div/div[4]/div/div[2]/button')


connection = mysql.connector.connect(
    user='baldo',
    password='AVNS_31sHK4CCPIr6p4Ifgzd',
    host='db-mysql-nyc1-47136-do-user-12226124-0.b.db.ondigitalocean.com',
    port=25060,
    database='Baldo',

)

cursor = connection.cursor()

listings = cursor.execute("select * from listings join URL_extra_data on listings.url = URL_extra_data.url")
listings = cursor.fetchall()
data = []
for single_list in listings:
    data.append(list(single_list))

# Database is Connected Successfully
print("Database is connected successfully")


# functions for adding new listings

def upload_image(btn_no, image_paths):
    specific_clicker(f"(//button[@data-caption])[{btn_no}]")
    print(image_paths)
    time.sleep(4)

    for image_path in image_paths:
        print(image_path)
        while True:
            try:
                driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(fr"{image_path}")
                break
            except Exception as e:
                print(e)
                time.sleep(1)
    time.sleep(5)
    specific_clicker(
        "//div[@class='supports-drag-drop' and not(@aria-hidden)]//button[text()='Seleccionar' and not(@disabled)]")


def fill_product_page(title, description, price, o_culture_x, o_academia_x, plusvalia_pros_contras_x,
                      plusvalia_comentarios_x, plusvalia_5anios_num_x):
    find_element_send_text('//input[@name="post_title"]', title)  # title
    while True:
        try:
            driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@id="content_ifr"]'))
            driver.find_element(By.XPATH, '//body').send_keys(description)  # description
            driver.switch_to.default_content()
            break
        except:
            time.sleep(0.1)

    specific_clicker('//*[@data-tab="#basic-facts"]')
    find_element_send_text('//input[@id="es-field-price"]', price)
    find_element_send_text('//input[@id="es-field-plusvalia"]', plusvalia_5anios_num_x)

    # bedrooms
    bedrooms = random.randint(1, 5)
    find_element_send_text('//input[@id="es-field-bedrooms"]', f"{bedrooms}")
    # bathrooms
    bathrooms = random.randint(1, 2)
    find_element_send_text('//input[@id="es-field-bathrooms"]', f"{bathrooms}")

    find_element_send_text('//*[@id="es-field-oferta-cultural"]', o_culture_x)
    find_element_send_text('//*[@id="es-field-oferta-academica"]', o_academia_x)
    pros_cons = plusvalia_pros_contras_x + "\n" + plusvalia_comentarios_x
    find_element_send_text('//*[@id="es-field-ventajas-y-desventajas"]', pros_cons)


def upload_product_images():
    specific_clicker('//*[@data-tab="#media"]')
    current_dir = os.getcwd() + "\\Files"
    main_image = current_dir + "\\image.png"

    upload_image("1", [main_image])

    list_of_images = os.listdir(current_dir)
    list_of_images.remove("image.png")
    upload_image("2", [current_dir + "\\" + image_x for image_x in list_of_images])
    time.sleep(4)


def download_image(image_url, folder_path, file_name):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Send a GET request to the URL
    response = requests.get(image_url)

    if response.status_code == 200:
        # Extract the file name from the URL

        # Determine the file path to save the image
        file_path = os.path.join(folder_path, file_name)

        # Save the image to the specified file path
        with open(file_path, "wb") as file:
            file.write(response.content)

        print("Image downloaded successfully!")
    else:
        print("Failed to download the image.")


close_chrome()
options = uc.ChromeOptions()
# path = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"
# using os
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Default')
driver = uc.Chrome(options=options)
driver.maximize_window()
driver.get("https://holabaldo.com/wp-login.php?wp_lang=en_US")
input("PLEASE LOGIN AND PRESS ENTER: ")

for index, single_product_record in enumerate(data):
    print(f"Working on {index + 1} out of {len(data)}")
    driver.get("https://holabaldo.com/wp-admin/post-new.php?post_type=properties")
    url_of_product = single_product_record[0]
    already_uploaded = get_file_data('Already Done')

    if url_of_product in already_uploaded:
        continue

    try:
        title_of_product = single_product_record[1]
        price_of_product = single_product_record[2]
        description_of_product = single_product_record[3]
        features_of_product = single_product_record[4]
        address_of_product = single_product_record[5]
        images_of_product = str(single_product_record[8]).split(",")

        o_culture = single_product_record[10]
        o_academia = single_product_record[11]
        plusvalia_pros_contras = single_product_record[12]
        plusvalia_comentarios = single_product_record[13]
        plusvalia_5anios_num = single_product_record[14]
    except:
        print("Error in data")
        continue

    try:
        download_image(images_of_product[0], "Files", "image.png")
    except:
        pass
    for image in images_of_product:
        file_name_x = "image-" + str(random.randint(1, 10040)) + str(random.randint(1, 10400)) + ".png"
        download_image(image, "Files", file_name_x)

    # fill data on basic page
    fill_product_page(title_of_product, description_of_product, price_of_product, o_culture, o_academia,
                      plusvalia_pros_contras, plusvalia_comentarios, plusvalia_5anios_num)

    # fill location data
    specific_clicker('//*[@data-tab="#location"]')
    find_element_send_text('//*[@id="es-field-address"]', address_of_product)

    # upload images
    upload_product_images()

    # delete all images in Files folder
    for file in os.listdir("Files"):
        os.remove("Files\\" + file)


    time.sleep(2)
    specific_clicker('//input[@value="Post"]')

    with open("Already Done", "a") as f:
        f.write(url_of_product + "\n")

driver.quit()