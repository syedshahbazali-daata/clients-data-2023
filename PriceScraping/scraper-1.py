import csv

import pandas as pd
import requests
from requests_html import HTMLSession
import re
from bs4 import BeautifulSoup

def clean_urls(urls_links):
    links = []
    for i in urls_links:
        if "http" in str(i).lower():
            links.append(i)

    links = list(set(links))
    print("Total link: ", len(links))
    return links


import requests


def amazon_scraper(url_x):
    payload = ""
    headers = {
        "authority": "www.amazon.ae",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en;q=0.9",
        "cookie": """session-id=259-4023346-6383354; session-id-time=2082787201l; i18n-prefs=AED; ubid-acbae=257-0675672-3490314; session-token="50almzfTImLrw6lgRDpVPDFwL2LCS+GyCy/pyLiE+P3xgxa2Cv5tIXvECCjC+ZagIBE8hnuWoxm3MP18a3qnmqoAgemOwflrpxQhADLZeJjn9y4Z2Kr0Bss4Udl7dUzBUDzr2o0zHyGyep0LsaRbazqZ/1InksZledfERDcHhrOec2iOPJNAtTLpnn8TQqDgEZMwWahoYOskiyp9YthK114ryOVqD6NLHfaJ2sdkJm8="; csm-hit=tb:WXH9CG0XKJDC8FM62BYR+s-WXH9CG0XKJDC8FM62BYR|1686868650041&t:1686868650041&adb:adblk_no""",
        "device-memory": "8",
        "downlink": "10",
        "dpr": "0.9",
        "ect": "4g",
        "rtt": "100",

        "sec-ch-dpr": "0.9",

        "sec-ch-ua-mobile": "?0",

        "sec-ch-viewport-width": "792",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "service-worker-navigation-preload": "true",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "viewport-width": "792"
    }

    session = HTMLSession()
    response = session.get(url_x, headers=headers)

    page_source = str(BeautifulSoup(response.text, 'html.parser'))

    print(page_source)
    print(url_x)
    quit()

    try:
        discounted_price = re.findall(r'"priceAmount":([^,]+)', page_source)
        discounted_price = str(discounted_price[0]).replace(',', '').strip()
    except:
        discounted_price = "NOT FOUND"

    try:
        old_price = re.findall(r'List Price:.*">AED([^<]+)', page_source)
        old_price = str(old_price[0]).replace(',', '').strip()
    except:
        old_price = "NOT FOUND"

    if old_price == "NOT FOUND" and discounted_price != "NOT FOUND":
        old_price = discounted_price
        discounted_price = "NOT FOUND"
    elif old_price == "NOT FOUND" and discounted_price == "NOT FOUND":
        with open('wrong_links.txt', 'a', encoding='utf-8') as wrong_file:
            wrong_file.write(url_x + "\n")

    return discounted_price, old_price


df = pd.read_csv('products.csv')

# NOON SCRAPING
amazon_links = df['Web Link'].tolist()
amazon_links = clean_urls(amazon_links)

# amazon_links = [
#     'https://www.amazon.ae/2021-Apple-8-3-inch-Wi-Fi-Cellular/dp/B09G93JWDQ/ref=sr_1_10?crid=1H0QIW3MSDUS8&keywords=iPad%2BMini%2B6&qid=1675532727&sprefix=ipad%2Bmini%2B6%2Caps%2C363&sr=8-10&th=1']
for i in amazon_links:
    result_amz = amazon_scraper(i)
    print(i)
    print(result_amz)

    with open('products_x.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([i, result_amz[0], result_amz[1], "amazon"])
