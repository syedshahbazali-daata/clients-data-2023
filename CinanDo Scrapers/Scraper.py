import csv

import requests
from bs4 import BeautifulSoup
from xextract import String

import threading


def thread_request(url_x, name_x, country_x, ind):
    res_x = requests.request("GET", url_x, headers=headers)
    page = res_x.text
    soup = BeautifulSoup(page, 'html.parser')

    # get email
    try:
        company_email = String(xpath='//div[@class="links"]//li//a[contains(@href, "mailto")]').parse_html(str(soup))[0]
    except:
        company_email = "NA"

    try:
        phone_number = String(xpath='//*[@class="phone"]').parse_html(str(soup))[0]
    except:
        phone_number = "NA"

    try:
        activities = String(xpath="//*[text()='Activity']/..//strong").parse_html(str(soup))
        activities = ", ".join(activities)
    except:
        activities = "NA"

    print(f"{ind} | {name_x} | {country_x} | {company_email} | {phone_number} | {activities}")
    with open('company_data.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([url_x, name_x, country_x, company_email, phone_number, activities])


start = 0

index_x = 0
while True:
    url = "https://cinando.com/en/Company/Search"

    payload = f"Start={start}&Length=500&SortColumn=name&SortDir=asc&criteria%5BQuery%5D=&criteria%5BKeyword%5D=&criteria%5BCountryAdvanced%5D=false&criteria%5BActivityMain%5D=false&criteria%5BOtherTerritories%5D=&criteria%5BCliste%5D=&criteria%5BEditable%5D=false&DontUpdateLength=false"
    headers = {
        "cookie": "cinandoConsent=\u0021analytics=true; cinando_stay-connected=EAAAAMcNMxD+TeuOGA1oU4JLxy9vXyFisjC226FjU/T1qDrP58l6CARnD0yGR0AmfaRzcA==; ASP.NET_SessionId=knhprzadgkz25feptjhdhrgt; current_market=||; ItemsPerPage=40",
        "authority": "cinando.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://cinando.com",
        "referer": "https://cinando.com/en/Search/Companies",

        "sec-ch-ua-mobile": "?0",

        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    result = response.json()['results']

    print("start: ", start, "len: ", len(result))
    if len(result) == 0:
        print("No more data")
        quit()

    for index, r in enumerate(result):
        name = r['Name']
        country = r['TxtCountry']

        url = "https://cinando.com" + str(r['Link'])

        index_x += 1
        with open('company_data_test.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([index_x, name, country, url])
        # threading.Thread(target=thread_request, args=(url, name, country, index_x)).start()

    start += 50


    # Name | Company | Country (of company) | Activity | Email (if any) | phone
