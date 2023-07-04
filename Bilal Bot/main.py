import datetime
import random

import undetected_chromedriver as uc
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

print(datetime.datetime.now())


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
            # print(e)
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
            # print(e)
            pass


def update_data(file, data):
    with open(file, "a") as f:
        f.write(f"{data}\n")


# //header/button[@aria-expanded="false"]
data = pd.read_csv("product_data.csv")
# sort table by column named "date" and "time" in ascending order
data.sort_values(by=["date", "time"], inplace=True, ascending=True)
total = len(data["url"].values)

options = uc.ChromeOptions()
options.add_argument("--headless")

driver = uc.Chrome(options=options, use_subprocess=True)

point = 0
while True:
    if point >= total:
        break

    for index, single_data in enumerate(data["url"].values):
        current_date = str(datetime.datetime.now()).split(" ")[0]
        current_time = str(datetime.datetime.now()).split(" ")[1][:5]
        my_date = current_date
        my_time = str(data["time"][index])
        already_done = get_file_data("Already Done.txt")
        email = str(data["email"][index])
        check = f"{email} {my_date} {my_time}"
        quantity = int(str(data["quantity"][index]))


        if my_date != current_date:
            continue

        print(f"Current Time: {current_time} | My Time: {my_time} | Current Date: {current_date} | My Date: {my_date}")

        if current_time == my_time and check not in already_done and current_date == my_date:

            driver_go(data["url"][index])  # open the product page
            print("Go to web page")
            for i in range(10):
                specific_clicker_pass('//a[@aria-label="dismiss cookie message"]')  # dismiss the cookie message
                time.sleep(0.3)

            for i in range(quantity - 1):
                specific_clicker('//quantity-input/button[2]')  # click on the plus button
                print("quantity increased")

            specific_clicker('//button[@data-testid="Checkout-button"]')  # click on the checkout button

            while True:
                try:
                    driver.find_element(By.XPATH, '//input[@placeholder="E-Mail"]')
                    break
                except Exception as e:
                    specific_clicker_pass('//button[@data-testid="Checkout-button"]')  # click on the checkout button
                    time.sleep(2)

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
            point += 1
            print(f"Done {point} of {total}")

        else:
            time.sleep(1)

