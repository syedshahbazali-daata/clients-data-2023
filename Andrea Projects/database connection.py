import pyodbc

connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=eutop.database.windows.net;"
    "Database=eutop_companies;"
    "UID=readonlylogin;"
    "PWD=eutop123#;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Establish the database connection
connection = pyodbc.connect(connection_string)

# Execute a sample query
cursor = connection.cursor()

# print all tables
cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES")
for row in cursor.fetchall():
    print(row)