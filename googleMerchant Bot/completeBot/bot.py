import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from faker import Faker
import pandas as pd
from textwrap import dedent
import undetected_chromedriver as uc
import os

########################################################################################################################
# Functions

BASE_DIR = os.path.dirname(os.path.abspath("_file_"))


def get_proxy_auth_extension(proxy):
    if proxy.strip() == '':
        return None
    cred, prox = proxy.split('@')
    PROXY_USER, PROXY_PASS = cred.split(':')
    PROXY_HOST, PROXY_PORT = prox.split(':')
    manifest_json = """
                    {
                        "version": "1.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                    """

    background_js = """
                    var config = {
                            mode: "fixed_servers",
                            rules: {
                            singleProxy: {
                                scheme: "http",
                                host: "%s",
                                port: parseInt(%s)
                            },
                            bypassList: ["localhost"]
                            }
                        };

                    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                    function callbackFn(details) {
                        return {
                            authCredentials: {
                                username: "%s",
                                password: "%s"
                            }
                        };
                    }

                    chrome.webRequest.onAuthRequired.addListener(
                                callbackFn,
                                {urls: ["<all_urls>"]},
                                ['blocking']
                    );
                    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    fn = os.path.join(BASE_DIR, 'proxy_ext')
    if not os.path.exists(fn):
        os.mkdir(fn)
    m_path = os.path.join(fn, "manifest.json")
    b_path = os.path.join(fn, "background.js")
    with open(m_path, 'w') as f:
        f.write(dedent(manifest_json))
    with open(b_path, 'w') as f:
        f.write(dedent(background_js))
    return fn


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


def element_xpath_with_text(text):
    return f"//*[text()='{text}' or text()='{text.upper()}' or text()='{text.lower()}' or text()='{text.capitalize()}']"


def get_text(ele):
    while True:
        try:
            element = driver.find_elements(By.XPATH, ele)
            texts = [str(x.text) for x in element]
            return texts
        except Exception as e:
            # print(e)
            pass


def login_to_google_account(mail_address, mail_pwd, mail_recovery=False):
    find_element_send_text('//input[@type="email"]', mail_address)
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(Keys.ENTER)

    find_element_send_text('//input[@type="password"]', mail_pwd)
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(Keys.ENTER)


def business_details_fill(b_name, b_address, card_number, card_month, card_year, card_cvv):
    while True:
        try:
            iframe_element = driver.find_element(By.XPATH, '//iframe[@title="Enter payment info"]')
            driver.switch_to.frame(iframe_element)
            print("switched")
            break
        except:
            time.sleep(2)
    find_element_send_text('//input[@name="ORGANIZATION"]', b_name)
    find_element_send_text('//input[@name="ADDRESS_LINE_1"]', b_address)
    time.sleep(2)
    while True:
        try:
            driver.find_element(By.XPATH, '//input[@name="ADDRESS_LINE_1"]/..//div[@role="listbox"]/div').click()
            break
        except:
            time.sleep(3)

    find_element_send_text('//input[@name="cardnumber"]', card_number)
    find_element_send_text('//input[@name="ccmonth"]', card_month)
    find_element_send_text('//input[@name="ccyear"]', card_year)
    find_element_send_text('//input[@name="cvc"]', card_cvv)

    try:

        driver.find_element(By.XPATH, '//*[contains(@class, "message-checkbox")]').click()
    except:
        pass
    driver.switch_to.default_content()
    specific_clicker("//*[text()='Continue']")


def merchant_center_join(mail_address, mail_pwd, b_name, b_address, card_number, card_month, card_year, card_cvv,
                         mail_recovery=False):
    driver.get('https://www.google.com/retail/solutions/merchant-center/')
    # zoom out
    driver.execute_script("document.body.style.zoom='70%'")
    time.sleep(2)
    signup_link = driver.find_element(By.XPATH, "//h1/..//a[text()='Sign up for free']").get_attribute("href")
    driver.get(signup_link)

    login_to_google_account(mail_address, mail_pwd, mail_recovery)
    time.sleep(3)
    specific_clicker('(//*[@aria-label="No"])[1]')
    time.sleep(1.5)
    specific_clicker('(//*[@aria-label="No"])[2]')
    specific_clicker("//*[text()='Continue with Merchant Center Account creation']")
    specific_clicker("//*[text()='Continue to Merchant Center']")

    fake = Faker()
    random_company_name = fake.name() + " company"
    find_element_send_text('//input[@type="text"]', random_company_name)
    specific_clicker('//div[@aria-haspopup="listbox"]')
    time.sleep(1)
    specific_clicker("//span[text()='Italy']")
    specific_clicker("//*[text()='Continue to Merchant Center']")

    specific_clicker("//span[text()='Continue']")

    specific_clicker("//*[text()='Growth']")
    time.sleep(3)
    specific_clicker("//*[text()='Manage programs']")

    specific_clicker("//div[text()='Shopping ads']/../..//*[text()='Get started']")
    specific_clicker("//span[text()='Link to Google Ads']")

    specific_clicker("//*[text()='Create account & continue']")
    specific_clicker("//*[text()='Create & link account']")

    # Add billing Details
    time.sleep(3)
    specific_clicker("//span[text()='Add billing details']")
    business_details_fill(b_name, b_address, card_number, card_month, card_year, card_cvv)
    time.sleep(8)


def set_google_ads(keywords, website_url, headlines, descriptions):
    driver.get("https://ads.google.com/")
    specific_clicker(element_xpath_with_text("Sign in"))
    time.sleep(6)
    driver.get("https://ads.google.com/aw/overview")
    specific_clicker('//button[@aria-label="New campaign"]')
    specific_clicker("//span[text()='Website traffic']")
    specific_clicker("//span[text()='Search']")
    specific_clicker("//div[text()='Continue']")
    specific_clicker("//*[text()='Next']")
    specific_clicker("//*[text()='Italy']/../../div")
    specific_clicker("(//material-button//span[text()='Next'])[2]")
    # keywords

    find_element_send_text('//textarea', keywords)
    find_element_send_text('//input[@aria-label="Final URL"]', website_url)

    # headlines
    for index, headline in enumerate(headlines):
        try:
            driver.find_element(By.XPATH, f"(//span[text()='Headline']/../../input)[{index + 1}]").send_keys(headline)
        except:
            pass

    # descriptions
    for index, description in enumerate(descriptions):
        try:
            driver.find_element(By.XPATH, f"(//section//textarea)[{index + 1}]").send_keys(description)
        except:
            pass

    specific_clicker("//*[text()='Done']")
    specific_clicker("(//span[text()='Next'])[3]")

    # budget
    find_element_send_text('//input[@aria-label="Set your average daily budget for this campaign"]', "2.00")

    specific_clicker("(//span[text()='Next'])[4]")
    specific_clicker("(//span[text()='Publish campaign'])[5]")


df = pd.read_csv("data.csv")

for row_index, row in df.iterrows():

    # READING ROW DATA
    already_done = get_file_data("already_done.txt")

    input_mail_address = row["EMAIL"]
    if input_mail_address in already_done:
        continue
    input_mail_pwd = row["PASSWORD"]
    input_mail_recovery = row["RECOVERY MAIL"]
    input_proxy = row["PROXY"]
    input_address = row["ADDRESS"]
    input_card_number = row["CARD NUMBER"]
    input_card_month = row["CARD MONTH"]
    input_card_year = row["CARD YEAR"]
    input_card_cvv = row["CVV"]

    input_keywords = row["KEYWORDS"]
    input_keywords = input_keywords.replace(",", "\n")
    input_headlines = row["HEADLINES"]
    input_headlines = input_headlines.split(",")
    input_descriptions = row["DESCRIPTIONS"]
    input_descriptions = input_descriptions.split(",")

    options = uc.ChromeOptions()

    my_proxy = input_proxy
    proxy = get_proxy_auth_extension(my_proxy)
    options.add_argument(f'--load-extension={proxy}')
    driver = uc.Chrome(options=options)
    driver.maximize_window()

    merchant_center_join(input_mail_address, input_mail_pwd, input_address, input_address, input_card_number,
                         input_card_month, input_card_year, input_card_cvv, input_mail_recovery)
    time.sleep(5)
    set_google_ads(input_keywords, input_address, input_headlines, input_descriptions)
    time.sleep(7)
    driver.quit()

    with open("already_done.txt", "a", encoding="utf-8") as f:
        f.write(input_mail_address + "\n")
