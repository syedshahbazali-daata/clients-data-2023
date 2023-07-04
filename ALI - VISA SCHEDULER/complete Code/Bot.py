import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta


# GOOGLE SHEET CONNECTION:
import gspread  # pip install oauth2client, pandas, flask,selenium
from oauth2client.service_account import ServiceAccountCredentials  # pip install oauth2client
import time
import json

with open('conf.json') as f:
    conf = json.load(f)

EMAIL = conf['email']
PASSWORD = conf['password']
SHEET_URL = conf['sheet_url']

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
sheet_url = 'https://docs.google.com/spreadsheets/d/1vWg0vVSvViDir9SalDyCLYNaXI3XOhVWHX4xRC9rl1w/edit?usp=sharing'

creds_sheet = ServiceAccountCredentials.from_json_keyfile_name(
    r"GoogleSheetsApi.json", scope)
client = gspread.authorize(creds_sheet)
sheet = client.open_by_url(sheet_url).worksheet('Sheet1')
print("Google Sheets API Connected")

def get_all_data():
    while True:
        try:
            data = sheet.get_all_values()[1:]
            return data
        except:
            print("Error in updating cell")
            time.sleep(10)
            continue





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

    #print(response_data)
    return response_data

def select_available_datetime(datetime_x):
    # execute a script to change input value
    driver.execute_script(f"document.getElementById('appointments_consulate_appointment_date').value = '{datetime_x}'")

    specific_clicker('//input[@id="appointments_consulate_appointment_date"]')
    while True:
        try:
            driver.find_element(By.XPATH, '//a[@class="ui-state-default ui-state-active"]')
            specific_clicker('//a[@class="ui-state-default ui-state-active"]')
        except:
            break
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//select[@id="appointments_consulate_appointment_time"]/option[@value]').click()
    except:
        return False

    return True

def range_of_dates(starting_date, ending_date):
    starting_date = datetime.strptime(starting_date, "%Y-%m-%d")
    ending_date = datetime.strptime(ending_date, "%Y-%m-%d")
    dates = []
    while starting_date <= ending_date:
        dates.append(starting_date.strftime("%Y-%m-%d"))
        starting_date += timedelta(days=1)
    return dates


# STEP 1: LOGIN TO THE WEBSITE
login(EMAIL, PASSWORD)

# STEP 2: GET THE LIST OF ALL THE APPOINTMENTS
page_no = 1
all_applicants_data = {}
page_url = str(driver.current_url)
while True:
    # print(f"Searched page no: {page_no}")

    driver.get(page_url + f"?page={page_no}")
    time.sleep(2)
    applicants_d = get_applicants_data()
    if applicants_d is None:
        break
    else:
        all_applicants_data.update(applicants_d)

    page_no += 1


# STEP 3: GET THE APPOINTMENT DATA FOR EACH APPLICANT
while True:
    print("Getting appointment data for each applicant")
    complete_data_from_sheet = get_all_data()
    list_of_applicants_ids = [x[0] for x in complete_data_from_sheet]
    list_of_applicants_initial_dates = [x[1] for x in complete_data_from_sheet]
    list_of_applicants_final_dates = [x[2] for x in complete_data_from_sheet]
    list_of_applicants_required_dates = [range_of_dates(x[1], x[2]) for x in complete_data_from_sheet]


    already_done = get_file_data("already_done.txt")
    for index, single_passport_id in enumerate(list_of_applicants_ids):
        try:
            applicant_url_x = all_applicants_data[single_passport_id]
        except:
            continue

        if single_passport_id in already_done:
            continue
        driver.get(applicant_url_x)
        # scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # Retrieve the network requests
        cookies_data = driver.get_cookies()
        cookies_string = ""
        for i in cookies_data:
            cookies_string += i["name"] + "=" + i["value"] + "; "

        applicant_required_dates = list_of_applicants_required_dates[index]

        appointments_dates = get_appointments_data(applicant_url_x, cookies_string)

        try:
            appointments_dates_data = [x.get('date', '') for x in appointments_dates]
            print("Appointments found: " + str(len(appointments_dates_data)))
        except:
            print("No appointments found for " + single_passport_id)
            print(appointments_dates)
            continue

        for single_required_date in applicant_required_dates:
            log_message = f"""Client Passport ID: {single_passport_id} | Date: {single_required_date} | Status: CHECKING"""
            try:
                appointments_dates_data.index(single_required_date)
                select_available_datetime(single_required_date)
                time.sleep(3)
                # APPLY FOR THE APPOINTMENT
                specific_clicker('//*[@value="Reschedule"]')
                time.sleep(2)
                specific_clicker("//*[text()='Confirm']")
                time.sleep(10)

                # save the passport id in the file
                with open("already_done.txt", "a") as f:
                    f.write(single_passport_id + "\n")

                print("APPOINTMENT BOOKED at " + single_required_date + " for " + single_passport_id)
            except:
                print("No appointments found for " + single_passport_id + " at " + single_required_date)
                continue

    print("Sleeping for 5 minutes")
    time.sleep(260)

