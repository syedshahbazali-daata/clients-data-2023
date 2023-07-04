import csv
import requests


def get_coordinates(address) -> dict or bool:
    """
    :param address: Address of the location
    :return: Coordinates of the location
    """
    try:
        YOUR_KEY = "AIzaSyD51L_tG0jpLr2mHAZQ73TnQED_e8xzVYo"
        new_address = f'{address}' + ", Australia"
        url_x = f"https://maps.googleapis.com/maps/api/geocode/json?address={new_address}&key={YOUR_KEY}"

        response_x = requests.request("GET", url_x)

        response_x = response_x.json()["results"][0]["geometry"]["location"]

        return response_x
    except:
        return False


ask_address = input("Enter address: ")
coordinates = get_coordinates(ask_address)
print(coordinates)
if coordinates is False:
    print("=> You entered wrong address")
    quit()

print("""Please select distance range:
1. 5km
2. 10km
3. 100km
4. unlimited
""")
distances_ranges = {
    "1": "5",
    "2": "10",
    "3": "100",
    "4": "10000"
}

ask_distance = input("Enter distance: ")
distance = distances_ranges.get(ask_distance, False)
if distance is False:
    print("=> You entered wrong distance")
    quit()

types_b = []

business_types = ['Builders', 'Building Certifiers', 'Building Inspectors', 'Designers', 'Client Side Project Managers', 'Air Con & Refrigeration', 'Bricklaying', 'Carpenters', 'Concretors', 'Flooring', 'Gasfitting', 'Glass & Glazing', 'Guttering', 'Kitchens', 'Landscaping (Structural)', 'Painting', 'Paving', 'Pest Control (Termites)', 'Plastering', 'Plumbing and Drainage', 'Roofs and Roof Restoration', 'Screens & Grilles', 'Shade Sails', 'Sheds', 'Soil Testing', 'Swimming Pools', 'Tiling', 'Waterproofing', 'Fire Services', 'Shop fitting', 'Structural Steel', 'Stone Masonry']
print("""Please select business type:""")
for index, business_type in enumerate(business_types):
    print(f"{index + 1}. {business_type}")

ask_business_type = input("Enter business type: ")

business_type_x = business_types[int(ask_business_type) - 1].replace(" ", "%20").replace("&", "%26")
types_b.append(business_type_x)




url = "https://my.qbcc.qld.gov.au/myQBCC/s/sfsites/aura"


# lic_no, title_of_license, business_type, suburb, postal_code, call_number, phone_number, email_data
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Licence Number", "Title of Licence", "Business Type", "Suburb", "Postal Code", "Call Number", "Phone Number", "Email"])

for single_type in types_b:
    print(f"Scraping {single_type}")
    querystring = {"r": "12", "other.FindLocalContractor.searchTradies": "1"}
    lat = coordinates['lat']
    lon = coordinates['lng']

    print(lat, lon)
    payload = f"message=%7B%22actions%22%3A%5B%7B%22id%22%3A%22777%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FFindLocalContractorController%2FACTION%24searchTradies%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AFALC_ContractorList%22%2C%22params%22%3A%7B%22businessType%22%3A%22{single_type}%22%2C%22lat%22%3A{lat}%2C%22lon%22%3A{lon}%2C%22distanceInKm%22%3A%2210000%22%2C%22batchSize%22%3A2000%2C%22lastLicenceNumber%22%3Anull%7D%7D%5D%7D&aura.context=%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%22U29CODJZUktMd3A0d3Q0OE5hWGdZUU9aTWNUb0FHT1BKNlBYY1JVSHlMbWcyNDQuMjAuMS0yLjQxLjQ%22%2C%22app%22%3A%22siteforce%3AcommunityApp%22%2C%22loaded%22%3A%7B%22APPLICATION%40markup%3A%2F%2Fsiteforce%3AcommunityApp%22%3A%22Iu8cP7tIHfh9t9rfKIseOA%22%2C%22COMPONENT%40markup%3A%2F%2Finstrumentation%3Ao11ySecondaryLoader%22%3A%22WAlywPtXLxVWA9DxV-jd3A%22%7D%2C%22dn%22%3A%5B%5D%2C%22globals%22%3A%7B%7D%2C%22uad%22%3Afalse%7D&aura.pageURI=%2FmyQBCC%2Fs%2Ffindlocalcontractor&aura.token=null"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "renderCtx=%7B%22pageId%22%3A%22f38146e9-ed17-404f-9552-93aec3aa6abb%22%2C%22schema%22%3A%22Published%22%2C%22viewType%22%3A%22Published%22%2C%22brandingSetId%22%3A%22914c5568-e9e6-404d-85c7-40a5738e5b95%22%2C%22audienceIds%22%3A%226Au2e00000000Ll%22%7D; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1; _ga=GA1.1.1552368801.1687368547; pctrk=ddad8b50-98f6-4892-9576-59ce05595591; _ga_Y0LXRS0M4C=GS1.1.1687608302.4.1.1687608336.0.0.0; _ga_47VYT4S7E7=GS1.1.1687608302.4.1.1687608336.0.0.0; _ga_ZHX5MDRYVG=GS1.1.1687608302.4.1.1687608336.0.0.0; _ga_GNCRFWWJ1P=GS1.1.1687608302.4.1.1687608336.0.0.0; _ga_66454451-1=GS1.1.1687608336.4.0.1687608336.0.0.0",
        "Origin": "https://my.qbcc.qld.gov.au",
        "Referer": "https://my.qbcc.qld.gov.au/myQBCC/s/findlocalcontractor",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-SFDC-Page-Scope-Id": "73c30160-65dd-4e4a-81f7-49459f1fe614",
        "X-SFDC-Request-Id": "3474516900008e149e",

        "sec-ch-ua-mobile": "?0",

    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    data = response.json()['actions'][0]['returnValue']
    for index, single_record in enumerate(data):
        print(f"Record {index + 1} of {len(data)}")

        title_of_license = single_record.get('name', 'NA')
        license_number = single_record.get('licenceNumber', 'NA')
        mobile_number = single_record.get('mobile', 'NA')
        email = single_record.get('email', 'NA')
        phone_number = single_record.get('phone', 'NA')
        suburb = single_record.get('suburb', 'NA')
        post_code = single_record.get('postCode', 'NA')
        business_type = single_record.get('businessTypes', 'NA')

        # lic_no, title_of_license, business_type, suburb, postal_code, call_number, phone_number, email_data
        record = [license_number, title_of_license, business_type, suburb, post_code, mobile_number, phone_number,
                  email]
        print(record)
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(record)
