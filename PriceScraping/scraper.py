import time
import pandas as pd
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import csv
import re


def get_text_soon(ele):
    found = False
    for i in range(10):
        try:
            text = driver.find_element(By.XPATH, ele).text
            found = True
            return text
        except:
            time.sleep(1)
    if not found:
        text = "NA"
        return text


def amazon_scraper(url):
    driver.get(url)

    whole_price = get_text_soon('//*[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-whole"]')
    fraction_price = get_text_soon('//*[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-fraction"]')
    fixed_price = f"{whole_price}.{fraction_price}"

    old_price = get_text_soon(
        '//*[@id="corePriceDisplay_desktop_feature_div"]//*[contains(text(), "List Price:")]/span')
    old_price = old_price.replace("AED", "")

    return fixed_price, old_price


def menakart_scraper(url):
    driver.get(url)

    fixed_price = get_text_soon('//div[@class="product-main-content"]//span[@data-price-type="finalPrice"]/span')
    old_price = get_text_soon('//div[@class="product-main-content"]//span[@data-price-type="oldPrice"]/span')

    fixed_price = fixed_price.replace("AED", "")
    old_price = old_price.replace("AED", "")
    fixed_price.strip()
    old_price.strip()

    if old_price == "NA" or old_price == "" and fixed_price != "NA":
        old_price = fixed_price
        fixed_price = "NA"

    return fixed_price, old_price


def carrefour_scraper(url):
    driver.get(url)

    fixed_price = get_text_soon('//main[@id="content"]//*[@class="total--sale-price"]')
    old_price = get_text_soon('//main[@id="content"]//*[@class="cross-price"]/span[@class="strike"]')

    fixed_price = fixed_price.upper().replace("AED", "")
    old_price = old_price.upper().replace("AED", "")
    fixed_price.strip()
    old_price.strip()

    return fixed_price, old_price


def clean_urls(urls_links):
    links = []
    for i in urls_links:
        if "http" in str(i).lower():
            links.append(i)

    links = list(set(links))
    print("Total link: ", len(links))
    return links


def noon_scraper(product_url: str):
    perma_link = product_url.split(".com/")[-1].replace("uae-en/", "")

    api_link = f"https://www.noon.com/_svc/catalog/api/v3/u/{perma_link}"
    headers = {
        "cookie": "visitor_id=3ccc47b2-70fd-45a5-abe1-3e365d96ea11; x-available-ae=ecom-daily; __zlcmid=1GCls7vZnq7oWp3; AKA_A2=A; ak_bmsc=5EEDD636C128CF989B2D89549117CAEB~000000000000000000000000000000~YAAQl9sNF4+ROaeIAQAAD/eWvhTLGqGrBNwOPzAeNkW37zwqgxIyS+ZUxgX1Fenna02GeG5nyulWPrpaai4X+NO+W9c0n10V/XvJpY4P2BaVzMhlDMB7MMvvYHWI+BDvkVGepw77msh9ET8evyYKbINYgQZCzXMppbelCKZVELDFhQT1hfzQAV17sGnRBmuCO6+NCnHkuS2tmTXg3eI7CQkSQ70Oh0hkGQEjXIPCyZOAOs3QB+71TCPbavrqBHJXwmIeWRRVw/QUJmoTsZNNT+tmtW+BTO0rHRDGB22Qn8DqMQGqWtrEgF0CG6RCa+ZapYLq1vlXdZXTV0k6VTPNTkiWLL7KHL0uLta0dMavppJ7bewTdPMBoAxkqKxmvATatt8Tj+vRYI8=; bm_mi=DC8309B039C55CA63D8E4F74C8943935~YAAQl9sNF8DbOaeIAQAAsP2gvhRB0THJ38mnYXJ+kweANQxvm4+Ang/X4+zoRMkpClvndGvQpelQV+bHBW/nwMop1zqQ/ijPVjE/OqhuogLaBQ8KgZ0jsh0mh1QzHkPuaJ1ES0h4c4N4uLfEuJlAqu1IpIf4lKNXAfhn2JEEbQHDUoEs9ClT372N/CDaEuQohRFhwheIjAMlFzysZphXG0C+63l0Gav2FXw9rk9rND56UznCGIkn7rfbPv5gyMkYvPR47J4543gdmYA43zbo1eeGeAiol1SlXzpv+N1zIX/BaOGGdm3Ofs++T2VJX/8EZK62h5ON8E566S1mtzvSjqtuqfAdlD5C/UbpL8P8QIvxD7Cw1J1hzi1Pb/ZeViv5/t7OMpy1~1; nguest=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnJhV1FpT2lKbVlqYzNZakU0TWpWbVpXVTBOalF6WWpGbU1UZzBOREJqWmpNNU5EUmlOaUlzSW1saGRDSTZNVFk0TlRrd016WXlNSDAuekJuaFRGbHNPWFZLaTJSYWt2LWh5SEozTjRNLWgyRGxNRV9hUWVETE5IYyIsImlhdCI6MTY4NjgyNjI1MX0.b7B5gpLZBPg-rrZ6nD84vZc7asXjQmcyjmqRn45bksg; _nsc=nsv1.public.eyJzdGlkIjoiMWNmN2NiZGUtM2M3Zi00YTQwLTlhZmItZWQzNWYwZjU3NWQ3Iiwic2lkIjoiZmI3N2IxODI1ZmVlNDY0M2IxZjE4NDQwY2YzOTQ0YjYiLCJpYXQiOjE2ODY4MjYyNTEsInZpZCI6IjNjY2M0N2IyLTcwZmQtNDVhNS1hYmUxLTNlMzY1ZDk2ZWExMSIsImhvbWVwYWdlIjp7fX16elMxejQ4UStyellaUTAwQXNnaFpNbUNwQVZ2OUhjeCsydHlGdHJSN01RPQ.MQ; bm_sv=E81249E120545DA45074855AB8ACA704~YAAQPmjdWJpv+6+IAQAA1+SvvhTGi/mPam+mNAC8a3zfnA70BUpP7av2+kJBKMqV6jr/Z8MLP3RUa8NxUku+jTCiVDqlMLUq88daavZ0dIEc6QX6tn5E9W/eCw5GtoHsiLE8xmKp1orH8u2tutAK609d0hS1vdmN6Zj1fgL2ZUMUBKWfG627K9aKawB/j9PepDsGCUgFnomFTtzu5PRruYtPpxSYV2SmIzOE0TLO21cM/o0/5Vr74COR+28IS0g=~1",
        "authority": "www.noon.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "cache-control": "max-age=0",

        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        json_res = requests.get(api_link, headers=headers)
        json_res = json_res.json()
        old_price = json_res['product']['variants'][0]['offers'][0]['price']
        discount_price = json_res['product']['variants'][0]['offers'][0]['sale_price']
        return discount_price, old_price

    except:
        return "NA", "NA"


def istyle_scraper(url):
    driver.get(url)

    special_price = get_text_soon('//*[@id="product-view-top-row"]//*[@class="special-price"]')
    if special_price != "NA":
        fixed_price = special_price
        old_price = get_text_soon('//*[@id="product-view-top-row"]//*[@class="old-price"]')
    else:
        fixed_price = get_text_soon('//*[@id="product-view-top-row"]//*[@id="final-price"]')
        old_price = "NA"

    fixed_price.replace("AED", "")
    old_price.replace("AED", "")

    if old_price == "NA" and fixed_price != "NA":
        old_price = fixed_price
        fixed_price = "NA"

    return fixed_price, old_price


df = pd.read_csv('products.csv')
driver = uc.Chrome()
# with open('products_x.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(["URL", "Discounted Price", "Original Price", "Retailer"])

# NOON SCRAPING

# noon_links = df['Web Link.1'].tolist()
# noon_links = clean_urls(noon_links)
noon_links = []
for index, product_url in enumerate(noon_links):
    print(f"current index: {index + 1} of {len(noon_links)} NOON")
    result = noon_scraper(product_url)
    print(product_url)
    print(result)
    with open('products_x.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([product_url, result[0], result[1], "noon"])

sharafdg_links = df['Web Link.4'].tolist()
for row_index, single_link in enumerate(sharafdg_links):
    print(row_index, single_link)
    # if column 6th is not empty, then skip
    if df.iloc[row_index, 18] == "NA":
        continue

    if str(single_link) == "nan":
        continue

    fixed_price_x, old_price_x = carrefour_scraper(single_link)
    print(fixed_price_x, old_price_x)

    # save in to CVS single_link, fixed_price_x, old_price_x
    with open('products_x.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([single_link, fixed_price_x, old_price_x, "sharafdg"])

menakart_links = df['Web Link.3'].tolist()
print(menakart_links)

for row_index, single_link in enumerate(menakart_links):
    print(row_index, single_link)
    # if column 6th is not empty, then skip
    if df.iloc[row_index, 15] == "NA":
        continue

    if str(single_link) == "nan":
        continue

    fixed_price_x, old_price_x = menakart_scraper(single_link)
    print(fixed_price_x, old_price_x)


    # save in to CVS single_link, fixed_price_x, old_price_x
    with open('products_x.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([single_link, fixed_price_x, old_price_x, "menakart"])

istyle_links = df['Web Link.2'].tolist()
for row_index, single_link in enumerate(istyle_links):
    print(row_index, single_link)
    # if column 6th is not empty, then skip
    if df.iloc[row_index, 13] == "NA":
        continue

    if str(single_link) == "nan":
        continue

    fixed_price_x, old_price_x = istyle_scraper(single_link)
    print(fixed_price_x, old_price_x)

    # save in to CVS single_link, fixed_price_x, old_price_x
    with open('products_x.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([single_link, fixed_price_x, old_price_x, "istyle"])

amazon_links = df['Web Link'].tolist()
for row_index, single_link in enumerate(amazon_links):
    print(row_index, single_link)
    # if column 6th is not empty, then skip
    if df.iloc[row_index, 6] == "NA":
        continue

    if str(single_link) == "nan":
        continue

    fixed_price_x, old_price_x = amazon_scraper(single_link)

    # save in to CVS single_link, fixed_price_x, old_price_x
    with open('products_x.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([single_link, fixed_price_x, old_price_x, "amazon"])

driver.quit()

df_1 = pd.read_csv('products.csv')
df_2 = pd.read_csv('products_x.csv')

urls = df_2['URL'].tolist()
fixed_price = df_2['Discounted Price'].tolist()
old_price = df_2['Original Price'].tolist()
retailers = df_2['Retailer'].tolist()

for row_index, single_link in enumerate(urls):
    if str(retailers[row_index]) == "noon":
        # change column 9th and where the link is same
        df_1.loc[df_1['Web Link.1'] == single_link, 'Discounted Price.1'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link.1'] == single_link, 'Original Price.1'] = old_price[row_index]

    elif str(retailers[row_index]) == "sharafdg":
        df_1.loc[df_1['Web Link.4'] == single_link, 'Discounted Price.4'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link.4'] == single_link, 'Original Price.4'] = old_price[row_index]

    elif str(retailers[row_index]) == "menakart":
        df_1.loc[df_1['Web Link.3'] == single_link, 'Discounted Price.3'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link.3'] == single_link, 'Original Price.3'] = old_price[row_index]

    elif str(retailers[row_index]) == "amazon":
        df_1.loc[df_1['Web Link'] == single_link, 'Discounted Price'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link'] == single_link, 'Original Price'] = old_price[row_index]

    elif str(retailers[row_index]) == "istyle":
        df_1.loc[df_1['Web Link.2'] == single_link, 'Discounted Price.2'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link.2'] == single_link, 'Original Price.2'] = old_price[row_index]

# save in new csv file: rock.csv
df_1.to_csv('Final_data.csv', index=False)
