from flask import Flask, render_template, request, redirect, url_for
import grequests
import schedule
import datetime

app = Flask(__name__)

def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        urls_list = f.read().strip().split('\n')
    return urls_list


def send_requests():
    print(datetime.datetime.now())
    urls_list = get_file_data('urls.txt')
    rs = (grequests.get(u) for u in urls_list)
    responses = grequests.map(rs)
    results = []
    for response in responses:
        url = response.url
        status_code = response.status_code
        results.append([url, status_code])
    return results


schedule.every(1).minutes.do(send_requests)




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        website_url = request.form['website-url']
        with open('urls.txt', 'a') as f:
            f.write(website_url + '\n')
        return redirect(url_for('index'))
    return render_template('live.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
