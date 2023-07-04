import csv

# Category	Commerce	Image	Material	Product Name	Price	SKU

import grequests
import pandas as pd
from bs4 import BeautifulSoup
import re
from xextract import String


def list_into_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


df = pd.read_csv('urls_data.csv')
urls = df['url'].tolist()
category = df['category'].tolist()

lists_of_urls = list(list_into_chunks(urls, 10))

# //div[contains(@class,'primary-images')]//div/img


# Headers:
headers = {
"cookie": """dwanonymous_782e5e3f35c2999b3f758c96afb94548=abQETsnujvfOJ0sabXgEQ2ObpP; OptanonAlertBoxClosed=2023-04-22T07:35:07.781Z; _cs_c=0; _pxvid=2f351736-e0e0-11ed-946d-6b6d7a554b71; mt.v=2.1955388778.1682148909785; __cq_uuid=abQETsnujvfOJ0sabXgEQ2ObpP; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; _mibhv=anon-1682148910285-6748341791_8738; mdLogger=false; kampyle_userid=c765-e771-582f-29eb-6608-b455-4736-de9d; adobe_vi=30678804252881946411351459502648909846; __exponea_etc__=9620cbb0-97b1-4715-a871-c2792280aaa2; _tt_enable_cookie=1; _ttp=TREclnaqW2c8NwUUZKFW6x37QtY; _clck=1y31gum|1|faz|0; smc_uid=1682148914698608; smc_tag=eyJpZCI6Mjg0NSwibmFtZSI6InBhbmRvcmFzaG9wLmVzIn0=; smc_refresh=24651; smc_not=default; crl8.fpcuid=23eb5078-df8e-48d6-abbd-b50a8b49f7c9; _gcl_au=1.1.825885055.1682148910.289669420.1682148928.1682148927; BVBRANDID=ab7cce47-0402-4109-a5fc-261832acd422; __cq_bc=%7B%22bfcr-PND-ES%22%3A%5B%7B%22id%22%3A%22598816C00%22%7D%5D%7D; dwpersonalization_782e5e3f35c2999b3f758c96afb94548=803fad2884c4425ce703345e8020230430214500000; _pxhd=/RHh8VVeVm1yTOUbsJD1tF2ZPHQGiiCd0uZeFS17M9dA4qcyZ7bQq0bWziK-f2bR-lD-SONfmR57bGGJ8lwTOQ==:eiXDHKfwavB2jPycL2j4NLxCEapUknFyLrnijMtUM-ai3jkQuZ4EvzWFSX/YKMhX/QT7LMWo6c8UcvLowDcvqKzV/bJthxhm1DlzsgXdodM=; __cq_dnt=0; cqcid=abQETsnujvfOJ0sabXgEQ2ObpP; cquid=||; dw_dnt=0; AMCVS_373EB12D55A8DB817F000101%40AdobeOrg=1; AMCV_373EB12D55A8DB817F000101%40AdobeOrg=-1124106680%7CMCIDTS%7C19475%7CMCMID%7C30678804252881946411351459502648909846%7CMCAAMLH-1683256811%7C6%7CMCAAMB-1683256811%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1682659211s%7CNONE%7CvVersion%7C5.2.0; s_cc=true; _cs_id=2916fdbf-b303-a041-98ac-295cd0399c41.1682148909.2.1682652017.1682652017.1573571364.1716312909571; _uetsid=a12469b0e57311edba87ffddc6e5f453; _uetvid=35e856e0e0e011edab4bc182098c2485; kampyleUserSession=1682652032799; kampyleUserSessionsCount=2; kampyleSessionPageCounter=1; kampyleUserPercentile=98.94583087245472; pxcts=99c1b910-e573-11ed-8e31-446756647046; smc_session_id=nBqDOv8fGdTjCxWNytnhWMvXuENlENNc; smc_spv=1; smc_tpv=3; smc_sesn=2; RT="z=1&dm=pandora.net&si=7568d5da-1b1e-4385-b2cc-a450c8aa0088&ss=lgzzjvvl&sl=1&tt=gul&bcn=%2F%2F684d0d46.akstat.io%2F&ld=gus&nu=1pb9k8pe&cl=369t"; smct_session={"s":1682652041047,"l":1682653248064,"lt":1682652143056,"t":81,"p":80}; s_cid_30=%5B%5B%27Direct%27%2C%271682630500073%27%5D%2C%5B%27Direct%27%2C%271682630839705%27%5D%2C%5B%27Direct%27%2C%271682630875941%27%5D%2C%5B%27Direct%27%2C%271682630979251%27%5D%2C%5B%27Direct%27%2C%271682631085238%27%5D%2C%5B%27Direct%27%2C%271682633826518%27%5D%2C%5B%27Direct%27%2C%271682634073884%27%5D%2C%5B%27Direct%27%2C%271682634248359%27%5D%2C%5B%27Direct%27%2C%271682634319747%27%5D%2C%5B%27Direct%27%2C%271682634323121%27%5D%2C%5B%27Direct%27%2C%271682652011023%27%5D%2C%5B%27Direct%27%2C%271682652132300%27%5D%2C%5B%27Direct%27%2C%271682652132336%27%5D%2C%5B%27Direct%27%2C%271682652708800%27%5D%2C%5B%27Direct%27%2C%271682653164783%27%5D%2C%5B%27Direct%27%2C%271682654015739%27%5D%2C%5B%27Direct%27%2C%271682654204071%27%5D%2C%5B%27Direct%27%2C%271682654899287%27%5D%2C%5B%27Direct%27%2C%271682655028099%27%5D%2C%5B%27Direct%27%2C%271682655257536%27%5D%5D; s_sq=%5B%5BB%5D%5D; s_ptc=9.43%5E%5E; dwsid=bfTXIVkVjLm9AQUp__zpr54tuYaayLWJkGBnuicvhfOkMyoDj-xr9RU-CQ0A0hV5IgYiyw1QLZyU7aj_-mYGlQ==; dwac_cffd3bd00d29d21fb14e6452f4=eood5zmTGXqsgpN3_RXPRIlTc0D6TiBKgeM%3D|dw-only|||EUR|false|Europe%2FMadrid|true; sid=eood5zmTGXqsgpN3_RXPRIlTc0D6TiBKgeM; __exponea_time2__=0.19764971733093262; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Apr+28+2023+17%3A42%3A28+GMT%2B0500+(Pakistan+Standard+Time)&version=202209.2.0&isIABGlobal=false&consentId=1b53497b-41dc-49a1-8b76-f4f8e108cbe5&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0005%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1%2CC0013%3A1&hosts=H296%3A1%2CH282%3A1%2CH283%3A1%2CH317%3A1%2CH321%3A1%2CH293%3A1%2CH295%3A1%2CH47%3A1%2CH4%3A1%2CH294%3A1%2CH134%3A1%2CH88%3A1%2CH19%3A1%2CH336%3A1%2CH281%3A1%2CH31%3A1%2CH297%3A1%2CH298%3A1%2CH313%3A1%2CH43%3A1%2CH329%3A1%2CH304%3A1%2CH61%3A1%2CH22%3A1%2CH337%3A1%2CH250%3A1%2CH7%3A1%2CH33%3A1%2CH333%3A1&genVendors=&geolocation=PK%3BPB&AwaitingReconsent=false; utag_main=v_id:0187a7e357a60020f52fe38bc2680506f001a0670086e$_sn:5$_se:3$_ss:0$_st:1682687551507$vapi_domain:pandora.net$dc_visit:1$ses_id:1682685722098%3Bexp-session$_pn:2%3Bexp-session; _px3=bad71e6a9ac169e298564476bc5c7580cb5ef364e7cf77793a44acc3327c6976:0U2BAaa7sTnZ7xWa1q46/FaHBo0+V4zyWhoJCE615ISbvAuLzxc1dJX15/a/1z9SF3ki/DaBrNtlOp+vNXCfQQ==:1000:fAFqOYMkticih6CTqrC6vDqFAHUxUW77ShHU/qfoz9mrj7L4sG334usOOo+0osRlsSqACaOh/kSwqymUUUGRNXnlMs+vo6IfQGzn1numms4po8/fSx7ZMcTJMzu80Jw1GuFrjmd70psvkK4IVyJ7uAZuiuZrUgVVXqzrHYuw9L+uAA6tZPee89guZG63jlR8i1L5IV0e+CLYDhgUUQ7xQw==""",
    "authority":"es.pandora.net",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language":"en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
    "cache-control":"max-age=0",

    "sec-ch-ua-mobile":"?0",

    "sec-fetch-dest":"document",
    "sec-fetch-mode":"navigate",
    "sec-fetch-site":"none",
    "sec-fetch-user":"?1",
    "upgrade-insecure-requests":"1",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

proxies = {
        "http": "http://vdtdaksm-rotate:tj0p16tz6bxk@p.webshare.io:80/",
        "https": "http://vdtdaksm-rotate:tj0p16tz6bxk@p.webshare.io:80/"
    }

for i in range(len(lists_of_urls)):

    rs = (grequests.get(u, headers=headers) for u in lists_of_urls[i])
    responses = grequests.map(rs)

    for response in responses:

        soup = str(BeautifulSoup(response.text, 'html.parser'))





        regex = '<script\s+type="application\/ld\+json">\s*\{(.+)}\s*<\/script>'
        data = re.findall(regex, str(soup))
        category_x = String(xpath='//li[@class="breadcrumb-item"]/a').parse_html(soup)
        try:
            category = str(category_x[-1]).strip().replace("\n", "")
        except:
            category = "N/A"

        if category == "N/A":
            input("Category not found. Press enter to continue: ")


        try:
            name = re.findall('"name":"(.+?)"', data[0])[0]

        except:
            name = "N/A"

        try:
            sku = re.findall('"sku":"(.+?)"', data[0])[0]

        except:
            sku = "N/A"

        try:
            material = re.findall('"material":"(.+?)"', str(soup))[0]

        except:
            material = "N/A"

        try:
            price = re.findall('"price":"(.+?)"', data[0])[0]

        except:
            price = "N/A"

        try:
            image = re.findall('"image":"(.+?)"', data[0])[0]

        except:
            image = "N/A"

        commerce = "Pandora"
        # Category	Commerce	Image	Material	Product Name	Price	SKU

        record = [category, commerce, image, material, name, price, sku]
        with open("pandora.csv", "a+", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(record)
        print(record)












        # name


