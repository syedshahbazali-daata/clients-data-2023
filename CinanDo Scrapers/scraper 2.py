import csv

import requests
import threading

total_scraped = 0


def scraper(start_x: int, scraper_name: str, end: int):
    start = start_x
    index_x = 0
    while True:
        url = "https://cinando.com/en/People/Search"
        if start > end:
            print(f"{scraper_name} finished")

        payload = f"Start={start}&Length=500&SortColumn=name&SortDir=asc&criteria%5BQuery%5D=&criteria%5BKeyword%5D=&criteria%5BCountryAdvanced%5D=false&criteria%5BCompanyActivityMain%5D=false&criteria%5BPeopleActivityMain%5D=false&criteria%5BCliste%5D=&criteria%5BEditable%5D=false&criteria%5BOnsiteOnly%5D=false&DontUpdateLength=false"
        headers = {
            "cookie": "cinandoConsent=\u0021analytics=true; cinando_stay-connected=EAAAAMcNMxD+TeuOGA1oU4JLxy9vXyFisjC226FjU/T1qDrP58l6CARnD0yGR0AmfaRzcA==; ASP.NET_SessionId=avhtlxdoeyqdviclezxov2by; current_market=||; ItemsPerPage=40",
            "authority": "cinando.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://cinando.com",
            "referer": "https://cinando.com/en/Search/People",

            "sec-ch-ua-mobile": "?0",

            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        result = response.json()['results']

        if len(result) == 0:
            print("No more data")
            quit()

        global total_scraped

        for index, r in enumerate(result):
            total_scraped += 1
            name = r['Name']
            country = r['TxtCountry']
            company_country = r.get('TxtLocalisation', 'NA')
            email = r.get('Email', 'NA')
            mobile = r.get('Mobile', 'NA')
            activities = r['Activities']
            if activities is None:
                activities = []
            activities_list = []
            for activity in activities:
                try:
                    activity = activity['Name']
                    activities_list.append(activity)
                except:
                    pass

            activities_names = ', '.join(activities_list)

            record = [name, country, company_country, email, mobile, activities_names]

            with open('people-new.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(record)

        start += 500
        print("start: ", start, "len: ", len(result), scraper_name, total_scraped)
        if start > end:
            break



scraper(0, "scraper 1", 66000)

