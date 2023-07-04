from requests_html import HTMLSession
from bs4 import BeautifulSoup
from xextract import String

url = "https://www.revolico.com/"
session = HTMLSession()
r = session.get(url)

page_source = r.text
soup = BeautifulSoup(page_source, 'html.parser')

xpath = "//h5[text()='Compra / Venta' or text()='Autos' or text()='Servicios' or text()='Computadoras']/../..//li/a"

links = String(xpath=xpath, attr="href").parse_html(str(soup))
links = ["https://www.revolico.com" + x for x in links]
with open("links.txt", "w") as f:
    f.write("\n".join(links))