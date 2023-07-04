import os
import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime as dt
import random
import json
import requests
import undetected_chromedriver as uc


# REQUIRED FUNCTIONS

def get_file_data(file_name):
    with open(file=file_name, mode="r", encoding="utf-8") as file:
        data = file.read().strip().split("\n")
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
            print(e)
            pass


def specific_clicker2(ele):
    try:
        element = driver.find_element(By.XPATH, ele)
        webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

    except Exception as e:
        print(e)
        pass


def drag_and_drop_file(drop_target, path):
    """
    Drag and drop the provided file path onto the provided element target.


    Parameters
    ----------
    drop_target : WebElement
        The web element to drop the file at path on

    path : str
        The file path to drag onto the web element

    Returns
    -------
    bool
        Whether or not dragging the file was successful

    """

    # https://stackoverflow.com/questions/43382447/python-with-selenium-drag-and-drop-from-file-system-to-webdriver
    JS_DROP_FILE = """
            var target = arguments[0],
                offsetX = arguments[1],
                offsetY = arguments[2],
                document = target.ownerDocument || document,
                window = document.defaultView || window;

            var input = document.createElement('INPUT');
            input.type = 'file';
            input.onchange = function () {
              var rect = target.getBoundingClientRect(),
                  x = rect.left + (offsetX || (rect.width >> 1)),
                  y = rect.top + (offsetY || (rect.height >> 1)),
                  dataTransfer = { files: this.files };

              ['dragenter', 'dragover', 'drop'].forEach(function (name) {
                var evt = document.createEvent('MouseEvent');
                evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
                evt.dataTransfer = dataTransfer;
                target.dispatchEvent(evt);
              });

              setTimeout(function () { document.body.removeChild(input); }, 25);
            };
            document.body.appendChild(input);
            return input;
        """
    try:

        # BUG: requires double to register file upload
        file_input = drop_target.parent.execute_script(JS_DROP_FILE, drop_target, 0, 0)
        file_input.send_keys(path)
        file_input = drop_target.parent.execute_script(JS_DROP_FILE, drop_target, 50, 50)
        file_input.send_keys(path)

        return True
    except Exception as e:
        print(e)

    return False


def close_chrome_app():


    try:
        os.system("taskkill /f /im chrome.exe")
    except:
        pass


def upload_photo(image_path):
    while True:
        try:
            image_form = driver.find_element(By.XPATH, '//*[@id="make_post_form"]')
            break
        except:
            pass

    drag_and_drop_file(image_form, fr"{image_path}")
    time.sleep(1)


def set_date(month_no: int, day_no: int, year: int):
    specific_clicker('(//input)[1]')

    # Select Year
    specific_clicker('//div[@class="vdatetime-popup__year"]')
    specific_clicker(f'//*[text()="20{year} "]')
    specific_clicker("//button[text()=' Save ']")

    # Select Month
    specific_clicker('//div[@class="vdatetime-popup__date"]')
    specific_clicker(f'(//div[@class="vdatetime-month-picker__list vdatetime-month-picker__list"]/div)[{month_no}]')
    specific_clicker("//button[text()=' Save ']")

    # Select Day
    specific_clicker(f'//div[@class="vdatetime-calendar"]//span[text()="{day_no}"]')
    specific_clicker("//button[text()=' Next ']")


def set_time(hour: int, minute: int, am_pm: str):
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    specific_clicker('(//input)[2]')

    # Select AM/PM
    specific_clicker(f'//div[text()="{am_pm.lower()}"]')

    # Select Hour
    specific_clicker(
        f'//div[@class="vdatetime-time-picker__list vdatetime-time-picker__list--hours"]//*[text()="{hour}"]')

    # Select Minute
    specific_clicker(
        f'//div[@class="vdatetime-time-picker__list vdatetime-time-picker__list--minutes"]//*[text()="{minute}"]')

    specific_clicker("//button[text()=' Save ']")


def add_text(text: str = ''):
    time.sleep(1)
    find_element_send_text('//textarea[@id="new_post_text_input"]', text)


def set_price(price: int = 0):
    if price > 0:
        specific_clicker('//button[@at-attr="price_btn"]')
        find_element_send_text('//input[@id="priceInput_1"]', str(price))
        specific_clicker("//button[text()=' Save ']")


def add_preview_image(no_of_preview_images: int):
    specific_clicker('//button/*[@class="b-make-post__sort-btn m-left"]')
    time.sleep(2)
    total_images_uploaded = driver.find_elements(By.XPATH, '//div[@class="checkbox-item__inside"]')
    if no_of_preview_images > len(total_images_uploaded) and no_of_preview_images == 0:
        return False

    for index, single_image in enumerate(total_images_uploaded[:no_of_preview_images]):
        specific_clicker(f'(//div[@class="checkbox-item__inside"]/..)[{index + 1}]')

    specific_clicker('//button[@class="b-make-post__sort-done-btn"]')
    return True


def post_image_with_schedule(schedule_date: str, schedule_time: str, media: list, set_post_price: int = 0,
                             set_text: str = '', no_of_preview_images: int = 0):
    driver.get('https://onlyfans.com/my/queue')
    specific_clicker('//button[@at-attr="add_event_header"]')

    # SET POST DATE : "12/21/22"
    format_date = schedule_date.split("/")
    post_schedule_date = [int(_) for _ in format_date]
    set_date(post_schedule_date[0], post_schedule_date[1], post_schedule_date[2])

    # SET POST TIME : "12:00 AM"
    split_time = schedule_time.split(" ")
    post_time = [int(_) for _ in split_time[0].split(":")]
    set_time(post_time[0], post_time[1], str(split_time[1]))

    specific_clicker("//button[text()=' Post ']")
    for single_media_file in media:
        upload_photo(single_media_file)

    while True:
        try:
            driver.find_element(By.XPATH, "//*[text()=' Media has already added. Please choose another. ']")
            specific_clicker2("//*[text()=' Close ']")
            time.sleep(1)
        except:
            break

    add_text(set_text)

    set_price(set_post_price)
    time.sleep(2)
    add_preview_image(no_of_preview_images)
    specific_clicker('//button[@at-attr="submit_post"]')


def bot_start():
    with open('schedules.json') as f:
        config = json.load(f)['schedule_data']
        print(config)

    global driver
    print("Starting Chrome")
    close_chrome_app()
    options = uc.ChromeOptions()
    path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data')
    options.add_argument(fr"user-data-dir={path}")
    options.add_argument(f'--profile-directory=Profile 3')

    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.maximize_window()

    for index, single_post in enumerate(config):
        print(single_post)
        post_index = index + 1

        # Required Data for Posting
        get_text_description = single_post['description']
        get_post_price = single_post['price']
        get_post_date = single_post['post_date']
        get_post_time = single_post['post_time']
        get_media_paths = single_post['media_paths']
        get_posts_interval = single_post['interval']

        current_time_with_am_pm = get_post_time
        preview_images = 1
        print(f"Post {post_index} : {get_post_date} {get_post_time} : {get_media_paths} : {get_text_description} : {get_post_price} : {get_posts_interval} : {preview_images}")

        post_image_with_schedule(get_post_date, current_time_with_am_pm, get_media_paths, get_post_price,
                                 get_text_description,
                                 preview_images)

        # xpath contains the text close in any format like "close", "Close", "CLOSE": //*[contains(text(), 'close')]

    input("add: ")
    driver.quit()
    return True

# pip freeze > requirements.txt
bot_start()