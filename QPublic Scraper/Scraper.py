########################################################################################################################
# Functions

def check_libraries_exist(libraries: list):
    import importlib
    for library in libraries:
        try:
            importlib.import_module(library)

        except:
            print(f"ERROR: {library} is not installed. Please install it and try again.")
            # install library
            import subprocess
            subprocess.check_call(["python", '-m', 'pip', 'install', library])

            exit()


check_libraries_exist(["undetected_chromedriver"])
import time, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


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


def get_text_pass(ele):
    try:
        element_text = driver.find_element(By.XPATH, ele).text


    except Exception as e:
        element_text = "N/A"
    return element_text


def get_year_data(year_no):
    try:
        x = str(driver.find_elements(By.XPATH, f"//*[text()='{year_no}']/ancestor::tr")[-1].text).split(" ")[-1]
    except:
        x = "N/A"
    return x


def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()
url = f"https://qpublic.schneidercorp.com/Application.aspx?AppID=1045&LayerID=23342&PageTypeID=4&PageID=9746&KeyValue=320010430000#ctlBodyPane_ctl10_lblName"

print("NOTE: This program will work with the latest version of Chrome only.")

driver.get(url)
time.sleep(2)
for i in range(5):
    specific_clicker2("//*[text()='Agree']")
    time.sleep(0.5)
# zoom in 150%
# driver.execute_script("document.body.style.zoom='150%'")
while True:
    specific_clicker('//a[@title="View next record"]')
    print(driver.current_url)
    for i in range(5):
        try:
            driver.find_element(By.XPATH, '//*[@title="toggle additional data"]')
            break
        except:
            time.sleep(1)
    specific_clicker2('//*[@title="toggle additional data"]')

    location_address = get_text_pass("//*[text()='Location Address']/../../td/*")
    property_class = get_text_pass("//*[text()='Property Class']/../../td/*")
    land_area = get_text_pass("//*[text()='Land Area (approximate sq ft)']/../../td/*")
    try:
        owner_names = str(driver.find_element(By.XPATH, "//*[text()='Owner Names']/../../span").text).split("\n")[1:]
        owner_names = ", ".join(owner_names)
    except:
        owner_names = "N/A"

    assessed_building_value = get_text_pass("//*[text()='Net Taxable Land Value:']/../*[2]")
    assessed_land_value = get_text_pass("//*[text()='Net Taxable Building Value:']/../*[2]")
    total_property_exemption = get_text_pass("//*[text()='Total Property Exemption:']/../*[2]")
    year_2022_amount_due = get_year_data("2022")
    year_2021_amount_due = get_year_data("2021")
    year_2020_amount_due = get_year_data("2020")

    record = [
        location_address,
        property_class,
        land_area,
        owner_names,
        assessed_building_value,
        assessed_land_value,
        total_property_exemption,
        year_2022_amount_due,
        year_2021_amount_due,
        year_2020_amount_due]

    print(location_address)
    with open("data.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(record)
