import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

import mysql.connector

# Set database connection parameters
config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'port': '3306',
    'database': 'amazonsellerdb'
}

# Connect to the database
try:
    db = mysql.connector.connect(**config)
    print("Connected to database")
except mysql.connector.Error as err:
    print("Failed to connect to database: {}".format(err))
    exit()

# Create a cursor object to execute SQL queries
cursor = db.cursor()


def insert_record(record):
    # Connect to the MySQL database

    # Prepare the SQL query to insert the record
    sql = "INSERT INTO orders (order_id, order_asin, order_item,order_buyer_name, order_address, order_city, order_state,order_zip_code, order_sku, purchase_date, shipping_service, ship_by, deliver_by, ship_to, phone, package_weight, order_sub_total, order_tax) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = tuple(record)

    # Execute the query and commit the changes
    cursor.execute(sql, values)
    db.commit()


def find_element_send_text(ele, text, clear=True):
    while True:
        try:
            input_field = driver.find_element(By.XPATH, ele)
            if clear:
                input_field.clear()
            input_field.send_keys(text)

            break
        except:
            time.sleep(0.1)


def specific_clicker(ele):
    while True:
        try:
            element = driver.find_element(By.XPATH, ele)
            webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

            break
        except Exception as e:
            # print(e)
            pass


def specific_clicker2(ele):
    try:
        element = driver.find_element(By.XPATH, ele)
        webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

    except Exception as e:
        # print(e)
        pass


def parse_address(address):
    # Split the address string into individual fields
    fields = address.split('\n')
    print(fields)

    # Get the buyer name from the first field
    try:
        buyer_name = fields[0]
    except:
        buyer_name = "NA"

    try:
        st_address = fields[1]
    except:
        st_address = "NA"

    try:
        city = fields[2].split(',')[0]

    except:
        city = "NA"

    try:
        state = fields[2].split(', ')[1].split(' ')[0]
    except:
        state = "NA"

    try:
        zip_code = fields[2].split(', ')[1].split(' ')[-1]
    except:
        zip_code = "NA"

    # Extract the address, city, state, and zip code from the second field

    # Return the parsed address fields as a list
    result = [buyer_name, st_address, city, state, zip_code]
    print(result)
    return result


def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass


def get_text(ele):
    while True:
        try:
            element = driver.find_elements(By.XPATH, ele)
            texts = [str(x.text) for x in element][0]
            return texts
        except Exception as e:
            return "NA"


close_chrome()
options = uc.ChromeOptions()
path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
options.add_argument(fr"user-data-dir={path}")
options.add_argument(f'--profile-directory=Profile 1')
driver = uc.Chrome(options=options)
driver.maximize_window()

# ----> Scraping All Orders Pages
order_pages_url = []
page_no = 1
while True:
    driver.get(f'https://sellercentral.amazon.com/orders-v3?page={page_no}')

    # Wait for the page to load
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@value="Hide Filters"]')
            time.sleep(4)
            driver.find_element(By.XPATH, '//*[@id="myo-table-results-per-page"]/option[@value="100"]').click()
            time.sleep(4)
            break
        except:
            time.sleep(1)

    urls = driver.find_elements(By.XPATH, '//*[@value="Buy shipping"]//ancestor::a')
    if len(urls) == 0:
        break

    urls = [x.get_attribute('href') for x in urls]
    order_pages_url.extend(urls)
    page_no += 1

print(order_pages_url)
print(len(order_pages_url))

for single_order_page in order_pages_url:
    driver.get(single_order_page)
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@data-test-id="order-details-label"]')
            time.sleep(4)
            break
        except:
            time.sleep(1)

    # FIELDS TO SCRAPE: ASIN, ORDER ID, SKU, Purchase date, Shipping service, Ship by, Deliver by, Ship to, Phone, Subtotal, Tax, Total, Order Weight, Brand

    # ASIN
    asins = driver.find_elements(By.XPATH, "//table[@class='a-keyvalue']//span[text()='ASIN']/..")
    asins = list(set([str(x.text).split(":")[1].strip() for x in asins]))

    # ORDER ID
    order_id = get_text('//*[@data-test-id="order-id-value"]')

    # SKU
    skus = driver.find_elements(By.XPATH, "//table[@class='a-keyvalue']//span[text()='SKU']/..")
    skus = list(set([str(x.text).split(":")[1].strip() for x in skus]))

    # Purchase date
    purchase_date = get_text('//*[@data-test-id="order-summary-purchase-date-value"]')

    # Shipping service
    shipping_service = get_text('//*[@data-test-id="order-summary-shipping-service-value"]')

    # Ship by
    ship_by = get_text('//*[@data-test-id="order-summary-shipby-value"]')

    # Deliver by
    deliver_by = get_text('//*[@data-test-id="order-summary-deliverby-value"]')

    # Ship to
    ship_to = get_text('//div[@data-test-id="shipping-section-buyer-address"]')
    order_buyer_name, order_address, order_city, order_state, order_zip_code = parse_address(ship_to)
    ship_to = ship_to.replace("\n", " ")
    print(ship_to)

    # Phone
    phone = get_text('//*[@data-test-id="shipping-section-phone"]')

    # Order Items
    order_items = driver.find_elements(By.XPATH, "//table[@class='a-keyvalue']//*[text()='Order Item ID']/..")
    order_items = list(set([str(x.text).split(":")[1].strip() for x in order_items]))

    # Package Weight
    package_weight = get_text('//*[@name="selected-custom-package"]/..//span[@class="a-dropdown-prompt"]')
    if str(package_weight).lower().strip() == "none":
        package_weight = "NA"

    # Subtotal
    sub_totals = driver.find_elements(By.XPATH,
                                      '//table[@class="a-keyvalue"]//table//*[@class="a-row"]//*[text()="Item subtotal"]//ancestor::div[@class="a-row"]//div[@postion="last"]/span')
    sub_totals = list(set([str(x.text).strip() for x in sub_totals]))
    print(sub_totals)

    # Tax
    taxes = driver.find_elements(By.XPATH,
                                 '//table[@class="a-keyvalue"]//table//*[@class="a-row"]//*[text()="Tax"]//ancestor::div[@class="a-row"]//div[@postion="last"]/span')

    taxes = list(set([str(x.text).strip() for x in taxes]))

    for index, single_order_item in enumerate(asins):
        try:
            order_asin = asins[index]
        except:
            order_asin = "NA"

        try:
            order_item = order_items[index]
        except:
            order_item = "NA"

        try:
            order_sku = skus[index]
        except:
            order_sku = "NA"

        try:
            order_sub_total = sub_totals[index]
        except:
            order_sub_total = "NA"

        try:
            order_tax = taxes[index]
        except:
            order_tax = "NA"

        record = [order_id, order_asin, order_item, order_buyer_name, order_address, order_city, order_state,
                  order_zip_code, order_sku, purchase_date, shipping_service, ship_by, deliver_by,
                  ship_to, phone, package_weight, order_sub_total, order_tax]
        print(record)
        try:
            insert_record(record)
        except:
            print("Error inserting record")
            print(record)

        print(record)

# Close the cursor and database connection
cursor.close()
db.close()

# delete all rows from the table: DELETE FROM `amazon_orders` WHERE 1