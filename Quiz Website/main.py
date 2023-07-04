import csv
from datetime import datetime, timedelta

import schedule as schedule
from flask import Flask, render_template, request, redirect, url_for
import time
import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
sheet_url = 'https://docs.google.com/spreadsheets/d/1UCSWTwrnI5RPflnBw40YZfcT8uV-3AGCI7NUfHbQmSo/edit?usp=sharing'

creds_sheet = ServiceAccountCredentials.from_json_keyfile_name(
    r"GoogleSheetsApi.json", scope)
client = gspread.authorize(creds_sheet)

print("Google Sheets API Connected")
# FUNCTION TO GET THE DATA FROM THE GOOGLE SHEET

questions_bank = []


def get_questions():
    while True:
        try:
            questions_bank.clear()
            sheet = client.open_by_url(sheet_url).sheet1
            complete_data = list(sheet.get_all_values())
            for row in complete_data:
                questions_bank.append(row)
            break
        except:
            time.sleep(20)
    return True


def convert_list_into_chunks_2d(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# run get_questions() function after every 10 minutes
get_questions()
schedule.every(10).minutes.do(get_questions)

app = Flask(__name__)


@app.route('/quiz-trial/<int:pagenum>')
def quiz_trial(pagenum):
    license_code = "free"
    print(license_code)
    global questions_bank
    pagenum = pagenum - 1
    if license_code == "free":
        trial_questions_data = [question for question in questions_bank[1:] if str(question[7]).lower() == "free"]
        trial_questions_data = list(convert_list_into_chunks_2d(trial_questions_data, 10))
    else:
        trial_questions_data = [question for question in questions_bank[1:]]
        trial_questions_data = list(convert_list_into_chunks_2d(trial_questions_data, 10))

    trial_questions = trial_questions_data[pagenum]
    # add index to each question
    for i in range(len(trial_questions)):
        trial_questions[i] = [i + 1] + trial_questions[i]

    try:
        next_page = trial_questions_data[pagenum + 1]

        next_page_available = "true"

    except:
        next_page_available = "false"

    current_page = pagenum + 1

    return render_template('quiz.html', questions=trial_questions, next_page_available=next_page_available,
                           current_page=current_page, license_code=license_code)


@app.route('/unlimited-access')
def unlimited_access():
    return render_template('unlimited-access.html')


@app.route('/test-system')
def tester():
    global questions_bank

    questions_world = []
    trial_questions_data = [question for question in questions_bank[1:] if str(question[7]).lower() == "free"]
    for i in range(len(trial_questions_data)):
        x = {
            'numb': i + 1,
            'question': f"{trial_questions_data[i][0]}",
            'answer': f'{trial_questions_data[i][3]}',
            'options': [
                f'{trial_questions_data[i][1]}',
                f'{trial_questions_data[i][2]}',
                f'{trial_questions_data[i][3]}',
                f'{trial_questions_data[i][4]}',
                f'{trial_questions_data[i][5]}'

            ]
        }
        print(trial_questions_data[i][1], trial_questions_data[i][2], trial_questions_data[i][3],
              trial_questions_data[i][4], trial_questions_data[i][5])
        questions_world.append(x)

    random.shuffle(questions_world)
    questions_world = questions_world[:10]

    return render_template('tester.html', questions=questions_world)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = str(request.form['email']).lower()
        password = request.form['pass']

        # Check if user exists
        with open('users.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if str(row[0]).lower() == email and row[1] == password:
                    return redirect(url_for('quiz_trial', pagenum=1))

        return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get form data

        email = request.form['email']
        password = request.form['pass']
        license_code = request.form['license']
        print(email, password, license_code)


        # Save user data to CSV
        with open('users.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, password, license_code, datetime.now().strftime('%d-%m-%Y'),
                             (datetime.now() + timedelta(days=365)).strftime('%d-%m-%Y')])

        return redirect(url_for('login'))
    else:
        return render_template('sign_up.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
