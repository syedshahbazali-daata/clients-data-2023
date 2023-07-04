import csv
import os
import random
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from textwrap import dedent
import os
import imaplib
import email
import traceback
import re
import email

API_KEY = "1ceb0ff9a99196a07a2ea24557cf83a3"

########################################################################################################################
#                                                                                                                      #
#                                        PLEASE DON'T CHANGE ANYTHING BELOW                                            #
#                                                                                                                      #
########################################################################################################################
BASE_DIR = os.path.dirname(os.path.abspath("_file_"))
# Login credentials

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "alikpopov.avp" + ORG_EMAIL
FROM_PWD = "jfhzldfwksmernqc"

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def read_email_from_gmail_and_get_code():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')

        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(str(i).encode(), '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    # print('From : ' + email_from + '\n')
                    # print('Subject : ' + email_subject + '\n')
                    email_body = msg.get_payload()
                    if isinstance(email_body, list):
                        email_body = ''.join(str(part) for part in email_body)
                    # print('Description : ' + email_body + '\n')
                    # print("------------------------------")

                    if "verification code".lower() in str(email_body).lower():
                        print('Found')
                        try:
                            code = re.findall(r'(\d{6})\n', email_body)[0]
                            print(code)
                            return code
                        except:
                            pass

    except Exception:
        traceback.print_exc()


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


def clear_cart():
    driver.get('https://www.cvs.com/rx/dotm/cart?flowType=FS')
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, "//*[text()='Your cart is empty']")
        return True
    except:
        pass

    # remove all items from cart
    while True:
        try:
            driver.find_element(By.XPATH, "//*[text()='Remove']")
            specific_clicker_pass("//*[text()='Remove']")
        except:
            break
    return True


def kill_chrome_app():
    try:
        os.system("taskkill /f /im chrome.exe")
    except:
        pass


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
            time.sleep(0.3)
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
        return True


    except Exception as e:
        print(e)

        return False


def specific_clicker_with_direct(element):
    try:

        webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()


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
            input('Press any key to continue...')

            pass


def login_2captcha_exe(api_key):
    driver.switch_to.window(driver.window_handles[0])
    print(driver.current_url)
    time.sleep(1)

    driver.find_element(By.XPATH, '//input[@name="apiKey"]').send_keys(api_key)
    time.sleep(1)
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


def update_data(file, data):
    with open(file, "a") as f:
        f.write(data + '\n')


def switch_to_tab(tab_number):
    while True:
        try:

            driver.switch_to.window(driver.window_handles[tab_number])
            break
        except:
            pass


def login_to_cvs(acc_email, pwd):
    driver_go('https://www.cvs.com/account/login')
    print("captcha")
    time.sleep(4)

    for checking_captcha in range(4):
        try:
            iframe = driver.find_element(By.XPATH, '//iframe[@id="main-iframe"]')
            driver.switch_to.frame(iframe)
            captcha_solver()
            break
        except:
            print("No captcha")

    time.sleep(1)

    find_element_send_text('//input[@id="emailField"]', acc_email)
    time.sleep(1)
    for i in range(3):
        try:
            driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@id="kampyleInvite"]'))
            specific_clicker_pass('//*[@aria-label="Close Survey"]')
            time.sleep(1)
        except:
            pass
    driver.switch_to.default_content()

    specific_clicker('//*[text()="Continue"]')
    time.sleep(1)
    for i in range(3):
        try:
            driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@id="kampyleInvite"]'))
            specific_clicker_pass('//*[@aria-label="Close Survey"]')
            time.sleep(1)
        except:
            pass
    driver.switch_to.default_content()
    for i in range(3):
        try:
            driver.find_element(By.XPATH, "//*[text()='An unexpected error occurred']")
            return False
        except:
            time.sleep(1)

    find_element_send_text('//input[@id="cvs-password-field-input"]', pwd)
    specific_clicker('//div[text()="Sign in"]')
    print("PLEASE WAIT FOR 65 SECONDS TO GET THE OTP")
    time.sleep(30)
    otp_code = str(read_email_from_gmail_and_get_code())

    find_element_send_text('//input[@id="forget-password-otp-input"]', otp_code)
    specific_clicker('//button[@id="forgot-password-verify-submit"]')
    return True


def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass


def login_2captcha(api_key):
    chrome_url = "chrome-extension://ifibfemgeogfhoebkmokieepdoobkbpo/popup/popup.html"
    driver.get(chrome_url)
    find_element_send_text('//input[@name="apiKey"]', api_key)
    specific_clicker("//button[text()='Login']")
    time.sleep(2)


df = pd.read_csv('data.csv')
names = df['NAME'].tolist()
emails = df['EMAIL'].tolist()
street_address = df['STREET ADDRESS'].tolist()
unit_apartment = df['UNIT'].tolist()
city = df['CITY'].tolist()
state = df['STATE'].tolist()
zip_code = df['ZIP CODE'].tolist()
phone_number = df['PHONE NUMBER'].tolist()
passwords = df['PASSWORD'].tolist()
csv_codes = df['CSV'].tolist()

for index, name in enumerate(names):
    print(f'{index} - {name}')
    account_email = str(emails[index]).strip()
    password = str(passwords[index]).strip()
    already_done = get_file_data("Already_done.txt")
    if account_email in already_done:
        print('Already Done')
        continue

    worked = []
    for i in range(3):

        options = webdriver.ChromeOptions()
        # path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
        # options.add_argument(fr"user-data-dir={path}")
        # options.add_argument(f'--profile-directory=Profile 2')
        # add extension 2captcha
        options.add_extension("2captcha-extension.crx")

        proxies_list = get_file_data('Proxies.txt')

        my_proxy = random.choice(proxies_list)
        print(my_proxy)

        proxy = get_proxy_auth_extension(my_proxy)
        options.add_argument(f'--load-extension={proxy}')
        global driver
        driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
        driver.maximize_window()
        time.sleep(2)
        driver_go('https://www.cvs.com/')
        # login to 2captcha
        for i in range(2):
            switch_to_tab(i)
            current_url = str(driver.current_url).lower()
            if 'popup' in current_url:
                pass
            else:
                driver.close()
                switch_to_tab(0)
                break
        login_2captcha(API_KEY)
        time.sleep(6)

        driver_go('https://www.cvs.com/')

        input("add: ")
        time.sleep(1)
        for i in range(3):
            try:
                driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@id="kampyleInvite"]'))
                specific_clicker_pass('//*[@aria-label="Close Survey"]')

            except:
                pass
            time.sleep(1)
        time.sleep(10)
        account_login = login_to_cvs(account_email, password)
        if not account_login:
            driver.quit()
            continue
        time.sleep(7)
        clear_cart()
        worked.append(True)
        break

    input("add: ")
    if len(worked) == 0:
        print("Not worked")
        driver.quit()
        continue

    print("Logged in")

    driver.get('https://www.cvs.com/shop/cerave-pm-facial-moisturizing-lotion-lightweight-oil-free-3-oz-prodid-1140223')

    time.sleep(2)
    specific_clicker('//div/label[@for="textSwatcher"]/..')
    specific_clicker("//*[text()='3 Ounces']")
    time.sleep(2)

    # check_pickup_available = driver.find_elements(By.XPATH, '//button[@aria-label="Pickup" and not(@disabled)]')
    # if len(check_pickup_available) > 0:
    #     print(account_email, " No pickup found")
    #     driver.quit()
    #     continue

    specific_clicker('//span[@class="tileTitle "]/..')
    time.sleep(1)
    specific_clicker("//*[text()='Add for shipping']")
    for i in range(3):
        specific_clicker_pass("//*[text()='Add for shipping']")
        time.sleep(1)

    specific_clicker("//div[text()='Checkout (1 items)']")

    # add Coupons

    time.sleep(4)
    while True:
        try:

            driver.find_element(By.XPATH, '//button[@aria-label="Check out"]')
            break
        except:
            time.sleep(1)
    coupons = driver.find_elements(By.XPATH, "//*[text()='Apply']/..")

    for index_coupon, single_coupons in enumerate(coupons):

        while True:
            try:
                driver.find_element(By.XPATH, "//*[text()='Apply']/..").click()
                break
            except Exception as e:
                print(e)
                time.sleep(2)

        time.sleep(4)
        print("Coupon is Applied")

    specific_clicker('//button[@aria-label="Check out"]')

    find_element_send_text('(//input)[1]', name)
    find_element_send_text('(//input)[2]', street_address[index])
    find_element_send_text('(//input)[3]', unit_apartment[index])
    find_element_send_text('(//input)[4]', city[index])
    find_element_send_text('(//input)[5]', zip_code[index])
    find_element_send_text('(//input)[6]', phone_number[index])
    find_element_send_text('(//input)[7]', account_email)

    try:
        driver.find_element(By.XPATH, f'//select[@name="state"]/option[@value="{state[index]}"]').click()
        print("State Selected")
    except:
        pass

    time.sleep(2)
    specific_clicker("//*[text()='Continue to payment']")
    time.sleep(4)
    for i in range(4):
        specific_clicker_pass("//button[text()='Use original']")
        time.sleep(1)

    find_element_send_text('//input[@id="securityCodeCC"]', str(csv_codes[index]))
    specific_clicker("//*[text()='Continue']")
    time.sleep(2)
    specific_clicker("//*[text()='Continue']")
    time.sleep(2)

    specific_clicker('//button[@aria-label="Place order"]')
    time.sleep(12)
    print("ORDER PLACED")

    update_data("Already_done.txt", account_email)
    driver.delete_all_cookies()
    driver.quit()
