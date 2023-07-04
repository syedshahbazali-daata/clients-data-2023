import os
import time, csv
from datetime import datetime
import os, re
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
import pyperclip
import pandas as pd

zip_codes_df = pd.read_csv('zip_code_database_small_business.csv')


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
    -> -> I need data in CSV format with following fields:
    NAME|DATE_OF_BIRTH|ADDRESS|CITY|STATE|COUNTRY|ZIPCODE|EMAIL|ZIP_CODE_CITY

    ZIP_CODE_CITY: find city on the base of zip_code and put in to this field or put N/A
    DATE_OF_BIRTH: put in MM/DD/YYYY format or put N/A
    NOTE: Try to find FirstName and LastName to join them and put in NAME field. If you can't find then just put NAME in NAME field.
    If any field is not available Put N/A in that field. Example and don't add headers in it:
    Micheal|7/18/1983|123 Main Street|New York|NY|USA|10001|michael@yahoo.com|New York
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
    while True:
        try:
            driver.find_element(By.XPATH, '//textarea/..//button//span')
            time.sleep(2)
            # scroll down
            specific_clicker2("//main//button[contains(@class, 'cursor-pointer')]")
            print("scrolling down")
        except:
            print("response received")
            time.sleep(2)
            try:
                response_x = driver.find_elements(By.XPATH, '//div/p/..')[-1].text
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

    # select gpt 3.5
    # time.sleep(3)
    # specific_clicker('(//main//button)[1]')
    # time.sleep(1)
    # while True:
    #     try:
    #         driver.find_element(By.XPATH, "//li//span[text()='Legacy (GPT-3.5)']")
    #         break
    #     except:
    #         time.sleep(2)
    #         specific_clicker('(//main//button)[1]')
    #         time.sleep(1)
    #
    # specific_clicker("//li//span[text()='Legacy (GPT-3.5)']")
    time.sleep(5)


def update_text_file_na(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read().strip().replace(';N/A', '').replace('; N/A', '')

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)


# functions for fixing
import random


def add_row_into_txt(file, row_text):
    if len(str(row_text).strip()) < 5:
        return
    # if row_text is start with space then remove it
    if row_text[0] == ' ':
        return
    if row_text[0] == ' ;':
        return

    row_text = row_text.replace(';;', ';')

    with open(file, 'a', encoding='utf-8') as f:
        f.write(row_text + '\n')


def pandas_txt(row_text):
    # Pandas.txt (format) Full name; Address; City; State; ZipCode; DOB
    pandas_record = f"{row_text[1]['NAME']}; {row_text[1]['ADDRESS']}; {row_text[1]['CITY']}; {row_text[1]['STATE']}; {row_text[1]['ZIPCODE'][:5]}; {row_text[1]['DATE_OF_BIRTH']}"
    pandas_record = pandas_record.replace('; N/A', '').replace("N/A", '')
    add_row_into_txt('Results/Pandas.txt', pandas_record)


def tayc_txt(row_text):
    # Tayc.txt (format) MICHAEL L;SMITH;COUNTY RD 431;MS;Water Valley;38965
    tayc_name = row_text[1]['NAME'].split(' ')
    if len(tayc_name) > 2:
        tayc_first_name = tayc_name[0]
        tayc_middle_name = " " + str(tayc_name[1])[0].title()
        tayc_last_name = tayc_name[2]
    elif len(tayc_name) == 2:
        tayc_first_name = tayc_name[0]
        tayc_middle_name = ''
        tayc_last_name = tayc_name[1]
    else:
        tayc_first_name = tayc_name[0]
        tayc_middle_name = ''
        tayc_last_name = ''

    tayc_record = f"{tayc_first_name}{tayc_middle_name};{tayc_last_name};{row_text[1]['ADDRESS']};{row_text[1]['STATE']};{row_text[1]['CITY']};{row_text[1]['ZIPCODE'][:5]}"

    tayc_record = tayc_record.replace(';N/A', '').replace("N/A", '').replace(" ;", ";")
    add_row_into_txt('Results/Tayc.txt', tayc_record)


def goldenlu_txt(row_text):
    goldenlu_name = row_text[1]['NAME'].split(' ')
    if len(goldenlu_name) > 1:
        goldenlu_first_name = goldenlu_name[0]
        goldenlu_last_name = goldenlu_name[-1]
    else:
        goldenlu_first_name = goldenlu_name[0]
        goldenlu_last_name = ''

    # GoldenLU.txt FirstName LastName ZipCode
    goldenlu_record = f"{goldenlu_first_name} {goldenlu_last_name} {row_text[1]['ZIPCODE'][:5]}"
    goldenlu_record = goldenlu_record.replace('N/A', '')
    add_row_into_txt('Results/GoldenLU.txt', goldenlu_record)


def s247_txt(row_text):
    s247_name = row_text[1]['NAME'].split(' ')
    if len(s247_name) > 1:
        s247_first_name = s247_name[0]
        s247_last_name = s247_name[-1]
    else:
        s247_first_name = s247_name[0]
        s247_last_name = ''

    # FirstName LastName ZipCode
    s247_record = f"{s247_first_name} {s247_last_name} {row_text[1]['ZIPCODE'][:5]}"
    s247_record = s247_record.replace('N/A', '')

    add_row_into_txt('Results/S247.txt', s247_record)


def capblack_txt(row_text):
    capblack_name = row_text[1]['NAME'].split(' ')
    if len(capblack_name) > 1:
        capblack_first_name = capblack_name[0]
        capblack_last_name = capblack_name[-1]
    else:
        capblack_first_name = capblack_name[0]
        capblack_last_name = ''

    # FirstName LastName;Street;City;State;Zip;DOB
    capblack_record = f"{capblack_first_name} {capblack_last_name};{row_text[1]['ADDRESS']};{row_text[1]['CITY']};{row_text[1]['STATE']};{row_text[1]['ZIPCODE'][:5]};{row_text[1]['DATE_OF_BIRTH']}"
    capblack_record = capblack_record.replace(';N/A', '').replace("N/A", '')

    add_row_into_txt('Results/CapBlack.txt', capblack_record)


def all_txt(row_text):
    all_name = row_text[1]['NAME'].split(' ')
    if len(all_name) > 1:
        all_first_name = all_name[0]
        all_last_name = all_name[-1]
    else:
        all_first_name = all_name[0]
        all_last_name = ''

    try:
        my_zipcode = row_text[1]['ZIPCODE'][:5]
        county = f" {convert_zipcode_to_county(str(my_zipcode))}"
    except:

        county = ''

    if row_text[1]['EMAIL'] == 'N/A' or row_text[1]['EMAIL'] == '':
        my_email = f"{all_first_name.lower()}{all_last_name.lower()}{random.randint(100000, 900000)}@outlook.com"
    else:
        my_email = str(row_text[1]['EMAIL']).lower().split('@')[0] + str(
            random.randint(100000, 900000)) + '@outlook.com'

    # All.txt format FirstName LastName CITY STATE ZIPCODE|EMAIL
    all_record = f"{all_first_name} {all_last_name} {row_text[1]['CITY']} {row_text[1]['STATE']} {row_text[1]['ZIPCODE'][:5]}{county}|{my_email}"
    all_record = all_record.replace('N/A', '')

    add_row_into_txt('Results/All.txt', all_record)


def convert_zipcode_to_county(zipcode_x):
    try:
        return zip_codes_df[zip_codes_df['zip'] == int(zipcode_x)]['county'].values[0]
    except:
        return ''


import pickle

already_done = []
# close_chrome()
options = uc.ChromeOptions()
# path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
# options.add_argument(fr"user-data-dir={path}")
# options.add_argument(f'--profile-directory=Profile 1')
driver = uc.Chrome(options=options)
driver.maximize_window()
driver.get('https://chat.openai.com/')
time.sleep(10)
# login through cookies pickle
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get('https://chat.openai.com/')

input("Add: ")

# save cookies

all_text_files = [file for file in os.listdir('Text Files') if file.endswith('.txt')]
all_text_files_data = [get_file_data(f"Text Files/{file}") for file in all_text_files]
for file_data in all_text_files_data:
    adjust_chat_gpt()

    chunks_of_data = list_in_chunks(file_data, 20)
    for chunk in chunks_of_data:
        data = []
        columns = ['NAME', 'DATE_OF_BIRTH', 'ADDRESS', 'CITY', 'STATE', 'COUNTRY', 'ZIPCODE', 'EMAIL', 'ZIP_CODE_CITY']

        chunk_text = '\n'.join(chunk)
        response = chat_gpt_response(chunk_text)
        response = response.split('\n')

        for single_line in response:
            try:
                if single_line.startswith('NAME'):
                    continue
                if "|" not in single_line:
                    continue
                single_line = single_line.split('|')
                row = dict(zip(columns, single_line))
                data.append(row)
            except:
                pass

        df = pd.DataFrame(data)
        # fill empty values with N/A
        df = df.fillna('N/A')
        # if any row field is '' then replace it with N/A
        df = df.replace(r'^\s*$', 'N/A', regex=True)
        # save into DF

        #
        # df.to_csv('Results/DF.csv', index=False)
        # input("Add: ")

        # convert to txt formats
        for each_row in df.iterrows():
            pandas_txt(each_row)
            tayc_txt(each_row)
            goldenlu_txt(each_row)
            s247_txt(each_row)
            capblack_txt(each_row)
            all_txt(each_row)
        # input("Add: ")
        # all text files in Results folder
        # all_text_files = [file for file in os.listdir('Results') if file.endswith('.txt')]
        # for single_result_file in all_text_files:
        #     update_text_file_na(f"Results/{single_result_file}")

print("Done!")
driver.quit()
