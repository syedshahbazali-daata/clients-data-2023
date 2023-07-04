import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from threading import Thread

bot_token = '5792992329:AAGGGWh_qA5G0V3cfva3GfjuU7KKERpdVlI'
bot_chatID = '-1001988258620'
url = "https://www.avto.net/Ads/results_100.asp?oglasrubrika=1&prodajalec=2"


def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')
    return data


def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
    params = {
        'chat_id': bot_chatID,
        'parse_mode': 'HTML',
        'text': bot_message
    }
    response = requests.post(send_text, data=params)
    return response.json()


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


def get_text(ele):
    try:
        element = driver.find_element(By.XPATH, ele)
        return element.text
    except Exception as e:
        # print(e)
        return "NA"


options = webdriver.ChromeOptions()
options.headless = False

options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
# max load time 20 seconds
driver.set_page_load_timeout(60)
driver.set_window_size(1920, 1080)

while True:
    driver.get("https://www.datatech.icu/")

    driver.execute_script("document.body.style.zoom='75%'")
    find_element_send_text('//*[@name="url"]', url)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@name="url"]').send_keys(Keys.ENTER)

    while True:
        try:
            driver.find_element(By.XPATH, "//div[contains(@class,'GO-Results-Row')]")
            # stop loading
            driver.execute_script("window.stop();")
            print("found")
            break
        except:
            pass

    work = False
    for check in range(20):
        try:
            driver.find_element(By.XPATH, "//div[contains(@class,'GO-Results-Row')]")
            work = True
            print("found")
            break
        except:
            print("not found")
            time.sleep(1)

    if work:
        print("working now")
        already_done = get_file_data("already_done.txt")
        all_rows = driver.find_elements(By.XPATH, "//div[contains(@class,'GO-Results-Row')]")
        total_row = len(all_rows)
        for single_row in range(1, total_row + 1):
            xpath = f"(//div[contains(@class,'GO-Results-Row')])[{single_row}]"

            ad_link = driver.find_element(By.XPATH, f"{xpath}/a").get_attribute("href")
            title = get_text(f"({xpath}//div/span)[1]")
            registracija = get_text(f"{xpath}//td[text()='1.registracija']//following-sibling::td")
            gorivo = get_text(f"{xpath}//td[text()='Gorivo']//following-sibling::td")
            km_ = get_text(f"{xpath}//td[text()='Prevoženih']//following-sibling::td")
            menjalnik = get_text(f"{xpath}//td[text()='Menjalnik']//following-sibling::td")
            motor = get_text(f"{xpath}//td[text()='Motor']//following-sibling::td")
            price = get_text(f"({xpath}//div[@class='GO-Results-Price-TXT-Regular'])[2]")
            if str(ad_link) in already_done:
                print("Already done")
                continue

            # <a href='https://www.avto.net/Ads/details.asp?id=16361504" target="_blank" class="GO-Results-Title-Link">Audi A4 Avant 1.9 TDI</a>
            title_formatted = '<a href="' + ad_link + '" target="_blank" class="GO-Results-Title-Link">' + title + '</a>'
            main_url = "https://www.avto.net/"

            message = f"<strong>RSS feed for: </strong>{main_url}\nTitle: {title_formatted}\n1.registracija: {registracija}\nPrevoženih: {km_}\nGorivo: {gorivo}\nMenjalnik: {menjalnik}\nMotor: {motor}\n\nPrice: {price}".strip()

            # threading
            telegram_bot_sendtext(message)

            with open("already_done.txt", "a", encoding='utf-8') as file:
                file.write(ad_link + "\n")

    else:
        pass
