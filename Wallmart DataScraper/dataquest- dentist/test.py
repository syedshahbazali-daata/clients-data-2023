import requests


url = "https://ais.usvisa-info.com/en-ae/niv/schedule/49718829/appointment/days/49.json"

querystring = {"appointments^\\[expedite^\\]":"false"}

payload = ""
headers = {

    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    #"Cookie": "_ga=GA1.2.812718811.1688239136; _gid=GA1.2.437894054.1688239136; _gat=1; _ga_W1JNKHTW0Y=GS1.2.1688239136.1.1.1688239777.0.0.0; _yatri_session=WFU3c21PaXBDd2YrUmgxY2lRTW9rRWxPL1JXYU16M2VjZ25lSzk4Y3h2NitMRnpmS0xWQW5PWng3SVVFeXdFZm1KKzFoWnZTNlVnZWw5dU1PTVpxUzRDSVpFWU1vbkZ0YjFEKzVxZFU4Z084S21IWVNFME9BRnNSMDBNSll2NytQS1FQalA5WU1HcFFBTXZLK3hGOXowNksySERSSlRMak1uTTlnSHFGQ3ZZMFpkRkl0YjdEUDgzUmdsdVZBSHFiREpSZ0xJaUlqUVM0YkZZSEdqcVRUY1lLQktLOTBWejlLTU9odFVyS09qUEhidUtZb3NkdjViNWliY0hpWm1IbE4xUS9pSCt0VzE1OW5MdXlKazBJTnNQVWY2bjYvbmwxTDQ3REMyUEZwc0dnNzB5Wk1ZK29mYitrNS9vd3ZvenJSV1dJQXBYL0JiQ3BLaVpuVjNFMGhkcFREMUNmNEFlZ2gzMVpuNDJ1NmU5TzZjZ3VBQTRSSUF6UDA5WXZub3RDUXhjTVFIM2haVC9PWlU5d01FRlZIUzRQZlQ5OVZjbXpNbC9ENkhnTDdaQkZwR2dBdTdnbjFNVnRKRks1TUJNTHdtWUJhMVlvL2VuTm0rUlJIVFNnTWt1Zkgrall4NTM1TDRoemdCTE1jU2gycUo3WjBzZ05iMytrS28yRVRaYys0cXVEOHFYTjhRQXA2VU5PUm96dFdOODV1dDE5bFRuRG9ZbFFMUGJQdVBnPS0tRjUzV1VYWkQ5d2ZXUlJWN01EbEdiQT09--93a76d89b903a33a88718ae03df550e383bce9ff",
    "Cookie": "_yatri_session=T1JMWTRhQzJMVjhKbnU4dFRURHJvaS95MXRTWXo4SzNySk1zWm02K2hGWVVKMVJlWkUybTg5Sm9rMWVNbzFmbEdPTlNMNW9BMzVrY01JOU1KWkNoaEErOHlmYWNFeW42dnVPNzJ2aVB1ZXphS0tZaWZzUWRwK0F6OEdnOHhyWFE4SlpheEJMa3BWVmRQUkdkUEtyQVZHQWhoK09saVRMYXRFMVBpQzFKcjJGZDBJMHYrbmVQWVlyOHZPR2JtMllXSnlwaytkK0g4WnFVYmpuUC9nZ3hDVDBoR2pleE03R3gvT2FzMlp3cWJSK05YTklGZC8wN09BVmI4bUp5OVlPNVIyZUZ4QmRjOVZJY2p0b1RpNkVTekFwYWl6K09nV0RUSkxKYUI1NmRDWEZ1QmoxZHRlb1k5cG1vb3hWRzBxbnVwV2NSeWVGZ1puZ3VvUGRzNzUvaFJZQ3d4dnZCUDdJdmVlSHh5L2FYZUJaOWZiWGlBV0dkMXdHU094a3BlN1kvNmtMUWFyR1B1ZGFJYzNJem5XM25hcTJPYjN6Wm1oWGVMLzg0SFFoZUlvZW15ZGwwS3FmSUpKdDMzcXFzUEhEOTAzQXg2TEZWQTdSTEZ0SERxbVVVV3Y5aFcvdzNvZnZ4aC9KZnN4ZnpKQmVzcEppN1MzdXZXWkZ3amIzdHBmOVNaaVo2UGlWY1crZmVGWHZCRTdxMWlQb0d0eUIyZ2dMWHYwdXprYU9SYnNBPS0tQWhtakduY01nR1FYMzNGajY4c3o2QT09--983caf1f949570a2878d98c8a22418ffa2d8d541; _ga_W1JNKHTW0Y=GS1.2.1688239136.1.1.1688240402.0.0.0; _gat=1; _gid=GA1.2.437894054.1688239136; _ga=GA1.2.812718811.1688239136;",
    "If-None-Match": "W/^\^cd68d9a2b5c306e5fa0eadf994eb8154^^",
    "Referer": "https://ais.usvisa-info.com/en-ae/niv/schedule/49718829/appointment",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "X-CSRF-Token": "BgTdyPY+9EL4kTNUYOUI/uru2SdSb7Hwm/RUIX4XgMzntg/7vJtJAy3N+GjYbFQfGezbpcCNSHh3szA2pPnFEA==",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "^\^Not.A/Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^114^^, ^\^Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
response_data = response.json()
print(response_data)