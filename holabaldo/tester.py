"""
username = baldo
password = AVNS_31sHK4CCPIr6p4Ifgzd
host = db-mysql-nyc1-47136-do-user-12226124-0.b.db.ondigitalocean.com
port = 25060
database = Baldo
sslmode = REQUIRED
"""


import mysql.connector
from mysql import connector
from mysql.connector import errorcode
import os


connection = mysql.connector.connect(
    user='baldo',
    password='AVNS_31sHK4CCPIr6p4Ifgzd',
    host='db-mysql-nyc1-47136-do-user-12226124-0.b.db.ondigitalocean.com',
    port=25060,
    database='Baldo',


)

cursor = connection.cursor()

#