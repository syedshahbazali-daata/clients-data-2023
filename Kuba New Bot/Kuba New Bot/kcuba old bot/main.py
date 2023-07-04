import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
import os
import pyperclip

category_url = "https://www.revolico.com/vivienda"  # Category URL
email_of_user = "cuentapropista.k@gmail.com"  # Email of the user
password_of_user = "@Muhammad@1"  # Password of the user
category_no = 10  # Category number
brand_name = "Cuba"  # Brand name


########################################################################################################################
# Functions
########################################################################################################################
# all files from the folder
files = os.listdir("images")
# remove all files from the folder
for f in files:
    os.remove(os.path.join("images", f))

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



def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')
    return data


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()

driver.get(category_url)
# open new tab

driver.tab_new('https://kbocuba.com/users/member_login')
# switch to the new tab
driver.switch_to.window(driver.window_handles[1])
find_element_send_text('(//div[@class="main_login_form"]//input[@id="login_email"])[2]', email_of_user)
find_element_send_text('(//div[@class="main_login_form"]//input[@id="login_password"])[2]', password_of_user)
specific_clicker('(//input[@type="submit"])[2]')
time.sleep(2)

# switch Language to English
driver.get("https://kbocuba.com/home/do_language/eng")

# switch to the 1st tab
switch_tab(0)
time.sleep(2)

ads_urls = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, '//main//li[@data-cy="adRow"]/a[@href]')]
for ad_url in ads_urls:
    already_done = get_file_data("Already Done.txt")
    if ad_url in already_done:
        print("This Ad is already Added")
        continue

    print(ad_url)
    try:
        driver.get(ad_url)  # open ad url
    except:
        continue

    time.sleep(1)

    # Scrape ad details

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    title_of_ad = str(driver.find_element(By.XPATH, '//h4').text)
    location_of_ad = str(driver.find_element(By.XPATH, '//div[@data-cy="adLocation"]').text)
    description_of_ad = str(driver.find_element(By.XPATH, '//div[@data-cy="adDescription"]').text)
    contact_details = driver.find_elements(By.XPATH, '//div[@data-cy="adName"]/../../div')
    contact_details = [str(i.text) for i in contact_details]
    contact_details = "\n".join(contact_details)
    description_of_ad = f"{description_of_ad}\n\n{contact_details}"

    ad_images = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, '//div[@data-cy="adPhoto"]/a')]
    print("total images", len(ad_images))

    # Download ad images
    for index_of_image, ad_image_url in enumerate(ad_images):
        # Send a GET request to the URL
        response = requests.get(ad_image_url)

        # Get the content of the response (i.e. the image data)
        image_data = response.content

        # Save the image to a file
        with open(f"images/ad_image_{index_of_image + 1}.jpg", "wb") as f:
            f.write(image_data)

        print(f"Image {index_of_image + 1} saved")

    # Upload ad data to the website
    # switch_tab(1)
    driver.get("https://kbocuba.com/classifieds/create/4")
    # specific_clicker('//div[@class="classified_button"]')

    find_element_send_text('//input[@id="name"]', title_of_ad)
    find_element_send_text('//input[@id="location"]', location_of_ad)
    find_element_send_text('//input[@id="price"]', "0.00")
    find_element_send_text('//input[@id="classified_brand_suggest"]', brand_name)

    while True:
        try:
            driver.find_element(By.XPATH, '(//input[@name="file"])[1]')
            break
        except Exception as e:
            print(e)

    # Upload images

    downloaded_images = os.listdir("images")
    if len(downloaded_images) > 0:
        driver.find_element(By.XPATH, '(//input[@name="file"])[1]').send_keys(
            os.getcwd() + f"\\images\\{downloaded_images[0]}")

    for single_image in downloaded_images:
        specific_clicker2('//div[@class="add_more"]')
        driver.find_element(By.XPATH, '(//input[@name="file"])[2]').send_keys(
            os.getcwd() + f"\\images\\{single_image}")

        specific_clicker('//a[@id="triggerUpload"]')

    # category
    driver.find_element(By.XPATH, f'(//select[@id="category_select_id"]//option)[{category_no + 1}]').click()

    # description_of_ad
    pyperclip.copy(description_of_ad)
    iframe = driver.find_element(By.XPATH, '//iframe[@id="editor_ifr"]')
    driver.switch_to.frame(iframe)
    time.sleep(1)
    driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL, 'v')
    driver.switch_to.default_content()

    specific_clicker("//button[text()='Save']")
    time.sleep(10)


    # all files from the folder
    files = os.listdir("images")
    # remove all files from the folder
    for f in files:
        os.remove(os.path.join("images", f))

    with open("Already Done.txt", "a") as already_done:
        already_done.write(f"{ad_url}\n")

    # Move to the item

    # switch_tab(0)
    # driver.delete_all_cookies()
    # driver.get(category_url)

driver.quit()
