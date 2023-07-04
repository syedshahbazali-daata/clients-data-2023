import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
import os
import pyperclip

category_url = "https://www.revolico.com/search?category=vivienda&subcategory=compra-venta"  # Category URL
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


# switch to the 1st tab
ads_urls = []
category_urls = ['https://www.revolico.com/search?category=vivienda&subcategory=alquiler-a-cubanos|3',
                 'https://www.revolico.com/search?category=vivienda&subcategory=alquiler-a-extranjeros|7',
                 'https://www.revolico.com/search?category=vivienda&subcategory=casa-en-la-playa|3',
                 'https://www.revolico.com/search?category=vivienda&subcategory=permuta|6']

for single_category_url in category_urls:
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    single_category_url_x = single_category_url.split('|')[0]


    driver.get(single_category_url_x)  # open category url
    category_code = single_category_url.split('|')[1]


    # open new tab

    time.sleep(2)

    ads_urls_x = [f'{i.get_attribute("href")}|{category_code}' for i in
                  driver.find_elements(By.XPATH, '//main//li[@data-cy="adRow"]/a[@href]')]
    ads_urls.extend(ads_urls_x)
    driver.quit()

random.shuffle(ads_urls)
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()

driver.get('https://kbocuba.com/users/member_login')
# switch to the new tab
find_element_send_text('(//div[@class="main_login_form"]//input[@id="login_email"])[2]', email_of_user)
find_element_send_text('(//div[@class="main_login_form"]//input[@id="login_password"])[2]', password_of_user)
specific_clicker('(//input[@type="submit"])[2]')
time.sleep(2)

# switch Language to English
driver.get("https://kbocuba.com/home/do_language/eng")

for  ad_url in ads_urls:
    already_done = get_file_data("Already Done.txt")
    ad_url = ad_url.split('|')[0]
    category_code = ad_url.split('|')[1]
    if ad_url in already_done:
        print("This Ad is already Added")
        continue

    print(ad_url)
    try:
        driver.get(ad_url)  # open ad url


    except:
        print("Ad Opened Error")
        continue
    print("Ad Opened")

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
    driver.get("https://kbocuba.com/properties/create/1")
    # specific_clicker('//div[@class="classified_button"]')

    while True:
        try:
            driver.find_element(By.XPATH,
                                f"//select[@name='data[category_select_id]']/option[@value='{category_code}']")
            break
        except:
            time.sleep(1)

    title_of_ad = title_of_ad.replace("auto", "")
    find_element_send_text('//input[@id="name"]', title_of_ad)
    find_element_send_text('//input[@id="location"]', location_of_ad)
    find_element_send_text('//input[@id="price"]', "0.00")

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

    # description_of_ad
    pyperclip.copy(description_of_ad)
    iframe = driver.find_element(By.XPATH, '//iframe[@id="editor_ifr"]')
    driver.switch_to.frame(iframe)
    time.sleep(1)
    driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL, 'v')
    driver.switch_to.default_content()

    while True:
        try:
            driver.find_element(By.XPATH, '//input[@name="data[expire_until]"]').click()
            specific_clicker('//div[@data-nav="1"]')
            break
        except:
            pass
    # current day 02
    import datetime

    current_day = datetime.datetime.now().strftime("%d")
    current_day = int(current_day)
    print(current_day)

    specific_clicker(f'//td/div[@data-pick and text()="{current_day}"]')
    time.sleep(2)
    driver.find_element(By.XPATH, '//input[@name="data[expire_until_time]"]').click()
    specific_clicker('//li[@aria-label="0:30"]')

    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    specific_clicker("//button[text()='Save']")
    time.sleep(16)

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
