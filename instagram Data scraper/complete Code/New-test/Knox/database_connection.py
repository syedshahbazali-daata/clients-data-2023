import mysql.connector

# Set database connection parameters
config = {
    'user': 'scrapersdb',
    'password': 'scrapersdb',
    'host': 'scrapersdb.cwfozzgc5i1y.ap-southeast-2.rds.amazonaws.com',
    'port': '3306',
    'database': 'scrapersdb'
}

# Connect to the database
try:
    cnx = mysql.connector.connect(**config)
    print("Connected to database")
except mysql.connector.Error as err:
    print("Failed to connect to database: {}".format(err))
    exit()


def add_row_to_table(table_name: str, values: tuple):
    # Create the INSERT INTO sql query
    query = "INSERT INTO " + table_name + " VALUES " + str(values)
    print(query)
    # Execute the query
    cursor.execute(query)
    # Commit the changes
    cnx.commit()


def create_table(table_name: str, columns: tuple):
    # Create the CREATE TABLE sql query
    query = "CREATE TABLE " + table_name + " " + str(columns)
    print(query)
    # Execute the query
    cursor.execute(query)
    # Commit the changes
    cnx.commit()


def delete_table(table_name: str):
    # Create the DROP TABLE sql query
    query = "DROP TABLE " + table_name
    print(query)
    # Execute the query
    cursor.execute(query)
    # Commit the changes
    cnx.commit()


# connect to the database
cursor = cnx.cursor()
cursor.execute("USE scrapersdb")



