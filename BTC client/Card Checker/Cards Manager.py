import pandas as pd
from card_checker import *
def get_files_data(file):
    with open(file, "r", encoding="utf-8") as file_x:
        file_x = file_x.read().strip().split("\n")
        return file_x


# ELIGIBLE COUNTRIES
eligible_countries = get_files_data("eligible countries")
eligible_countries = [country.upper() for country in eligible_countries]


# READ BINS LIST
df = pd.read_csv("data.csv")
# only Bin start with 4
df["Bin"] = df["Bin"].astype(str)
df = df[df["Bin"].str.startswith("4")]

# all countries upper case
df["Country"] = df["Country"].str.upper()



count = 0

for each_row in df.iterrows():
    card_bin = str(each_row[1]["Bin"])
    card_country = str(each_row[1]["Country"]).upper()
    print(card_country)

    if card_country in eligible_countries:
        result = card_checker(card_bin, card_country)
        if not result:
            print("error")
            continue

        record = [card_bin, card_country]
        record.extend(result)




        print(record)
        count += 1
    break

print(count)



