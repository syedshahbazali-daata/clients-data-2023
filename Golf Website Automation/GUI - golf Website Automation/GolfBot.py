import base64
# encoding: utf-8
from flask import Flask, render_template, request, redirect, url_for, flash
import json
from Bot import *
import webview
from threading import Thread
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

app = Flask(__name__)

window = webview.create_window('Golf Bot', app, width=1280, height=720)



@app.route('/', methods=['GET', 'POST'])
def index():
    with open('profile-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    profile_data = data  # data is a dictionary (USERNAME/PWD)
    if request.method == 'POST':
        # print(request.form)
        profile_data['username'] = request.form['username']
        profile_data['password'] = request.form['password']

        with open('profile-data.json', 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=4)
        return redirect(url_for('main', running=False))

    return render_template('index.html', profile_data=profile_data)


@app.route('/main/<running>', methods=['GET', 'POST'])
def main(running):
    print(running)
    with open('profile-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    profile_data = data

    all_times = ['11:00 AM', '11:10 AM', '11:20 AM', '11:30 AM', '11:40 AM', '11:50 AM', '12:00 PM', '12:10 PM',
                 '12:20 PM', '12:30 PM', '12:40 PM', '12:50 PM', '1:00 PM', '1:10 PM', '1:20 PM', '1:30 PM', '1:40 PM',
                 '1:50 PM', '2:00 PM', '2:10 PM', '2:20 PM', '2:30 PM', '2:40 PM', '2:50 PM', '3:00 PM', '3:10 PM',
                 '3:20 PM', '3:30 PM', '3:40 PM', '3:50 PM', '4:00 PM', '4:10 PM', '4:20 PM', '4:30 PM', '4:40 PM',
                 '4:50 PM', '5:00 PM', '5:10 PM', '5:20 PM', '5:30 PM', '5:40 PM', '5:50 PM', '6:00 PM', '6:10 PM',
                 '6:20 PM', '6:30 PM', '6:40 PM', '6:50 PM', '7:00 PM', '7:10 PM', '7:20 PM', '7:30 PM', '7:40 PM',
                 '7:50 PM', '8:00 PM', '8:10 PM', '8:20 PM', '8:30 PM', '8:40 PM', '8:50 PM', '9:00 PM', '9:10 PM',
                 '9:20 PM', '9:30 PM', '9:40 PM', '9:50 PM', '10:00 PM', '10:10 PM', '10:20 PM', '10:30 PM', '10:40 PM',
                 '10:50 PM', '11:00 PM', '11:10 PM', '11:20 PM', '11:30 PM', '11:40 PM', '11:50 PM']
    available_times = get_file_data("available-times.txt")

    # a new_list in which unique values from all_times will be appended and not the values from available_times
    new_list = []
    for i in all_times:
        if i not in available_times:
            new_list.append(i)
    all_times = new_list

    if request.method == 'POST':
        new_time = request.form['time']
        # add new_time
        with open('available-times.txt', 'a', encoding='utf-8') as f:
            f.write(f'{new_time}\n')

        return redirect(url_for('main', running=False))

    return render_template('main.html', profile_data=profile_data, available_times=available_times, all_times=all_times,running=str(running))


@app.route('/delete/<string:time>', methods=['GET', 'POST'])
def delete(time):
    print(time)

    available_times = get_file_data("available-times.txt")
    available_times.remove(time)
    with open('available-times.txt', 'w', encoding='utf-8') as f:
        for i in available_times:
            f.write(f'{i}\n')
    return redirect(url_for('main', running=False))


@app.route('/run-bot', methods=['GET', 'POST'])
def run_bot():
    Thread(target=run_chrome_bot).start()
    return redirect(url_for('main', running=True))


if __name__ == '__main__':
    # app.run(debug=True)
    webview.start()
