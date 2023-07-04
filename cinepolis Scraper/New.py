import requests
import time, csv
from datetime import datetime
import undetected_chromedriver as uc

url = "https://cinepolis.com/Cartelera.aspx/GetNowPlayingByCity"

payload = {
    "claveCiudad": "torreon",
    "esVIP": False
}
headers = {
    "authority": "cinepolis.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "cookie": "Ciudad=torreon; CinepolisOnline=0tf2pq5mpkow54vrjpodd1zk; dtCookie=v_4_srv_15_sn_5904C9FE704315C763A2B078AF48DDBB_perc_100000_ol_0_mul_1_app-3A0f0496eabd307937_1_rcs-3Acss_0; AWSALB=gwCpNy//wrvhkbVvhaW2oLBkQ4puU/Z1V/xcNIlbp+PhFcB6Zlbg2HQ9kVUMRxv7gggRUrYc0bOr2hJIKd2gJO+J2HM9gZjI3ZUgw2AxEDYKSC+ptbQzUVxrfSiF; AWSALBCORS=gwCpNy//wrvhkbVvhaW2oLBkQ4puU/Z1V/xcNIlbp+PhFcB6Zlbg2HQ9kVUMRxv7gggRUrYc0bOr2hJIKd2gJO+J2HM9gZjI3ZUgw2AxEDYKSC+ptbQzUVxrfSiF",
    "origin": "https://cinepolis.com",
    "referer": "https://cinepolis.com/cartelera/torreon/cinepolis-galerias-laguna",

    "sec-ch-ua-mobile": "?0",

    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()
response = requests.request("POST", url, json=payload, headers=headers)

# save json response to file
data = response.json()['d']['Cinemas']

for single_row in data:
    name_complex = single_row['Name']
    # name_group = single_row['Group']
    name_city = single_row['CityName']
    dates = single_row['Dates']
    for date in dates:
        movies = date['Movies']
        for movie in movies:
            gender_movie = movie['Gender']
            distributor = movie['Distributor']
            original_title = movie['Title']
            rating_movie = movie['Rating']
            language_format = [language['Language'] for language in movie['Formats']]
            language_format = ', '.join(language_format)
            name_format = [name['Name'] for name in movie['Formats']]
            name_format = ', '.join(name_format)
            showtimes = movie['Formats'][0]['Showtimes']
            urls = []
            for showtime in showtimes:
                vista_id = showtime['VistaCinemaId']
                vista_showtime_id = showtime['ShowtimeId']
                url = f"https://compra.cinepolis.com/?cinemaVistaId={vista_id}&showtimeVistaId={vista_showtime_id}"
                urls.append(url)


            # save to csv
            with open('cinepolis.csv', 'a', newline='') as file:
                filewriter = csv.writer(file)
                filewriter.writerow([gender_movie, distributor, original_title, rating_movie, language_format, name_format, name_complex, name_city, url])

            print(urls)
            for url in urls:
                driver.get(url)
                time.sleep(5)


