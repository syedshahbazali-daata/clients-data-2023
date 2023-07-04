import requests

proxies = {
        "http": "http://vdtdaksm-rotate:tj0p16tz6bxk@p.webshare.io:80/",
        "https": "http://vdtdaksm-rotate:tj0p16tz6bxk@p.webshare.io:80/"
    }


res = requests.get("http://httpbin.org/ip", proxies=proxies)
print(res.text)