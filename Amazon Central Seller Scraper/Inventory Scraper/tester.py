
def get_file_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')
    return data

asin_urls = get_file_data("product_urls.txt")
asin_urls = list(set(asin_urls))
print(asin_urls)
print(len(asin_urls))

with open('product_urls.txt', 'w', encoding='utf-8') as f:
    f.write("")

for single_asin in asin_urls:
    with open('product_urls.txt', 'a', encoding='utf-8') as f:
        f.write(single_asin + "\n")

