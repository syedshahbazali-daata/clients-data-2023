# CREATE TABLE QUERY:

"""
CREATE TABLE orders (
    order_id VARCHAR(255),
    order_asin VARCHAR(255),
    order_item VARCHAR(255),
    order_buyer_name VARCHAR(255),
    order_address VARCHAR(255),
    order_city VARCHAR(255),
    order_state VARCHAR(255),
    order_zip_code VARCHAR(255),
    order_sku VARCHAR(255),
    purchase_date VARCHAR(255),
    shipping_service VARCHAR(255),
    ship_by VARCHAR(255),
    deliver_by VARCHAR(255),
    ship_to VARCHAR(255),
    phone VARCHAR(255),
    package_weight VARCHAR(255),
    order_sub_total VARCHAR(255),
    order_tax VARCHAR(255)
);"""


def insert_record(record):
    # Connect to the MySQL database

    # Prepare the SQL query to insert the record
    sql = "INSERT INTO orders (order_id, order_asin, order_item,order_buyer_name, order_address, order_city, order_state,order_zip_code, order_sku, purchase_date, shipping_service, ship_by, deliver_by, ship_to, phone, package_weight, order_sub_total, order_tax) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = tuple(record)

    # Execute the query and commit the changes
    cursor.execute(sql, values)
    db.commit()


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


cursor = db.cursor()

# Create a cursor object to execute SQL queries
x = ['111-9403300-1693814', 'B0BTWJVRZY', '75515931278921', 'Pam R Thornton', '982 DRIFTWOOD RD', 'TITUS', 'AL', '36080-2848', '01-DWFT-Q7EY', 'Fri, Mar 24, 2023, 6:32 AM PDT', 'Standard', 'Mon, Mar 27, 2023 to Mon, Mar 27, 2023', 'Wed, Mar 29, 2023 to Fri, Mar 31, 2023', 'Pam R Thornton 982 DRIFTWOOD RD TITUS, AL 36080-2848', '+1 314-282-9402 ext. 12855', 'Custom 9 in x 6 in x 3 in', 'US$39.98', 'US$3.20']
insert_record(x)

print("Record inserted successfully")