import pyodbc
import pandas as pd
import re
import csv


# Functions require
def split_words(string):
    words = re.findall(r'\w+', string)
    words = [word.lower() for word in words]

    # initial letters of each word
    letters = [word[0] for word in words]
    letters = "".join(letters)
    words.append(letters)
    if "the" in words:
        words.remove("the")
        letters = letters.replace("t", "")

    if "and" in words:
        words.remove("and")
        letters = letters.replace("a", "")

    words.append(letters)
    return words


def check_list_of_words_in_string(list_of_words, string):

    if string is None or string == "":
        return True
    for word in list_of_words:
        if word in string:
            return True
    return False


# Connect to the database

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
print("Connected")
# convert the data to a pandas dataframe "SELECT COUNT(*) FROM tb_investors"

data = []
cursor.execute("SELECT * FROM tb_investors")
for row in cursor.fetchall():

    print(list(row))

quit()
col_names = [i[0] for i in cursor.description]
df = pd.DataFrame(data, columns=col_names)


# duplicates
new_data = df[df.duplicated(subset=["name", "website"], keep=False)]
# take two columns name and website and add a new column with the name of Reason
new_data["reason"] = "DUPLICATES"

new_data = new_data[["name", "website", "reason"]]

# save the data to a csv file
new_data.to_csv("wrong_data.csv", index=False)

list_of_investors_name = df["name"].tolist()
list_of_investors_website = df["website"].tolist()

for i in range(len(list_of_investors_website)):
    try:
        list_of_words_in_name = split_words(str(list_of_investors_name[i]))
        result = check_list_of_words_in_string(list_of_words_in_name, list_of_investors_website[i])

        if not result:
            with open("wrong_data.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([list_of_investors_name[i], list_of_investors_website[i], "WRONG WEBSITE"])

    except:
        pass


print("Done")
