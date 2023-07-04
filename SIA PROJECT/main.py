import os
import random
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for
import webview
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import undetected_chromedriver as uc

# get the primary monitor screen dimensions

import json
import urllib.request

app = Flask(__name__)





##### BOT Functions #####
# def login():
#     login_driver = uc.Chrome()
#     login_driver.get('https://onlyfans.com/')
#     while True:
#         url = str(login_driver.current_url)
#         if 'onlyfans.com' in url:
#             try:
#                 login_driver.find_element(By.XPATH, '//form/h4')
#             except:
#                 break


#########################

def get_file_data(file_name):
    with open(file=file_name, mode="r", encoding="utf-8") as file:
        data = file.read().strip().split("\n")
    return data


@app.route('/')
def index():
    return render_template('SplashScreen.html')


@app.route('/sia_login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        # /sia_home
        return redirect(url_for('tester'))

    return render_template('LoginPage.html')


# ----------------------------------------------------- #
@app.route('/schedule_data', methods=['GET', 'POST'])
def schedule_data():
    if request.method == 'POST':
        print(request.form)
        uploading_method = request.form['uploading_method']
        interval = request.form['interval']
        post_date = request.form['date']
        post_time = request.form['time']
        platform = request.form['platform']

        if post_date == "false":
            # post date next hour from now
            post_date = datetime.now().strftime("%Y-%m-%d")
            post_time = datetime.now().strftime("%H:%M")
            post_time = datetime.strptime(post_time, "%H:%M")
            post_time = post_time + timedelta(hours=1)
            post_time = post_time.strftime("%H:%M")

        description_type = request.form['description_type']
        description = request.form['description']
        ai_generated = request.form['ai_generated']
        if ai_generated == 'true':
            ai_generated_text_file = get_file_data('AI Generated Text')
            description = random.choice(ai_generated_text_file)

        price = request.form['price']
        if price == '':
            price = '0'
        media_paths = []
        files = request.files.getlist('files')
        for file in files:
            file_new_name = f"{file.filename} - {random.randint(0, 1000)} - {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"
            file.save(os.path.join('download_files', file_new_name))
            absolute_path = os.path.abspath(os.path.join('download_files', file_new_name))
            media_paths.append(absolute_path)

        print(uploading_method, interval, post_date, post_time, description_type, description, ai_generated, price,
              media_paths,
              files)

        # Update json file
        with open('schedules.json', 'r') as f:
            data = json.load(f)["schedule_data"]
            data.append({
                "index": len(data) + 1,
                "uploading_method": uploading_method,
                "interval": interval,
                "post_date": post_date,
                "post_time": post_time,
                "description_type": description_type,
                "description": description,
                "ai_generated": ai_generated,
                "price": price,
                "media_paths": media_paths,
                'platform': platform
            })

        with open('schedules.json', 'w') as f:
            json.dump({"schedule_data": data}, f)

    return "Schedule Data"


@app.route('/delete_schedule', methods=['GET', 'POST'])
def delete_schedule():
    if request.method == 'POST':
        with open('schedules.json', 'r') as f:
            data = json.load(f)["schedule_data"]
            index_of_schedule = int(request.form['index']) - 1
            media_paths = data[index_of_schedule]['media_paths']

            for media_path in media_paths:
                try:
                    os.remove(media_path)
                except:
                    pass

            data.pop(index_of_schedule)

            for i in range(len(data)):
                data[i]['index'] = i + 1

        with open('schedules.json', 'w') as f:
            json.dump({"schedule_data": data}, f)
        print("deleted")

    return "Schedule Deleted"


# ----------------------------------------------------- #
@app.route('/tester', methods=['GET', 'POST'])
def home():
    with open('schedules.json', 'r') as f:
        data = json.load(f)["schedule_data"]

    if request.method == 'POST':
        print(request.form)

    return render_template('tester.html', schedules_data=data)


# ----------------------------------------------------- #


@app.route('/suggest_caption', methods=['GET', 'POST'])
def suggest_caption():
    descriptions = get_file_data("AI Generated Text")
    print(descriptions)
    return random.choice(descriptions)


@app.route('/change_schedules', methods=['GET', 'POST'])
def change_schedules():
    if request.method == 'POST':

        with open('schedules.json', 'r') as f:
            data = json.load(f)["schedule_data"]
            hour = int(request.form['interval'])

        # change data post_date and post_time to hour + hour from now
        previous_time = datetime.now()
        for i in range(len(data)):
            date_now = datetime.now().strftime("%Y-%m-%d")
            time_now = previous_time + timedelta(hours=hour)
            time_now = time_now.strftime("%H:%M")
            previous_time = datetime.strptime(time_now, '%H:%M')

            data[i]['post_date'] = date_now
            data[i]['post_time'] = time_now

        with open('schedules.json', 'w') as f:
            json.dump({"schedule_data": data}, f)
        print("changed")
        return "Schedules Changed"


@app.route('/sia_home', methods=['GET', 'POST'])
def tester():
    with open('schedules.json', 'r') as f:
        data = json.load(f)["schedule_data"]
        data = [schedule for schedule in data if schedule['platform'] == 'onlyfans']

    if request.method == 'POST':
        print(request.form)

    return render_template('Home.html', schedules_data=data)


@app.route('/tiktok_page', methods=['GET', 'POST'])
def tiktok_page():
    with open('schedules.json', 'r') as f:
        data = json.load(f)["schedule_data"]

    if request.method == 'POST':
        print(request.form)

    return render_template('TikTok.html', schedules_data=data)


@app.route('/twitter_page', methods=['GET', 'POST'])
def twitter_page():
    with open('schedules.json', 'r') as f:
        data = json.load(f)["schedule_data"]
        data = [schedule for schedule in data if schedule['platform'] == 'twitter']




    if request.method == 'POST':
        print(request.form)

    return render_template('Twitter.html', schedules_data=data)


if __name__ == '__main__':
    # app.run(port=8000, host='0.0.0.0', debug=True)
    webview.create_window('SiA', app, min_size=(800, 600))
    webview.start()
