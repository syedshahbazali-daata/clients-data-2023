import csv

import grequests
from bs4 import BeautifulSoup
from xextract import String
import pandas as pd


def thread_request(url_x, name_x, country_x, ind):
    res_x = grequests.request("GET", url_x, headers=headers)
    page = res_x.text
    soup = BeautifulSoup(page, 'html.parser')



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

def batch_list(lst, n)->list:
    print(f"Batching list of size {len(lst)}")
    # reutrn list of lists of size n
    for i in range(0, len(lst), n):
        yield lst[i:i + n]




df = pd.read_csv("company_data_test.csv")

urls = df['url'].tolist()
names = df['title'].tolist()
countries = df['country'].tolist()

sub_lists = list(batch_list(urls, 10))

for ind, sub_list in enumerate(sub_lists):
    print(len(sub_list))
    print(ind)
    continue
    print(f"Batch {ind}")
    rs = (grequests.get(u, headers=headers) for u in sub_list)
    responses = grequests.map(rs)
    for ind, response in enumerate(responses):
        try:
            url_x  = str(response.url)
        except:
            url_x = "NA"


        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            company_email = \
            String(xpath='//div[@class="links"]//li//a[contains(@href, "mailto")]').parse_html(str(soup))[0]
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

        with open('company_data.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([url_x, company_email, phone_number, activities])



    print("Batch Done")

    # time.sleep(1)



