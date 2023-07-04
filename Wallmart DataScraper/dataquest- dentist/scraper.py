import requests
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome options to open the developer tools
chrome_options = Options()
chrome_options.add_argument("--auto-open-devtools-for-tabs")

# Set up the Chrome driver

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://dentaquest.healthsparq.com/healthsparq/public/#/one/&city=&insurerCode=DENTAQUEST_I&brandCode=DQSTANDARD/search/isPromotionSearch=false&location=Michigan%252C%2520US&page=4&productCode=DQSBCCOM&radius=25&searchCategory=GENERAL&sort=BEST_MATCH')

time.sleep(8)
cookies_data = driver.get_cookies()
cookies_string = ""
for i in cookies_data:
    cookies_string += i["name"] + "=" + i["value"] + "; "

driver.quit()


with open('dentaquest-data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # headers: [doctor_name, clinic_name, complete_address, phone, email_address,special_attributes, web_site, accepting_new_patients]
    writer.writerow(['Doctor Name', 'Clinic Name', 'Complete Address', 'Phone', 'Email Address', 'Special Attributes', 'Web Site', 'Accepting New Patients'])


page_number = 1
while True:

    url = "https://dentaquest.healthsparq.com/healthsparq/public/service/v4/search"

    payload = {
        "guid": "551f676c-9807-4f61-8caa-003e291295fd",
        "languageCode": "EN",
        "isPromotionSearch": False,
        "location": "Michigan, US",
        "page": page_number,
        "productCode": "DQSBCCOM",
        "radius": 25,
        "searchCategory": "GENERAL",
        "sort": "BEST_MATCH",
        "locationDetails": {
            "city": "",
            "county": None,
            "line1": "",
            "outOfState": None,
            "state": "Michigan",
            "stateCode": "MI",
            "empty": False,
            "isGeocoded": True,
            "isDefault": False,
            "display": "Michigan, US",
            "zip": "",
            "country": "US",
            "countyName": "",
            "countyType": "",
            "latitude": 44.9337458924535,
            "longitude": -84.525239999781,
            "locationType": "STATE",
            "score": 0.7
        }
    }
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "Connection": "keep-alive",
        "Cookie": cookies_string,
        # "Cookie": "_ga=GA1.1.478393331.1688137674; _ga_V89DNZFP5J=GS1.1.1688137675.1.1.1688137876.0.0.0; _gid=GA1.2.1359945376.1688137674; _ga=GA1.1.478393331.1688137674; prev_page_ppv=100; ANALYTICS_ID=924940073528043.1688211378806; visit_num=1; visit_num=1; tealiumid=01890cd8983f004e64d6c60c7d980506f00fa0670086e; trace-session-id=c75958c3-2816-494a-b792-55d09991018a; SESSION=YzQ3N2NmNzItNzYxNi00M2E3LWE5NjEtZDFkNTZjNzg1OGQ3; _gid=GA1.2.1925431458.1688211390; utag_main=v_id:01890cd8983f004e64d6c60c7d980506f00fa0670086e$_sn:2$_se:12$_ss:0$_st:1688213567231$_ga:01890cd8983f004e64d6c60c7d980506f00fa0670086e$ses_id:1688211762726%3Bexp-session$_pn:1%3Bexp-session; _ga_V89DNZFP5J=GS1.1.1688211391.1.1.1688211765.0.0.0; tealiumid=0189113d68ea0089d6d591153a880506f00fa0670086e; utag_main=v_id:01890cd8983f004e64d6c60c7d980506f00fa0670086e$_sn:1$_se:57$_ss:0$_st:1688139676778$ses_id:1688137668675%3Bexp-session$_pn:4%3Bexp-session$_ga:01890cd8983f004e64d6c60c7d980506f00fa0670086e; ANALYTICS_ID=544811378017567.1688137667062;",
        "Origin": "https://dentaquest.healthsparq.com",
        "Referer": "https://dentaquest.healthsparq.com/healthsparq/public/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "content-type": "application/json",

        "sec-ch-ua-mobile": "?0",

    }
    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.json()['providerResults']
    if len(data) == 0:
        break

    for i in data:

        doctor_name = i.get('provider', {}).get('fullName', '')
        clinic_name = i.get('location', {}).get('name', '')

        street_address = i.get('location', {}).get('address', {}).get('line1', '')
        city = i.get('location', {}).get('address', {}).get('city', '')
        state = i.get('location', {}).get('address', {}).get('state', '')
        zip_code = i.get('location', {}).get('address', {}).get('zip', '')
        complete_address = f'{street_address}, {city}, {state}, {zip_code}'.strip()

        phone = i.get('location', {}).get('phone', '')

        # i['attributes'][0]['value']
        try:
            special_attributes = i['attributes'][0]['value']
            special_attributes = ', '.join(special_attributes)

        except:
            special_attributes = ''

        try:
            email_address = i['attributes'][4]['value'][1]['values'][0]['url']
        except:
            email_address = ''

        try:
            web_site = i['attributes'][4]['value'][2]['values'][0]['url']
        except:
            web_site = ""

        try:
            accepting_new_patients = i['elevatedAttributes'][0]['messages'][0]['content']
            if accepting_new_patients == 'Accepting new patients':
                accepting_new_patients = 'Y'
        except:
            accepting_new_patients = 'N'


        row = [doctor_name, clinic_name, complete_address, phone, email_address,special_attributes, web_site, accepting_new_patients]


        with open('dentaquest-data.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    page_number += 1
    print("Page Number: ", page_number)

