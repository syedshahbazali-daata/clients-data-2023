import grequests
import requests
from bs4 import BeautifulSoup
from xextract import String
import re
import csv
start_from = 1


def get_file_data(file_name):
    with open(file_name, "r") as f:
        file_data = f.read().strip().split("\n")

    return file_data


def list_into_chunks(list_name, chunk_size):
    for i in range(0, len(list_name), chunk_size):
        yield list_name[i:i + chunk_size]


while True:
    main_url = f"https://m.jdsports.co.uk/men/brand/adidas,nike,mckenzie,crocs,adidas-originals,converse,the-north-face,timberland,lacoste,vans,jordan,reebok,under-armour,puma,polo-ralph-lauren,emporio-armani-ea7,fila,levis,fred-perry,juicy-couture,pink-soda-sport,supply-and-demand,tommy-hilfiger,billionaire-boys-club,ugg,calvin-klein,new-balance,boss,tommy-jeans,napapijri,hoodrich,sonneti,hugo,champion,ea7,gym-king,11-degrees,calvin-klein-jeans,nicce,clarks-originals,guess,align,mercier/sale/?from={start_from}&priceband-gbp=20%3Cprice%3C101&sort=price-low-high&AJAX=1"
    response = requests.get(main_url)
    print(main_url)
    soup = BeautifulSoup(response.text, "html.parser")
    # //*[@class="itemTitle"]/a to css: .itemTitle > a

    list_of_products = soup.find_all("a", {"data-e2e": "product-listing-name"})
    list_of_products = ["https://m.jdsports.co.uk" + x.get("href") for x in list_of_products]
    total_products = len(list_of_products)
    if total_products == 0:
        break
    start_from += total_products
    print("Total Products: ", start_from)
    with open("jdsports.txt", "a") as f:
        for product in list_of_products:
            f.write(product + "\n")

complete_data = get_file_data("jdsports.txt")
urls_list = list(list_into_chunks(complete_data, 100))
for single_chunk in urls_list:
    res = grequests.map((grequests.get(u) for u in single_chunk))
    for r in res:
        product_url = r.url
        html = r.text
        soup = str(BeautifulSoup(html, "html.parser"))
        images = String(xpath='//picture/img', attr='data-src').parse_html(soup)
        images = list(set([x for x in images if len(x) > 3]))
        images = ",".join(images)

        page_source = str(r.text).replace("\n", "")

        try:
            data = re.findall(r'content="product">.*?>([\s\S]*?)<\/script>', page_source)[0]
        except:
            print("-------------------------")
            print(product_url)
            print("-------------------------")
            continue
        # convert into a dictionary
        data = eval(data)
        name_of_product = data.get("name", "")
        sku = data.get("sku", "")
        description = data.get("description", "")
        price = data.get("offers", {}).get("price", "")
        availability = data.get("offers", {}).get("availability", "")

        ebay_category = ""

        record = [product_url, name_of_product, sku, description, price, availability, images, ebay_category]
        with open("jdsports.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(record)
        print(record)
