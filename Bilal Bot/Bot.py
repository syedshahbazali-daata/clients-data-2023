import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time
from selenium.webdriver.common.keys import Keys
from keepAlive import keep_alive
import gspread
from oauth2client.service_account import ServiceAccountCredentials
print(datetime.datetime.now())


########################################################################################################################
#                                                                                                                      #
#                                        PLEASE DON'T CHANGE ANYTHING BELOW                                            #
#                                                                                                                      #
########################################################################################################################

keep_alive()

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
    while True:
        try:

            webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

            break
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
            pass


def update_data(file, data):
    with open(file, "a") as f:
        f.write(f"{data}\n")


# //header/button[@aria-expanded="false"]
data = pd.read_csv("product_data.csv")
print(data["url"].values)

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)

while True:
    for index, single_data in enumerate(data["url"].values):
        current_date = str(datetime.datetime.now()).split(" ")[0]
        current_time = str(datetime.datetime.now()).split(" ")[1][:5]
        my_date = str(data["date"][index])
        my_time = str(data["time"][index])
        already_done = get_file_data("Already Done.txt")
        email = str(data["email"][index])
        check = f"{email} {my_date} {my_time}"
        if current_time == my_time and check not in already_done and current_date == my_date:
            driver_go(data["url"][index])  # open the product page
            specific_clicker_pass('//a[@aria-label="dismiss cookie message"]')  # dismiss the cookie message
            find_element_send_text('//input[@id="Quantity"]', '1')
            find_element_send_text('//input[@id="Quantity"]', '1')

            specific_clicker('//button[@data-testid="Checkout-button"]')  # click on the checkout button

            for i in range(3):
                specific_clicker_pass('//button[@data-testid="Checkout-button"]')  # click on the checkout button
                time.sleep(1)


            # fill the checkout form
            first_name = str(data["first name"][index])
            last_name = str(data["last name"][index])
            company_name = str(data["company name"][index])
            street_address = str(data['street address'][index])
            other_address = str(data['other address'][index])
            city = str(data['city'][index])
            postal_code = str(data['postal code'][index])
            phone_number = str(data['phone number'][index])

            find_element_send_text('//input[@placeholder="E-Mail"]', email)
            find_element_send_text('//input[@placeholder="Vorname (optional)"]', first_name)
            find_element_send_text('//input[@placeholder="Nachname"]', last_name)
            find_element_send_text('//input[@placeholder="Firma (optional)"]', company_name)
            find_element_send_text('//input[@placeholder="Adresse" or @placeholder="Straße und Hausnummer"]',
                                   street_address)
            find_element_send_text(
                '//input[@placeholder="Wohnung, Zimmer, usw. (optional)" or @placeholder="Zusätzliche Adressangaben (optional)"]',
                other_address)
            find_element_send_text('//input[@placeholder="Stadt"]', city)
            find_element_send_text('//input[@placeholder="Postleitzahl"]', postal_code)
            find_element_send_text('//input[@placeholder="Telefon (optional)"]', phone_number)
            specific_clicker("//span[text()='Weiter zum Versand']/..")
            specific_clicker("//span[text()='Weiter zur Zahlung']/..")
            specific_clicker("//span[text()='Kaufen']/..")
            time.sleep(15)
            update_data("Already Done.txt", check)

            driver.delete_all_cookies()
            print(my_date, my_time)
