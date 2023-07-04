import requests
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options to open the developer tools
chrome_options = Options()
chrome_options.add_argument("--auto-open-devtools-for-tabs")


# Set up the Chrome driver

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


driver = webdriver.Chrome(options=chrome_options)
driver.get('https://ais.usvisa-info.com/en-ae/niv/users/sign_in')
driver.maximize_window()


def login(email, pwd):
    find_element_send_text('//*[@id="user_email"]', email)
    time.sleep(1)
    find_element_send_text('//*[@id="user_password"]', pwd)
    time.sleep(1)
    specific_clicker('//*[@id="policy_confirmed"]')
    current_url = str(driver.current_url)
    specific_clicker('//*[@value="Sign In"]')
    while True:
        if current_url != str(driver.current_url):

            break
        else:
            print("waiting for LOGIN")
            time.sleep(1)


def get_applicants_data():
    applicants_data = {}

    applicants_card = driver.find_elements(By.XPATH, "//div[contains(@class, 'application')]")
    if len(applicants_card) == 0:
        return None
    for applicant_card_no in range(1, len(applicants_card) + 1):
        xpath = f"(//div[contains(@class, 'application')])[{applicant_card_no}]"
        passport_id = str(driver.find_element(By.XPATH, xpath + "//tbody//td[2]").text)
        applicant_link = str(
            driver.find_element(By.XPATH, xpath + "//a[text()='Continue']").get_attribute('href')).replace(
            "continue_actions", "appointment")
        applicants_data[passport_id] = applicant_link

    return applicants_data

def get_appointments_data(applicant_url, cookies_):
    url = f"{applicant_url}/days/49.json"

    querystring = {"appointments^\\[expedite^\\]":"false"}

    payload = ""
    headers = {

        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": f"{cookies_}",
        "If-None-Match": "W/^\^cd68d9a2b5c306e5fa0eadf994eb8154^^",
        "Referer": "https://ais.usvisa-info.com/en-ae/niv/schedule/49718829/appointment",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-CSRF-Token": "BgTdyPY+9EL4kTNUYOUI/uru2SdSb7Hwm/RUIX4XgMzntg/7vJtJAy3N+GjYbFQfGezbpcCNSHh3szA2pPnFEA==",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "^\^Not.A/Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^114^^, ^\^Google",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    try:
        response_data = response.json()
    except:
        response_data = response.text
    return response_data

# STEP 1: LOGIN TO THE WEBSITE
login("Comandodelgolfojomalonper@gmail.com", "Jose141218.")

# STEP 2: GET THE LIST OF ALL THE APPOINTMENTS
page_no = 1
all_applicants_data = {}
page_url = str(driver.current_url)
while True:
    print(f"Searched page no: {page_no}")

    driver.get(page_url + f"?page={page_no}")
    time.sleep(2)
    applicants_d = get_applicants_data()
    if applicants_d is None:
        break
    else:
        all_applicants_data.update(applicants_d)

    page_no += 1

# STEP 3: GET THE APPOINTMENT DATA FOR EACH APPLICANT
applicant_url_x = all_applicants_data['RD5898910']
driver.get(applicant_url_x)
time.sleep(2)
# Retrieve the network requests
cookies_data = driver.get_cookies()
cookies_string = ""
for i in cookies_data:
    cookies_string += i["name"] + "=" + i["value"] + "; "

appointments_dates = get_appointments_data(applicant_url_x, cookies_string)
appointments_dates_data = [x.get('date', '') for x in appointments_dates]
