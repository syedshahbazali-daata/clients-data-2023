import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from xextract import String
import csv


def get_file_data(file):
    with open(file, "r", encoding="utf-8") as file_x:
        return file_x.read().strip().split("\n")


session = HTMLSession()

data_links = get_file_data("links.txt")
for single_product_link in data_links:
    payload = ""
    headers = {
        "authority": "es.pandora.net",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "cache-control": "max-age=0",
        "cookie": """_pxhd=C9AKgZegzPhO-xVwpJEGaElhCfrd0R5W4UKa09nIZJRnI22XtwjisahQasNdv69-VsPX93F6wv8itkMqUIJ/sA==:CqoH/Qa0Rq-O8WACSyE/Xfeg8tzOHJKsCVN2fZDhVnq2a6QhF/4X349an3ll0sy02c1cB4A6yUq2-bbRXlJ8qwOSOdInBSieNJQiaQjJqTo=; dwsid=rvvhCDuZQ0AdAfC_1oZF-5dGvQ-Ps9pQX3cRtGRYUxGQqm2-zm9QKVihR0YA33zW2kZmZfKLZM2DcRid8wUzLQ==; dwanonymous_782e5e3f35c2999b3f758c96afb94548=abQETsnujvfOJ0sabXgEQ2ObpP; sid=TZjcYx8wnabokybUMErDhXQlgGSrGgS2quU; OptanonAlertBoxClosed=2023-04-22T07:35:07.781Z; __cq_dnt=0; dw_dnt=0; dwac_cffd3bd00d29d21fb14e6452f4=TZjcYx8wnabokybUMErDhXQlgGSrGgS2quU%3D|dw-only|||EUR|false|Europe%2FMadrid|true; cqcid=abQETsnujvfOJ0sabXgEQ2ObpP; cquid=||; _cs_c=0; pxcts=3452b62c-e0e0-11ed-8d94-7a62456b7978; _pxvid=2f351736-e0e0-11ed-946d-6b6d7a554b71; mt.v=2.1955388778.1682148909785; __cq_uuid=abQETsnujvfOJ0sabXgEQ2ObpP; __cq_seg=0~0.00\u00211~0.00\u00212~0.00\u00213~0.00\u00214~0.00\u00215~0.00\u00216~0.00\u00217~0.00\u00218~0.00\u00219~0.00; _mibhv=anon-1682148910285-6748341791_8738; mdLogger=false; kampyle_userid=c765-e771-582f-29eb-6608-b455-4736-de9d; kampyleUserSession=1682148910459; kampyleUserSessionsCount=1; kampyleUserPercentile=86.55687706200949; AMCVS_373EB12D55A8DB817F000101%40AdobeOrg=1; AMCV_373EB12D55A8DB817F000101%40AdobeOrg=-1124106680%7CMCIDTS%7C19470%7CMCMID%7C30678804252881946411351459502648909846%7CMCAAMLH-1682753710%7C3%7CMCAAMB-1682753710%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1682156110s%7CNONE%7CvVersion%7C5.2.0; adobe_vi=30678804252881946411351459502648909846; s_cc=true; __exponea_etc__=9620cbb0-97b1-4715-a871-c2792280aaa2; __exponea_time2__=-2.374077081680298; _tt_enable_cookie=1; _ttp=TREclnaqW2c8NwUUZKFW6x37QtY; _clck=1y31gum|1|faz|0; smc_uid=1682148914698608; smc_tag=eyJpZCI6Mjg0NSwibmFtZSI6InBhbmRvcmFzaG9wLmVzIn0=; smc_session_id=mIL0kxRf2evABFxVd1ZYqEVQIQIkIX18; smc_refresh=24651; smc_sesn=1; smc_not=default; crl8.fpcuid=23eb5078-df8e-48d6-abbd-b50a8b49f7c9; _cs_id=2916fdbf-b303-a041-98ac-295cd0399c41.1682148909.1.1682148924.1682148909.1573571364.1716312909571; _uetsid=35e7cc10e0e011ed8f15cdda42f8cb5e; _uetvid=35e856e0e0e011edab4bc182098c2485; _cs_s=2.0.1.1682150725432; kampyleSessionPageCounter=2; _gcl_au=1.1.825885055.1682148910.289669420.1682148928.1682148927; BVBRANDID=ab7cce47-0402-4109-a5fc-261832acd422; BVBRANDSID=381e5be6-2f3b-4fec-8aca-3a2e86962904; __cq_bc=%7B%22bfcr-PND-ES%22%3A%5B%7B%22id%22%3A%22598816C00%22%7D%5D%7D; smc_spv=2; smc_tpv=2; RT="z=1&dm=pandora.net&si=7568d5da-1b1e-4385-b2cc-a450c8aa0088&ss=lgro0uam&sl=1&tt=61c&bcn=%2F%2F684d0d46.akstat.io%2F&ld=a09&nu=13gwhs7d9&cl=br6&ul=9aqa&hd=9bcy"; s_cid_30=%5B%5B%27Direct%27%2C%271682148910643%27%5D%2C%5B%27Direct%27%2C%271682149337513%27%5D%5D; dwpersonalization_782e5e3f35c2999b3f758c96afb94548=803fad2884c4425ce703345e8020230430214500000; gpv_pn=estore%3Aproduct%3Adetail%20view; gpv_pt=product; BVImplmain_site=22249; utag_main=v_id:0187a7e357a60020f52fe38bc2680506f001a0670086e$_sn:1$_se:10$_ss:0$_st:1682151865605$ses_id:1682148906919%3Bexp-session$_pn:7%3Bexp-session$vapi_domain:pandora.net; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Apr+22+2023+12%3A54%3A26+GMT%2B0500+(Pakistan+Standard+Time)&version=202209.2.0&isIABGlobal=false&consentId=1b53497b-41dc-49a1-8b76-f4f8e108cbe5&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0005%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1%2CC0013%3A1&hosts=H296%3A1%2CH282%3A1%2CH283%3A1%2CH317%3A1%2CH321%3A1%2CH293%3A1%2CH295%3A1%2CH47%3A1%2CH4%3A1%2CH294%3A1%2CH134%3A1%2CH88%3A1%2CH19%3A1%2CH336%3A1%2CH281%3A1%2CH31%3A1%2CH297%3A1%2CH298%3A1%2CH313%3A1%2CH43%3A1%2CH329%3A1%2CH304%3A1%2CH61%3A1%2CH22%3A1%2CH337%3A1%2CH250%3A1%2CH7%3A1%2CH33%3A1%2CH333%3A1&genVendors=&geolocation=PK%3BPB&AwaitingReconsent=false; s_ptc=4.12%5E%5E; _px3=fab680583765dfd37fb83d1c094998506b5b09caac6d5f15df900cdcfdb528eb:pYJ50nzzgFnQfN4NCGjRpcdbMiU2oNDlMXALWOTefkH4NvJOEuTb5BN5xXV8SkS6mVUX0tSef1uSS0olznkW5w==:1000:bWuDgTJ1qJoITottFszsiKjL+u5Xt4w7WDfMjie5pi0sL835pkOObmF4mhRdCYhi2ONUVq1Ku23lktT/GmudZaDwobxW+6REebTTJX1PDzyc2oCXMjzUD+pOl+ecKxfsggl9LmSBot4V9TFBq9NLAh3EMN/htSO5KVTq98s+GOuq1lK88Vrk2Oh/uApqNr7B3MW3oFKO6lia6rJiB5vePg==; smct_session={"s":1682148915759,"l":1682150086012,"lt":1682149334765,"t":189,"p":93}; smct_session={"s":1682148915759,"l":1682150086012,"lt":1682149334765,"t":189,"p":93}""",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", single_product_link, data=payload, headers=headers)

    page_soup = BeautifulSoup(response.text, 'html.parser')
    page_source = str(page_soup)

    try:
        title_of_product = String(xpath='//h1').parse_html(page_source)[0]
    except:
        title_of_product = ""

    try:
        price = String(xpath='//*[@class="price"]//span[@content]', attr='content').parse_html(page_source)[0]
    except:
        price = ""

    try:
        sizes = String(xpath='//ul[@class="size-container"]/li/button[@data-sizeattr]').parse_html(page_source)

        sizes = " ,".join(sizes).replace("\n","")
    except:
        sizes = ""

    data_point = String(xpath='//span[@class="datalayer-view-event"]', attr='data-tealium-view').parse_html(page_source)
    print(data_point)





    record = f"{single_product_link},{title_of_product},{price},{sizes}"
    with open("data.txt", "a", encoding="utf-8") as csv_file:
        csv_file.write(record)


    print(single_product_link)



quit()
