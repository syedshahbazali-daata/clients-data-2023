import time

import requests
import csv
from bs4 import BeautifulSoup
from xextract import String
from selenium import webdriver

def append_into_csv(dataframe, file_name):
    for single_row in dataframe:
        with open(file_name, "a", encoding="utf-8", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(single_row)


def trip_advisor_reviews_scraper(trip_adv_url):
    hotel_id = trip_adv_url.lower().split("-d")[1].split("-reviews")[0]
    start_page = 1
    start_offset = 0

    dataframe = []
    index = 0

    while True:
        url = "https://www.tripadvisor.com/data/graphql/ids"
        payload = [
            {
                "query": "0eb3cf00f96dd65239a88a6e12769ae1",
                "variables": {"interaction": {"productInteraction": {
                    "interaction_type": "CLICK",
                    "site": {
                        "site_name": "ta",
                        "site_business_unit": "Hotels",
                        "site_domain": "www.tripadvisor.com"
                    },
                    "pageview": {
                        "pageview_request_uid": "0d46e2a6-70b0-40c6-8a8b-be08a5308516",
                        "pageview_attributes": {
                            "location_id": hotel_id,
                            "geo_id": 32596,
                            "servlet_name": "Hotel_Review"
                        }
                    },
                    "user": {
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                        "site_persistent_user_uid": "web422a.119.160.99.187.188FD39D70A",
                        "unique_user_identifiers": {"session_id": "18B79C1588B04787A6152ED46F764927"}
                    },
                    "search": {},
                    "item_group": {"item_group_collection_key": "0d46e2a6-70b0-40c6-8a8b-be08a5308516"},
                    "item": {
                        "product_type": "Hotels",
                        "item_id_type": "ta-location-id",
                        "item_id": hotel_id,
                        "item_attributes": {
                            "element_type": "number",
                            "action_name": "REVIEW_NAV",
                            "page_number": start_page,
                            "offset": start_offset,
                            "limit": 10
                        }
                    }
                }}}
            },
            {
                "query": "ea9aad8c98a6b21ee6d510fb765a6522",
                "variables": {
                    "locationId": hotel_id,
                    "offset": start_offset,
                    "filters": [
                        {
                            "axis": "LANGUAGE",
                            "selections": ["en"]
                        }
                    ],
                    "prefs": None,
                    "initialPrefs": {},
                    "limit": 10,
                    "filterCacheKey": f"locationReviewFilters_{hotel_id}",
                    "prefsCacheKey": f"locationReviewPrefs_{hotel_id}",
                    "needKeywords": False,
                    "keywordVariant": "location_keywords_v2_llr_order_30_en"
                }
            },
            {
                "query": "ba6039385f4493938c3e8d3821471da5",
                "variables": {"request": {
                    "clientRequestTimestampMs": 1687885981765,
                    "request": [
                        {
                            "pageUid": "0d46e2a6-70b0-40c6-8a8b-be08a5308516",
                            "sessionId": "18B79C1588B04787A6152ED46F764927",
                            "userAgent": "DESKTOP",
                            "eventTimestampMs": 1687885981765,
                            "team": "Other",
                            "page": "Hotel_Review",
                            "itemType": "MembershipHardGateGhost",
                            "customData": "{\"variant\":\"unbucketed\",\"googleOneTapEligible\":false,\"businessLogicEligible\":false,\"showHardGate\":false}",
                            "geoId": 32596,
                            "locationId": hotel_id,
                            "impressionKey": "9c7990c8-e077-4efb-8c3b-12c85eb52d8d"
                        }
                    ]
                }}
            },
            {
                "query": "d4ead89c1436b0934c1f3cbe457425c6",
                "variables": {
                    "locationId": hotel_id,
                    "application": "HOTEL_DETAIL",
                    "currencyCode": "USD",
                    "pricingMode": "BASE_RATE",
                    "sessionId": "18B79C1588B04787A6152ED46F764927",
                    "pageviewUid": "0d46e2a6-70b0-40c6-8a8b-be08a5308516",
                    "travelInfo": {
                        "adults": 2,
                        "rooms": 1,
                        "checkInDate": "2023-07-09",
                        "checkOutDate": "2023-07-10",
                        "childAgesPerRoom": [],
                        "usedDefaultDates": True
                    },
                    "requestNumber": 1,
                    "filters": None,
                    "route": {
                        "page": "Hotel_Review",
                        "params": {
                            "detailId": hotel_id,
                            "geoId": 32596,
                            "offset": f"r{start_offset}"
                        }
                    }
                }
            },
            {
                "query": "44136c06115b0e6638f1de27d15da1e5",
                "variables": {"request": {
                    "page": "Hotel_Review",
                    "event": "ENTER_DATES",
                    "pixelMetrics": [
                        {
                            "id": "13",
                            "name": "TAPS_GTM_MONITORING",
                            "status": "success",
                            "executionTime": 19
                        },
                        {
                            "id": "139",
                            "name": "TAPS_PINTEREST_EVENT",
                            "status": "success",
                            "executionTime": 8
                        },
                        {
                            "id": "171",
                            "name": "TRAQ_FACEBOOK_PAGEVIEW_VIEWCONTENT",
                            "status": "success",
                            "executionTime": 1
                        }
                    ],
                    "consent": True
                }}
            }
        ]
        headers = {
            # "cookie": "TADCID=55Hjn_kPXsacxzV8ABQCXdElnkGETRW-Svh01l3nWnZ5ifIDxbkb4Mt-TBE9I2AclLFkKP0PWKM3fNsmseh3MOO5u2hbDgy2FQU; TAUnique=%1%enc%3A57KubAv3KYBNUGLyE12%2BmRKC3hmUTNY2%2BSbDX4odIWRlvAmHg3GS6Q%3D%3D; TASSK=enc%3AADj5E7hbkTMB542Wj5VOs1XyseKXGR30xSfhotF%2BxsFFvfKa%2BbkgLd%2BH57%2BSFpXx%2BcXfF5m3EEyWOYwGcYNA%2FtajWdYuii4yz1rhObOOhQiUtRM0L9Jyy6sGsTi5sv6p0g%3D%3D; ServerPool=A; PMC=V2*MS.10*MD.20230627*LD.20230627; TART=%1%enc%3ATVBi8hNdvpmTzF8pd00NgUZH1CkV7hq5dkRMP%2FZo58fs2bi8ItZR%2BPT4AcwppebBYYWFX73vQrA%3D; TATravelInfo=V2*AY.2023*AM.7*AD.9*DY.2023*DM.7*DD.10*A.2*MG.-1*HP.2*FL.3*DSM.1687875606427*RS.1; TAReturnTo=%1%%2FHotel_Review-g32596-d78641-Reviews-Quality_Inn_Suites_Irvine_Spectrum-Lake_Forest_California.html; _abck=4DDB4CF92BDA24A2EBD0714E0D7517D3~-1~YAAQ38TdWM3Lx9uIAQAA19k5/QpK6Sky3aQy2Sr4dC6d0QJP6UNRkhd6f7OdB59h8nYAMKI669T0jb06K/9TECw5AC7s1S2ICZSVmjr+ZFZaa6fNg4QEEn3SYTJSXyy6w9swfiHnkVGt/qDxeZ6n+rnil3/rAQmCLL9zTvGPWRpDhzqJmso7Hyo9BPsD7MCiS5LPcpM+pwcd5pD9mgBbbQo42SzGYNhpfbVoDvtFPIlAVUA5nPWFNAzWjXIwJU/sf+Smlg4ZpLdZIAQaVZIIVFtb6YNh5YoV8JRKR5F3Es5sYMYazGj7VbPwh9zfHY8nO5KAFH6Gf9ULsrxdy4xdT1ZY1t9j7qHXPmF5Qi/aDeTalO3ZR5qozkPXbz8chJoZvQ==~-1~-1~-1; bm_sz=15E3F2D382631E4C2D8A38C039067BA0~YAAQ38TdWM7Lx9uIAQAA19k5/RQsoHesLsP928VuLjySMUum9uigqCxShBUV+gwhIAn/V5qtdK2qIFScOIODejnUUY12JJghAwqQtWAn6N8Joo1A5hBX8ykaMhtuF9YfkA6LioXgh1pgJkPvvxf68j3dmzdZ8o6Whsa/bOEoCAsaC/GDaFKFhEFSh8kxvoGF5oOeEm5K5Ua8q96CGujGVZpguvg1CFc85rUuWfQ9EvRZy2+oD4nJB0hCtQV1p/1ZkraFn8mXwY/sL9NoWv9suBOwObkKhO8hfDQf2BmgKf/w5qh5LvNs/Q==~3159106~4604228; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; _ga=GA1.1.1828114426.1687875616; __vt=ZHOHOpswacYsH_FQABQCwDrKuA05TCmUEEd0_4-PPCZX1Af5ysy8jhhSwOFF_agWMgqV1Zw9TcXTdAKy-1Ea3vBqdvdO9HZarsGODY7WKy9F3SBVX2cyjQzIYtbl1HfCok5FScDmtMHvvQl9GdG_7nlgwA; PAC=AE-gai47CH7R7alSIlbBGwvG88Z6OKfPIDtDSsLdpPcGhdhYzfR7IgTDmfG5DVu1bHiEvFAPmlHrL5sUDvBwFY-kdjeeJIs0p98LslTISkoBiOzdMT84Los_mUrfxf329Wj-jYFfF0Ew-_guvcco9Xa4a8qd_vvzmxbg_UXHfG1e6ko3pAJnoyLeUSDyexQ-Xrgv3RIFN7I4n6gMFh78EHdCKuAPksFmmvQoJQ2raPLC-Ipdh-ST9ZKZYvBndbpMbw%3D%3D; TASID=18B79C1588B04787A6152ED46F764927; roybatty=TNI1625\u0021AGpLckWwpgtmkQyItMs6u%2B50COgiKoxRX5QYQIP3xiDcLxzYLTEdaUUKN40yPnUFUYs4bngId4fQiHwQcrEzvdskIF4rgO26490jCa2%2B4k7iv51Ec6rRsRxVAVUDu4%2BT7VVUKAtCn2WsS%2BWzgwGHN9u1noTap45GRyWruwOQFg2J%2C1; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+27+2023+22%3A11%3A40+GMT%2B0500+(Pakistan+Standard+Time)&version=202209.1.0&isIABGlobal=false&hosts=&consentId=e2cf490a-d22d-488e-829e-48ceadcda455&interactionCount=0&landingPath=https%3A%2F%2Fwww.tripadvisor.com%2FHotel_Review-g32596-d78641-Reviews-Quality_Inn_Suites_Irvine_Spectrum-Lake_Forest_California.html&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; TASession=V2ID.18B79C1588B04787A6152ED46F764927*SQ.8*LS.PageMoniker*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*TRA.false*LD.78641*EAU._; TAUD=LA-1687875611780-1*HDD-1-2023_07_09.2023_07_10*RDD-1-2023_06_27*LD-10288774-2023.7.9.2023.7.10*LG-10288776-2.1.F.; datadome=54IYw3FcBg4hy_t5g4dB1kYlSQAmahuG~lSoe2roM14A5sqGVB7vHTo7ZT~hhWjA26m8hfKb5Y2IaVs1TEzakDf8xssxvo_3BIc_PreNhm4x3vvMDX~oxVh2eeNvX1xt; _ga_QX0Q50ZC9P=GS1.1.1687885902.2.0.1687885902.60.0.0; SRT=%1%enc%3ATVBi8hNdvpmTzF8pd00NgUZH1CkV7hq5dkRMP%2FZo58fs2bi8ItZR%2BPT4AcwppebBYYWFX73vQrA%3D",
            "authority": "www.tripadvisor.com",
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.tripadvisor.com",
            "referer": f"https://www.tripadvisor.com/Hotel_Review-g32596-d{hotel_id}-Reviews-or20-Quality_Inn_Suites_Irvine_Spectrum-Lake_Forest_California.html",
            "sec-ch-device-memory": "8",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "x-requested-by": "TNI1625\u0021ACgkOrhH+T2+AYpJE6CxK8dLfkp9Ffj6BLSOBg8bRieV1udP+6cN/FDUmGrONXzN06el+emwpYZ3ur1YIUu6oHy0tcBA0Yj0SE04XNBLWIyK7Yv8wAWka2r/fJVeKr100uDTO1ktS21olgpgQjeX39oJ/+Swnb6dcuvip+prpHOC"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        try:
            data = response.json()
            reviews_data = data[1]["data"]["locations"][0]["reviewListPage"]["reviews"]
            print(data)
        except:
            return None

        if len(reviews_data) == 0:
            append_into_csv(dataframe, "tripadvisor.csv")
            return dataframe

        for review in reviews_data:
            index += 1
            review_text = review["text"]
            user_name = review["userProfile"]["username"]
            review_date = review["createdDate"]

            row = [review_text, user_name, review_date]
            dataframe.append(row)
            print(row)
            print(f"Review {index} scraped successfully ---> TRIPADVISOR")

        start_page += 1
        start_offset += 10


# trip_advisor_reviews_scraper("https://www.tripadvisor.com/Hotel_Review-g32253-d78641-Reviews-Travelodge_by_Wyndham_Orange_County_Airport_Costa_Mesa-Costa_Mesa_California.html")

# BOOKING.com

def booking_review_scraper(main_url):
    aid_value = main_url.split("?")[1].split("&")[0].split("=")[1]
    label_value = main_url.split("?")[1].split("&")[1].split("=")[1]
    page_name_value = main_url.split("/hotel/us/")[1].split(".")[0]
    print(aid_value, label_value, page_name_value)

    offset = 0
    dataframe = []
    index = 0
    while True:

        review_url = f"https://www.booking.com/reviewlist.en-gb.html?aid={aid_value}&label={label_value}&sid=ca1cf5447367ae48cbe5ce807b8ca8f3&cc1=us;dist=1;pagename={page_name_value};type=total&&offset={offset};rows=10"
        print(review_url)

        payload = ""
        headers = {

            "authority": "www.booking.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7",
            "cache-control": "max-age=0",

            "sec-ch-ua-mobile": "?0",

            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        def date_cleaning(index_date):
            dates = String(
                xpath=f"(//li[@class='review_list_new_item_block'])[{index_date + 1}]//*[contains(text(), 'Reviewed')]").parse_html(
                soup)
            dates = [str(date.lower().split("reviewed: ")[1]).replace("\n", "").strip() for date in dates]
            try:
                date = dates[0]

            except:
                date = "NA"

            return date

        def clean_data(xpath):
            str_text = String(xpath=xpath).parse_html(soup)

            try:
                text = str_text[0]
            except:
                text = "NA"
            return text

        response = requests.request("GET", review_url, data=payload, headers=headers)
        soup = str(BeautifulSoup(response.text, "html.parser"))

        total_reviews_container = len(String(xpath="//li[@class='review_list_new_item_block']").parse_html(soup))
        if total_reviews_container == 0:
            return dataframe

        for single_review in range(total_reviews_container):
            review_date = date_cleaning(single_review)

            liked_review_text = clean_data(
                f"(//li[@class='review_list_new_item_block'])[{single_review + 1}]//span[text()='Liked']/../../span[@class='c-review__body']")
            dislike_review_text = clean_data(
                f"(//li[@class='review_list_new_item_block'])[{single_review + 1}]//span[text()='Disliked']/../../span[@class='c-review__body']")
            review_text = f"Liked: {liked_review_text} \n Disliked: {dislike_review_text}"
            user_name = clean_data(
                f"(//li[@class='review_list_new_item_block'])[{single_review + 1}]//span[@class='bui-avatar-block__title']")
            row = [review_text, user_name, review_date]
            index += 1
            print(f"Review {index} scraped successfully ---> BOOKING")
            dataframe.append(row)
        offset += 10


def expedia_review_scraper(main_url):
    property_id = main_url.split(".h")[1].split(".Hotel")[0]

    dataframe = []
    index = 0
    offset = 0
    while True:
        print(offset, "OFFSET")
        url = "https://www.expedia.com/graphql"

        payload = [
            {
                "operationName": "PropertyFilteredReviewsQuery",
                "variables": {
                    "context": {
                        "siteId": 1,
                        "locale": "en_US",
                        "eapid": 0,
                        "currency": "USD",
                        "device": {"type": "DESKTOP"},
                        "identity": {
                            "duaid": "98eb8364-2b57-4a58-ae7b-baf9a2e98c22",
                            "expUserId": "-1",
                            "tuid": "-1",
                            "authState": "ANONYMOUS"
                        },
                        "privacyTrackingState": "CAN_TRACK",
                        "debugContext": {
                            "abacusOverrides": [],
                            "alterMode": "RELEASED"
                        }
                    },
                    "propertyId": f"{property_id}",
                    "searchCriteria": {
                        "primary": {
                            "dateRange": {
                                "checkInDate": {
                                    "day": 28,
                                    "month": 6,
                                    "year": 2023
                                },
                                "checkOutDate": {
                                    "day": 29,
                                    "month": 6,
                                    "year": 2023
                                }
                            },
                            "destination": {
                                "regionName": "Costa Mesa, California, United States of America",
                                "regionId": "7674",
                                "coordinates": {
                                    "latitude": 33.641132,
                                    "longitude": -117.918671
                                },
                                "pinnedPropertyId": "10062",
                                "propertyIds": None,
                                "mapBounds": None
                            },
                            "rooms": [
                                {
                                    "adults": 2,
                                    "children": []
                                }
                            ]
                        },
                        "secondary": {
                            "booleans": [
                                {
                                    "id": "includeRecentReviews",
                                    "value": True
                                },
                                {
                                    "id": "includeRatingsOnlyReviews",
                                    "value": True
                                },
                                {
                                    "id": "overrideEmbargoForIndividualReviews",
                                    "value": True
                                }
                            ],
                            "counts": [
                                {
                                    "id": "startIndex",
                                    "value": offset
                                },
                                {
                                    "id": "size",
                                    "value": 200
                                }
                            ],
                            "selections": [
                                {
                                    "id": "sortBy",
                                    "value": "NEWEST_TO_OLDEST_BY_LANGUAGE"
                                },
                                {
                                    "id": "searchTerm",
                                    "value": ""
                                }
                            ]
                        }
                    }
                },
                "query": "query PropertyFilteredReviewsQuery($context: ContextInput!, $propertyId: String!, $searchCriteria: PropertySearchCriteriaInput!) {\n  propertyReviewSummaries(\n    context: $context\n    propertyIds: [$propertyId]\n    searchCriteria: $searchCriteria\n  ) {\n    ...__PropertyReviewSummaryFragment\n    __typename\n  }\n  propertyInfo(context: $context, propertyId: $propertyId) {\n    id\n    reviewInfo(searchCriteria: $searchCriteria) {\n      ...__PropertyReviewsListFragment\n      sortAndFilter {\n        ...TravelerTypeFragment\n        ...SortTypeFragment\n        ...SearchTextFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment __PropertyReviewSummaryFragment on PropertyReviewSummary {\n  accessibilityLabel\n  overallScoreWithDescriptionA11y {\n    ...LodgingEnrichedMessageFragment\n    __typename\n  }\n  propertyReviewCountDetails {\n    fullDescription\n    __typename\n  }\n  ...ReviewDisclaimerFragment\n  reviewSummaryDetails {\n    label\n    ratingPercentage\n    formattedRatingOutOfMax\n    __typename\n  }\n  totalCount {\n    raw\n    __typename\n  }\n  __typename\n}\n\nfragment ReviewDisclaimerFragment on PropertyReviewSummary {\n  reviewDisclaimer\n  reviewDisclaimerLabel\n  reviewDisclaimerAnalytics {\n    referrerId\n    linkName\n    __typename\n  }\n  reviewDisclaimerUrl {\n    value\n    accessibilityLabel\n    link {\n      url\n      __typename\n    }\n    __typename\n  }\n  reviewDisclaimerAccessibilityLabel\n  __typename\n}\n\nfragment LodgingEnrichedMessageFragment on LodgingEnrichedMessage {\n  __typename\n  subText\n  value\n  theme\n  state\n  accessibilityLabel\n  icon {\n    id\n    size\n    theme\n    __typename\n  }\n  mark {\n    id\n    __typename\n  }\n  egdsMark {\n    url {\n      value\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment __PropertyReviewsListFragment on PropertyReviews {\n  summary {\n    paginateAction {\n      text\n      analytics {\n        referrerId\n        linkName\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  reviews {\n    contentDirectFeedbackPromptId\n    ...ReviewParentFragment\n    managementResponses {\n      ...ReviewChildFragment\n      __typename\n    }\n    reviewInteractionSections {\n      primaryDisplayString\n      reviewInteractionType\n      __typename\n    }\n    __typename\n  }\n  ...NoResultsMessageFragment\n  __typename\n}\n\nfragment ReviewParentFragment on PropertyReview {\n  id\n  superlative\n  locale\n  title\n  brandType\n  reviewScoreWithDescription {\n    label\n    value\n    __typename\n  }\n  text\n  seeMoreAnalytics {\n    linkName\n    referrerId\n    __typename\n  }\n  submissionTime {\n    longDateFormat\n    __typename\n  }\n  impressionAnalytics {\n    event\n    referrerId\n    __typename\n  }\n  themes {\n    ...ReviewThemeFragment\n    __typename\n  }\n  reviewFooter {\n    ...PropertyReviewFooterSectionFragment\n    __typename\n  }\n  ...FeedbackIndicatorFragment\n  ...AuthorFragment\n  ...PhotosFragment\n  ...TravelersFragment\n  ...ReviewTranslationInfoFragment\n  ...PropertyReviewSourceFragment\n  ...PropertyReviewRegionFragment\n  __typename\n}\n\nfragment AuthorFragment on PropertyReview {\n  reviewAuthorAttribution {\n    text\n    __typename\n  }\n  __typename\n}\n\nfragment PhotosFragment on PropertyReview {\n  id\n  photoSection {\n    imageClickAnalytics {\n      referrerId\n      linkName\n      __typename\n    }\n    exitAnalytics {\n      referrerId\n      linkName\n      __typename\n    }\n    navClickAnalytics {\n      referrerId\n      linkName\n      __typename\n    }\n    __typename\n  }\n  photos {\n    description\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment TravelersFragment on PropertyReview {\n  travelers\n  __typename\n}\n\nfragment ReviewThemeFragment on ReviewThemes {\n  icon {\n    id\n    __typename\n  }\n  label\n  __typename\n}\n\nfragment FeedbackIndicatorFragment on PropertyReview {\n  reviewInteractionSections {\n    primaryDisplayString\n    accessibilityLabel\n    reviewInteractionType\n    feedbackAnalytics {\n      linkName\n      referrerId\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReviewTranslationInfoFragment on PropertyReview {\n  translationInfo {\n    loadingTranslationText\n    targetLocale\n    translatedBy {\n      description\n      __typename\n    }\n    translationCallToActionLabel\n    seeOriginalText\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyReviewSourceFragment on PropertyReview {\n  propertyReviewSource {\n    accessibilityLabel\n    graphic {\n      description\n      id\n      size\n      token\n      url {\n        value\n        __typename\n      }\n      __typename\n    }\n    text {\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyReviewRegionFragment on PropertyReview {\n  reviewRegion {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyReviewFooterSectionFragment on PropertyReviewFooterSection {\n  messages {\n    seoStructuredData {\n      itemscope\n      itemprop\n      itemtype\n      content\n      __typename\n    }\n    text {\n      ... on EGDSPlainText {\n        text\n        __typename\n      }\n      ... on EGDSGraphicText {\n        text\n        graphic {\n          ... on Mark {\n            description\n            id\n            size\n            url {\n              ... on HttpURI {\n                relativePath\n                value\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReviewChildFragment on ManagementResponse {\n  id\n  header {\n    text\n    __typename\n  }\n  response\n  __typename\n}\n\nfragment NoResultsMessageFragment on PropertyReviews {\n  noResultsMessage {\n    __typename\n    ...MessagingCardFragment\n    ...EmptyStateFragment\n  }\n  __typename\n}\n\nfragment MessagingCardFragment on UIMessagingCard {\n  graphic {\n    __typename\n    ... on Icon {\n      id\n      description\n      __typename\n    }\n  }\n  primary\n  secondaries\n  __typename\n}\n\nfragment EmptyStateFragment on UIEmptyState {\n  heading\n  body\n  __typename\n}\n\nfragment TravelerTypeFragment on SortAndFilterViewModel {\n  sortAndFilter {\n    name\n    label\n    options {\n      label\n      isSelected\n      optionValue\n      description\n      clickAnalytics {\n        linkName\n        referrerId\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SortTypeFragment on SortAndFilterViewModel {\n  sortAndFilter {\n    name\n    label\n    clickAnalytics {\n      linkName\n      referrerId\n      __typename\n    }\n    options {\n      label\n      isSelected\n      optionValue\n      description\n      clickAnalytics {\n        linkName\n        referrerId\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SearchTextFragment on SortAndFilterViewModel {\n  sortAndFilter {\n    name\n    label\n    graphic {\n      ... on Icon {\n        description\n        id\n        token\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
            }
        ]
        headers = {
            "cookie": "linfo=v.4,|0|0|255|1|0||||||||1033|0|0||0|0|0|-1|-1; CRQSS=e|0; CRQS=t|1`s|1`l|en_US`c|USD; currency=USD; iEAPID=0; tpid=v.1,1; NavActions=acctWasOpened; EG_SESSIONTOKEN=dFw4NEjr1wXc6ddKUl8wlQTvjdxwz6ExI9_99Dz9OOd8Yw:KcjJjhThajmWEVwpXNZ3If-OtNM31EMEusQgZTYB_k2zFK0qXHDxsISlGOC3ZZuOQ_nPPIpcPPAsK9jYkS2_Kw; MC1=GUID=98eb83642b574a58ae7bbaf9a2e98c22; DUAID=98eb8364-2b57-4a58-ae7b-baf9a2e98c22; CRAS=US.META.HPA.HOTEL-CORESEARCH-desktop.HOTEL; _abck=14364A235942E293D9E3C534A8E35506~-1~YAAQV54QAqPaPcaIAQAAxxGiAAq9HP3+7u+ij6C1HMaRjTLCl112SNhm4W0+RGLgPwvAyvp6C6DzHf4qheymzWiVxOXQc/jY7aphaIrRL1CQDRizsWe5GnJTTWJWihCm3ax5Dewkx2//Jca7XW8g1fMtW73CMUW6hxZXqmjQCQQe3wbVGpdGt2VU1kZgE4oDi3pa1yFTyXvZSOLPVFwcEZnPej14LgggTd1PxLEgb1o+F2zQYGR57JxljlmOq36VulNggzJQM4BV9DbeaM9aFcYy4M2TENnawWv6o5BtcnLV9ZLL+VNbCmFMwS/cVYrma0G9q5l9pun1k+akRZBq0lJ1+UaJQCGlp+EX01vVaJ7PE+3VCE82jRJSeHF9~-1~-1~-1; bm_sz=F8C8925499AC27B22E46A5777539857A~YAAQV54QAqbaPcaIAQAAxxGiABRPUvEq2RZPUfKm3BrBEG99J6vhH3tHOB3rDU9p764bv9tF9jdiTXdZsXb6y26ahkiAXIz1IwKNEgtoKJ3ugalogJ0to1reBRw/jmJl6W8HrXwM2ZIpGwS7stQAfvL8s2rphSRmb1wLBgCEg2OleLxaFuHYRcBBo1Q6vF/R1FGK50E8WOYsIMqa+zMkwubWoopmbwtehcYebGEp57Tcq2yo6t85FiAeR/ZLggaV9lgycfKxVl5VcaYFAtiOXFrqQyL26ibJPHYfqIfL6Ya0MdkW~3160120~4339268; eg_ppid=6df076bc-f79c-479e-aaf7-7fc7c3e7fe31; s_ecid=MCMID%7C77977448111800498944448896178392236239; s_ppv=%5B%5BB%5D%5D; s_ips=1; AMCVS_C00802BE5330A8350A490D4C%40AdobeOrg=1; s_cc=true; AMCV_C00802BE5330A8350A490D4C%40AdobeOrg=1585540135%7CMCIDTS%7C19537%7CMCMID%7C77977448111800498944448896178392236239%7CMCAID%7CNONE%7CMCOPTOUT-1687939975s%7CNONE%7CMCAAMLH-1688537575%7C3%7CMCAAMB-1688537575%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCCIDH%7C-2034012538%7CvVersion%7C4.4.0; session_id=de0da2cf-c644-44c9-a765-29291935c999; page_name=page.Hotels.Infosite.Information; _uetsid=da4515e0157a11eebc90fba2c3493c78; _uetvid=da452610157a11ee8d988376425389f7; _gcl_aw=GCL.1687932789.Cj0KCQjwy9-kBhCHARIsAHpBjHggSRdvZBoWbdtPlh9FjHzBdfLx53FrV3_xXAtCn7_ZboiRsg5xerUaAhZLEALw_wcB; _gcl_au=1.1.774790809.1687932789; _fbp=fb.1.1687932789531.1832402212; _ga_8HQXZ49CXH=GS1.1.1687932790.1.0.1687932790.0.0.0; _ga=GA1.2.1449946732.1687932790; _gid=GA1.2.543993252.1687932791; _gac_UA-35711341-2=1.1687932791.Cj0KCQjwy9-kBhCHARIsAHpBjHggSRdvZBoWbdtPlh9FjHzBdfLx53FrV3_xXAtCn7_ZboiRsg5xerUaAhZLEALw_wcB; __gads=ID=cd05fc9be6f77f41:T=1687932792:RT=1687932792:S=ALNI_MYyW6KSqdMJhkCMwm9nBaUwi-IniA; __gpi=UID=00000c5e8c372bab:T=1687932792:RT=1687932792:S=ALNI_MaFwEJkd8g8TT9BzgsaH75aIOPo4w; xdid=447c1b93-d3f0-4a82-a8af-9e1ee89910a1|1687932795|expedia.com; s_tp=6060; ak_bmsc=AD89B35FB4A7237D9BDBC52047B2EA97~000000000000000000000000000000~YAAQFp4QArSr2/qIAQAAAPksARQk9QPUKg9W72XrSIEn/wkugE4iqTEoe3iq/mI5dO2sa/vO2dpW7l4k8tl/18mgsv9M3p8TRBahEY7uLE/H2M4SJZ9kPinXWAYK/dV6MXUWoTDqRzzvealwY8zQHstqW0JdHWaE7YJSvkTL/mZqyman/oANCRH2R0rogr1gVTXtazPpXeYgFoDIotk4k3h0+e2OfzYBll68xjyKq8yb0GpcMvYJJhIclA6G92u0STileWZrvCl8XZHkxHCTCiur+AjHV1jB34ukNFrJCOlSH+/Hh4TkfdBNLqEm84X13XtVuINz9zS/3+9SakIJMcB6disikV32onRv4hlJ5ML+sxfTp9gvrkFNHIRhyHx1WLwIvealBdZTk18=; AWSELB=D79B53F10ADCF9DDDF09C7B84896C09A6222EC2F5DC82C53E2E9201DC264A9501B993E8251F2A58F84B43F61ADD9D865003C2FA4F62524FDD05E6B98C1F794BDCC9BB3A0C9; AWSELBCORS=D79B53F10ADCF9DDDF09C7B84896C09A6222EC2F5DC82C53E2E9201DC264A9501B993E8251F2A58F84B43F61ADD9D865003C2FA4F62524FDD05E6B98C1F794BDCC9BB3A0C9; HMS=17e7e080-62eb-4bd5-835e-c3a0a08b8584; cesc=%7B%22lpe%22%3A%5B%2258c8ca24-1261-489d-a6fb-d744bd70d560%22%2C1687944893134%5D%2C%22gclid%22%3A%5B%22Cj0KCQjwy9-kBhCHARIsAHpBjHggSRdvZBoWbdtPlh9FjHzBdfLx53FrV3_xXAtCn7_ZboiRsg5xerUaAhZLEALw_wcB%22%2C1687932768640%5D%2C%22marketingClick%22%3A%5B%22false%22%2C1687944893134%5D%2C%22lmc%22%3A%5B%22MDP.US.META.HPA.HOTEL-CORESEARCH-DESKTOP.HOTEL%22%2C1687944893134%5D%2C%22hitNumber%22%3A%5B%222%22%2C1687944893134%5D%2C%22dps%22%3A%5B%22MDP.US.META.HPA.HOTEL-CORESEARCH-desktop.HOTEL.HTL.10062.20230628.20230629.DDT.3.CID.2040586220.AUDID..RRID.bex_us_desktop%22%2C1687932768640%5D%2C%22amc%22%3A%5B%22MDP.US.META.HPA.HOTEL-CORESEARCH-DESKTOP.HOTEL%22%2C1687944893134%5D%2C%22visitNumber%22%3A%5B%222%22%2C1687944887049%5D%2C%22ape%22%3A%5B%2258c8ca24-1261-489d-a6fb-d744bd70d560%22%2C1687944893134%5D%2C%22entryPage%22%3A%5B%22page.Hotels.Infosite.Information%22%2C1687944893134%5D%2C%22cid%22%3A%5B%22MDP.US.META.HPA.HOTEL-CORESEARCH-desktop.HOTEL%22%2C1687932768640%5D%7D; bm_sv=9BFE06693F5BB340B02068175A37D3C5~YAAQTZ4QAm5CSseIAQAAFChbARSZ27iaPJonL4KP37UBvLjL9a/V10T/L1TityqBCuRSYRfowopDFqhPtkJPkSYmbDBoRibT25NYALudaeDoPnHiKSDvpeByP0HsFHHEs1THTQ3Mwz9pyZDKBnEAOBldIKyycu5VS1hwzw92mT8l1A7L6sJKwWGjmFBo+ZQXn8HH2/P2rmIktp1C19pqh1MZsOPrQiJPGcyv87x4fZHSXhInx7KS6hYSAHZqt0Q1jQ==~1; _dd_s=rum=0&expire=1687945834472",
            "authority": "www.expedia.com",
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "client-info": "shopping-pwa,f9b264009ef7108e803a5d284fc7c624a5d5e7f9,us-west-2",
            "content-type": "application/json",
            "origin": "https://www.expedia.com",
            "referer": "https://www.expedia.com/Costa-Mesa-Hotels-Travelodge-By-Wyndham-Orange-County-Airport-Costa-Mesa.h10062.Hotel-Information?chkin=2023-06-28&chkout=2023-06-29&destType=MARKET&destination=Costa%20Mesa%2C%20California%2C%20United%20States%20of%20America&gclid=Cj0KCQjwy9-kBhCHARIsAHpBjHggSRdvZBoWbdtPlh9FjHzBdfLx53FrV3_xXAtCn7_ZboiRsg5xerUaAhZLEALw_wcB&latLong=33.641132%2C-117.918671&mctc=10&mdpcid=US.META.HPA.HOTEL-CORESEARCH-desktop.HOTEL&mdpdtl=HTL.10062.20230628.20230629.DDT.3.CID.2040586220.AUDID..RRID.bex_us_desktop&neighborhoodId=553248635976472271&pwaDialog=reviews&pwa_ts=1687716621660&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jb20vSG90ZWwtU2VhcmNo&regionId=7674&rfrr=HSR&rm1=a2&searchId=9d4c3a08-44e4-4b7e-930f-313f94d5abc8&selected=10062&selectedRatePlan=389797746&selectedRoomType=209981&sort=RECOMMENDED&top_cur=USD&top_dp=114&useRewards=false&userIntent=&x_pwa=1",

            "sec-ch-ua-mobile": "?0",

            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "x-page-id": "page.Hotels.Infosite.Information,H,30"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        try:
            data = response.json()
            reviews_data = data[0]['data']['propertyInfo']['reviewInfo']['reviews']
            print(len(reviews_data))
        except:
            return None

        if len(reviews_data) == 0:
            return dataframe

        for single_review in reviews_data:
            review_text = single_review['text']
            review_date = single_review['submissionTime']['longDateFormat']
            user_name = single_review['reviewAuthorAttribution']['text']
            row = [review_text, user_name, review_date]
            print(row)
            dataframe.append(row)
            index += 1
            print(f"Scraping review {index} ==> Expedia")

        offset += 200


x = booking_review_scraper("https://www.booking.com/hotel/us/travelodge-o-c-airport.en-gb.html?aid=356929&label=metagha-link-luus-hotel-442239_dev-desktop_los-1_bw-3_dow-wednesday_defdate-1_room-0_gstadt-2_rateid-public_aud-0_gacid-6623578701_mcid-10_ppa-0_clrid-0_ad-1_gstkid-0_checkin-20230628__lp-1014240_r-3649148382057870081&sid=bc32467f49e922535edc01bf1d0d00bc&all_sr_blocks=44223912_246093390_2_0_0;checkin=2023-06-28;checkout=2023-06-29;dest_id=20012348;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=44223912_246093390_2_0_0;hpos=1;matching_block_id=44223912_246093390_2_0_0;no_rooms=1;req_adults=2;req_children=0;room1=a%2ca;sb_price_type=total;sr_order=popularity;sr_pri_blocks=44223912_246093390_2_0_0__11430;srepoch=1687716395;srpvid=fe437f54ef210189;type=total;ucfs=1&#tab-reviews")
print(x)



# https://www.booking.com/reviewlist.en-gb.html?aid=2018368&label=irvine-spectrum-*xy0yju*vsdlviorxmflyqs589115169542:pl:ta:p1:p2:ac:ap:neg:fi:tikwd-317352231748:lp9031079:li:dec:dm&sid=4d8209433b94d53bae2a1fd5742b7b08&cc1=us&dist=1&pagename=quality-inn-amp-suites-lake-forest&srpvid=ce067c2c3f5a002c&type=total&offset=10&rows=10&_=1688436531888
# https://www.booking.com/reviewlist.en-gb.html?aid=2018368&label=irvine-spectrum-%2axy0yju%2avsdlviorxmflyqs589115169542%3apl%3ata%3ap1%3ap2%3aac%3aap%3aneg%3afi%3atikwd-317352231748%3alp9031079%3ali%3adec%3adm&sid=ca1cf5447367ae48cbe5ce807b8ca8f3&cc1=us;dist=1;pagename=quality-inn-amp-suites-lake-forest.html?aid=2018368&label=irvine-spectrum-%2axy0yju%2avsdlviorxmflyqs589115169542%3apl%3ata%3ap1%3ap2%3aac%3aap%3aneg%3afi%3atikwd-317352231748%3alp9031079%3ali%3adec%3adm&sid=bc32467f49e922535edc01bf1d0d00bc&all_sr_blocks=45755601_94470146_2_0_0;checkin=2023-06-25;checkout=2023-06-26;dest_id=900074376;dest_type=landmark;dist=0;group_adults=2;group_children=0;hapos=11;highlighted_blocks=45755601_94470146_2_0_0;hpos=11;matching_block_id=45755601_94470146_2_0_0;no_rooms=1;req_adults=2;req_children=0;room1=a%2ca;sb_price_type=total;sr_order=popularity;sr_pri_blocks=45755601_94470146_2_0_0__11305;srepoch=1687714779;srpvid=ce067c2c3f5a002c;type=total;ucfs=1&#tab-reviews;type=total&&offset=0;rows=10
# https://www.booking.com/hotel/us/quality-inn-amp-suites-lake-forest.html?room1=a%2Ca&hapos=11&group_children=0&sid=bc32467f49e922535edc01bf1d0d00bc&highlighted_blocks=45755601_94470146_2_0_0&matching_block_id=45755601_94470146_2_0_0&all_sr_blocks=45755601_94470146_2_0_0&srepoch=1687714779&dest_type=landmark&type=total&checkin=2023-06-25&req_adults=2&hpos=11&no_rooms=1&sr_order=popularity&aid=2018368&ucfs=1&srpvid=ce067c2c3f5a002c&req_children=0&sr_pri_blocks=45755601_94470146_2_0_0__11305&sb_price_type=total&dist=0&checkout=2023-06-26&group_adults=2&dest_id=900074376&label=irvine-spectrum-*xy0yju*vsdlviorxmflyqs589115169542%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-317352231748%3Alp9031079%3Ali%3Adec%3Adm#tab-reviews
# https://www.booking.com/hotel/us/travelodge-o-c-airport.en-gb.html?aid=356929&label=metagha-link-luus-hotel-442239_dev-desktop_los-1_bw-3_dow-wednesday_defdate-1_room-0_gstadt-2_rateid-public_aud-0_gacid-6623578701_mcid-10_ppa-0_clrid-0_ad-1_gstkid-0_checkin-20230628__lp-1014240_r-3649148382057870081&sid=bc32467f49e922535edc01bf1d0d00bc&all_sr_blocks=44223912_246093390_2_0_0;checkin=2023-06-28;checkout=2023-06-29;dest_id=20012348;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=44223912_246093390_2_0_0;hpos=1;matching_block_id=44223912_246093390_2_0_0;no_rooms=1;req_adults=2;req_children=0;room1=a%2ca;sb_price_type=total;sr_order=popularity;sr_pri_blocks=44223912_246093390_2_0_0__11430;srepoch=1687716395;srpvid=fe437f54ef210189;type=total;ucfs=1&#tab-reviews