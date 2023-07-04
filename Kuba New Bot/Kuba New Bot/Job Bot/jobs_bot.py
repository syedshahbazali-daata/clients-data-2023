import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
import os
import pyperclip

category_url = "https://www.revolico.com/search?category=empleos&subcategory=ofertas-de-empleo"  # Category URL
email_of_user = "cuentapropista.k@gmail.com"  # Email of the user
password_of_user = "@Muhammad@1"  # Password of the user
category_no = 2  # Category number
brand_name = "Cuba"  # Brand name


########################################################################################################################
# Functions
########################################################################################################################

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


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()

# open new tab


driver.get('https://kbocuba.com/users/member_login')

find_element_send_text('(//div[@class="main_login_form"]//input[@id="login_email"])[2]', email_of_user)
find_element_send_text('(//div[@class="main_login_form"]//input[@id="login_password"])[2]', password_of_user)
specific_clicker('(//input[@type="submit"])[2]')
time.sleep(2)

# switch Language to English
driver.get("https://kbocuba.com/home/do_language/eng")

# switch to the 1st tab

driver.get(category_url)
time.sleep(2)

while True:
    ads_urls = [i.get_attribute("href") for i in
                driver.find_elements(By.XPATH, '//main//li[@data-cy="adRow"]/a[@href]')]
    if len(ads_urls) > 0:
        break
    time.sleep(1)
for ad_url in ads_urls:
    driver.get(ad_url)  # open ad url
    time.sleep(3)

    # Scrape ad details

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    title_of_ad = str(driver.find_element(By.XPATH, '//h4').text)
    location_of_ad = str(driver.find_element(By.XPATH, '//div[@data-cy="adLocation"]').text)
    description_of_ad = str(driver.find_element(By.XPATH, '//div[@data-cy="adDescription"]').text)
    contact_details = driver.find_elements(By.XPATH, '//div[@data-cy="adName"]/../../div')
    contact_details = [str(i.text) for i in contact_details]
    contact_details = "\n".join(contact_details)
    description_of_ad = f"{description_of_ad}\n\n{contact_details}"

    # Upload ad data to the website

    driver.get("https://kbocuba.com/job/jobs/create/1")
    time.sleep(2)

    find_element_send_text('//input[@id="name"]', title_of_ad)
    find_element_send_text('//input[@id="location"]', location_of_ad)
    find_element_send_text('//input[@id="salary_per_hour"]', "10.00")
    find_element_send_text('//input[@name="data[number_of_vacancies]"]', "1")

    driver.find_element(By.XPATH, '//*[@name="data[job_level_id]"]//option[@value="6"]').click()
    driver.find_element(By.XPATH, '//*[@name="data[job_type_id]"]//option[@value="5"]').click()
    driver.find_element(By.XPATH, '//*[@name="data[industry][]"]//*[text()="Cuba Jobs"]').click()

    # find_element_send_text('//input[@name="data[valid_until]"]', '2023-03-25')
    # find_element_send_text('//input[@name="data[valid_until_time]"]', '17:30')


    # description_of_ad
    pyperclip.copy(description_of_ad)
    while True:
        try:
            iframe = driver.find_element(By.XPATH, '//iframe[@id="editor_ifr"]')
            break
        except:
            print("Waiting for iframe")
    driver.switch_to.frame(iframe)
    time.sleep(1)
    driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL, 'v')
    driver.switch_to.default_content()
    input("Press Enter to continue...")

    specific_clicker("//button[text()='Save']")
    time.sleep(2)

driver.quit()
