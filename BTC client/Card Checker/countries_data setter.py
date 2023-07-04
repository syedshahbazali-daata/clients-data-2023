import requests
import re
import csv

x = """
<select class="vds-input--select" required="" aria-required="true" aria-describedby="input-message-help-countryCode input-message-error-countryCode countrySelectorHelperTextId" aria-invalid="false" autocomplete="off" id="countryCode" name="countryCode"><option value="AI">Anguilla</option><option value="AG">Antigua and Barbuda</option><option value="AR">Argentina</option><option value="AW">Aruba</option><option value="BS">Bahamas</option><option value="BB">Barbados</option><option value="BZ">Belize</option><option value="BM">Bermuda</option><option value="BO">Bolivia</option><option value="BQ">Bonaire</option><option value="BR">Brazil</option><option value="VG">British Virgin Islands</option><option value="KY">Cayman Islands</option><option value="CL">Chile</option><option value="CO">Colombia</option><option value="CR">Costa Rica</option><option value="CW">Curacao</option><option value="DM">Dominica</option><option value="DO">Dominican Republic</option><option value="EC">Ecuador</option><option value="SV">El Salvador</option><option value="GD">Grenada</option><option value="GP">Guadeloupe</option><option value="GT">Guatemala</option><option value="GY">Guyana</option><option value="HT">Haiti</option><option value="HN">Honduras</option><option value="JM">Jamaica</option><option value="MQ">Martinique</option><option value="MX">Mexico</option><option value="MS">Montserrat</option><option value="NI">Nicaragua</option><option value="PA">Panama</option><option value="PY">Paraguay</option><option value="PE">Peru</option><option value="PR">Puerto Rico</option><option value="LC">Saint Lucia</option><option value="KN">St. Kitts and Nevis</option><option value="SX">St. Maarten</option><option value="MF">St. Martin</option><option value="VC">St. Vincent</option><option value="SR">Suriname</option><option value="TT">Trinidad and Tobago</option><option value="TC">Turks and Caicos</option><option value="VI">U.S. Virgin Islands</option><option value="US">United States</option><option value="UY">Uruguay</option></select>"""

eligible_coutries = ['ANGUILLA', 'ANTIGUA AND BARBUDA', 'ARGENTINA', 'ARUBA', 'BAHAMAS', 'BARBADOS', 'BELIZE', 'BERMUDA', 'BOLIVIA', 'BONAIRE', 'BRAZIL', 'BRITISH VIRGIN ISLANDS', 'CAYMAN ISLANDS', 'CHILE', 'COLOMBIA', 'CURACAO', 'DOMINICA', 'DOMONICAN REPUBLIC', 'ECUADOR', 'EL SALVADOR', 'GRENADA', 'GUADELOUPE', 'GUATEMALA', 'GUYANA', 'HAITI', 'HONDURAS', 'JAMAICA', 'MARTINIQUE', 'MEXICO', 'MONTSERRAT', 'NICARAGUA', 'PANAMA', 'PARAGUAY', 'PERU', 'PUERTO RICO', 'SAINT LUCIA', 'ST. KITTS AND NEVIS', 'ST. MAARTEN', 'ST. MARTIN', 'ST. VINCENT', 'SURINAME', 'TRINIDAD AND TOBAGO', 'TURKS AND CAICOS', 'U.S. VIRGIN ISLANDS', 'UNITED STATES', 'URUGUAY']
countries_code = re.findall(r'value="(.*?)"', x)
countries_name = re.findall(r'value.*?">(.*?)<', x)
data = []
for i in range(len(countries_code)):
    countries_name[i] = countries_name[i].upper()
    if countries_name[i] in eligible_coutries:
        record = {
            "country_name": countries_name[i],
            "country_code": countries_code[i]
        }
        data.append(record)
print(data)




for single in data:

    country_code_X = single['country_code']
    url = "https://purchasealerts.visa.com/pas/apps/7d955368-76f3-4862-410a-18d406710101/configurations"

    querystring = {"countryCode": country_code_X}

    payload = ""
    headers = {
        "authority": "purchasealerts.visa.com",
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "cookie": "_did=P4FBCxLpslMuu1Ha0_TBKE0MB_Pzu7rf1XEUisVQ2_sQjQmkfNKKerZyeLopNX9wpnp0dpaS1ETGbGwca9B5J2BhK1e93BcjFJVe; wscrCookieConsent=1=true&2=true&3=true&4=true&5=true&visitor=60090056-bdf9-47dc-b388-eb66b568a1af&version=20230415-001; __cfruid=d0c976ef6b9bc3659244d0cf9832f9a1e25464f2-1683139872; JSESSIONID=C8495C70D2B4969B13C50228DA6D170F.d001",
        "dfpsessionid": "WpC8qa3l0RLTMVs2amvxyXPImgVUXBd77MyfQpysOU8Wuls7BYghm_DgH3eef8ZRVJD_FVOAEoD5rES_d9QsiAQhlPEGLyeNfi1n",
        "referer": "https://purchasealerts.visa.com/vca-web/check",

        "sec-ch-ua-mobile": "?0",

        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "x-correlation-id": "2_1683142134_599_71_b2k8l55-6f958457d5s4_VCA-WEB",
        "x-requested-with": "XMLHttpRequest",
        "x-thmid": "WpC8qa3l0RLTMVs2amvxyXPImgVUXBd77MyfQpysOU8Wuls7BYghm_DgH3eef8ZRVJD_FVOAEoD5rES_d9QsiAQhlPEGLyeNfi1n"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    print(response.text)

    try:
        result = response.json()['countryNumericCode']
        record_x = [single['country_name'], country_code_X, result]
        # save into CSV


        with open("countries_data.csv", "a", newline="", encoding="utf-8") as csv_file:
            csv_file = csv.writer(csv_file)
            csv_file.writerow(record_x)

    except:
        result = response.text

    print(result)
