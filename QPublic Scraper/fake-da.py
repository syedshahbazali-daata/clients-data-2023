import pandas as pd


df = pd.read_csv("brands_names_sku_numbers.csv")

urls = df["URL"].tolist()
urls = list(set(urls[:100]))
for url in urls:
    print(url)




quit()
brand_names = df["BRAND NAME"].tolist()

x = 0
for i in brand_names[:100]:
    x += 1
    print(f"{x}. {i}")