import time

import requests
import pandas as pd

df_1 = pd.read_csv('countries_data.csv')
names = df_1['name'].tolist()
codes = df_1['code'].tolist()


def card_checker(pan_prefix, country_name):
    url = "https://purchasealerts.visa.com/pas/apps/7d955368-76f3-4862-410a-18d406710101/issuerOptStatus"
    print(country_name)
    try:
        index = int(names.index(str(country_name).upper()))
        numeric_code = int(codes[index])

    except:
        return False



    payload = {
        "panPrefix": pan_prefix,
        "countryCode": numeric_code
    }
    headers = {
        "authority": "purchasealerts.visa.com",
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
        "content-type": "application/json",
        "cookie": "JSESSIONID=712BACDB94300EAAA2645046AA8E7016.d001; _did=P4FBCxLpslMuu1Ha0_TBKE0MB_Pzu7rf1XEUisVQ2_sQjQmkfNKKerZyeLopNX9wpnp0dpaS1ETGbGwca9B5J2BhK1e93BcjFJVe; __cfruid=6313ed8a997206d6b0dbec5a0076517ae36df26d-1683064461; wscrCookieConsent=1=true&2=true&3=true&4=true&5=true&visitor=60090056-bdf9-47dc-b388-eb66b568a1af&version=20230415-001",
        "dfpsessionid": "bZcSIh0WknLJ5LXSqjJP4AZsP8y5SOtS_07wpb3Q4GUiAPs071bFV6LdzOf0fA3p1MXTmCHifHUu3E6UGaA2kkWfgCUUUiX_A_ae",
        "origin": "https://purchasealerts.visa.com",
        "referer": "https://purchasealerts.visa.com/vca-web/check",

        "sec-ch-ua-mobile": "?0",

        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "v-c-vaap-token": "Mi40LjB8ZW5jcnlwdGVkfDE2ODMwNjUwNzI1NzZ8biy9OK5sluyXZfzDusBqPuEmcc88_2tf2-r4pGi8tCu9oljJ3hicaHBMXkTgSQRXS92bclUbv6ED5vWsR2Ov_9xuTh-ULNARWkugZWuBEqM6jnhCLVapDC1jqlUiJstGUicdAFOP2zk-3C7-vAfhWEDtpo4BdMR0w6Jyl_1SsvXOFSYrOUTBWTO8hbB-Gu1mbDd7DmMLr-L8adK-meGG58x6myYOSajdbvn6WJ4oMTMKSu32cNqagVGXRI8qPWVyoTbLxebYmXckDA2dvifDXwSLQEZCLTc36Es3Pe41WtEHCP3xlnciE-NdsBlp-aem2mgushUGXy7yx1NbV-4OwPEyIDqbXLSdpLR0cC_5N4WCcqXz2xKj7uOuQ7nqVtJA83WWJTRZMzXH8rU5d3Fr9ODV0A0WQD8toMZ0yqI9qX0I1zysAEvN9NZhFZXbHdbedWlmwl4_r9hZ3FEUvgnEz5K-fe5uqVtnXVYwWnBJPjR5SFMKYvcrqN3ZDkI_otMeAcrXY-CpluXqwsDYxk9lQzWrWqj6MQRkv_UWXdXyfSbq-kv8yxZL6fAZnM9S0MG78i5zVcq33_AeIlNTA9vnMy9pWvprpWX3DPAEii9xtoxw6WBcoIIoitmxKNv1kMYevVVUOxIYbJFzEymTfoNaqAkQkCC-W7Y-xE-QgjeIQsbN4SljtltLnIMHDbZHSiuya5pbMSXijKGpJpJZEvRkc-GtTI_kFVX0JNQ1rMgVnRqx3KHLIK1Tps2e2iVmGWbYU5ZTamlqezORXcJO9McKclvA6vGg3ZWCGPjV9ypV1lFDmDBdBMTD-dFIthpg807imgDNXHzsZnQ_XLSVnczU_O-fSZxH4sWylh96OzWYnTuFWdhAs0WYuFeiiOV2TrPm4k3P-FhBxlNQGfAjLZVV1eLdAO1E4B5tg9b2IE8arGHWe2Vkq8me-LhONjfomVpvrayVzCOAq97YKK4oMBIIeSZwy2RSIhVmyLjQel_TGPyagjZN_6UZwL4HZ9QqZro-nE5fzvfbC0TJXQSyYZFsXluFly8IAA1he0KgkjpQyeoUaGSzv2SNv4SphrEpdHLEzZx-z-NZUtwWwPg17y7EnrtN1SCRrP4_FFUSC05u_-_EXDmNFj91vxVM2b5vtfmrcfK1bOmDMtv2aNPCilM412izNHcWznysdYVFLXQFVQSfNdJ3eFD3_uAXprWXocaMvd5krVJW53OEPeuE1ccZ2yYj4Mdt27SMhc_4xoJF7z37g76yXcx6_7A82qJ0GsIgBtSoBgdX0A8Ls6Cnqc3DS78AbE-cbqMzc2M9psbPIgoH5R2LvvfSB2btXV3qECslfp5vZG39Zq9yJ9boxDE1H3F0OUgCxMW-9URatKc2OcpOulgQbZ4BXbSI7nFVxWB2-6gqi_IpPhiTaILEAFvZhrhXEmv2gY8M6U_RgPD5BxSvnyzv5QYFLpAq5xG5yaOiDUN_lgPBV7iNVASXnXzclTBQO_OOg1SVYDpggAD57wel_qet24JlIhNOLIxl4y_3gYZaZr8m8R_wtn7jd8JIaAAQvxCS4iNLqXKG81-3P3hEYT0fdp5VQRnnosnvBlCbZd1jEvBtvmNvmKIRk8g2yYhxjdtE1Vq0gGH4_ub0lciUB9C7JAh_9ZPCDedMbUwymG4lI7VnzwGLN5wqBJ8BcYfQOeKA_My0N_gqlv5w6zk919HytdATSscaSgVp6uXzBGeDqWouvPiv1d7IY7mFGP_4hpc8aePogjdlT_yET2jorl5WCNbsCyDkJN--kMUeQPfNYEn4fN56A0o9ygauH6lyYzRmCuQa6NTjGTAuaGdG3nHYGNLI2rdhx13dawKPMgx7Eq64ub8ZuEYXiSiyO4ZweWJnIN4aQqSUrXhwsn2mpRmm5ZzRxm_G27hgTCkgaQK1YaoUpA8Q8CBN5YopwjkZm5BGAbvE9iil4yLps-I0xsWtnWRxVxPtaLXpRJQxslFloMteos_6aVq0mYGlMnl-26CpE0vivr33g1ZXKlQre-WSzRUYUOAqClzUgcFVqBU5U9nZVr4B5aTC9tmGez9kR_5YGOjDN9ON_1jF7ZhY9-V9wNr7JV20g-9LlLMa744tx8rEByl2Fs0DnoKhT5StZVh50JI8sLlvzQDgU8jHgeIVsgiIDisfZBTIQav5FU2sOYhzpzoqpAOodc_ixB6QAC9pHXW5_NmtSMB41I5Cu3CqKnXJInpU2j46yaETkSb3frF6u7eq1prYJ3VhZVZNyil9LULtrwaXJZPxr2rOz2wgoBTRel2Dc2-TEg0F0iMI7V26cbJUR-WGefTjx0lTzRQUAaCUuRq369TBE9K29L7Oo-OOI6RV6leCY3d-koJfXVOWHQnQnSGh_HlVuicaciYHfQa-bRoAG4QskIQ7B10hNsSGbIUUyMAXHtpwLV9MXMUtyOVzNwpQinzhZtDeHvOS5HzutCOU6S6tjedJlmZ4CpWNAfQwJMeA-byZb6oBl34DTflU9gHiRHhOhEyrrR48uREe4KYKtDfOG4X0RE1QMBBY9VpnGS440mQZ7hp_qidRDbCQXWUVi3uKYlNdyVWYFK0Zn8OklwUM8JpaOb2cLEqAagKZZWKmrLGcNcsYZZIkFUGorp0bEAMhKIKs-6LPjV7iB_V8XcGt_fPQuZfUfqADAK55Y5gfwzY1F_H_AYDxPtuOpJnH48dZwCvK4Kd-FDgJXbr18p1BVgdDDUl8wa0d7qv9_ADwsYXkCkNFkmodYcBcKF1IoAg0rnm8KsgLPjdMVvdb_cGqTytFDKHpHVSJ69A6W0HbKqUoWECipZiV8_IHCtSzs_CC5gZzTVL2IbIJvr5FrmCGlWOYLVjx8peGHTsfSh8zLRqMVf_nGG5I",
        "x-correlation-id": "2_1683065025_133_62_b2k8l55-6f958457d5s4_VCA-WEB",
        "x-requested-with": "XMLHttpRequest",
        "x-thmid": "bZcSIh0WknLJ5LXSqjJP4AZsP8y5SOtS_07wpb3Q4GUiAPs071bFV6LdzOf0fA3p1MXTmCHifHUu3E6UGaA2kkWfgCUUUiX_A_ae"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    try:
        eligible = str(response.json()["eligibility"]).lower().strip()
        if eligible == "true":
            return [True, str(response.text)]
    except:
        return [False, str(response.text)]
