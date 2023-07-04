import requests



url = "https://smtickets.com/users/login"

payload = "username=shahbazali1639%40gmail.com&password=AliM%40l%4012%2B"
headers = {
    "cookie": "smtickets_v2=f89d99e3eb04ee0f442f4ec3f8c1572e27d4944d; AWSALB=ycmDfiTRdVgje4YpHtacn4FShy0bCTqMN7yTNF93qbZ1j6eLpq6NdsfGJeAyMhR+ZmAGfeBs5TQc4LLW4qgV/nCgASsXhRMZUx7i0OfSe4Gukc9I8yU2us4lCsNE; AWSALBCORS=ycmDfiTRdVgje4YpHtacn4FShy0bCTqMN7yTNF93qbZ1j6eLpq6NdsfGJeAyMhR+ZmAGfeBs5TQc4LLW4qgV/nCgASsXhRMZUx7i0OfSe4Gukc9I8yU2us4lCsNE",
    "authority": "smtickets.com",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://smtickets.com",
    "referer": "https://smtickets.com/",

    "sec-ch-ua-mobile": "?0",

    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)