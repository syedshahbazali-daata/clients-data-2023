import os
import time, csv
from datetime import datetime

import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

csv_file_name = f"Senior Software Engineer Denver"


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


def main(job_title, location, csv_file_name):
    close_chrome()
    options = uc.ChromeOptions()
    #path = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"
    # using os
    path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
    options.add_argument(fr"user-data-dir={path}")
    options.add_argument(f'--profile-directory=Default')
    global driver
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}&refresh=true"

    driver.get(url)
    time.sleep(6)

    page_num = 1
    while True:

        # # pyautogui hotkey
        # pyautogui.moveTo(100, 100)
        # pyautogui.click()
        # for i in range(10):
        #     pyautogui.hotkey('ctrl', '-')
        #     time.sleep(0.4)

        try:
            driver.find_element(By.XPATH, "//*[text()='No matching jobs found.']")
            print("No matching jobs found.")
            break
        except:
            pass

        job_per_page = driver.find_elements(By.XPATH, "//div[@data-job-id]")
        print(f"Page {page_num} has {len(job_per_page)} jobs")

        records = []
        for job_index in range(len(job_per_page)):
            job_title = driver.find_element(By.XPATH, f'((//div[@data-job-id])[{job_index + 1}]//a[text()])').text
            job_linkedIn_url = driver.find_element(By.XPATH,
                                                   f'((//div[@data-job-id])[{job_index + 1}]//a[text()])').get_attribute(
                'href')

            record = [job_title, str(job_linkedIn_url)]

            records.append(record)

        for index, single_record in enumerate(records):
            time.sleep(4)
            driver.get(single_record[1])
            time.sleep(4)

            found = False
            for i in range(10):
                try:
                    driver.find_element(By.XPATH, '//*[@class="jobs-company__box"]')
                    found = True
                    break
                except:
                    time.sleep(1)

            try:
                company_title_2 = driver.find_element(By.XPATH, '//h1').text
            except:
                company_title_2 = ''

            if not found:
                print("No company info found")
                continue

            company_name = driver.find_element(By.XPATH, '(//*[@class="jobs-company__box"]//a)[2]').text
            company_about_url = driver.find_element(By.XPATH, '(//*[@class="jobs-company__box"]//a)[2]').get_attribute(
                'href')
            driver.get(company_about_url)
            time.sleep(4)

            found = False

            for i in range(10):
                try:
                    driver.find_element(By.XPATH,
                                        "//button[contains(@class, 'follow')]//following-sibling::a").get_attribute(
                        'href')

                    found = True
                    break
                except:

                    time.sleep(1)

            if not found:
                company_website = ''
            else:
                company_website = driver.find_element(By.XPATH,
                                                      "//button[contains(@class, 'follow')]//following-sibling::a").get_attribute(
                    'href')

            row = [company_title_2, company_name, company_website]

            with open(f'LinkedIn CSV/{csv_file_name}.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(row)

            print(f"Scraped {index + 1} out of {len(records)} jobs on page {page_num}")
            time.sleep(7)

        page_num += 1
        url = f"{url}&start={page_num * 25}"
        driver.get(url)
        time.sleep(10)

    driver.quit()


########################################################################################################################


if __name__ == '__main__':
    queries = get_file_data('query.txt')
    for query in queries:
        job_title, location = query.split(':')

        main(job_title, location, csv_file_name)
