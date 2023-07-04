import requests

max_id_x = '1680414829.856'
for i in range(10):
    print("Page: ", max_id_x)
    url = "https://poshmark.com/vm-rest/users/miamioclock/posts/filtered"

    querystring = {
        "request": "{\"filters\":{\"department\":\"All\",\"inventory_status\":[\"all\"]},\"query_and_facet_filters\":{\"creator_id\":\"miamioclock\"},\"experience\":\"all\",\"max_id\":max_id_x,\"count\":48}".replace('max_id_x', max_id_x),
        "summarize": "true", "app_version": "2.55", "pm_version": "238.0.0"}

    print(querystring)

    payload = ""
    headers = {
        "authority": "poshmark.com",
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "cookie": "ps=%7B%22bid%22%3A%2264230c2fe67283e992f21efa%22%2C%22extvid%22%3A%22ext1%3A223a211a-f2bf-4483-a8c4-6b45d304f49b%22%7D; vsegv3=eyJsMDEiOiIwOTgiLCJsMDIiOiIxMjEiLCJsMDMiOiIwNjUiLCJsMDQiOiIwNzciLCJsMDUiOiIxMjgiLCJsMDYiOiIwNDMiLCJsMDciOiIwNjIiLCJsMDgiOiIwODYifQ%3D%3D; __ssid=38a0c779c02c5e21c0d59c2748fc0c0; _gcl_au=1.1.45196378.1680018488; FPC=e7e1443b-f3a3-459e-b3d9-ad1a17fd7c62; G_ENABLED_IDPS=google; io_token_7c6a6574-f011-4c9a-abdd-9894a102ccef=mai5K20oop2GCqw4wVq+kyKDPilOyh+kZirvB/JkqBg=; _scid=7e253c57-1cc8-4477-b448-13a302018306; _tt_enable_cookie=1; _ttp=RWzXYBHiEGsmgfL3pQeRsDH0yDy; _sctr=1|1679943600000; tracker_device=d24b1aae-757c-4669-bdb2-494e55c85604; rt=%7B%22src%22%3A%5B%7B%22rf%22%3A%22%22%2C%22lpu%22%3A%22%2Fcloset%2Fmiamioclock%3Futm_source%26utm_content%3Dext_trk%253Dbranch%2526feature%253Dsh_cl_ss_ios%2526campaign%253Dshare_content_other_user__us.default.001%2526rfuid%253Dext1%253Aadf5571f-8c6b-4f53-9022-22c6288688e7%26br_t%3Dtrue%26_branch_match_id%3D1169289125428012244%26_branch_referrer%3DH4sIAAAAAAAAA8soKSkottLXL8gvztDLzdZP9c4zKynzSkqvTAIAILn1dhsAAAA%253D%22%2C%22lpt%22%3A%22Other%22%2C%22rs%22%3Anull%2C%22ca%22%3A%222023-03-28T15%3A48%3A05.964Z%22%7D%2C%7B%22rf%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22lpu%22%3A%22%2Flisting%2F6201578d6e2846223a6cf756%2C2022-02-07%2Csold_out%2C34B%2CNatori%2COther%2Cnicolestate%2C23%2Csold_out%2C1%2C0.0%2C5100.0%22%2C%22lpt%22%3A%22Listing%20Details%22%2C%22rs%22%3A%22gs%22%2C%22ca%22%3A%222023-03-30T08%3A33%3A10.953Z%22%7D%2C%7B%22rf%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22lpu%22%3A%22%2Flisting%2F6421c232253a8c85c8067f4a%2C2023-03-27%2Csold_out%2CM%2CNA%2CTops%2Cstateofposh%2C17%2Csold_out%2C1%2C352.0%2C5100.0%22%2C%22lpt%22%3A%22Listing%20Details%22%2C%22rs%22%3A%22gs%22%2C%22ca%22%3A%222023-03-30T08%3A35%3A51.405Z%22%7D%5D%7D; _uetvid=ef785d10cd7f11eda3dcbbb7fdfbee2e; _ga=GA1.1.1728920342.1680018488; _ga_S34VRNNVTV=GS1.1.1680165227.6.1.1680165978.60.0.0; _csrf=qx9JVqrJefRtw3ZQeUu-QaKW; _dd_s=rum=0&expire=1680421462755",
        "pragma": "no-cache",
        "referer": "https://poshmark.com/closet/miamioclock",

        "sec-ch-ua-mobile": "?0",

        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "x-xsrf-token": "OAn6thZK-E44ntWIUi1pBi4MYRPv4Mh9gfCo"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    next_page = response.json()['more']['next_max_id']
    print(next_page)
    max_id_x = str(next_page)

