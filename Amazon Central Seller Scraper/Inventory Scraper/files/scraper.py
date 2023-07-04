import csv

import grequests
import pandas as pd
from bs4 import BeautifulSoup
from xextract import String
import re

def list_into_chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


df = pd.read_csv("output.csv")
urls = df['URL'].tolist()
urls = list(set(urls))

list_or_urls = list(list_into_chunks(urls, 50))
headers = {
    "cookie": """session-id=143-0879716-3082319; s_pers=%20s_fid%3D6F0A8B4B7A54CFC6-073F12F916E77D21%7C1837706617492%3B%20s_dl%3D1%7C1679855617493%3B%20s_ev15%3D%255B%255B%2527Google%2527%252C%25271679853817110%2527%255D%252C%255B%2527NSGoogle%2527%252C%25271679853817498%2527%255D%255D%7C1837706617498%3B; ubid-main=134-8514737-7489119; sid="Bx48wFAUtSTmgp0232Dulw==|W49bYdN74vL7sfroeOKjhcOW6no9v9lp5cBhYHS/Zew="; aws-ubid-main=721-7873856-2486328; x-main="xUnks1cphnJ9rgs3h7wi6wnMhndBJQu3r0nx3jmE?2ENRqpB@xMGTWbBZct9W4??"; at-main=Atza|IwEBIOyF1JlPqLIV4ZLXiGMhLxy5lmraGmoj70OGUbhS8jPD7oDtk0albXhis0nWohwUuYT9QYbzxx5bJNdudQ-OqmYWFk-E5znITg4I7gFNLDe2C-RFxcV81ONNGzmwcRzvYLQ2r7j9psmLgmWsBse7ZNS8uUyOiyzoQ1AMZN2KVxIUvjpgmGTLxNra70MWDuOshRX0byAwDFpw_Krn3KaDaYU-_KAis2ToUx7KiEcMyYzD1g; sess-at-main="SRl8vyc1PGJD9ZwSdq2vg3AgBZhGtDhtqchhXD9cw64="; sst-main=Sst1|PQGbNYk9h6JM533fOJLO4jeuCUP7fsFMCXIk030AsSPGmDBICwNb1hXGBoU_cEORMBiYq_vX8C-bQaZFLpP4L-otIDUmON4jmJ4lebd5hS-0Hya7TUqmpCFxvQVu4W6ko33YgSnNgSBz7MewSU26hGeL2Rn-QD-chp0haQ8grMF93tc0yystDgnCOpQXODba8SCwMsYPMNALVVwGzacRQ9l2Wnec3zXG7NosVbTMHeNxRbnhuNKEecksja9YcfpG_XAmprHbbOpZ_3b2JNUOH-jgp4n8sHU0EhYjOkJ2c8kKyDk; session-id-time=2082787201l; i18n-prefs=USD; lc-main=en_US; aws-account-alias=382547926795; remember-account=true; regStatus=registered; awsc-color-theme=light; awsc-uh-opt-in=; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A382547926795%3Auser%2Fsyed-fiverr%22%2C%22alias%22%3A%22382547926795%22%2C%22username%22%3A%22syed-fiverr%22%2C%22keybase%22%3A%22xHHE0K83UgKdoqo1mShuW8ZzA0aHbdmI%2FOxVhpdyVQc%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJhcC1zb3V0aC0xIiwiYWxnIjoiRVMzODQiLCJraWQiOiJkNzc3YzU0MS1mYWU2LTRkZDgtYTlkZS1lMDhjNDY3MDQ2MWIifQ.eyJzdWIiOiIzODI1NDc5MjY3OTUiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoieEhIRTBLODNVZ0tkb3FvMW1TaHVXOFp6QTBhSGJkbUlcL094VmhwZHlWUWM9IiwiYXJuIjoiYXJuOmF3czppYW06OjM4MjU0NzkyNjc5NTp1c2VyXC9zeWVkLWZpdmVyciIsInVzZXJuYW1lIjoic3llZC1maXZlcnIifQ.yvTKauf-CZ69ff65cqbmmAFGEzugmzxWgm0H2Zsa7lOPI2ErSoirOAj5sNiP4cO4HKzn3ZwjYdnC9VXCJiJb1qQ3PlVbcXuRaX0McGkSZ1xofhnMHdYXsp9Oz-kyDdX7; noflush_awsccs_sid=1bf943f574123a1050ea104ed6e6bc48dba5a3e7ecc85653f808e72de07432d2; skin=noskin; csm-hit=tb:HP7KCN5091QX7FVN2E1V+s-HP7KCN5091QX7FVN2E1V|1681495234182&t:1681495234182&adb:adblk_yes; session-token=FrCdOmnuwiMZSsNsiZMwt+WPc85+zaZti5yk+HZpfjTaS/RYCN93U+fvBZTsnIFABoFDyDqAMl9qWgqLKMYLkM1pmvDwuu/n8qVQUY+Ee+n+D8Xw+5zref2YSBjhD9bc64owZvxSgJVhMgr/oDCZeL2t0l6seOC4XB6mFb5XIiB8fqQRW7TjXz4ZiXmP+YO4s83RWFKGJuFG6jQH1Gcyfjzw7KUSwBO4PDV34W1wAUXWDf5LsmhNOw==""",
    "authority": "www.amazon.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
    "cache-control": "max-age=0",
    "device-memory": "8",
    "downlink": "10",
    "dpr": "0.8",
    "ect": "4g",
    "rtt": "150",
    "sec-ch-device-memory": "8",
    "sec-ch-dpr": "0.8",

    "sec-ch-ua-mobile": "?0",


    "sec-ch-viewport-width": "726",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "viewport-width": "726"
}
for single_list in list_or_urls:

    rs = (grequests.get(url, headers=headers) for url in single_list)
    responses = grequests.map(rs)
    for response in responses:


        try:
            price = re.findall('price-data.*?"displayPrice":"\$([^"]+)', str(response.text))[0]
        except:
            price = ""
        url_x = response.url
        with open("prices.csv", "a", encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([url_x, price])

        print(url_x, price)


