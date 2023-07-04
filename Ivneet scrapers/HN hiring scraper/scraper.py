import os
import time, csv
from datetime import datetime
import os, re
import traceback
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
import pyperclip
import pandas as pd


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
            time.sleep(1)
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


def chat_gpt_response(raw_prompt: str) -> str:
    # enter prompt
    prompt = f"""{raw_prompt}\n\n
    
    I need the job title, company name, and company website in PSV format :
    note: if website not available add apply link otherwise NA
    and it should be in this format nothing else:
    JOB TITLE|COMPANY NAME|COMPANY WEBSITE
    
    answer must be in 1 line only

    """
    pyperclip.copy(prompt)
    while True:
        try:
            driver.find_element(By.XPATH, '//textarea')
            break
        except:
            time.sleep(2)

    driver.find_element(By.XPATH, '//textarea').send_keys(Keys.CONTROL, 'v')
    driver.find_element(By.XPATH, '//textarea').send_keys(Keys.ENTER)
    time.sleep(1)
    while True:
        try:
            btns = driver.find_elements(By.XPATH, '//textarea/..//button//span')
            print(len(btns))
            if len(btns) == 1:
                error = {"error": "error"}
                print(error["new"])

            time.sleep(2)
            # scroll down
            specific_clicker2("//main//button[contains(@class, 'cursor-pointer')]")
            print("scrolling down")
        except:
            print("response received")
            time.sleep(2)
            try:
                response_x = driver.find_elements(By.XPATH, '//div/p/..')[-1].text
                print(response_x)
                if response_x not in already_done:
                    already_done.append(response_x)
                    return response_x
                else:
                    print("response already done")
                    adjust_chat_gpt()
                    return chat_gpt_response(raw_prompt)
            except:
                adjust_chat_gpt()
                return chat_gpt_response(raw_prompt)


def list_in_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def adjust_chat_gpt():
    # adjust ChatGpt
    url = f"http://chat.openai.com/"
    driver.get(url)

    time.sleep(5)


close_chrome()
already_done = []
options = uc.ChromeOptions()
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Profile 1')
driver = uc.Chrome(options=options)
driver.maximize_window()

main_urls = get_file_data("query.txt")
for single_main_url in main_urls:
    already_done_file = get_file_data("already_done.txt")
    if single_main_url in already_done_file and single_main_url != "":
        continue
    driver.get(single_main_url)
    time.sleep(3)
    # scroll bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    all_jobs_description = driver.find_elements(By.XPATH, '//ul[@class="jobs"]/li//div[@class="body"]')
    all_jobs_description = [str(x.text).strip().replace("\n", " ") for x in all_jobs_description]
    all_jobs_description = [x for x in all_jobs_description if x != ""]

    print(len(all_jobs_description))
    print(all_jobs_description)

    adjust_chat_gpt()
    with open("responses.txt", "w", encoding="utf-8") as f:
        f.write("JOB TITLE|COMPANY NAME|COMPANY WEBSITE\n")

    for job_index, single_job in enumerate(all_jobs_description):
        print(f"job index: {job_index + 1} out of {len(all_jobs_description)}")
        response = chat_gpt_response(single_job)

        with open("responses.txt", "a", encoding="utf-8") as f:
            f.write(response + "\n")

    with open("already_done.txt", "a", encoding="utf-8") as f:
        f.write(single_main_url + "\n")

driver.quit()

data = get_file_data('responses.txt')
headers = data[0]
body = data[1:]

# body is a list of strings, each string is a row and cells are separated by pipes |

df = pd.DataFrame([x.split('|') for x in body], columns=headers.split('|'))
df.to_csv('result.csv', index=False)
