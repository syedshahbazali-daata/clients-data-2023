import os
import pickle

import undetected_chromedriver as uc
from selenium import webdriver
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


def login_account(username, password):
    global driver
    # change language to english
    options = uc.ChromeOptions()
    options.add_argument("--lang=en")

    driver = uc.Chrome()  # open chrome driver
    driver.maximize_window()
    driver_go('https://accounts.spotify.com/en/login')
    find_element_send_text('(//input[@placeholder])[1]', username)
    find_element_send_text('(//input[@placeholder])[2]', password)
    old_url = str(driver.current_url)
    specific_clicker('(//button[@id])[1]')
    while True:
        check_username = []
        current_url = str(driver.current_url)
        if current_url != old_url:
            time.sleep(4)
            break
        else:
            try:
                driver.find_element(By.XPATH, "//span[text()='Incorrect username or password.']")
                print("Incorrect username or password.")
                driver.quit()
                check_username.append(0)
            except Exception as e:
                pass
            if len(check_username) > 0:
                raise Exception("Incorrect username or password.")
    driver_go('https://open.spotify.com/')
    cookies = driver.get_cookies()
    # pkl file to save the cookies
    with open(f'Accounts FIles/{username}.pkl', 'wb') as f:
        pickle.dump(cookies, f)
    driver.quit()



