import requests
from bs4 import BeautifulSoup
from concurrent import futures as cf  # Rename the module import
from xextract import String
import re
import csv

# install multiple modules at once: pip install pyperclip pandas
start_from = 1

def get_file_data(file_name):
    with open(file_name, "r") as f:
        file_data = f.read().strip().split("\n")
    return file_data

def list_into_chunks(list_name, chunk_size):
    for i in range(0, len(list_name), chunk_size):
        yield list_name[i:i + chunk_size]

def process_response(response):
    product_url = response.url
    html = response.text

    soup = str(BeautifulSoup(html, "html.parser"))
    images = String(xpath='//picture/img', attr='data-src').parse_html(soup)
    images = list(set([x for x in images if len(x) > 3]))
    images = ",".join(images)

    page_source = str(response.text).replace("\n", "")
    try:
        variant_data = str(re.findall(r'variants:(.*?])', page_source)[0])
        variant_data = re.findall(r'name:"(.*?)"', variant_data)
        variant_data = ",".join(variant_data)
    except:
        variant_data = ""

    try:
        data = re.findall(r'content="product">.*?>([\s\S]*?)<\/script>', page_source)[0]
        print(data)
    except:
        print("-------------------------")
        print(product_url)
        print("-------------------------")
        return

    # convert into a dictionary
    data = eval(data)
    name_of_product = data.get("name", "")
    sku = data.get("sku", "")
    description = data.get("description", "")
    price = data.get("offers", {}).get("price", "")
    availability = data.get("offers", {}).get("availability", "")
    color = data.get("color", "")

    ebay_category = ""

    record = [product_url, name_of_product, sku, description, price, availability, images, variant_data, color, ebay_category]

    with open("jdsports.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(record)
    print(record)

from_ = 1
while True:

    main_url = str(get_file_data('url.txt')[0]) + "&AJAX=1"
    main_url = re.sub(r"from=\d+", f"from={start_from}", main_url)
    print(main_url)

    response = requests.get(main_url)

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



complete_data = list(set(get_file_data("jdsports.txt")))
urls_list = list(list_into_chunks(complete_data, 100))
session = cf.ThreadPoolExecutor(max_workers=10)

for single_chunk in urls_list:
    futures_list = [session.submit(requests.get, u) for u in single_chunk]  # Rename the variable
    responses = cf.wait(futures_list, timeout=None)  # Use the renamed variable
    for future in responses.done:
        response = future.result()
        process_response(response)

session.shutdown()