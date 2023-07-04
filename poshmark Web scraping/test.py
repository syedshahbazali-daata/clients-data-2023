import csv
import time

import requests

import requests


def scrape_record(username, max_id, listing_followers):
    url = f"https://poshmark.com/vm-rest/users/{username}/posts/filtered"

    querystring = {
        "request": "{\"filters\":{\"department\":\"All\",\"inventory_status\":[\"all\"]},\"query_and_facet_filters\":{\"creator_id\":\"username\"},\"experience\":\"all\",\"max_id\":max_id_x,\"count\":50}".replace(
            'username', username).replace('max_id_x', str(max_id)),
        "summarize": "true", "app_version": "2.55", "pm_version": "238.0.0"}

    payload = ""
    headers = {
        "authority": "poshmark.com",
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "cookie": "ps=%7B%22bid%22%3A%2264230c2fe67283e992f21efa%22%2C%22extvid%22%3A%22ext1%3A223a211a-f2bf-4483-a8c4-6b45d304f49b%22%7D; vsegv3=eyJsMDEiOiIwOTgiLCJsMDIiOiIxMjEiLCJsMDMiOiIwNjUiLCJsMDQiOiIwNzciLCJsMDUiOiIxMjgiLCJsMDYiOiIwNDMiLCJsMDciOiIwNjIiLCJsMDgiOiIwODYifQ%3D%3D; __ssid=38a0c779c02c5e21c0d59c2748fc0c0; _gcl_au=1.1.45196378.1680018488; FPC=e7e1443b-f3a3-459e-b3d9-ad1a17fd7c62; G_ENABLED_IDPS=google; io_token_7c6a6574-f011-4c9a-abdd-9894a102ccef=mai5K20oop2GCqw4wVq+kyKDPilOyh+kZirvB/JkqBg=; _scid=7e253c57-1cc8-4477-b448-13a302018306; _tt_enable_cookie=1; _ttp=RWzXYBHiEGsmgfL3pQeRsDH0yDy; _sctr=1|1679943600000; tracker_device=d24b1aae-757c-4669-bdb2-494e55c85604; rt=%7B%22src%22%3A%5B%7B%22rf%22%3A%22%22%2C%22lpu%22%3A%22%2Fcloset%2Fmiamioclock%3Futm_source%26utm_content%3Dext_trk%253Dbranch%2526feature%253Dsh_cl_ss_ios%2526campaign%253Dshare_content_other_user__us.default.001%2526rfuid%253Dext1%253Aadf5571f-8c6b-4f53-9022-22c6288688e7%26br_t%3Dtrue%26_branch_match_id%3D1169289125428012244%26_branch_referrer%3DH4sIAAAAAAAAA8soKSkottLXL8gvztDLzdZP9c4zKynzSkqvTAIAILn1dhsAAAA%253D%22%2C%22lpt%22%3A%22Other%22%2C%22rs%22%3Anull%2C%22ca%22%3A%222023-03-28T15%3A48%3A05.964Z%22%7D%2C%7B%22rf%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22lpu%22%3A%22%2Flisting%2F6201578d6e2846223a6cf756%2C2022-02-07%2Csold_out%2C34B%2CNatori%2COther%2Cnicolestate%2C23%2Csold_out%2C1%2C0.0%2C5100.0%22%2C%22lpt%22%3A%22Listing%20Details%22%2C%22rs%22%3A%22gs%22%2C%22ca%22%3A%222023-03-30T08%3A33%3A10.953Z%22%7D%2C%7B%22rf%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22lpu%22%3A%22%2Flisting%2F6421c232253a8c85c8067f4a%2C2023-03-27%2Csold_out%2CM%2CNA%2CTops%2Cstateofposh%2C17%2Csold_out%2C1%2C352.0%2C5100.0%22%2C%22lpt%22%3A%22Listing%20Details%22%2C%22rs%22%3A%22gs%22%2C%22ca%22%3A%222023-03-30T08%3A35%3A51.405Z%22%7D%5D%7D; _uetvid=ef785d10cd7f11eda3dcbbb7fdfbee2e; _ga=GA1.1.1728920342.1680018488; _ga_S34VRNNVTV=GS1.1.1680165227.6.1.1680165978.60.0.0; _csrf=qx9JVqrJefRtw3ZQeUu-QaKW; _dd_s=rum=0&expire=1680420108830",
        "pragma": "no-cache",
        "referer": f"https://poshmark.com/closet/{username}",

        "sec-ch-ua-mobile": "?0",

        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "x-xsrf-token": "LpfbtMtQ-Emg_hP2znCWdrnG4bGGzmJaKt2s"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)


    json_data = response.json()['data']


    try:
        next_page = response.json()['more']['next_max_id']
        print("next_page: ", next_page)
    except:
        return None
    if len(json_data) == 0:
        print("No data")
        return None

    json_ids = ['https://poshmark.com/listing/'+item['id'] for item in json_data]
    created_ats = [item['cover_shot']['created_at'] for item in json_data]
    created_ats = [item.split('T')[0] for item in created_ats]
    available_status = [item['inventory']['status'] for item in json_data]
    sizes = [item['inventory']['size_quantities'][0]['size_id'] for item in json_data]
    # brands list comprehension try except "" if no brand
    brands = []
    for item in json_data:
        try:
            brands.append(item['brand'])
        except:
            brands.append("NA")

    category = [item['category'] for item in json_data]

    prices = []
    for item in json_data:
        try:
            prices.append(item['price'])
        except:
            prices.append("NA")

    for index in range(len(json_data)):
        record = [json_ids[index], created_ats[index], available_status[index], sizes[index], brands[index],
                  category[index], username, prices[index], listing_followers]
        with open(f'poshmark-xas.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(record)

    print(len(json_data))
    return next_page


def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')
    return data


users_details = get_file_data('user-details.txt')

for single_user in users_details:
    # current utc epoch time
    epoch_time = (time.time())
    max_id_list = ['1680422699']
    username_x = single_user.split(':')[0].replace("@", "")
    followers = single_user.split(':')[1]
    total_scraped = 0

    while True:
        print(f"Scraping {username_x} with max_id {max_id_list[0]} and scraped {total_scraped}")
        try:
            result = scrape_record(f"{username_x}", max_id_list[0], followers)

            if result is not None:
                print("new_max: ", result)

                max_id_list.clear()
                max_id_list.append(str(result))

        except Exception as e:
            print(e)
            print("Error scraping")
            result = None

        if result is None:
            break

        total_scraped += 50



