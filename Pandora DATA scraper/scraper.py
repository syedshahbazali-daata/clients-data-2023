from requests_html import HTMLSession
from bs4 import BeautifulSoup
from xextract import String

session = HTMLSession()
res = session.get("https://es.pandora.net/es/ideas-de-regalo/ocasiones-especiales/dia-de-la-madre/?showSalesBadge=false&seoPlacementIndex=2&seoModuleIndex=2")
page_soup = BeautifulSoup(res.text, 'html.parser')
page_source = str(page_soup)

link_xpath = '//a[@class="link suggestionhit"]'

links_data = String(xpath=link_xpath, attr='href').parse_html(page_source)
for single_link in links_data:
    x_link = "https://es.pandora.net"+single_link
    print(x_link)

