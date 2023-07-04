import random
import time
from datetime import datetime
import pyperclip
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import os
import pandas as pd

start_page = 1
end_page = 5
path = fr"/Users/shahbazali/Library/Application Support/Google/Chrome"  # Path to your chrome profile


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
    try:
        os.system("taskkill /f /im chrome.exe")
    except:
        pass


def get_file_data(file):
    with open(file, "r", encoding="utf-8") as f:
        return f.read().strip().split("\n")


#
total_no_files = len(os.listdir("data"))
if len(os.listdir("data")) > 0:

    if len(os.listdir("data")) > 1:
        # Delete the old_etop.csv
        try:
            os.remove("data/old_etop.csv")
        except:
            pass

        try:
            os.remove("data/comparison_etop.csv")
        except:
            pass

    # Rename the current new_etop.csv to old_etop.csv
    try:
        os.rename("data/new_etop.csv", "data/old_etop.csv")
    except:
        pass


# compare the old_etop.csv and new_etop.csv and save the new data in new_etop.csv
def compare_data(file_1, file_2):
    try:
        df1 = pd.read_csv(file_1, encoding="utf-8")

        # add four columns to the dataframe for extra space
        df1[""] = ""
        df1[" "] = ""
        df1["  "] = ""
        df1["   "] = ""

        df2 = pd.read_csv(file_2, encoding="utf-8")
        # merge the two files vertically and drop the duplicates










    except:
        return

    # just merge the two files side by side
    df3 = pd.concat([df1, df2], axis=1)
    df3.to_csv("data/comparison_etop.csv", index=False, encoding="utf-8")


if __name__ == '__main__':
    options = uc.ChromeOptions()
    # options.add_argument(fr"user-data-dir={path}")
    # options.add_argument(f'--profile-directory=Default')

    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://www.etopfun.com/en/store/")
    input("Press Enter to continue...")

    driver.get("https://www.etopfun.com/en/store/")

    time.sleep(2)
    specific_clicker("//ul//span[text()='Order Items Page']")

    while True:
        try:
            current_page = int(
                str(driver.find_element(By.XPATH, "//ul[@class='el-pager']//li[contains(@class, 'active')]").text))
            print(current_page)
        except:
            time.sleep(2)
            continue

        if current_page > end_page:
            break
        if current_page >= start_page and current_page <= end_page:
            time.sleep(5)
            total_items = driver.find_elements(By.XPATH, '//ul[contains(@class, "dota2-ul")]/li')
            for i in range(1, len(total_items) + 1):
                xpath = f'(//ul[contains(@class, "dota2-ul")]/li)[{i}]'
                name_x = str(driver.find_element(By.XPATH, f"{xpath}//p[@title]").text)
                try:
                    name = name_x.split("(")[0]

                except:
                    name = name_x

                # exterior = driver.find_element(By.XPATH, f"{xpath}/p[@class='count']/label/span").text
                try:
                    exterior = name_x.split("(")[1].split(")")[0]
                except:
                    exterior = "N/A"

                price = driver.find_element(By.XPATH, f"{xpath}/p[@class='count']/label/b").text

                record = [name, exterior, price]

                with open("DATA/new_etop.csv", "a", encoding="utf-8", newline="") as f:
                    csv.writer(f).writerow(record)
            specific_clicker('//button[@class="btn-next"]')

        else:
            print("skipping page")
            specific_clicker('//button[@class="btn-next"]')

    driver.quit()

    headers = ["Name", "Exterior", "Price"]
    df = pd.read_csv("DATA/new_etop.csv", names=headers)
    df.drop_duplicates(inplace=True)
    df.to_csv("DATA/new_etop.csv", index=False)

    print("Done")

    # compare the old_etop.csv and new_etop.csv and save the new data in new_etop.csv
    compare_data("data/old_etop.csv", "data/new_etop.csv")

# testingetop
# testingclone1234

