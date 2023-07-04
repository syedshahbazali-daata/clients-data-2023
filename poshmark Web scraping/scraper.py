"""
Username of account x
followers they have x
number of active listings x
number of sold listings y
the brands for the active listings y
the brand for the sold listings y -
the size for active listings y -
the size for the sold listings y -
listing creation date y -
categories y -
"""

import requests
from bs4 import BeautifulSoup
from xextract import String

# print current date and time : [30/03/2023 ; 16:54:10]
from datetime import datetime
print([datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%H:%M:%S")])


def scrape_text(xpath, source_code):
    try:
        text = str(String(xpath=xpath).parse_html(str(source_code))[0]).strip()
        return text
    except:
        return ""


response = requests.get(
    'https://poshmark.com/closet/miamioclock?utm_source&utm_content=ext_trk%3Dbranch%26feature%3Dsh_cl_ss_ios%26campaign%3Dshare_content_other_user__us.default.001%26rfuid%3Dext1%3Aadf5571f-8c6b-4f53-9022-22c6288688e7&br_t=true&_branch_match_id=1169289125428012244&_branch_referrer=H4sIAAAAAAAAA8soKSkottLXL8gvztDLzdZP9c4zKynzSkqvTAIAILn1dhsAAAA%3D')
soup = BeautifulSoup(response.text, 'html.parser')

# Username of account
username = scrape_text('//h1/../h4', soup)

# followers they have
followers = scrape_text("//*[contains(text(), 'Followers')]/../span", soup)
print(followers)



