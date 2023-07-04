import csv
import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver

API_KEY = "1ceb0ff9a99196a07a2ea24557cf83a3"


########################################################################################################################

########################################################################################################################

def find_element_send_text(ele, text, clear=True, Enter=False):
    while True:
        try:
            input_field = driver.find_element(By.XPATH, ele)
            if clear:
                input_field.clear()
            input_field.send_keys(text)
            if Enter:
                input_field.send_keys(Keys.ENTER)

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


def get_file_data(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read().strip().split("\n")


def switch_to_tab(tab_number):
    while True:
        try:

            driver.switch_to.window(driver.window_handles[tab_number])
            break
        except:
            pass


def login_2captcha_exe(api_key):
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.XPATH, '//input[@name="apiKey"]').send_keys(api_key)
    specific_clicker('//button[@id="connect"]')
    while True:
        try:
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(2)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            break
        except:
            time.sleep(2)


def captcha_solver():
    while True:
        try:
            driver.find_element(By.XPATH, "//*[text()='Solve with 2Captcha']").click()
            break
        except:
            time.sleep(2)

    while True:
        try:
            driver.find_element(By.XPATH, "//*[text()='ERROR_SITEKEY']")
            return False
        except:
            pass

        try:
            driver.find_element(By.XPATH, "//*[text()='Captcha solved!']")
            return True
        except:
            time.sleep(2)


def login_to_rumble_mail(single_email_pass_row):
    my_email = single_email_pass_row.split(":")[0]
    my_pass = single_email_pass_row.split(":")[1]
    print(my_email, my_pass)
    while True:
        find_element_send_text('(//input)[1]', my_email)
        find_element_send_text('(//input)[2]', my_pass, Enter=True)
        print(my_email, my_pass)
        time.sleep(4)
        captcha_response = captcha_solver()
        if not captcha_response:
            driver.delete_all_cookies()
            driver.get("https://mail.rambler.ru/")
            continue
        else:
            break

    print(my_email, my_pass)
    time.sleep(2)
    current_url = str(driver.current_url)
    driver.find_element(By.XPATH, '(//input)[2]').send_keys(Keys.ENTER)
    while True:
        try:
            new_url = str(driver.current_url)
            if new_url != current_url:
                break
        except:
            time.sleep(2)
    time.sleep(2)
    for i in range(5):
        specific_clicker2('//button[@class="rui-Popup-close"]')

    return [my_email, my_pass]


def choose_topics():
    while True:
        topics = driver.find_elements(By.XPATH, '//span/span/span')
        if len(topics) > 0:
            break
    choose = 0
    limit = random.randint(5, 8)
    for topic in topics:
        specific_clicker("//*[text()='{}']".format(topic.text))

        if choose >= limit:
            break
        choose += 1

    specific_clicker("//*[text()='Done']")


def sign_up_quora(email, pwd, random_name):
    # --> 1. Open new tab
    driver.switch_to.new_window("tab")
    driver.get("https://www.quora.com/")
    # --> 2. Click on Sign up button
    specific_clicker("//*[text()='Sign up with email']")
    find_element_send_text('//input[@name="profile-name"]', random_name)
    find_element_send_text('//input[@name="email"]', email)
    time.sleep(2)
    specific_clicker("//*[text()='Next']/../../../../*[not(@disabled)]")

    worked = False
    for i in range(5):
        try:
            driver.find_element(By.XPATH, "//*[text()='Confirm your email']")
            worked = True
            break
        except:
            time.sleep(2)

    # --> 3. Enter confirmation code
    if not worked:
        input("Please confirm your email and press enter to continue:")

    switch_to_tab(0)
    while True:
        confirmation_code = str(driver.find_element(By.XPATH, "//*[text()='Email Confirmation']/../*[2]").text)
        break
    switch_to_tab(1)
    find_element_send_text('//input[@name="confirmationCode"]', confirmation_code)
    specific_clicker("//*[text()='Next']/../../../../*[not(@disabled)]")
    # --> 4. Enter password
    find_element_send_text('//input[@name="password"]', pwd)
    captcha_solver()
    specific_clicker("//*[text()='Finish']/../../../../*[not(@disabled)]")
    time.sleep(2)
    choose_topics()


# create a space
def create_space(space_name):
    for i in range(5):
        specific_clicker2("//*[text()='Create Space']")
        time.sleep(2)
    time.sleep(2)
    driver.find_element(By.XPATH, '//input').send_keys(Keys.CONTROL, "a")
    driver.find_element(By.XPATH, '//input').send_keys(Keys.DELETE)
    find_element_send_text('//input', space_name)
    specific_clicker("//*[text()='Create']/../../../../*[not(@disabled)]")
    time.sleep(5)
    driver.get("https://www.quora.com/")


options = webdriver.ChromeOptions()
options.add_extension("2captcha-extension.crx")
driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
time.sleep(3)
switch_to_tab(1)
login_2captcha_exe(API_KEY)
input("add: ")
email_data_file = get_file_data("Emails.txt")
names_list = get_file_data("Names.txt")

for row in email_data_file:
    driver.get("https://mail.rambler.ru/")
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe'))
    result = login_to_rumble_mail(row)
    quora_email, quora_pass = result[0], result[1]
    random_quora_name = random.choice(names_list)
    sign_up_quora(quora_email, quora_pass, random_quora_name)
    choose_topics()

    spaces_names = get_file_data("Spaces-names.txt")
    random_space_name = random.choice(spaces_names)

    # ---> 1. Create a space
    create_space(random_space_name)

    specific_clicker('//div[@class="q-box"]//img')
    time.sleep(2)
    profile_link = driver.find_element(By.XPATH,
                                       "//div[@class='q-box']//a[contains(@href, 'https://www.quora.com/profile')]").get_attribute(
        "href")

    with open("Output.csv", "a") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([quora_email, quora_pass, profile_link])

    input("add: ")
    driver.close()
