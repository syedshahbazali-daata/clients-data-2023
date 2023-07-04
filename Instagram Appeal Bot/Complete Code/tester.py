import requests



# 209.20.237.255:8570
proxy = "209.20.237.255:8570"

proxies = {
    "http": f"http://{proxy}",
    "https": f"http://{proxy}"
}

r = requests.get("http://httpbin.org/ip", proxies=proxies)
print(r.text)
